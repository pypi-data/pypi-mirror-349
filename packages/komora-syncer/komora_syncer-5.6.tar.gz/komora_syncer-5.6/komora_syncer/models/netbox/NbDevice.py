from loguru import logger

from komora_syncer.config import get_config
from komora_syncer.connections.NetboxConnection import NetboxConnection
from komora_syncer.helpers.utils import batch_query
from komora_syncer.models.netbox.NetboxBase import NetboxBase
from komora_syncer.models.netbox.NetboxCache import NetboxCache


class NbDevice(NetboxBase):
    def __init__(self, komora_obj):
        super().__init__()
        self.name = komora_obj.name
        self.komora_id = komora_obj.id
        self.site_name = komora_obj.siteName
        self.komora_url = f"{get_config()['komora']['KOMORA_URL']}/app/device/{self.komora_id}"
        self.api_object = None

    def find(self):
        # 1. lookup Device by KOMORA_ID
        device_cache = NetboxCache.get_device_cache()

        if not self.komora_id:
            return None

        try:
            if self.komora_id in device_cache:
                netbox_device = device_cache[self.komora_id]
            else:
                netbox_device = self.nb.dcim.devices.get(cf_komora_id=self.komora_id)

            if netbox_device is not None:
                self.api_object = netbox_device
                return self.api_object
        except Exception as e:
            logger.exception(f"Unable to get Device by komora_id: {self.komora_id}. Error: {e}")

        # 2. Lookup device by name, if komora id is not presented
        # - log a problem, when the name exists, but komora_id was not found
        try:
            self.site_name = self.site_name if self.site_name else "SKLAD"

            netbox_site = self.nb.dcim.sites.get(name__ie=self.site_name)
            netbox_device = self.nb.dcim.devices.get(name__ie=self.name, site_id=netbox_site.id)

            if netbox_device is not None:
                logger.warning(
                    f"komora_id: {str(self.komora_id)} was not found, but Device {self.name} at site {self.site_name} already exists"
                )
                self.api_object = netbox_device
                return self.api_object
        except Exception as e:
            logger.exception(f"Unable to get Device by name: {self.name}. Error: {e}")

        return self.api_object

    def update(self, nb_device):
        try:
            if nb_device.update(self.params):
                self.api_object = nb_device
                logger.info(f"Device: {self.name} updated successfully")
        except Exception as e:
            logger.exception(f"Unable to update device {self.name}. Error: {e}")

    def synchronize(self):
        device = self.find()

        if device:
            self.update(device)
        else:
            logger.info(f"Device {self.name} - komora_id: {self.komora_id} not found in netbox")

    @property
    def params(self):
        params = {}

        if self.api_object:
            if isinstance(self.api_object.custom_fields, dict):
                params["custom_fields"] = self.api_object.custom_fields
                params["custom_fields"]["komora_id"] = self.komora_id
                params["custom_fields"]["komora_url"] = self.komora_url
        else:
            params["custom_fields"] = {
                "komora_id": self.komora_id,
                "komora_url": self.komora_url,
            }

        return params

    @staticmethod
    def get_info_from_cache(cache, id, include_tenant=False, additional_fields=[]):
        item = cache.get(id)
        if item:
            info = {
                "id": item.id,
                "name": item.name,
                "custom_fields": item.custom_fields,
            }
            for field in additional_fields:
                info[field] = getattr(item, field)
            if include_tenant and item.tenant:
                info["tenant"] = {
                    "id": str(item.tenant.id),
                    "name": item.tenant.name,
                    "custom_fields": item.tenant.custom_fields,
                }
            return info
        return None

    @staticmethod
    def get_nb_devices_data():
        nb = NetboxConnection.get_connection()

        # Fetch necessary data
        filter_device_roles = list(nb.dcim.device_roles.filter(name=["Passive component", "unknown", "Server"]))
        filter_device_role_ids = [device.id for device in filter_device_roles]

        devices = list(nb.dcim.devices.filter(status="active", name__empty=False, role_id__n=filter_device_role_ids))
        device_ids = [device.id for device in devices]
        interfaces = batch_query(nb.dcim.interfaces.filter, device_ids, batch_size=50, id_param="device_id")
        locations = list(nb.dcim.locations.all())
        sites = list(nb.dcim.sites.all())
        unique_tenant_ids = {device.tenant.id for device in devices if device.tenant}
        tenants = list(nb.tenancy.tenants.filter(tenant_id__in=list(unique_tenant_ids)))

        # Create caches
        interface_cache = {iface.device.id: [] for iface in interfaces}
        for iface in interfaces:
            interface_cache[iface.device.id].append(
                {"id": iface.id, "name": iface.name, "description": iface.description}
            )

        location_cache = {loc.id: loc for loc in locations}
        site_cache = {site.id: site for site in sites}
        tenant_cache = {tenant.id: tenant for tenant in tenants}

        # Construct the output data structure
        output_data = {
            "data": {
                "device_list": [
                    {
                        "id": str(device.id),
                        "name": device.name,
                        "primary_ip4": {
                            "id": device.primary_ip4.id,
                            "address": device.primary_ip4.address,
                        }
                        if device.primary_ip4
                        else None,
                        "comments": device.comments,
                        "serial": device.serial,
                        "custom_fields": device.custom_fields,
                        "location": NbDevice.get_info_from_cache(location_cache, device.location.id)
                        if device.location
                        else None,
                        "tenant": NbDevice.get_info_from_cache(tenant_cache, device.tenant.id)
                        if device.tenant
                        else None,
                        "site": NbDevice.get_info_from_cache(site_cache, device.site.id, include_tenant=True)
                        if device.site
                        else None,
                        "interfaces": interface_cache.get(device.id, []),
                    }
                    for device in devices
                ]
            }
        }

        return output_data

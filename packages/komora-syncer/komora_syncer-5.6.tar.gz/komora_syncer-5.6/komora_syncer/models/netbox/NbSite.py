from loguru import logger
from slugify import slugify

from komora_syncer.config import get_config
from komora_syncer.helpers.utils import sanitize_lat_lon
from komora_syncer.models.netbox.NbLocation import NbLocation
from komora_syncer.models.netbox.NetboxBase import NetboxBase
from komora_syncer.models.netbox.NetboxCache import NetboxCache


class NbSite(NetboxBase):
    def __init__(self, komora_obj):
        super().__init__()
        # Locations are already flatten via Komora site obj
        self.site_locations = komora_obj.flatten_locations

        self.name = komora_obj.name
        self.slug = slugify(self.name)

        self.description = komora_obj.fullName
        self.comments = komora_obj.description

        self.physical_address = komora_obj.address.text if komora_obj.address else ""
        self.shipping_address = ""
        self.latitude = sanitize_lat_lon(komora_obj.latitude)
        self.longitude = sanitize_lat_lon(komora_obj.longitude)

        self.komora_id = komora_obj.id
        self.komora_url = f"{get_config()['komora']['KOMORA_URL']}/app/site/{self.komora_id}"

        # site id
        self.code = komora_obj.code
        # Types: Připojný bod, virtuální bod, etc
        self.type_name = komora_obj.typeName
        self.type_id = komora_obj.typeId

        self.api_object = None
        self.region = None
        self.tenant = None

        try:
            if komora_obj.address:
                municipality_komora_id = komora_obj.address.municipalityId

                if municipality_komora_id:
                    self.region = self.nb.dcim.regions.get(cf_komora_id=municipality_komora_id)
            elif komora_obj.regionId:
                self.region = self.nb.dcim.regions.get(cf_komora_id=komora_obj.regionId)
        except Exception as e:
            logger.critical(f"Unable to find region {komora_obj.address} for site {self.name}")
            logger.exception(e)

        try:
            komora_org_id = komora_obj.organizationId

            if komora_org_id:
                self.tenant = self.nb.tenancy.tenants.get(cf_komora_id=komora_org_id)
        except Exception as e:
            logger.critical(f"Unable to find tenant {komora_obj.organization} for site {self.name}")
            logger.exception(e)

    def find(self):
        if self.komora_id is None:
            return self.api_object

        site_cache = NetboxCache.get_site_cache()
        netbox_site = (
            site_cache[self.komora_id]
            if self.komora_id in site_cache
            else self.nb.dcim.sites.get(cf_komora_id=self.komora_id)
        )
        if netbox_site:
            self.api_object = netbox_site

        return self.api_object

    def create(self):
        try:
            params = self.params
            netbox_site = self.nb.dcim.sites.create(params)

            logger.info("Site: %s created sucessfully", self.name)
            self.api_object = netbox_site
        except Exception as e:
            logger.exception("Unable to create netbox site: %s", self.name)
            raise e

        return self.api_object

    def update(self):
        try:
            if self.api_object.update(self.params):
                logger.info(f"Site: {self.name} updated successfuly")
        except Exception as e:
            logger.critical(f"Unable to update site {self.name}")
            logger.exception(e)

    def find_or_create(self):
        self.find()
        if self.api_object is None:
            self.create()

        return self.api_object

    def synchronize(self):
        site = self.find()

        if site:
            self.update()
        else:
            self.create()

        # sync location of site
        for location in self.site_locations:
            parent = (
                next(
                    (parent for parent in self.site_locations if parent.id == location.parentId),
                    None,
                )
                if location.parentId
                else None
            )

            nb_location = NbLocation(location, parent, self.api_object)
            nb_location.synchronize()

    @property
    def params(self):
        params = {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "comments": self.comments,
            "physical_address": self.physical_address,
            "shipping_address": self.shipping_address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "custom_fields": {
                "komora_id": self.komora_id,
                "komora_url": self.komora_url,
                "code": self.code,
                "type": self.type_name,
            },
        }

        if self.region:
            params["region"] = self.region.id

        if self.tenant:
            params["tenant"] = self.tenant.id

        return params

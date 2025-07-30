from loguru import logger
from slugify import slugify

from komora_syncer.helpers.utils import build_tenant_name
from komora_syncer.models.netbox.NetboxBase import NetboxBase
from komora_syncer.models.netbox.NetboxCache import NetboxCache


class NbProvider(NetboxBase):
    # komora_obj -> Organization(isSupplier=True)
    def __init__(self, komora_obj=None):
        super().__init__()
        self.name = build_tenant_name(komora_obj.clientId, komora_obj.name)
        self.slug = slugify(self.name)
        self.description = (
            " / ".join(komora_obj.keywords) if isinstance(komora_obj.keywords, list) else komora_obj.keywords
        )

        tenant = self.nb.tenancy.tenants.get(cf_komora_id=komora_obj.id)
        self.custom_fields = {
            "client_id": komora_obj.clientId,
            "client_name": komora_obj.name,
            "komora_id": komora_obj.id,
            "tenant": tenant.id if tenant else None,
        }

        self.api_object = None

    def find_or_create(self):
        self.find()
        if not self.api_object:
            self.create()

        return self.api_object

    def find(self):
        komora_id = self.custom_fields.get("komora_id")
        provider_cache = NetboxCache.get_provider_cache()

        try:
            if komora_id in provider_cache:
                netbox_provider = provider_cache[komora_id]
            else:
                netbox_provider = self.nb.circuits.providers.get(cf_komora_id=komora_id)

            if netbox_provider:
                self.api_object = netbox_provider
        except Exception:
            logger.exception(f"Unable to find provider by komora_id: {komora_id}")
            netbox_provider = None

        if not netbox_provider:
            try:
                netbox_provider = self.nb.circuits.providers.get(name__ie=self.name)

                if netbox_provider:
                    logger.warning(
                        f"komora_id: {str(komora_id)} was not found, but Provider {self.name} already exists"
                    )
                    self.api_object = netbox_provider
            except Exception:
                logger.exception(f"Unable to find provider by name: {self.name}")
                raise

        return self.api_object

    def create(self):
        try:
            netbox_provider = self.nb.circuits.providers.create(self.params)

            logger.info(f"Provider: {self.name} created successfully")
            self.api_object = netbox_provider
        except Exception:
            logger.exception(f"Unable to create netbox provider: {self.name}")
            raise

        return self.api_object

    def update(self, nb_provider):
        try:
            if nb_provider.update(self.params):
                self.api_object = nb_provider
                logger.info(f"Provider: {self.name} updated successfully")
        except Exception as e:
            logger.critical(
                f"Unable to update provider: {self.name} {nb_provider.id}",
            )
            logger.exception(e)

    def synchronize(self):
        provider = self.find()

        if provider:
            self.update(provider)
        else:
            self.create()

    @property
    def params(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "custom_fields": self.custom_fields,
        }

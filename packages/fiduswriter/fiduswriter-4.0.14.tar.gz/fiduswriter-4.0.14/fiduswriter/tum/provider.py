from allauth.socialaccount.app_settings import QUERY_EMAIL
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from .views import TUMOAuth2Adapter


class Scope(object):
    EMAIL = "GET@loc.user.email"
    UID = "GET@loc.user.uid"
    NAME = "GET@loc.user.name"


class TUMAccount(ProviderAccount):
    def to_str(self):
        dflt = super(TUMAccount, self).to_str()
        return self.account.extra_data.get("name", dflt)


class TUMProvider(OAuth2Provider):
    id = "tum"
    name = "TUM"
    account_class = TUMAccount
    oauth2_adapter_class = TUMOAuth2Adapter

    def get_default_scope(self):
        scope = [Scope.UID, Scope.NAME]
        if QUERY_EMAIL:
            scope.append(Scope.EMAIL)
        return scope

    def extract_uid(self, data):
        return str(data["sub"])

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
            last_name=data.get("family_name"),
            first_name=data.get("given_name"),
        )


provider_classes = [TUMProvider]

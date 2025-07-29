from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties
from cartography.models.core.nodes import CartographyNodeSchema
from cartography.models.core.relationships import CartographyRelProperties
from cartography.models.core.relationships import CartographyRelSchema
from cartography.models.core.relationships import LinkDirection
from cartography.models.core.relationships import make_target_node_matcher
from cartography.models.core.relationships import TargetNodeMatcher


@dataclass(frozen=True)
class KeycloakClientNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef('id')
    client_id: PropertyRef = PropertyRef('clientId')
    name: PropertyRef = PropertyRef('name')
    description: PropertyRef = PropertyRef('description')
    type: PropertyRef = PropertyRef('type')
    root_url: PropertyRef = PropertyRef('rootUrl')
    admin_url: PropertyRef = PropertyRef('adminUrl')
    base_url: PropertyRef = PropertyRef('baseUrl')
    surrogate_auth_required: PropertyRef = PropertyRef('surrogateAuthRequired')
    enabled: PropertyRef = PropertyRef('enabled')
    always_display_in_console: PropertyRef = PropertyRef('alwaysDisplayInConsole')
    client_authenticator_type: PropertyRef = PropertyRef('clientAuthenticatorType')
    secret: PropertyRef = PropertyRef('secret')
    registration_access_token: PropertyRef = PropertyRef('registrationAccessToken')
    not_before: PropertyRef = PropertyRef('notBefore')
    bearer_only: PropertyRef = PropertyRef('bearerOnly')
    consent_required: PropertyRef = PropertyRef('consentRequired')
    standard_flow_enabled: PropertyRef = PropertyRef('standardFlowEnabled')
    implicit_flow_enabled: PropertyRef = PropertyRef('implicitFlowEnabled')
    direct_access_grants_enabled: PropertyRef = PropertyRef('directAccessGrantsEnabled')
    service_accounts_enabled: PropertyRef = PropertyRef('serviceAccountsEnabled')
    authorization_services_enabled: PropertyRef = PropertyRef('authorizationServicesEnabled')
    direct_grants_only: PropertyRef = PropertyRef('directGrantsOnly')
    public_client: PropertyRef = PropertyRef('publicClient')
    frontchannel_logout: PropertyRef = PropertyRef('frontchannelLogout')
    protocol: PropertyRef = PropertyRef('protocol')
    full_scope_allowed: PropertyRef = PropertyRef('fullScopeAllowed')
    node_re_registration_timeout: PropertyRef = PropertyRef('nodeReRegistrationTimeout')
    client_template: PropertyRef = PropertyRef('clientTemplate')
    use_template_config: PropertyRef = PropertyRef('useTemplateConfig')
    use_template_scope: PropertyRef = PropertyRef('useTemplateScope')
    use_template_mappers: PropertyRef = PropertyRef('useTemplateMappers')
    origin: PropertyRef = PropertyRef('origin')
    protocol_mappers_id: PropertyRef = PropertyRef('protocolMappers.id')
    authorization_settings_id: PropertyRef = PropertyRef('authorizationSettings.id')
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
class KeycloakClientToRealmRelProperties(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef('lastupdated', set_in_kwargs=True)


@dataclass(frozen=True)
# (:KeycloakClient)<-[:RESOURCE]-(:KeycloakRealm)
class KeycloakClientToRealmRel(CartographyRelSchema):
    target_node_label: str = 'KeycloakRealm'
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher(
        {'id': PropertyRef('realm_id', set_in_kwargs=True)},
    )
    direction: LinkDirection = LinkDirection.INWARD
    rel_label: str = "RESOURCE"
    properties: KeycloakClientToRealmRelProperties = KeycloakClientToRealmRelProperties()




@dataclass(frozen=True)
class KeycloakClientSchema(CartographyNodeSchema):
    label: str = 'KeycloakClient'
    properties: KeycloakClientNodeProperties = KeycloakClientNodeProperties()
    sub_resource_relationship: KeycloakClientToRealmRel = KeycloakClientToRealmRel()

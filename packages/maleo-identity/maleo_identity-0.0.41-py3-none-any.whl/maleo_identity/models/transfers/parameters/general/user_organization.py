from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_identity.models.schemas.general.user_organization import MaleoIdentityUserOrganizationGeneralSchemas
from maleo_identity.models.schemas.parameters.user_organization import MaleoIdentityUserOrganizationParametersSchemas

class MaleoIdentityUserOrganizationGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class GetSingle(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        MaleoIdentityUserOrganizationParametersSchemas.Base
    ): pass

    class AssignQuery(
        MaleoIdentityUserOrganizationGeneralSchemas.Expand
    ): pass

    class AssignData(MaleoIdentityUserOrganizationParametersSchemas.Base): pass

    class Assign(
        AssignData,
        AssignQuery
    ): pass
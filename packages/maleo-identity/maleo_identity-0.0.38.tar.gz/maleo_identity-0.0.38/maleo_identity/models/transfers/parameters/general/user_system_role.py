from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_metadata.models.expanded_schemas.system_role import MaleoMetadataSystemRoleExpandedSchemas
from maleo_identity.models.schemas.general.user_system_role import MaleoIdentityUserSystemRoleGeneralSchemas
from maleo_identity.models.schemas.parameters.user_system_role import MaleoIdentityUserSystemRoleParametersSchemas

class MaleoIdentityUserSystemRoleGeneralParametersTransfers:
    class GetSingleQuery(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses
    ): pass

    class GetSingle(
        MaleoIdentityUserSystemRoleGeneralSchemas.Expand,
        BaseGeneralSchemas.Statuses,
        MaleoIdentityUserSystemRoleParametersSchemas.Base
    ): pass

    class AssignQuery(MaleoIdentityUserSystemRoleGeneralSchemas.Expand): pass

    class AssignFromUserBody(MaleoMetadataSystemRoleExpandedSchemas.SimpleSystemRole): pass

    class AssignData(MaleoIdentityUserSystemRoleParametersSchemas.Base): pass

    class Assign(AssignData, AssignQuery): pass
from enum import Enum

class EuRepoC(Enum):
    INCIDENTS = "/incidents"
    INCLUSION_CRITERIA = "/incidents/inclusion_criteria"
    SOURCES_OF_DISCLOSURE = "/incidents/sources_of_disclosure"
    OPERATION_TYPES = "/incidents/operation_types" #operation types are usually not required because they are included in incident main data
    INCIDENT_TYPES = "/incidents/incident_types"
    RECEIVERS = "/incidents/receivers"
    ATTRIBUTIONS = "/incidents/attributions"
    INITIATORS = "/incidents/initiators"
    CYBER_CONFLICT_ISSUES = "/incidents/cyber_conflict_issues"
    OFFLINE_CONFLICTS = "/incidents/offline_conflicts"
    POLITICAL_RESPONSES = "/incidents/political_responses"
    TECHNICAL_VARIABLES = "/incidents/technical_variables"
    CYBER_INTENSITY_VARIABLES = "/incidents/cyber_intensity_variables"
    MITRE_INITIAL_ACCESS = "/incidents/mitre_initial_access"
    MITRE_IMPACT = "/incidents/mitre_impact"
    IMPACT_INDICATOR_VARIABLES = "/incidents/impact_indicator_variables"
    LEGAL_VARIABLES = "/incidents/legal_variables"
    IL_BREACH_INDICATOR = "/incidents/il_breach_indicator"
    LEGAL_RESPONSES = "/incidents/legal_responses"
    SOURCES_URLS = "/incidents/sources_urls"
    ATTRIBUTION_SOURCES = "/incidents/attribution_sources"
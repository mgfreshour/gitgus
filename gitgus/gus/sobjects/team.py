"""Team."""
# Do not Edit this file.
# This file is generated from the "gitgus dev generate-sobjects" command
#
# Remember, you can always regenerate this file by running the above command.
# If you have made changes to this file, they will be lost.
# Edit template: sobject.py.jinja2

from datetime import date
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Self
from typing import Dict
from typing import List
from typing import Optional
from typing import Generator

from pydantic import Field, ConfigDict, computed_field
from ..gus_client import GUSClient
from .sobject_base import SObjectBase, SObjectType


class CurrencyIsoCodeEnum(str, Enum):
    """Currency ISO Code."""

    OPTION_0 = "AUD"
    OPTION_1 = "GBP"
    OPTION_2 = "CAD"
    OPTION_3 = "EUR"
    OPTION_4 = "INR"
    OPTION_5 = "JPY"
    OPTION_6 = "SGD"
    OPTION_7 = "SEK"
    OPTION_8 = "USD"


class VelocityTypeEnum(str, Enum):
    """Velocity Type."""

    OPTION_0 = "Story Points"
    OPTION_1 = "Record Count"


class EscalatePriorityEnum(str, Enum):
    """Escalate Priority."""

    OPTION_0 = "P0"
    OPTION_1 = "P1"
    OPTION_2 = "P2"


class PriorityForTotalNumOfCasesEnum(str, Enum):
    """Priority For Total Num of Cases."""

    OPTION_0 = "P0"
    OPTION_1 = "P1"
    OPTION_2 = "P2"


class KnownIssuesPriorityEnum(str, Enum):
    """Known Issues Priority."""

    OPTION_0 = "P0"
    OPTION_1 = "P1"
    OPTION_2 = "P2"


class TeamCategoryEnum(str, Enum):
    """Team Category."""

    OPTION_0 = "GTM"
    OPTION_1 = "Indirect Product Development"
    OPTION_2 = "Infrastructure"
    OPTION_3 = "Management Shared"
    OPTION_4 = "Non-Cloud Funded Shared Service"
    OPTION_5 = "Product Development"
    OPTION_6 = "Security"


class EnableTeamForOnCallSupportEnum(str, Enum):
    """Enable Team for On-Call Support."""

    OPTION_0 = "No"
    OPTION_1 = "Yes"


class BoardPreferenceEnum(str, Enum):
    """Board Preference."""

    OPTION_0 = "Sprint"
    OPTION_1 = "Kanban"


class Team(SObjectBase, metaclass=SObjectType):
    """Team."""

    _can_be_approved = True
    _base_sf_object = "ADM_Scrum_Team__c"

    model_config = ConfigDict(
        title="ADM_Scrum_Team__c",
        validate_assignment=True,
    )

    id_: str = Field(..., alias="Id", title="Record ID", frozen=True, exclude=True)
    owner_id: str = Field(..., alias="OwnerId", title="Owner ID", frozen=True, exclude=True)
    is_deleted: bool = Field(..., alias="IsDeleted", title="Deleted", frozen=True, exclude=True)
    name: Optional[str] = Field(..., alias="Name", title="Team Name", frozen=True, exclude=True)
    currency_iso_code: CurrencyIsoCodeEnum = Field(
        ..., alias="CurrencyIsoCode", title="Currency ISO Code", frozen=True, exclude=True
    )
    record_type_id: Optional[str] = Field(..., alias="RecordTypeId", title="Record Type ID", frozen=True, exclude=True)
    created_date: datetime = Field(..., alias="CreatedDate", title="Created Date", frozen=True, exclude=True)
    created_by_id: str = Field(..., alias="CreatedById", title="Created By ID", frozen=True, exclude=True)
    last_modified_date: datetime = Field(
        ..., alias="LastModifiedDate", title="Last Modified Date", frozen=True, exclude=True
    )
    last_modified_by_id: str = Field(
        ..., alias="LastModifiedById", title="Last Modified By ID", frozen=True, exclude=True
    )
    system_modstamp: datetime = Field(..., alias="SystemModstamp", title="System Modstamp", frozen=True, exclude=True)
    may_edit: bool = Field(..., alias="MayEdit", title="May Edit", frozen=True, exclude=True)
    is_locked: bool = Field(..., alias="IsLocked", title="Is Locked", frozen=True, exclude=True)
    last_viewed_date: Optional[datetime] = Field(
        ..., alias="LastViewedDate", title="Last Viewed Date", frozen=True, exclude=True
    )
    last_referenced_date: Optional[datetime] = Field(
        ..., alias="LastReferencedDate", title="Last Referenced Date", frozen=True, exclude=True
    )
    external_id: Optional[str] = Field(..., alias="External_ID__c", title="External ID", frozen=True, exclude=True)
    active: Optional[bool] = Field(..., alias="Active__c", title="Active", frozen=True, exclude=True)
    division: Optional[str] = Field(..., alias="Division__c", title="Division", frozen=True, exclude=True)
    external_name: Optional[str] = Field(
        ..., alias="External_Name__c", title="External Name", frozen=True, exclude=True
    )
    group_id_link: Optional[str] = Field(
        ..., alias="Group_ID_Link__c", title="Group ID Link", frozen=True, exclude=True
    )
    product_area: Optional[str] = Field(..., alias="Product_Area__c", title="Product Area", frozen=True, exclude=True)
    product_line: Optional[str] = Field(
        ..., alias="Product_Line__c", title="Product Line TO BE DELETED", frozen=True, exclude=True
    )
    rollup_reporting_group: Optional[str] = Field(
        ..., alias="Rollup_Reporting_Group__c", title="Rollup Reporting Group TO BE DELETED", frozen=True, exclude=True
    )
    scrum_meeting_time_location: Optional[str] = Field(
        ..., alias="Scrum_Meeting_Time_Location__c", title="Scrum Meeting Time/Location", frozen=True, exclude=True
    )
    scrum_team_domain: Optional[str] = Field(
        ..., alias="Scrum_Team_Domain__c", title="Scrum Team Domain", frozen=True, exclude=True
    )
    scrumforce_id: Optional[str] = Field(
        ..., alias="Scrumforce_ID__c", title="Scrumforce ID", frozen=True, exclude=True
    )
    story_point_scale: Optional[str] = Field(
        ..., alias="Story_Point_Scale__c", title="Story Point Scale", frozen=True, exclude=True
    )
    team_queue_id: Optional[str] = Field(
        ..., alias="Team_Queue_ID__c", title="Team Queue ID", frozen=True, exclude=True
    )
    team_queue: Optional[str] = Field(..., alias="Team_Queue__c", title="Team Queue", frozen=True, exclude=True)
    total_dev: Optional[float] = Field(..., alias="Total_Dev__c", title="Total Dev", frozen=True, exclude=True)
    total_members: Optional[float] = Field(
        ..., alias="Total_Members__c", title="Total Members", frozen=True, exclude=True
    )
    total_qe: Optional[float] = Field(..., alias="Total_QE__c", title="Total QE", frozen=True, exclude=True)
    total_dev_with_allocation: Optional[float] = Field(
        ..., alias="Total_Dev_with_Allocation__c", title="Total Dev with Allocation", frozen=True, exclude=True
    )
    total_members_with_allocation: Optional[float] = Field(
        ..., alias="Total_Members_with_Allocation__c", title="Total Members with Allocation", frozen=True, exclude=True
    )
    total_qe_with_allocation: Optional[float] = Field(
        ..., alias="Total_QE_with_Allocation__c", title="Total QE with Allocation", frozen=True, exclude=True
    )
    total_dev_allocation: Optional[float] = Field(
        ..., alias="Total_Dev_Allocation__c", title="Total Dev Allocation", frozen=True, exclude=True
    )
    total_member_allocation: Optional[float] = Field(
        ..., alias="Total_Member_Allocation__c", title="Total Member Allocation", frozen=True, exclude=True
    )
    total_qe_allocation: Optional[float] = Field(
        ..., alias="Total_QE_Allocation__c", title="Total QE Allocation", frozen=True, exclude=True
    )
    chatter_groups: Optional[str] = Field(
        ..., alias="Chatter_Groups__c", title="Lockout Notification Chatter Groups", frozen=True, exclude=True
    )
    copy_record_type_name: Optional[str] = Field(
        ..., alias="Copy_Record_Type_Name__c", title="Copy Record Type Name", frozen=True, exclude=True
    )
    distribution_lists: Optional[str] = Field(
        ..., alias="Distribution_Lists__c", title="Distribution Lists", frozen=True, exclude=True
    )
    end_date: Optional[date] = Field(..., alias="End_Date__c", title="End Date", frozen=True, exclude=True)
    overall_status: Optional[str] = Field(
        ..., alias="Overall_Status__c", title="Overall Status", frozen=True, exclude=True
    )
    start_date: Optional[date] = Field(..., alias="Start_Date__c", title="Start Date", frozen=True, exclude=True)
    status_report_format: Optional[str] = Field(
        ..., alias="Status_Report_Format__c", title="Status Report Sections", frozen=True, exclude=True
    )
    type_: Optional[str] = Field(..., alias="Type__c", title="Type", frozen=True, exclude=True)
    vision: Optional[str] = Field(..., alias="Vision__c", title="Team Charter", frozen=True, exclude=True)
    lock_report: Optional[str] = Field(..., alias="Lock_Report__c", title="Lock Report", frozen=True, exclude=True)
    cloud: Optional[str] = Field(..., alias="Cloud__c", title="Cloud (Deprecated)", frozen=True, exclude=True)
    domain: Optional[str] = Field(..., alias="Domain__c", title="Domain", frozen=True, exclude=True)
    release_coverage_needed: Optional[bool] = Field(
        ..., alias="Release_Coverage_Needed__c", title="Release Coverage Needed", frozen=True, exclude=True
    )
    team_home_page: Optional[str] = Field(
        ..., alias="Team_Home_Page__c", title="Team Homepage", frozen=True, exclude=True
    )
    kanban: Optional[bool] = Field(..., alias="Kanban__c", title="Kanban", frozen=True, exclude=True)
    cloud_lu: Optional[str] = Field(..., alias="Cloud_LU__c", title="Cloud", frozen=True, exclude=True)
    business_hours: Optional[str] = Field(
        ..., alias="Business_Hours__c", title="Business Hours", frozen=True, exclude=True
    )
    status_change_notify: Optional[bool] = Field(
        ..., alias="Status_Change_Notify__c", title="Status Change Notify", frozen=True, exclude=True
    )
    capex_enabled: Optional[bool] = Field(
        ..., alias="Capex_Enabled__c", title="Capitalizable", frozen=True, exclude=True
    )
    definition_of_done: Optional[str] = Field(
        ..., alias="Definition_of_Done__c", title="Definition of Done", frozen=True, exclude=True
    )
    definition_of_ready: Optional[str] = Field(
        ..., alias="Definition_of_Ready__c", title="Definition of Ready", frozen=True, exclude=True
    )
    capex_lead: Optional[str] = Field(
        ..., alias="Capex_Lead__c", title="Capitalization Lead", frozen=True, exclude=True
    )
    colocation: Optional[float] = Field(..., alias="Colocation__c", title="Colocation", frozen=True, exclude=True)
    po_certified: Optional[bool] = Field(..., alias="PO_Certified__c", title="PO Certified", frozen=True, exclude=True)
    po_more_than_one_team: Optional[bool] = Field(
        ..., alias="PO_more_than_one_team__c", title="PO more than one team", frozen=True, exclude=True
    )
    parent_cloud: Optional[str] = Field(..., alias="Parent_Cloud__c", title="Parent Cloud", frozen=True, exclude=True)
    product_owner: Optional[str] = Field(
        ..., alias="Product_Owner__c", title="Product Owner", frozen=True, exclude=True
    )
    sm_certified: Optional[bool] = Field(
        ..., alias="SM_Certified__c", title="Scrum Lead Certified", frozen=True, exclude=True
    )
    sm_more_than_one_team: Optional[bool] = Field(
        ..., alias="SM_more_than_one_team__c", title="Scrum Lead for more than one team", frozen=True, exclude=True
    )
    scrum_master: Optional[str] = Field(..., alias="Scrum_Master__c", title="Scrum Lead", frozen=True, exclude=True)
    team_size: Optional[float] = Field(..., alias="Team_Size__c", title="Team Size", frozen=True, exclude=True)
    tenure_on_team: Optional[float] = Field(
        ..., alias="Tenure_on_team__c", title="One year tenure on team", frozen=True, exclude=True
    )
    number_of_tenured_team_members: Optional[float] = Field(
        ..., alias="Number_of_Tenured_Team_Members__c", title="Number_100% Allocation", frozen=True, exclude=True
    )
    definition_of_done_check: Optional[bool] = Field(
        ..., alias="Definition_of_Done_Check__c", title="Definition of Done Check", frozen=True, exclude=True
    )
    definition_of_ready_check: Optional[bool] = Field(
        ..., alias="Definition_of_Ready_Check__c", title="Definition of Ready Check", frozen=True, exclude=True
    )
    number_80_allocated: Optional[float] = Field(
        ..., alias="Number_80_Allocated__c", title="Number 80% Allocated", frozen=True, exclude=True
    )
    forwarding_team: Optional[str] = Field(
        ..., alias="Forwarding_Team__c", title="Forwarding Team", frozen=True, exclude=True
    )
    don_t_use_ssdl_workflow: Optional[bool] = Field(
        ..., alias="Don_t_Use_SSDL_Workflow__c", title="SSDL Exempt", frozen=True, exclude=True
    )
    velocity_type: Optional[VelocityTypeEnum] = Field(
        ..., alias="Velocity_Type__c", title="Velocity Type", frozen=True, exclude=True
    )
    prefer_board_column_auto_update: Optional[bool] = Field(
        ...,
        alias="Prefer_Board_Column_Auto_Update__c",
        title="Prefer Board Column Auto Update",
        frozen=True,
        exclude=True,
    )
    average_age_of_bugs: Optional[float] = Field(
        ..., alias="Average_Age_of_Bugs__c", title="Average Age of Bugs", frozen=True, exclude=True
    )
    code_coverage: Optional[float] = Field(
        ..., alias="Code_Coverage__c", title="Code Coverage", frozen=True, exclude=True
    )
    number_of_open_bugs: Optional[float] = Field(
        ..., alias="Number_of_Open_Bugs__c", title="Number of Open Bugs", frozen=True, exclude=True
    )
    number_of_open_bugs_with_cases: Optional[float] = Field(
        ...,
        alias="Number_of_Open_Bugs_with_Cases__c",
        title="Number of Open Bugs with Cases",
        frozen=True,
        exclude=True,
    )
    number_of_open_investigations: Optional[float] = Field(
        ..., alias="Number_of_Open_Investigations__c", title="Number of Open Investigations", frozen=True, exclude=True
    )
    number_of_open_test_failure_bugs: Optional[float] = Field(
        ...,
        alias="Number_of_Open_Test_Failure_Bugs__c",
        title="Number of Open Test Failure Bugs",
        frozen=True,
        exclude=True,
    )
    say_do_ratio: Optional[float] = Field(
        ..., alias="Say_Do_ratio__c", title="Sprint Forecast Ratio", frozen=True, exclude=True
    )
    team_work_in_progress: Optional[float] = Field(
        ..., alias="Team_Work_In_Progress__c", title="# of Open Stories (WIP)", frozen=True, exclude=True
    )
    throughput_variation: Optional[float] = Field(
        ..., alias="Throughput_Variation__c", title="Throughput Variation", frozen=True, exclude=True
    )
    velocity_variation: Optional[float] = Field(
        ..., alias="Velocity_Variation__c", title="Velocity Variation", frozen=True, exclude=True
    )
    agile_health_overall: Optional[float] = Field(
        ..., alias="Agile_Health_Overall__c", title="Agile Health Overall", frozen=True, exclude=True
    )
    agile_survey_question_1: Optional[float] = Field(
        ..., alias="Agile_Survey_Question_1__c", title="Agile Survey Question 1", frozen=True, exclude=True
    )
    agile_survey_question_2: Optional[float] = Field(
        ..., alias="Agile_Survey_Question_2__c", title="Agile Survey Question 2", frozen=True, exclude=True
    )
    agile_survey_question_3: Optional[float] = Field(
        ..., alias="Agile_Survey_Question_3__c", title="Agile Survey Question 3", frozen=True, exclude=True
    )
    agile_survey_question_4: Optional[float] = Field(
        ..., alias="Agile_Survey_Question_4__c", title="Agile Survey Question 4", frozen=True, exclude=True
    )
    agile_survey_question_5: Optional[float] = Field(
        ..., alias="Agile_Survey_Question_5__c", title="Agile Survey Question 5", frozen=True, exclude=True
    )
    include_lightning_platform_freeze: Optional[bool] = Field(
        ...,
        alias="Include_Lightning_Platform_Freeze__c",
        title="Include Lightning Platform Freeze",
        frozen=True,
        exclude=True,
    )
    total_investment_theme_allocation: Optional[float] = Field(
        ...,
        alias="Total_Investment_Theme_Allocation__c",
        title="Total Investment Theme % Allocation",
        frozen=True,
        exclude=True,
    )
    security_survey: Optional[str] = Field(
        ..., alias="Security_Survey__c", title="Security Survey", frozen=True, exclude=True
    )
    has_team_members_in_roster: Optional[bool] = Field(
        ..., alias="Has_Team_Members_in_Roster__c", title="Has Team Members in Roster", frozen=True, exclude=True
    )
    exclude_capacity_reports: Optional[bool] = Field(
        ..., alias="Exclude_Capacity_Reports__c", title="Exclude from IT Capacity Reports", frozen=True, exclude=True
    )
    team_help_page: Optional[str] = Field(
        ..., alias="Team_help_page__c", title="Team help page", frozen=True, exclude=True
    )
    max_team_story_points: Optional[float] = Field(
        ..., alias="Max_Team_Story_Points__c", title="Max Team Story Points", frozen=True, exclude=True
    )
    case_velocity_enable: Optional[bool] = Field(
        ..., alias="Case_Velocity_Enable__c", title="Enable Case Velocity", frozen=True, exclude=True
    )
    escalate_priority: Optional[EscalatePriorityEnum] = Field(
        ..., alias="Escalate_Priority__c", title="Escalate Priority", frozen=True, exclude=True
    )
    number_of_days_for_org62_cases: Optional[float] = Field(
        ..., alias="Number_of_Days_for_Org62Cases__c", title="Number of Days for Org62Case", frozen=True, exclude=True
    )
    number_of_new_org62_cases: Optional[float] = Field(
        ..., alias="Number_of_new_org62_Cases__c", title="Number of new org62 Cases", frozen=True, exclude=True
    )
    org62_cases_num_enable: Optional[bool] = Field(
        ..., alias="Org62_Cases_Num_Enable__c", title="Enable Org62 Num of Cases", frozen=True, exclude=True
    )
    priority_for_total_num_of_cases: Optional[PriorityForTotalNumOfCasesEnum] = Field(
        ...,
        alias="Priority_For_Total_Num_of_Cases__c",
        title="Priority For Total Num of Cases",
        frozen=True,
        exclude=True,
    )
    total_num_of_org62_cases: Optional[float] = Field(
        ..., alias="Total_Num_of_Org62_Cases__c", title="Total Num of Org62 Cases", frozen=True, exclude=True
    )
    ssdl_form: Optional[str] = Field(..., alias="SSDL_Form__c", title="SSDL Form", frozen=True, exclude=True)
    agile_health_overall_score: Optional[float] = Field(
        ..., alias="Agile_Health_Overall_Score__c", title="Agile Health Overall Score", frozen=True, exclude=True
    )
    quip_url: Optional[str] = Field(..., alias="Quip_URL__c", title="Quip_URL", frozen=True, exclude=True)
    enforce_test_suites: Optional[bool] = Field(
        ..., alias="Enforce_Test_Suites__c", title="Enforce Test Suites", frozen=True, exclude=True
    )
    exempt_from_feature_release_freeze: Optional[bool] = Field(
        ...,
        alias="Exempt_from_Feature_Release_Freeze__c",
        title="Exempt From Feature & Release Freeze",
        frozen=True,
        exclude=True,
    )
    engineering_manager: Optional[str] = Field(
        ..., alias="Engineering_Manager__c", title="Engineering Manager", frozen=True, exclude=True
    )
    known_issues_count_enable: Optional[bool] = Field(
        ..., alias="Known_Issues_Count_Enable__c", title="Known Issues Count Enable", frozen=True, exclude=True
    )
    known_issues_count: Optional[float] = Field(
        ..., alias="Known_Issues_Count__c", title="Known Issues Count", frozen=True, exclude=True
    )
    known_issues_priority: Optional[KnownIssuesPriorityEnum] = Field(
        ..., alias="Known_Issues_Priority__c", title="Known Issues Priority", frozen=True, exclude=True
    )
    lt_l_enhanced_sla: Optional[bool] = Field(
        ..., alias="LtL_Enhanced_SLA__c", title="LtL Enhanced SLA", frozen=True, exclude=True
    )
    working_agreements: Optional[str] = Field(
        ..., alias="Working_Agreements__c", title="Working Agreements", frozen=True, exclude=True
    )
    public_slack_channel: Optional[str] = Field(
        ..., alias="Public_Slack_Channel__c", title="Public Team Slack Channel Link", frozen=True, exclude=True
    )
    ssdl_reporting_contact: Optional[str] = Field(
        ..., alias="SSDL_Reporting_Contact__c", title="SSDL Reporting Contact", frozen=True, exclude=True
    )
    security_assurance_team: Optional[str] = Field(
        ..., alias="Security_Assurance_Team__c", title="Security Assurance Team", frozen=True, exclude=True
    )
    has_working_agreement: Optional[bool] = Field(
        ..., alias="Has_Working_Agreement__c", title="Has Working Agreement", frozen=True, exclude=True
    )
    exempt_from_accessibility_reporting: Optional[bool] = Field(
        ...,
        alias="Exempt_From_Accessibility_Reporting__c",
        title="Exempt From Accessibility Reporting",
        frozen=True,
        exclude=True,
    )
    slack_channels: Optional[str] = Field(
        ..., alias="Slack_Channels__c", title="Slack Channel Id for Notifications", frozen=True, exclude=True
    )
    pager_duty_primary_team_url: Optional[str] = Field(
        ..., alias="Pager_Duty_Primary_Team_URL__c", title="PagerDuty Primary Team URL", frozen=True, exclude=True
    )
    ssdl_v2: Optional[bool] = Field(..., alias="SSDL_V2__c", title="SSDL V2", frozen=True, exclude=True)
    team_category: Optional[TeamCategoryEnum] = Field(
        ..., alias="Team_Category__c", title="Team Category", frozen=True, exclude=True
    )
    exempt_from_pager_duty_on_call: Optional[bool] = Field(
        ..., alias="Exempt_from_PagerDuty_On_Call__c", title="Exempt from PagerDuty On-Call", frozen=True, exclude=True
    )
    pager_duty_escalation_service_url: Optional[str] = Field(
        ...,
        alias="Pager_Duty_Escalation_Service_URL__c",
        title="PagerDuty Escalation Service URL",
        frozen=True,
        exclude=True,
    )
    l1_product_shared_service: Optional[str] = Field(
        ..., alias="L1_Product_Shared_Service__c", title="L1 APM Cloud / Shared Service", frozen=True, exclude=True
    )
    l2_apm_cloud_shared_service: Optional[str] = Field(
        ..., alias="L2_APM_Cloud_Shared_Service__c", title="L2 APM Cloud / Shared Service", frozen=True, exclude=True
    )
    description: Optional[str] = Field(..., alias="Description__c", title="Description", frozen=True, exclude=True)
    enable_team_for_on_call_support: Optional[EnableTeamForOnCallSupportEnum] = Field(
        ...,
        alias="Enable_Team_for_On_Call_Support__c",
        title="Enable Team for On-Call Support",
        frozen=True,
        exclude=True,
    )
    last_sync_for_on_call: Optional[datetime] = Field(
        ..., alias="Last_sync_for_on_call__c", title="Last Sync for On-Call Setup", frozen=True, exclude=True
    )
    board_preference: Optional[BoardPreferenceEnum] = Field(
        ..., alias="Board_Preference__c", title="Board Preference", frozen=True, exclude=True
    )
    l3_product_shared_service: Optional[str] = Field(
        ..., alias="L3_Product_Shared_Service__c", title="L3 APM Cloud / Shared Service", frozen=True, exclude=True
    )
    l4_product_shared_service: Optional[str] = Field(
        ..., alias="L4_Product_Shared_Service__c", title="L4 APM Cloud / Shared Service", frozen=True, exclude=True
    )
    public_slack_channel_name: Optional[str] = Field(
        ..., alias="Public_Slack_Channel_Name__c", title="Public Slack Channel Name", frozen=True, exclude=True
    )
    public_slack_channel_url: Optional[str] = Field(
        ..., alias="Public_Slack_Channel_URL__c", title="Public Slack Channel", frozen=True, exclude=True
    )
    sa_component_review: Optional[bool] = Field(
        ..., alias="SA_Component_Review__c", title="SA Component Review", frozen=True, exclude=True
    )

    @property
    def owner_name(self):
        return self._get_connected_object_name(["Group", "User"], self.owner_id)

    @property
    def record_type_name(self):
        return self._get_connected_object_name(["RecordType"], self.record_type_id)

    @property
    def created_by_name(self):
        return self._get_connected_object_name(["User"], self.created_by_id)

    @property
    def last_modified_by_name(self):
        return self._get_connected_object_name(["User"], self.last_modified_by_id)

    @property
    def cloud_lu_name(self):
        return self._get_connected_object_name(["ADM_Cloud__c"], self.cloud_lu)

    @property
    def business_hours_name(self):
        return self._get_connected_object_name(["BusinessHours"], self.business_hours)

    @property
    def capex_lead_name(self):
        return self._get_connected_object_name(["User"], self.capex_lead)

    @property
    def product_owner_name(self):
        return self._get_connected_object_name(["User"], self.product_owner)

    @property
    def scrum_master_name(self):
        return self._get_connected_object_name(["User"], self.scrum_master)

    @property
    def forwarding_team_name(self):
        return self._get_connected_object_name(["ADM_Scrum_Team__c"], self.forwarding_team)

    @property
    def security_survey_name(self):
        return self._get_connected_object_name(["Survey"], self.security_survey)

    @property
    def ssdl_form_name(self):
        return self._get_connected_object_name(["ADM_Form__c"], self.ssdl_form)

    @property
    def engineering_manager_name(self):
        return self._get_connected_object_name(["User"], self.engineering_manager)

    @property
    def ssdl_reporting_contact_name(self):
        return self._get_connected_object_name(["User"], self.ssdl_reporting_contact)

    @property
    def security_assurance_team_name(self):
        return self._get_connected_object_name(["ADM_Security_Assurance_Team__c"], self.security_assurance_team)

    @property
    def l1_product_shared_service_name(self):
        return self._get_connected_object_name(["RSTR_L1_Product_Shared_Service__c"], self.l1_product_shared_service)

    @property
    def l2_apm_cloud_shared_service_name(self):
        return self._get_connected_object_name(["RSTR_L2_Product_Shared_Service__c"], self.l2_apm_cloud_shared_service)

    @property
    def l3_product_shared_service_name(self):
        return self._get_connected_object_name(["RSTR_L2_Product_Shared_Service__c"], self.l3_product_shared_service)

    @property
    def l4_product_shared_service_name(self):
        return self._get_connected_object_name(["RSTR_L2_Product_Shared_Service__c"], self.l4_product_shared_service)

    def __init__(self, **kwargs: Any):
        """
        Initialize Salesforce Object.

        :param **kwargs: keyword arguments
        """
        super().__init__(**kwargs)

    @property
    def web_url(self) -> str:
        """
        Web URL.

        :returns: web url
        """
        return f"https://{GUSClient.instance().sf.sf_instance}/{self.id_}"

    @classmethod
    def get_by_id(cls, id_: str) -> Self:
        """
        Get team.

        :param id_: Salesforce Object Id
        :returns: Team object
        """
        x = GUSClient.instance().sf.__getattr__("ADM_Scrum_Team__c").get(id_)
        return Team(**{"sf": GUSClient.instance().sf, **x})

    @classmethod
    def soql_query(cls, where_clause: str) -> Generator[Self, None, None]:
        """
        Query Teams by SOQL WHERE clause.

        :param where_clause: where clause of SOQL query
        :yields: Team objects
        """
        for x in cls._query_soql("ADM_Scrum_Team__c", where_clause):
            yield Team(**x)
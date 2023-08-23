"""Release."""
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


class MajorReleaseTypeEnum(str, Enum):
    """Major Release Type."""

    OPTION_0 = "SB0"
    OPTION_1 = "R0"
    OPTION_2 = "R1"
    OPTION_3 = "SB1"
    OPTION_4 = "SB2"
    OPTION_5 = "R2a"
    OPTION_6 = "R2b"


class RollbackStatusEnum(str, Enum):
    """Rollback Status."""

    OPTION_0 = "Can Rollback"
    OPTION_1 = "Cannot Rollback"


class BranchEnum(str, Enum):
    """Branch."""

    OPTION_0 = "prod"
    OPTION_1 = "freeze"
    OPTION_2 = "patch"
    OPTION_3 = "main"
    OPTION_4 = "mainfreeze"


class MajorReleaseCycleEnum(str, Enum):
    """Major Release Cycle."""

    OPTION_0 = "SB0"
    OPTION_1 = "SB1"
    OPTION_2 = "SB2"
    OPTION_3 = "R0"
    OPTION_4 = "R1"
    OPTION_5 = "R2"
    OPTION_6 = "R2a"
    OPTION_7 = "R2b"
    OPTION_8 = "R3"
    OPTION_9 = "BYPASS"


class Release(SObjectBase, metaclass=SObjectType):
    """Release."""

    _can_be_approved = True
    _base_sf_object = "ADM_Release__c"

    model_config = ConfigDict(
        title="ADM_Release__c",
        validate_assignment=True,
    )

    id_: str = Field(..., alias="Id", title="Record ID", frozen=True, exclude=True)
    owner_id: str = Field(..., alias="OwnerId", title="Owner ID", frozen=True, exclude=True)
    is_deleted: bool = Field(..., alias="IsDeleted", title="Deleted", frozen=True, exclude=True)
    name: Optional[str] = Field(..., alias="Name", title="Release Name", frozen=True, exclude=True)
    currency_iso_code: CurrencyIsoCodeEnum = Field(
        ..., alias="CurrencyIsoCode", title="Currency ISO Code", frozen=True, exclude=True
    )
    created_date: datetime = Field(..., alias="CreatedDate", title="Created Date", frozen=True, exclude=True)
    created_by_id: str = Field(..., alias="CreatedById", title="Created By ID", frozen=True, exclude=True)
    last_modified_date: datetime = Field(
        ..., alias="LastModifiedDate", title="Last Modified Date", frozen=True, exclude=True
    )
    last_modified_by_id: str = Field(
        ..., alias="LastModifiedById", title="Last Modified By ID", frozen=True, exclude=True
    )
    system_modstamp: datetime = Field(..., alias="SystemModstamp", title="System Modstamp", frozen=True, exclude=True)
    last_activity_date: Optional[date] = Field(
        ..., alias="LastActivityDate", title="Last Activity Date", frozen=True, exclude=True
    )
    may_edit: bool = Field(..., alias="MayEdit", title="May Edit", frozen=True, exclude=True)
    is_locked: bool = Field(..., alias="IsLocked", title="Is Locked", frozen=True, exclude=True)
    last_viewed_date: Optional[datetime] = Field(
        ..., alias="LastViewedDate", title="Last Viewed Date", frozen=True, exclude=True
    )
    last_referenced_date: Optional[datetime] = Field(
        ..., alias="LastReferencedDate", title="Last Referenced Date", frozen=True, exclude=True
    )
    api_version: Optional[str] = Field(..., alias="API_version__c", title="API version", frozen=True, exclude=True)
    build: Optional[str] = Field(..., alias="Build__c", title="Build", frozen=True, exclude=True)
    external_id: Optional[str] = Field(..., alias="External_ID__c", title="External ID", frozen=True, exclude=True)
    release_date: Optional[datetime] = Field(
        ..., alias="Release_Date__c", title="Base Release Date", frozen=True, exclude=True
    )
    release_type: Optional[str] = Field(..., alias="Release_Type__c", title="Release Type", frozen=True, exclude=True)
    short_note: Optional[str] = Field(..., alias="Short_Note__c", title="Short Note", frozen=True, exclude=True)
    note: Optional[str] = Field(..., alias="Note__c", title="Note", frozen=True, exclude=True)
    created_by_import: Optional[str] = Field(
        ..., alias="Created_By_import__c", title="Created By (import)", frozen=True, exclude=True
    )
    created_on_import: Optional[datetime] = Field(
        ..., alias="Created_On_import__c", title="Created On (import)", frozen=True, exclude=True
    )
    number_of_bugs: Optional[float] = Field(
        ..., alias="Number_of_Bugs__c", title="Number of Work Records", frozen=True, exclude=True
    )
    status: Optional[str] = Field(..., alias="Status__c", title="Status", frozen=True, exclude=True)
    week_prior_to_release: Optional[float] = Field(
        ..., alias="Week_Prior_to_Release__c", title="Week Prior to Release", frozen=True, exclude=True
    )
    actual_release_date: Optional[datetime] = Field(
        ..., alias="Actual_Release_Date__c", title="Actual Release Date", frozen=True, exclude=True
    )
    planned_gus_release_date: Optional[datetime] = Field(
        ..., alias="Planned_GUS_Release_Date__c", title="Scheduled GS0 Release Date", frozen=True, exclude=True
    )
    planned_unplanned: Optional[str] = Field(
        ..., alias="Planned_Unplanned__c", title="Daily / Planned / Unplanned", frozen=True, exclude=True
    )
    deployment_delayed_minutes: Optional[float] = Field(
        ..., alias="Deployment_Delayed_minutes__c", title="Deployment Delayed (minutes)", frozen=True, exclude=True
    )
    release_delay_category: Optional[str] = Field(
        ..., alias="Release_Delay_Category__c", title="Release Delay Category", frozen=True, exclude=True
    )
    duplicate_validator: Optional[str] = Field(
        ..., alias="Duplicate_Validator__c", title="Duplicate Validator", frozen=True, exclude=True
    )
    number_of_stamps: Optional[float] = Field(
        ..., alias="Number_of_Stamps__c", title="Number of Stamps", frozen=True, exclude=True
    )
    release_manager: Optional[str] = Field(
        ..., alias="Release_Manager__c", title="Release Manager", frozen=True, exclude=True
    )
    planned_duration: Optional[float] = Field(
        ..., alias="Planned_Duration__c", title="Planned Duration", frozen=True, exclude=True
    )
    planned_g_s0_duration: Optional[float] = Field(
        ..., alias="Planned_GS0_Duration__c", title="Planned GS0 Duration", frozen=True, exclude=True
    )
    planned_g_s0_end_date: Optional[datetime] = Field(
        ..., alias="Planned_GS0_End_Date__c", title="Scheduled GS0 End Date", frozen=True, exclude=True
    )
    scheduled_end_date: Optional[datetime] = Field(
        ..., alias="Scheduled_End_Date__c", title="Base End Date", frozen=True, exclude=True
    )
    customer_facing_release_name: Optional[str] = Field(
        ..., alias="Customer_Facing_Release_Name__c", title="Customer Facing Release Name", frozen=True, exclude=True
    )
    application: Optional[str] = Field(..., alias="Application__c", title="Application", frozen=True, exclude=True)
    deployment_instances: Optional[str] = Field(
        ..., alias="Deployment_Instances__c", title="Deployment Instances", frozen=True, exclude=True
    )
    additional_information_for_customers: Optional[str] = Field(
        ...,
        alias="Additional_Information_for_Customers__c",
        title="Additional Information for Customers",
        frozen=True,
        exclude=True,
    )
    availability_during_maintenance: Optional[str] = Field(
        ...,
        alias="Availability_during_maintenance__c",
        title="Availability during maintenance",
        frozen=True,
        exclude=True,
    )
    explain_other_delay: Optional[str] = Field(
        ..., alias="Explain_Other_Delay__c", title="Explain Other Delay", frozen=True, exclude=True
    )
    release_delay_reason: Optional[str] = Field(
        ..., alias="Release_Delay_Reason__c", title="Release Delay Reason", frozen=True, exclude=True
    )
    release_coverage: Optional[str] = Field(
        ..., alias="Release_Coverage__c", title="Release Coverage", frozen=True, exclude=True
    )
    verification_complete_date: Optional[datetime] = Field(
        ..., alias="Verification_Complete_Date__c", title="Verification Complete Date", frozen=True, exclude=True
    )
    verification_delay_category: Optional[str] = Field(
        ..., alias="Verification_Delay_Category__c", title="Verification Delay Category", frozen=True, exclude=True
    )
    verification_delayed: Optional[float] = Field(
        ..., alias="Verification_Delayed__c", title="Verification Delayed", frozen=True, exclude=True
    )
    major_release_type: Optional[MajorReleaseTypeEnum] = Field(
        ..., alias="MajorReleaseType__c", title="Major Release Type", frozen=True, exclude=True
    )
    major_release: Optional[str] = Field(
        ..., alias="Major_Release__c", title="Major Release", frozen=True, exclude=True
    )
    chatter_post_id: Optional[str] = Field(
        ..., alias="Chatter_Post_ID__c", title="Chatter Post ID", frozen=True, exclude=True
    )
    rollback_status: Optional[RollbackStatusEnum] = Field(
        ..., alias="Rollback_Status__c", title="Rollback Status", frozen=True, exclude=True
    )
    application_activity_plan: Optional[str] = Field(
        ..., alias="Application_Activity_Plan__c", title="Application Activity Plan", frozen=True, exclude=True
    )
    verification_release_event_1: Optional[str] = Field(
        ..., alias="Verification_Release_Event_1__c", title="Verification Release Event 1", frozen=True, exclude=True
    )
    verification_release_event_2: Optional[str] = Field(
        ..., alias="Verification_Release_Event_2__c", title="Verification Release Event 2", frozen=True, exclude=True
    )
    branch: Optional[BranchEnum] = Field(..., alias="Branch__c", title="Branch", frozen=True, exclude=True)
    build_freeze: Optional[datetime] = Field(
        ..., alias="Build_Freeze__c", title="Release Freeze", frozen=True, exclude=True
    )
    release_cycle_status: Optional[str] = Field(
        ..., alias="Release_Cycle_Status__c", title="Release Cycle Status", frozen=True, exclude=True
    )
    verification_event_1_date: Optional[datetime] = Field(
        ..., alias="Verification_Event_1_Date__c", title="Verification Event 1 Date", frozen=True, exclude=True
    )
    verification_event_2_date: Optional[datetime] = Field(
        ..., alias="Verification_Event_2_Date__c", title="Verification Event 2 Date", frozen=True, exclude=True
    )
    staging_branch: Optional[str] = Field(
        ..., alias="Staging_Branch__c", title="Staging Branch", frozen=True, exclude=True
    )
    staging_change_list: Optional[str] = Field(
        ..., alias="Staging_Change_List__c", title="Staging Change List", frozen=True, exclude=True
    )
    staging_directives: Optional[str] = Field(
        ..., alias="Staging_Directives__c", title="Staging Directives", frozen=True, exclude=True
    )
    engineering_manager: Optional[str] = Field(
        ..., alias="Engineering_Manager__c", title="Engineering Manager", frozen=True, exclude=True
    )
    current_case: Optional[str] = Field(..., alias="Current_Case__c", title="Current Case", frozen=True, exclude=True)
    target_instances: Optional[str] = Field(
        ..., alias="Target_Instances__c", title="Release Targets", frozen=True, exclude=True
    )
    should_not_cannot_rollback_reason: Optional[str] = Field(
        ..., alias="Should_Not_Cannot_Rollback_Reason__c", title="Cannot Rollback Reason", frozen=True, exclude=True
    )
    gia_release_event_count: Optional[float] = Field(
        ..., alias="GIA_Release_Event_Count__c", title="GIA Release Event Count", frozen=True, exclude=True
    )
    release_cycle: Optional[str] = Field(
        ..., alias="Release_Cycle__c", title="Release Cycle", frozen=True, exclude=True
    )
    major_release_cycle: Optional[MajorReleaseCycleEnum] = Field(
        ..., alias="Major_Release_Cycle__c", title="Major Release Cycle", frozen=True, exclude=True
    )
    number_of_p0_work_items: Optional[float] = Field(
        ..., alias="Number_of_P0_Work_Items__c", title="Number of P0 Work Items", frozen=True, exclude=True
    )

    @property
    def owner_name(self):
        return self._get_connected_object_name(["Group", "User"], self.owner_id)

    @property
    def created_by_name(self):
        return self._get_connected_object_name(["User"], self.created_by_id)

    @property
    def last_modified_by_name(self):
        return self._get_connected_object_name(["User"], self.last_modified_by_id)

    @property
    def build_name(self):
        return self._get_connected_object_name(["ADM_Build__c"], self.build)

    @property
    def created_by_import_name(self):
        return self._get_connected_object_name(["User"], self.created_by_import)

    @property
    def release_manager_name(self):
        return self._get_connected_object_name(["User"], self.release_manager)

    @property
    def application_name(self):
        return self._get_connected_object_name(["ADM_Application__c"], self.application)

    @property
    def release_coverage_name(self):
        return self._get_connected_object_name(["ONC_Event_Coverage__c"], self.release_coverage)

    @property
    def major_release_name(self):
        return self._get_connected_object_name(["ADM_Release__c"], self.major_release)

    @property
    def application_activity_plan_name(self):
        return self._get_connected_object_name(["ADM_Application_Activity_Plan__c"], self.application_activity_plan)

    @property
    def verification_release_event_1_name(self):
        return self._get_connected_object_name(["ADM_Release_Event__c"], self.verification_release_event_1)

    @property
    def verification_release_event_2_name(self):
        return self._get_connected_object_name(["ADM_Release_Event__c"], self.verification_release_event_2)

    @property
    def engineering_manager_name(self):
        return self._get_connected_object_name(["User"], self.engineering_manager)

    @property
    def current_case_name(self):
        return self._get_connected_object_name(["Case"], self.current_case)

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
        Get release.

        :param id_: Salesforce Object Id
        :returns: Release object
        """
        x = GUSClient.instance().sf.__getattr__("ADM_Release__c").get(id_)
        return Release(**{"sf": GUSClient.instance().sf, **x})

    @classmethod
    def soql_query(cls, where_clause: str) -> Generator[Self, None, None]:
        """
        Query Releases by SOQL WHERE clause.

        :param where_clause: where clause of SOQL query
        :yields: Release objects
        """
        for x in cls._query_soql("ADM_Release__c", where_clause):
            yield Release(**x)
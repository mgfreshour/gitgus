"""Build."""
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


class Build(SObjectBase, metaclass=SObjectType):
    """Build."""

    _can_be_approved = True
    _base_sf_object = "ADM_Build__c"

    model_config = ConfigDict(
        title="ADM_Build__c",
        validate_assignment=True,
    )

    id_: str = Field(..., alias="Id", title="Record ID", frozen=True, exclude=True)
    owner_id: str = Field(..., alias="OwnerId", title="Owner ID", frozen=True, exclude=True)
    is_deleted: bool = Field(..., alias="IsDeleted", title="Deleted", frozen=True, exclude=True)
    name: Optional[str] = Field(..., alias="Name", title="Name", frozen=True, exclude=True)
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
    may_edit: bool = Field(..., alias="MayEdit", title="May Edit", frozen=True, exclude=True)
    is_locked: bool = Field(..., alias="IsLocked", title="Is Locked", frozen=True, exclude=True)
    last_viewed_date: Optional[datetime] = Field(
        ..., alias="LastViewedDate", title="Last Viewed Date", frozen=True, exclude=True
    )
    last_referenced_date: Optional[datetime] = Field(
        ..., alias="LastReferencedDate", title="Last Referenced Date", frozen=True, exclude=True
    )
    external_id: Optional[str] = Field(..., alias="External_ID__c", title="External ID", frozen=True, exclude=True)
    scrumforce_id: Optional[str] = Field(
        ..., alias="Scrumforce_ID__c", title="Scrumforce ID", frozen=True, exclude=True
    )
    release_freeze: Optional[date] = Field(
        ..., alias="Release_Freeze__c", title="Release Freeze (legacy)", frozen=True, exclude=True
    )
    weeks_prior_to_release: Optional[float] = Field(
        ..., alias="Weeks_prior_to_release__c", title="Weeks Prior to Release", frozen=True, exclude=True
    )
    release_freeze_datetime: Optional[datetime] = Field(
        ..., alias="Release_Freeze_Datetime__c", title="Release Freeze", frozen=True, exclude=True
    )
    duplicate_validator: Optional[str] = Field(
        ..., alias="Duplicate_Validator__c", title="Duplicate Validator", frozen=True, exclude=True
    )
    require_checkin_to_create_freeze_records: Optional[bool] = Field(
        ...,
        alias="Require_Checkin_to_create_Freeze_Records__c",
        title="Require Checkin To Create Freeze Records",
        frozen=True,
        exclude=True,
    )
    weeks_after_sandbox: Optional[float] = Field(
        ..., alias="Weeks_After_Sandbox__c", title="Weeks After Sandbox", frozen=True, exclude=True
    )
    weeks_prior_to_feature_freeze: Optional[float] = Field(
        ..., alias="Weeks_Prior_to_Feature_Freeze__c", title="Weeks Prior to Feature Freeze", frozen=True, exclude=True
    )
    code_line_open: Optional[date] = Field(
        ..., alias="Code_Line_Open__c", title="Code Line Open", frozen=True, exclude=True
    )
    feature_freeze: Optional[date] = Field(
        ..., alias="Feature_Freeze__c", title="Feature Freeze", frozen=True, exclude=True
    )
    lightning_platform_and_s1_hybrid_ff: Optional[date] = Field(
        ...,
        alias="Lightning_Platform_and_S1_Hybrid_FF__c",
        title="Lightning Platform and S1 Hybrid FF",
        frozen=True,
        exclude=True,
    )
    schema_freeze: Optional[date] = Field(
        ..., alias="Schema_Freeze__c", title="Schema Freeze", frozen=True, exclude=True
    )
    application: Optional[str] = Field(..., alias="Application__c", title="Application", frozen=True, exclude=True)
    notification_type: Optional[str] = Field(
        ..., alias="Notification_Type__c", title="Notification Type", frozen=True, exclude=True
    )
    send_open_work_notifications: Optional[bool] = Field(
        ..., alias="Send_Open_Work_Notifications__c", title="Send Open Work Notifications", frozen=True, exclude=True
    )
    freeze_signoffs: Optional[str] = Field(
        ..., alias="Freeze_Signoffs__c", title="Freeze Signoffs", frozen=True, exclude=True
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
    def application_name(self):
        return self._get_connected_object_name(["ADM_Application__c"], self.application)

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
        Get build.

        :param id_: Salesforce Object Id
        :returns: Build object
        """
        x = GUSClient.instance().sf.__getattr__("ADM_Build__c").get(id_)
        return Build(**{"sf": GUSClient.instance().sf, **x})

    @classmethod
    def soql_query(cls, where_clause: str) -> Generator[Self, None, None]:
        """
        Query Builds by SOQL WHERE clause.

        :param where_clause: where clause of SOQL query
        :yields: Build objects
        """
        for x in cls._query_soql("ADM_Build__c", where_clause):
            yield Build(**x)

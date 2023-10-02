"""Planned Release."""
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


class PlannedRelease(SObjectBase, metaclass=SObjectType):
    """Planned Release."""

    _can_be_approved = True
    _base_sf_object = "ADM_Planned_Release__c"

    model_config = ConfigDict(
        title="ADM_Planned_Release__c",
        validate_assignment=True,
    )

    id_: str = Field(..., alias="Id", title="Record ID", frozen=True, exclude=True)
    owner_id: str = Field(..., alias="OwnerId", title="Owner ID")
    is_deleted: bool = Field(
        ..., alias="IsDeleted", title="Deleted", frozen=True, exclude=True
    )
    name: Optional[str] = Field(..., alias="Name", title="Planned Release Name")
    currency_iso_code: Optional[CurrencyIsoCodeEnum] = Field(
        ..., alias="CurrencyIsoCode", title="Currency ISO Code"
    )
    created_date: datetime = Field(
        ..., alias="CreatedDate", title="Created Date", frozen=True, exclude=True
    )
    created_by_id: str = Field(
        ..., alias="CreatedById", title="Created By ID", frozen=True, exclude=True
    )
    last_modified_date: datetime = Field(
        ...,
        alias="LastModifiedDate",
        title="Last Modified Date",
        frozen=True,
        exclude=True,
    )
    last_modified_by_id: str = Field(
        ...,
        alias="LastModifiedById",
        title="Last Modified By ID",
        frozen=True,
        exclude=True,
    )
    system_modstamp: datetime = Field(
        ..., alias="SystemModstamp", title="System Modstamp", frozen=True, exclude=True
    )
    last_activity_date: Optional[date] = Field(
        ...,
        alias="LastActivityDate",
        title="Last Activity Date",
        frozen=True,
        exclude=True,
    )
    may_edit: bool = Field(
        ..., alias="MayEdit", title="May Edit", frozen=True, exclude=True
    )
    is_locked: bool = Field(
        ..., alias="IsLocked", title="Is Locked", frozen=True, exclude=True
    )
    last_viewed_date: Optional[datetime] = Field(
        ..., alias="LastViewedDate", title="Last Viewed Date", frozen=True, exclude=True
    )
    last_referenced_date: Optional[datetime] = Field(
        ...,
        alias="LastReferencedDate",
        title="Last Referenced Date",
        frozen=True,
        exclude=True,
    )
    end_date: Optional[date] = Field(..., alias="End_Date__c", title="End Date")
    goals_objectives: Optional[str] = Field(
        ..., alias="Goals_Objectives__c", title="Goals, Objectives, and Risks"
    )
    start_date: Optional[date] = Field(..., alias="Start_Date__c", title="Start Date")
    team: Optional[str] = Field(..., alias="Team__c", title="Team")
    forecast_items_completed: Optional[float] = Field(
        ..., alias="Forecast_Items_Completed__c", title="# Forecast Epics Completed"
    )
    forecast_items: Optional[float] = Field(
        ..., alias="Forecast_Items__c", title="# Forecast Epics"
    )
    quip_document: Optional[str] = Field(
        ..., alias="Quip_Document__c", title="Quip Document"
    )
    release: Optional[str] = Field(..., alias="Release__c", title="Release")
    number_epics_added: Optional[float] = Field(
        ..., alias="Number_Epics_Added__c", title="# Epics Added"
    )
    number_forecast_epics_removed: Optional[float] = Field(
        ..., alias="Number_Forecast_Epics_Removed__c", title="# Forecast Epics Removed"
    )
    number_forecast_work_items_completed: Optional[float] = Field(
        ...,
        alias="Number_Forecast_Work_Items_Completed__c",
        title="# Forecast Work Items Completed",
    )
    number_forecast_work_items_removed: Optional[float] = Field(
        ...,
        alias="Number_Forecast_Work_Items_Removed__c",
        title="# Forecast Work Items Removed",
    )
    number_forecast_work_items: Optional[float] = Field(
        ..., alias="Number_Forecast_Work_Items__c", title="# Forecast Work Items"
    )
    number_work_items_added: Optional[float] = Field(
        ..., alias="Number_Work_Items_Added__c", title="# Work Items Added"
    )
    number_forecast_story_points: Optional[float] = Field(
        ..., alias="Number_Forecast_Story_Points__c", title="# Forecast Story Points"
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
    def team_name(self):
        return self._get_connected_object_name(["ADM_Scrum_Team__c"], self.team)

    @property
    def release_name(self):
        return self._get_connected_object_name(["ADM_Release__c"], self.release)

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
        Get planned release.

        :param id_: Salesforce Object Id
        :returns: Planned Release object
        """
        x = GUSClient.instance().sf.__getattr__("ADM_Planned_Release__c").get(id_)
        return PlannedRelease(**{"sf": GUSClient.instance().sf, **x})

    @classmethod
    def create(cls, **kwargs: Any) -> Self:
        """
        Create planned release.
        :param **kwargs: values for the fields of the Planned Release object
        :returns: Planned Release object
        :raises RuntimeError: if object creation failed
        """
        lookup = cls._get_field_to_sf_name_dict()
        fields = {lookup[k]: v for k, v in kwargs.items()}
        return cls._create("FeedItem", fields)

    @classmethod
    def update(cls, model: Self, headers: Optional[Dict[str, str]] = None) -> None:
        """
        Update Salesforce API with changes.
        :param model: Planned Release object to update
        :param headers: headers to send with REST call
            https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/headers.htm
        """

        updates = model.model_dump_json(
            by_alias=True, exclude_unset=True, exclude_defaults=True, exclude_none=True
        )
        import json

        updates = json.loads(updates)  # TODO - better way to do this?
        if updates:
            GUSClient.instance().sf.__getattr__("ADM_Planned_Release__c").update(
                model.id_, updates, headers=headers
            )

    @classmethod
    def soql_query(cls, where_clause: str) -> Generator[Self, None, None]:
        """
        Query Planned Releases by SOQL WHERE clause.

        :param where_clause: where clause of SOQL query
        :yields: Planned Release objects
        """
        for x in cls._query_soql("ADM_Planned_Release__c", where_clause):
            yield PlannedRelease(**x)

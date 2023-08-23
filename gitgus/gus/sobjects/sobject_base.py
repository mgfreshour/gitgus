from abc import ABC
from typing import Optional, List, Generator, Self, Tuple

from pydantic import BaseModel
from pydantic._internal import _model_construction

from gitgus.utils.cache import persist_to_file
from ..gus_client import GUSClient


class Like:
    def __init__(self, val):
        self.val = val


class SObjectType(_model_construction.ModelMetaclass):
    def __getattr__(cls, key: str):
        if key in cls.__dict__:
            return cls.__dict__[key]
        if key in cls.model_fields:
            return cls.model_fields[key]

        is_find_by = key[: len("find_by_")] == "find_by_"
        is_get_by = key[: len("get_by_")] == "get_by_"

        if is_find_by or is_get_by:
            if is_get_by:
                fields = key[len("get_by_") :].split("_and_")
            else:
                fields = key[len("find_by_") :].split("_and_")
            if len(fields) == 0:
                raise ValueError(f"{key} must have at least one field")

            def ret(*args):
                if len(args) != len(fields):
                    raise ValueError(f"{key} must have {len(fields)} arguments")
                translated_fields = []
                arguments = []
                for k, v in zip(fields, args):
                    if k[-5:] == "_like":
                        translated_fields.append(k[:-5])
                        arguments.append(Like(v))
                    else:
                        translated_fields.append(k)
                        arguments.append(v)

                find_dict = {k: v for k, v in zip(translated_fields, arguments)}
                res = cls.find_by(**find_dict)
                if is_get_by:
                    res = list(res)
                    if len(res) == 0:
                        return None
                    if len(res) > 1:
                        raise ValueError(f"{key} returned more than one result")
                    return res[0]
                return res

            return ret

        super().__getattr__(key)


class SObjectBase(BaseModel, ABC):
    _can_be_approved = False
    _id_field = "id_"

    def id(self):
        return self.__getattr__(self._id_field)

    @classmethod
    def find_by(cls, **kwargs) -> Generator[Self, None, None]:
        field_definitions = cls.model_fields
        sf_fields = {}
        for k in kwargs.keys():
            if k not in field_definitions:
                raise ValueError(f"Field {k} not in {cls.__name__}")
            alias = field_definitions[k].alias
            sf_fields[alias] = kwargs[k]

        clauses = []
        for k, v in sf_fields.items():
            if isinstance(v, Like):
                clauses.append(f"{k} LIKE '%{v.val}%'")
            elif isinstance(v, SObjectBase):
                clauses.append(f"{k} = '{v.id()}'")
            else:
                clauses.append(f"{k} = '{v}'")

        query = "WHERE " + " AND ".join(clauses)
        return cls.soql_query(query)

    @classmethod
    def _get_field_names(cls) -> Tuple[str, ...]:
        """
        Get Salesforce object field names.

        :returns: field names
        """
        field_definitions = cls.model_fields
        return tuple(field_definitions[k].alias for k in field_definitions.keys())

    @classmethod
    def _get_field_to_sf_name_dict(cls) -> dict[str, str]:
        """
        Get Salesforce object field names.

        :returns: field names
        """
        field_definitions = cls.model_fields
        return {k: field_definitions[k].alias for k in field_definitions.keys()}

    @classmethod
    def _get_sf_name_to_field_dict(cls) -> dict[str, str]:
        """
        Get Salesforce object field names.

        :returns: field names
        """
        field_definitions = cls.model_fields
        return {field_definitions[k].alias: k for k in field_definitions.keys()}

    @classmethod
    def _create(cls, sobject_name: str, fields: dict[str, str]) -> Self:
        result = GUSClient.instance().create(sobject_name, fields)

        if result["success"]:
            return cls.get_by_id(result["id"])
        else:
            raise RuntimeError("Errors occurred during object creation\n" + "\n".join(result["errors"]))

    @classmethod
    @persist_to_file()
    def _query_soql(cls, sobject_name: str, where_clause: str) -> Generator[dict, None, None]:
        """
        Query API using SOQL.

        :param sobject_name: Salesforce object name
        :param where_clause: where clause of SOQL query
        :yields: objects from API
        """
        field_names = cls._get_field_names()
        result = GUSClient.instance().sf.query(f"SELECT {','.join(field_names)} FROM {sobject_name} {where_clause}")
        while True:
            for record in result["records"]:
                del record["attributes"]
                yield record
            if not result["done"]:
                result = GUSClient.instance().sf.query_more(result["nextRecordsUrl"], identifier_is_url=True)
            else:
                break

    @persist_to_file()
    def _get_connected_object_name(self, sobject_names, id):
        objs = [GUSClient.instance().sf.__getattr__(sobject).get(id) for sobject in sobject_names]
        if len(objs) > 1:
            raise RuntimeError(f"Multiple reference objects found with id {id} in {sobject_names}")
        if len(objs) == 0:
            return None
        # find the names
        obj = objs[0]
        if "name" in obj:
            return obj["name"]
        elif "Name" in obj:
            return obj["Name"]
        elif "Username" in obj:
            return obj["Username"]
        return None

    def submit_for_approval(
        self,
        comments: Optional[str] = None,
        context_actor_id: Optional[str] = None,
        next_approver_ids: Optional[List[str]] = None,
        process_definition_name_or_id: Optional[str] = None,
        skip_entry_criteria: Optional[bool] = None,
    ) -> None:
        """
        Submit for approval.

        :param comments: The comment to add to the history step associated with this
            request.
        :param context_actor_id: The ID of the submitter who's requesting the approval
            record.
        :param next_approver_ids: If the process requires specification of the next
            approval, the ID of the user to be assigned the next request.
        :param process_definition_name_or_id: The developer name or ID of the process
            definition.
        :param skip_entry_criteria: Determines whether to evaluate the entry criteria
            for the process (true) or not (false) if the process definition name or ID
            isn't null. If the process definition name or ID isn't specified, this
            argument is ignored, and standard evaluation is followed based on process
            order. By default, the entry criteria isn't skipped if it's not set by this
            request.
        """
        if not self._can_be_approved:
            raise RuntimeError(f"{self.__class__.__name__} cannot be approved")
        request = {
            "actionType": "Submit",
            "contextId": self.__getattr__(self._id_field),
            "comments": comments,
            "contextActorId": context_actor_id,
            "nextApproverIds": next_approver_ids,
            "processDefinitionNameOrId": process_definition_name_or_id,
            "skipEntryCriteria": skip_entry_criteria,
        }
        request = {k: v for k, v in request.items() if v is not None}
        GUSClient.instance().sf.restful("process/approvals/", method="POST", json={"requests": [request]})

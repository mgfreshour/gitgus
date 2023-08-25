"""Client."""
import sys
from typing import Self

from requests import Session
from simple_salesforce import Salesforce

from .sf_conn import get_session_token


class GUSClient:
    """GUS."""

    _instance = None

    def __init__(
        self,
        session_id: str,
        instance: str = "gus.my.salesforce.com",
    ) -> None:
        """
        Initialize client.

        :param session_id: Salesforce session id
        :param instance: Salesforce instance
        :raises ValueError: if Salesforce instance URL doesn't end with salesforce.com
        """
        if not instance.endswith("salesforce.com"):
            raise ValueError("Salesforce instance URL doesn't end with salesforce.com")
        session = Session()
        self.sf = Salesforce(
            instance=instance,
            session_id=session_id,
            version="51.0",
            session=session,
        )
        self.user_id: str = self.sf.restful("", method="GET")["identity"].rsplit("/", 1)[1]
        GUSClient._instance = self

    def create(self, sobject_name: str, fields: dict[str, str]):
        """
        Create a Salesforce object.

        :param sobject_name: Salesforce object name
        :param fields: fields to set
        :returns: created object
        """
        return self.sf.__getattr__(sobject_name).create(fields)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls._connect_gus_with_sso()
        return GUSClient._instance

    # @property
    # def authenticated_user(self) -> User:
    #     """
    #     Get currently authenticated user.
    #
    #     :returns: currently authenticated user
    #     """
    #     return next(User.find_by_id(self.user_id))

    @classmethod
    def _connect_gus_with_sso(cls, instance: str = "gus.my.salesforce.com") -> Self:
        """
        Connect to GUS with SSO (for CLI applications) using sfdx CLI.

        Users must have sfdx cli installed:
        <https://developer.salesforce.com/tools/sfdxcli>

        :param instance: Salesforce instance (gus.my.salesforce.com)
        :returns: authenticated GUS client
        """
        if "pytest" in sys.modules:
            raise RuntimeError("Someone forgot to mock out the connection to GUS.")
        return GUSClient(get_session_token(instance), instance=instance)

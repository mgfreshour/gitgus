"""gitgus.gus.workitem."""

from .gus_client import GUSClient

from .sobjects.epic import Epic
from .sobjects.feed_item import FeedItem
from .sobjects.work import Work

# enum of record types
RECORD_TYPES = {
    "User Story": "0129000000006gDAAQ",
    "Bug": "012T00000004MUHIA2",
}


class WorkItems:
    """Work Items."""

    def __init__(self):
        """Initialize."""

    def create(self, **kwargs) -> Work:
        """Create a work item."""
        return Work.create(**kwargs)

    def get_epics_work(self, team, planned_release) -> list:
        """Get epics."""
        res = []
        epics = list(Epic.find_by(team=team, planned_release=planned_release))
        for epic in epics:
            wis = list(Work.find_by(epic=epic))
            res.append((epic, wis))
        return res

    def list(self, query: str) -> list[Work]:
        return list(Work.soql_query(query))

    def user_id(self):
        return GUSClient.instance().user_id

    def update(self, work_item: Work, updates: dict):
        for k, v in updates.items():
            if v is not None:
                work_item.__setattr__(k, v)
        work_item.update(work_item)

    def add_feed_post(self, work_item: Work, comment: str):
        return FeedItem.create(parent_id=work_item.id_, body=comment)

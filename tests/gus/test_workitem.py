from datetime import datetime
from unittest.mock import MagicMock

import pytest
import gitgus.gus.workitems as workitem
import gitgus.utils.cache as cache
from gitgus.gus.gus_client import GUSClient
from gitgus.gus.sobjects.work import Work
from gitgus.gus.sobjects.feed_item import FeedItem

testee: workitem.WorkItems
mock_gus: MagicMock


def _create_wi(name: str, description: str) -> Work:
    return Work.model_construct(
        sf=MagicMock(),
        Id="1234",
        OwnerId="1234",
        Name=name,
        IsDeleted=False,
        CreatedDate=datetime.utcnow(),
        CreatedById="1234",
        LastModifiedDate=datetime.utcnow(),
        LastModifiedById="1234",
        SystemModstamp=datetime.utcnow(),
        Description=description,
        Status="Open",
        MayEdit=True,
        IsLocked=False,
    )


@pytest.fixture(autouse=True)
def _setup(monkeypatch):
    global testee, mock_gus
    cache.global_cache_enabled = False
    mock_gus = MagicMock()
    monkeypatch.setattr(GUSClient, "_connect_gus_with_sso", mock_gus)
    monkeypatch.setattr(Work, "soql_query", MagicMock())
    mock_gus.return_value = mock_gus
    mock_wi = _create_wi("W-1234", "Test Work Item")
    mock_wi.description = "Test Work Item"
    mock_gus.query_work.return_value = [mock_wi]
    mock_gus.get_user.return_value = MagicMock()
    mock_gus.get_user.return_value.name = "Test User"

    testee = workitem.WorkItems()


def test_list(monkeypatch):
    Work.soql_query.return_value = iter([_create_wi("W-1234", "Test Work Item")])

    res = testee.list("SELECT Id, Name, Description FROM Work WHERE Name = 'W-1234'")

    assert len(res) == 1
    assert res[0].name == "W-1234"
    Work.soql_query.assert_called_with(
        "SELECT Id, Name, Description FROM Work WHERE Name = 'W-1234'"
    )


def test_user_id(monkeypatch):
    GUSClient.instance().user_id = "1234"
    assert testee.user_id() == "1234"


def test_update(monkeypatch):
    mock_wi = _create_wi("W-1234", "Test Work Item")
    monkeypatch.setattr(Work, "update", MagicMock())

    testee.update(mock_wi, {"description": "Updated Description"})

    mock_wi.update.assert_called_once()
    assert mock_wi.description == "Updated Description"


def test_add_feed_post(monkeypatch):
    mock_wi = _create_wi("W-1234", "Test Work Item")
    monkeypatch.setattr(FeedItem, "get_by_id", MagicMock())
    mock_gus.create_feed_item.return_value = "1234"
    monkeypatch.setattr(GUSClient.instance(), "create", MagicMock())
    GUSClient.instance().create.return_value = {"success": True, "id": "1234"}

    testee.add_feed_post(mock_wi, "Test Comment")

    assert FeedItem.get_by_id.call_count == 1
    assert FeedItem.get_by_id.call_args[0][0] == "1234"

from unittest.mock import MagicMock

from gitgus.gus.sobjects.work import Work
from gitgus.gus.sobjects.sobject_base import Like


def test_sobject_type_find_by_two_fields(monkeypatch):
    monkeypatch.setattr(Work, "find_by", MagicMock())
    Work.find_by_name_and_owner_id("hello", "world")
    Work.find_by.assert_called_once()
    Work.find_by.assert_called_with(name="hello", owner_id="world")


def test_sobject_type_get_by_two_fields(monkeypatch):
    monkeypatch.setattr(Work, "find_by", MagicMock())
    Work.get_by_name_and_owner_id("hello", "world")
    Work.find_by.assert_called_once()
    Work.find_by.assert_called_with(name="hello", owner_id="world")


def test_sobject_type_find_by_like_field(monkeypatch):
    monkeypatch.setattr(Work, "find_by", MagicMock())
    Work.find_by_owner_id_like("hello")
    Work.find_by.assert_called_once()
    assert list(Work.find_by.call_args[1].keys()) == ["owner_id"]
    vals = list(Work.find_by.call_args[1].values())
    assert len(vals) == 1
    assert isinstance(vals[0], Like)
    assert vals[0].val == "hello"


def test_sobject_find_by(monkeypatch):
    monkeypatch.setattr(Work, "soql_query", MagicMock())
    Work.find_by(name="hello", owner_id="world")
    Work.soql_query.assert_called_once()
    Work.soql_query.assert_called_with("WHERE Name = 'hello' AND OwnerId = 'world'")


def test_sobject_find_by_like(monkeypatch):
    monkeypatch.setattr(Work, "soql_query", MagicMock())
    Work.find_by(name="hello", owner_id=Like("world"))
    Work.soql_query.assert_called_once()
    Work.soql_query.assert_called_with("WHERE Name = 'hello' AND OwnerId LIKE '%world%'")


def test_sobject_find_by_object_value(monkeypatch):
    monkeypatch.setattr(Work, "soql_query", MagicMock())
    Work.find_by(name="hello", owner_id=Work.model_construct(id_="world"))
    Work.soql_query.assert_called_once()
    Work.soql_query.assert_called_with("WHERE Name = 'hello' AND OwnerId = 'world'")

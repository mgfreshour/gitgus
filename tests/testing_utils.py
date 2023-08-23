from unittest.mock import Mock

from gitgus.gus.workitems import RECORD_TYPES
from gitgus.gus.sobjects.work import Work


def create_wi(name: str, subject: str = "Test Work Item", body="Test Details"):
    vals = {
        "id_": "1234",
        "name": name,
        "subject": subject,
        "work_id_and_subject": name + " " + subject,
        "status": "New",
        "web_url": "https://example.com/" + name,
        "assignee": "Test User",
        "assignee_name": "Test User",
        "scheduled_build": None,
        "scheduled_build_name": None,
        "RecordTypeId": RECORD_TYPES["Bug"],
        "update": Mock(),
        "details": body,
        "details_and_steps_to_reproduce": "",
        "priority": "P1",
        "epic": "",
        "epic_name": "",
    }
    wi = Work.model_construct(**vals)
    return wi


def create_build():
    build = type("", (), {"name": "test_build_name", "id_": "test_build_id_"})
    return build


def create_pr(title: str):
    pr = type(
        "",
        (),
        {
            "title": title,
            "html_url": "https://example.com/" + title,
            "requested_reviewers": [],
        },
    )()

    return pr

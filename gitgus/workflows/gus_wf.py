import enum
import re

from string import Template
from typing import Generator

from gitgus.gus.sobjects.work import Work

from gitgus.git_repo import GitRepo
from gitgus.config import Config
from gitgus.gus.workitems import WorkItems
from gitgus.utils.external_editor import ExternalEditor
from gitgus.gus.sobjects.team import Team
from gitgus.gus.sobjects.planned_release import PlannedRelease


class Status(enum.Enum):
    """Status."""

    NEW = "New"
    IN_PROGRESS = "In Progress"
    READY_FOR_REVIEW = "Ready for Review"
    CLOSED = "Closed"
    NEVER = "Never"


class GusWorkflow:
    def __init__(
        self,
        config: Config,
        work_items: WorkItems,
        external_editor: ExternalEditor,
        git_repo: GitRepo,
    ):
        self.config = config
        self.work_items = work_items
        self.external_editor = external_editor
        self.git_repo = git_repo

    def query(self, query_name: str = "default") -> list[Work]:
        """List PRs."""
        query = Template(self.config.get(f"GUS.queries.{query_name}")).safe_substitute(me=self.work_items.user_id())
        return list(Work.soql_query(query))

    def _find_status(self, status: str) -> Status:
        """Find status."""
        for s in Status:
            if s.value == status:
                return s
        raise Exception(f"Status {status} not found")

    def set_status(self, work_id: str, status: str):
        """Set status of work item."""
        wi = Work.get_by_name(work_id)
        if not wi:
            raise Exception(f"Work item {work_id} not found")
        status = self._find_status(status)
        self.work_items.update(wi, {"status": status.value})
        return wi

    def checkout(self, chooser, mark_as_in_progress: bool = False):
        tickets = self.query()
        if not tickets:
            return None
        choices = [wi.work_id_and_subject for wi in tickets]
        n = chooser(choices)
        wi = tickets[n]
        branch = self._checkout_branch(wi)
        if mark_as_in_progress:
            self.set_status(wi.name, "In Progress")
        return branch, wi

    def _checkout_branch(self, wi) -> str:
        """Checkout branch associated with work item."""
        branches = self.git_repo.get_branches()
        for branch in branches:
            if wi.name in branch.name:
                self.git_repo.checkout(branch.name)
                return branch.name
        subject = re.sub(r"[^a-zA-Z0-9- ]", "", wi.subject)
        subject = subject.replace(" ", "-").replace("/", "-")[0:36]
        branch_name = Template(self.config.get("GUS.branch_name_template")).safe_substitute(
            me=self.work_items.user_id(),
            team_prefix=self.config.get("PRs.team_prefix"),
            work_id=wi.name,
            subject=subject,
        )
        self.git_repo.checkout(branch_name, create=True)
        return branch_name

    def get(self, work_id: str):
        """Get work item."""
        wi = Work.get_by_name(work_id)
        return wi

    def dekanban(self, work_id):
        """Removes an item from the kanban board."""
        wi = Work.get_by_name(work_id)
        if not wi:
            raise Exception(f"Work item {work_id} not found")
        self.work_items.update(wi, {"column": ""})
        return wi

    def swap_bug_story_details(self, work_id):
        wi = Work.get_by_name(work_id)
        details = wi.details
        details_and_steps_to_reproduce = wi.details_and_steps_to_reproduce
        self.work_items.update(
            wi, {"details_and_steps_to_reproduce": details, "details": details_and_steps_to_reproduce}
        )
        return wi

    def sort_tickets(self, team_name: str, planned_release_name: str, dry_run: bool) -> list[dict]:
        """Sort tickets."""
        team = Team.get_by_name_like(team_name)
        base_query = f"Status__c IN ('New', 'Triaged') " f"AND Scrum_Team__c = '{team.id_}'"
        # Move all P0 & P1 to the very top.
        # Then P2s if we've decided a customer needs us to work on this now.
        # Next is all planned epic work.
        # Then P2s that don't have customer pressure
        # Then P3s we triaged recently
        # Then all the junk work
        # Then P3s that have been sitting around forever
        # Then P4s
        p0_tickets = Work.soql_query(
            f"WHERE Priority__c = 'P0' AND {base_query}",
        )
        p1_tickets = Work.soql_query(
            f"WHERE Priority__c = 'P1' AND {base_query}",
        )
        p2_tickets = Work.soql_query(
            f"WHERE Priority__c = 'P2' AND {base_query}",
        )
        # Find all the tickets that have been triaged recently
        p3_recent_tickets = Work.soql_query(
            f"WHERE Priority__c = 'P3' AND {base_query} AND Age_Since_Last_Modified__c < 30",
        )
        p3_old_tickets = Work.soql_query(
            f"WHERE Priority__c = 'P3' AND {base_query} AND Age_Since_Last_Modified__c >= 30",
        )
        # p4_tickets = self.list(
        #     query=f"WHERE Priority__c = 'P4' AND Status__c != 'Closed'",
        #     include_users=False,
        # )

        # Find all the tickets tied to epics in the current planned release
        planned_release = PlannedRelease.get_by_team_and_name_like(team, planned_release_name)
        epics = self.work_items.get_epics_work(team, planned_release)
        epic_tickets = []
        # sort epics by priority
        epics.sort(key=lambda x: x[0].priority, reverse=True)
        for epic, wis in epics:
            print(f"epic {epic.name} has {len(wis)} tickets")
            wis = [wi for wi in wis if "New" in wi.status or "Triaged" in wi.status]
            print(f"epic {epic.name} has {len(wis)} tickets after filtering")
            for wi in wis:
                wi.epic = epic.name
            epic_tickets.extend(wis)

        tickets: list[Work] = []
        tickets.extend(p0_tickets)
        tickets.extend(p1_tickets)
        tickets.extend(epic_tickets)
        tickets.extend(p2_tickets)
        tickets.extend(p3_recent_tickets)
        tickets.extend(p3_old_tickets)

        # Save the old priority rank
        ret: list[dict] = [vars(t) for t in tickets]
        for i, t in enumerate(ret):
            t["old_rank"] = t["priority_rank"]
            t["priority_rank"] = i + 1

        if not dry_run:
            for i, t in enumerate(tickets):
                self.work_items.update(t, {"priority_rank": i + 1})

        return ret

import datetime
import logging
import os
import re
from string import Template
from typing import Callable

from markdown import markdown
from rich.prompt import Prompt

from gitgus.git_repo import GitRepo
from gitgus.config import Config
from gitgus.gus.workitems import RECORD_TYPES, WorkItems
from gitgus.utils.menu import get_choice
from gitgus.jenki import Jenki
from gitgus.gus.sobjects.work import Work

TICKET_TYPE_DISABLE = "Disable"
TICKET_TYPE_FIX = "Fix"


class FlakyWorkflow:
    def __init__(
        self,
        config: Config,
        work_items: WorkItems,
        jenki: Jenki,
        git: GitRepo,
        chooser: Callable = get_choice,
        asker: Callable = Prompt.ask,
    ):
        self.config = config
        self.work_items = work_items
        self.jenki = jenki
        self.git = git
        self.chooser = chooser
        self.asker = asker

    def _get_fix_description_template(self):
        """Returns the description for the fix ticket."""
        file = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            os.path.pardir,
            "templates",
            "flaky_fix_description.md",
        )
        with open(file) as f:
            return Template(markdown(f.read()))

    def create(
        self,
        build: int,
        job_name: str = "",
        branch: str = "master",
        ticket_types: list = [TICKET_TYPE_DISABLE, TICKET_TYPE_FIX],
    ):
        """Creates the tickets for a flaky test."""
        job_name = self._get_job_name(job_name)

        if build != 0:
            stack_trace, test = self._get_test_stacktrace(branch, build, job_name)
        else:
            test = self.asker("Please tell me the test name")
            stack_trace = "TODO: Add stack trace here"

        tickets = self._create_flaky_tickets(test, stack_trace, build, ticket_types)
        return tickets

    def _get_job_name(self, job_name):
        if not job_name:
            repo_name = self.git.get_repo_name()
            job_name = repo_name.split("/")[-1]
        return job_name

    def _get_test_stacktrace(self, branch, build, repo_name):
        broken_tests = self.jenki.get_failed_tests_stacktraces(f"{repo_name}/{branch}", build)
        if not broken_tests:
            test = self.asker("No broken tests found. Please tell me the test name:")
            stack_trace = "TODO: Add stack trace here"
        elif len(broken_tests) > 1:
            n = self.chooser(broken_tests.keys())
            test = list(broken_tests.keys())[n]
            stack_trace = broken_tests[test]
        else:
            test = list(broken_tests.keys())[0]
            stack_trace = broken_tests[test]
        return stack_trace, test

    def _create_flaky_tickets(self, test, stack_trace, build, ticket_types: list[str]):
        rem_subject = f"[Flaky Test] - Disable test: {test}"
        rem_description = (
            f"Test {test} is flaky in build https://jenkins.devergage.com/job/evergage-product/job/master/{build}/."
        )
        fix_subject = f"[Flaky Test] - Fix {test}"
        fix_description = self._get_fix_description_template().safe_substitute(
            test=test, build=build, stack_trace=stack_trace
        )
        tickets = []
        if TICKET_TYPE_DISABLE in ticket_types:
            tickets.append(
                Work.create(
                    subject=rem_subject,
                    details_and_steps_to_reproduce=rem_description,
                    assignee=self.work_items.user_id(),
                    record_type_id=RECORD_TYPES["Bug"],
                    found_in_build="a06T0000001VeY4IAK",
                    priority="P2",
                    scrum_team=self.config.get("GUS.default_team"),
                    product_tag=self.config.get("GUS.default_product_tag"),
                )
            )

        if TICKET_TYPE_FIX in ticket_types:
            tickets.append(
                Work.create(
                    subject=fix_subject,
                    details_and_steps_to_reproduce=fix_description,
                    assignee=self.work_items.user_id(),
                    record_type_id=RECORD_TYPES["Bug"],
                    found_in_build="a06T0000001VeY4IAK",
                    priority="P2",
                    scrum_team=self.config.get("GUS.default_team"),
                    product_tag=self.config.get("GUS.default_product_tag"),
                )
            )
        return tickets

    def report(self, build_name_like: str, start_date: datetime, end_date: datetime):
        return self.jenki.get_all_flaky_tests(build_name_like, start_date, end_date)

    def build_report(self, job_name_like, start_date, end_date):
        return self.jenki.get_all_builds(job_name_like, start_date, end_date)

    def get_flaky_tagged_tests(self):
        func_regex = re.compile('\\s*(public)?\\s*void "?([^"]*)"?\\s*\\(.*\\)\\s*(throws .*)?\\s*{')
        test_anno_re = re.compile("\\s*@Test\\(?.*\\)?")
        known_flaky_re = re.compile("\\s*@KnownFlaky\\(workItems = [\"']([^)]+)[\"']\\)")
        multi_known_flaky_re = re.compile("\\s*@KnownFlaky\\(workItems = \\[([^]]+)]\\)")
        package_re = re.compile("^package\\s+(\\S+);?$")
        space_re = re.compile("^\\s*$")
        suppress_re = re.compile("\\s*@SuppressWarnings")
        verifies_re = re.compile("\\s*@VerifiesIssue")
        comment_block_start_re = re.compile("\\s*/\\*")
        comment_block_end_re = re.compile("\\s*\\*/")
        inline_comment_re = re.compile("\\s*//.*")
        class_re = re.compile("\\s*class\\s+(\\S+)\\s.*{")

        function_tickets = {}
        in_comment = False
        tickets = None
        package = None
        class_name = None
        old_path = None
        for line, path, line_num in self.git.files_lines("*.groovy"):
            if path != old_path:
                old_path = path
                tickets = None
                package = None
                class_name = None
            if comment_block_start_re.match(line):
                in_comment = True
            elif comment_block_end_re.match(line):
                in_comment = False
            elif match := class_re.match(line):
                class_name = match.group(1)
            elif match := package_re.match(line):
                package = match.group(1)
            elif (
                space_re.match(line)
                or test_anno_re.match(line)
                or suppress_re.match(line)
                or verifies_re.match(line)
                or in_comment
                or inline_comment_re.match(line)
            ):
                continue
            elif match := known_flaky_re.match(line):
                tickets = [match.group(1)]
            elif match := multi_known_flaky_re.match(line):
                tickets = match.group(1)
                tickets = [t.strip('"').strip("'") for t in tickets.split(",")]
            elif match := func_regex.match(line):
                func_name = match.group(2)
                if tickets:
                    name = f"{package}.{class_name}:{func_name}"
                    if name in function_tickets:
                        logging.warn(
                            f"Found duplicate flaky ticket {tickets} for {package}.{func_name}: {line.strip()}"
                            f"\n  in file {path}:{line_num}"
                        )
                    function_tickets[name] = tickets
                    tickets = None
            else:
                if tickets:
                    logging.warn(
                        f"Found unknown line after flaky annotation: {line.strip()}\n   in file {path}:{line_num}"
                    )
                    tickets = None

        return function_tickets

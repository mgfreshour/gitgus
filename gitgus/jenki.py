from datetime import datetime, timedelta


import jenkins
from gitgus.config import Config, DEFAULT_CONFIG_PATH


class Jenki:
    def __init__(self, config: Config):
        self.config = config
        self._jenkins: jenkins.Jenkins = None

    def _conn(self) -> jenkins.Jenkins:
        if (
            not self.config.get("jenkins.url")
            or not self.config.get("jenkins.username")
            or not self.config.get("jenkins.password")
        ):
            raise Exception(
                "Jenkins config is not set.  Please update in your config file. "
                + DEFAULT_CONFIG_PATH
            )

        if self._jenkins is None:
            self._jenkins = jenkins.Jenkins(
                self.config.get("jenkins.url"),
                username=self.config.get("jenkins.username"),
                password=self.config.get("jenkins.password"),
                timeout=60,
            )
        return self._jenkins

    def get_build_test_report(self, job_name: str, build_number: int):
        return self._conn().get_build_test_report(job_name, build_number)

    def get_branch_job(self, repo_name: str, branch: str):
        name = repo_name + "/" + branch
        job = self._conn().get_job_info(name)
        return job

    def get_failed_tests_stacktraces(
        self, job_name: str, build_number: int
    ) -> dict[str, str]:
        test_report = self.get_build_test_report(job_name, build_number)
        failed_tests = {}
        for suite in test_report["suites"]:
            for case in suite["cases"]:
                if case["status"] not in ["PASSED", "SKIPPED", "FIXED"]:
                    name = case["className"] + ":" + case["name"]
                    failed_tests[name] = case["errorStackTrace"]
        return failed_tests

    def get_all_jobs_like(self, job_name_like: str):
        jobs = self._conn().get_all_jobs()
        full_jobs = []
        for job in jobs:
            if job_name_like.lower() in job["fullname"].lower():
                full_job = self._conn().get_job_info(name=job["fullname"])
                full_jobs.append(full_job)
        return full_jobs

    def get_all_flaky_tests(
        self, job_name_like: str, start_date: datetime = None, end_date: datetime = None
    ):
        total_builds = 0
        all_testcases = []
        full_jobs = self.get_all_jobs_like(job_name_like)
        for job in full_jobs:
            testcases, builds_scanned = self.get_flaky_tests_in_job(
                job, start_date, end_date
            )
            total_builds += builds_scanned
            all_testcases.extend(testcases)

        return all_testcases, total_builds

    def get_all_builds(
        self, job_name_like: str, start_date: datetime = None, end_date: datetime = None
    ):
        full_jobs = self.get_all_jobs_like(job_name_like)
        results = []
        for job in full_jobs:
            builds = []
            if "builds" not in job:
                continue
            for build in job["builds"]:
                full_build = self._conn().get_build_info(
                    job["fullName"], build["number"]
                )
                ts = datetime.fromtimestamp(full_build["timestamp"] / 1000)
                if start_date and ts < start_date:
                    continue
                if end_date and ts > end_date:
                    continue
                builds.append(full_build)
            if len(builds) > 0:
                results.append({"job": job, "builds": builds})
        return results

    def get_flaky_tests_in_job(
        self, job, start_date: datetime = None, end_date: datetime = None
    ):
        testcases = []
        if not job or "builds" not in job:
            return testcases, 0
        total_builds = len(job["builds"])
        for build in job["builds"]:
            # confusing, get_all_jobs makes "fullname", but get_job_info makes "fullName"
            rpt = self._conn().get_build_test_report(job["fullName"], build["number"])
            if not rpt:
                continue

            for suite in rpt["suites"]:
                # '2023-05-09T17:55:38' or '09 May 2023 17:43:11 GMT' ... wtf?!?
                if "-" in suite["timestamp"]:
                    ts = datetime.strptime(suite["timestamp"][:19], "%Y-%m-%dT%H:%M:%S")
                else:
                    ts = datetime.strptime(suite["timestamp"], "%d %b %Y %H:%M:%S %Z")
                if start_date and ts < start_date:
                    continue
                if end_date and ts > end_date:
                    continue
                for case in suite["cases"]:
                    if (
                        case["errorDetails"]
                        and "This test is flaky" in case["errorDetails"]
                    ):
                        case["timestamp"] = suite["timestamp"]
                        testcases.append(case)
        return testcases, total_builds

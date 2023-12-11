from datetime import datetime, timedelta

from github.PullRequest import PullRequest
from slack_sdk import WebClient

from gitgus.config import Config


class SlackWriter:
    def __init__(self, cfg: Config):
        self.token = cfg.get("slack.token")
        self.client = WebClient(token=self.token)

    def post_message(self, channel: str, text: str):
        self.client.chat_postMessage(
            channel=channel,
            text=text,
            icon_emoji=":robot_face:",
            username="GitGus",
        )

    def post_prs(self, pr_list: list[PullRequest], channel: str):
        slack_message = self.format_prs(pr_list)

        self.post_message(channel, slack_message)

    def format_prs(self, pr_list):
        past_week = list()
        past_month = list()
        older = list()
        for pr in pr_list:
            if pr.created_at > datetime.now() - timedelta(days=7):
                past_week.append(self.format_pr(pr))
            elif pr.created_at > datetime.now() - timedelta(days=30):
                past_month.append(self.format_pr(pr))
            else:
                older.append(self.format_pr(pr))
        slack_message = (
            "*PR REMINDERS*\n"
            f"\t:update_pd: Updated\t\t:date-1: Age\t\t:person: Github Username\n"
            f"\n:party-parrot: *Recently Updated*\n{''.join(past_week)}"
            f"\n:old-timey-parrot:   *Past Month*\n{''.join(past_month)}"
            f"\n:slow_parrot: *Old* _please clean up or convert to drafts_ \n{''.join(older)}"
        )
        return slack_message

    def format_pr(self, pr: PullRequest) -> str:
        icon = ":pr:"
        if pr.draft:
            icon = ":draft:"
        else:
            for review in pr.get_reviews():
                if review.state == "APPROVED":
                    icon = ":approved:"
                if review.state == "CHANGES_REQUESTED":
                    icon = ":thoughts_bubble:"
        last_update_days = (datetime.now() - pr.updated_at).days
        updated_text = "Today" if last_update_days <= 0 else f"{last_update_days} Day"
        created_days = (datetime.now() - pr.created_at).days
        created_text = "Today" if created_days <= 0 else f"{created_days} Day"
        title = pr.title
        title = "".join([c for c in title if c.isalnum() or c in [" ", "-", "_", "."]])
        if len(title) > 70:
            title = title[:50] + "..." + title[-17:]
        return (
            f"{icon} [{title}]({pr.html_url})\n"
            f"\t:update_pd: {updated_text}\t\t:date-1: {created_text}\t\t:person: {pr.user.login}\n"
        )

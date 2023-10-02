import logging
import os

import toml

from gitgus.utils.secret_store import get_secret, set_secret

_config = None
DEFAULT_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), ".config", "gitgus", "config.toml"
)
LOCAL_CONFIG_NAME = ".gitgus.toml"
IS_SECRET_TOKEN = "***secret***"


def instance():
    global _config
    if not _config:
        _config = Config()
        _config.load()
    return _config


class Config:
    """Reads config information from ~/.config/gitgus/config.toml"""

    def __init__(self):
        self._config = dict()
        self._secret_domain = "gitgus"

    def load(self, config_path=None):
        """Loads the config file."""
        if not config_path:
            config_path = DEFAULT_CONFIG_PATH
        self.load_defaults()
        if os.path.exists(config_path):
            logging.info("Loading config from %s", config_path)
            self._merge(self._read_config(config_path), self._config)
        else:
            logging.error("No config file found. Please run gitgus config init")
        local_config = self._get_local_config(os.getcwd())
        if local_config:
            logging.info("Loading local config from %s", local_config)
            self._merge(self._read_config(local_config), self._config)
        self.load_envs()

    def _get_local_config(self, dir) -> str | bool:
        if os.path.exists(os.path.join(dir, LOCAL_CONFIG_NAME)):
            return os.path.join(dir, LOCAL_CONFIG_NAME)
        # recurse up the tree
        parent = os.path.dirname(dir)
        if parent == dir:
            return False
        return self._get_local_config(parent)

    def load_defaults(self):
        self._config = self._get_defaults()

    def load_global_init_values(self):
        self._merge(self._get_init_values(), self._config)

    def write(self, config_path):
        """create the config file and directory"""
        if not config_path:
            config_path = DEFAULT_CONFIG_PATH
        if not os.path.exists(os.path.dirname(config_path)):
            os.makedirs(os.path.dirname(config_path))
        with open(config_path, "w") as config_file:
            toml.dump(self._config, config_file)

    def _read_config(self, configpath) -> dict:
        """Reads config information from ~/.config/gitgus/config.toml"""
        with open(configpath, "r") as config_file:
            return toml.load(config_file)

    def all(self):
        """Returns the entire config."""
        return self._config

    def set(self, key: str, value: any):
        """Sets the value of the key."""
        self._set(key, value, self._config)

    def _set(self, key: str, value: any, tree: dict):
        """Sets the tree of the key."""
        if "." in key:
            key, rest = key.split(".", 1)
            self._set(rest, value, tree[key])
        else:
            tree[key] = value

    def get(self, key: str) -> str:
        """Returns the value of the key."""
        val = self._get(key, self._config)
        if val == IS_SECRET_TOKEN:
            val = get_secret(self._secret_domain, key)
        return val

    def _get(self, key: str, tree: dict) -> any:
        """Returns the tree of the key."""
        try:
            if "." in key:
                key, rest = key.split(".", 1)
                return self._get(rest, tree[key])
            return tree[key]
        except KeyError:
            return None

    def set_secret(self, key: str, value: any):
        """Sets the value of the key."""
        set_secret(self._secret_domain, key, value)
        self.set(key, IS_SECRET_TOKEN)

    def _get_init_values(self) -> dict:
        return {
            "PRs": {
                "body_template": ".github/PULL_REQUEST_TEMPLATE.md",
                "reviewers": [],
                "queries": {
                    "default": "is:open repo:${repo} head:${team_prefix}",
                    "mine": "is:open repo:${repo} author:${username}",
                },
            },
            "GUS": {
                "branch_name_template": "${team_prefix}/@${work_id}@-${subject}",
                "queries": {
                    "default": "WHERE Assignee__c = '${me}' AND (NOT Status__c  LIKE 'Closed%') "
                    + "AND Status__c NOT IN ('Never', 'Rejected')",
                    "closed": "WHERE Assignee__c = '${me}' AND (Status__c  LIKE 'Closed%' OR "
                    + "Status__c IN ('Never', 'Rejected'))",
                },
                "style": {
                    "work_id": "bold red",
                    "subject": "bold blue",
                    "status": "bold yellow",
                    "assignee": "bold green",
                    "url": "blue underline",
                    "table_header": "bold blue",
                    "build": "bold yellow",
                },
            },
        }

    def _get_defaults(self) -> dict:
        return {
            "jenkins": {},
            "github": {},
            "slack": {},
            "PRs": {
                "queries": {},
            },
            "GUS": {
                "queries": {},
                "style": {},
            },
        }

    def _merge(self, param, tree):
        """Merges the param into the tree."""
        for key, value in param.items():
            if isinstance(value, dict):
                self._merge(value, tree[key])
            else:
                tree[key] = value

    def load_envs(self):
        """Loads environment variables."""
        for key, value in os.environ.items():
            if key.startswith("GITGUS_"):
                self.set(key[7:].lower(), value)
        # and some special ones
        if "GITHUB_TOKEN" in os.environ:
            self.set("github.token", os.environ["GITHUB_TOKEN"])
        if "SLACK_TOKEN" in os.environ:
            self.set("slack.token", os.environ["SLACK_TOKEN"])

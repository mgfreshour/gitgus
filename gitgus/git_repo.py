from pathlib import Path

from git import Repo


class GitRepo:
    def __init__(self):
        self._repo = None

    def repo(self):
        """Returns the git repo."""
        if not self._repo:
            self._repo = Repo()
        return self._repo

    def get_branch_name(self) -> str:
        """Returns the current branch name."""
        return self.repo().active_branch.name

    def get_repo_name(self) -> str:
        """Returns the current repo name."""
        return self.repo().remote().url.split(":")[1].split(".")[0]

    def push(self):
        """Pushes the current branch to the remote."""
        self.repo().git.push()

    def get_branches(self):
        """Returns a list of all branches."""
        return self.repo().branches

    def checkout(self, branch_name, create=False):
        """Checkout a branch."""
        if create:
            self.repo().git.checkout("-b", branch_name)
        else:
            self.repo().git.checkout(branch_name)

    def files_lines(self, glob):
        return FilesLineIterator(glob, self.repo().working_tree_dir)


class FilesLineIterator:
    def __init__(self, glob, repo_dir):
        self.files = Path(repo_dir).rglob(glob)
        self.file = None
        self.line = None
        self.line_num = 0
        self.file_num = 0

    def __iter__(self):
        return self

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def __next__(self):
        while True:
            if self.file is None:
                self.file_path = next(self.files)
                if self.file_path is None:
                    raise StopIteration
                self.file = open(self.file_path)
                self.line_num = 0
            self.line = self.file.readline()
            self.line_num += 1
            if self.line == "":
                self.file.close()
                self.file = None
                continue
            return self.line, self.file_path, self.line_num

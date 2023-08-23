def _create_branch(name):
    branch = type("", (), {"name": name})()
    return branch

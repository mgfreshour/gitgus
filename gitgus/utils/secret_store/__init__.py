import platform

from gitgus.utils.secret_store.mac_os import get_macos, set_macos


def get_secret(service, name):
    if platform.system() == "Darwin":
        return get_macos(service, name)
    else:
        raise NotImplementedError("Only MacOS is supported at this time for secret storage.")


def set_secret(service, name, value):
    if platform.system() == "Darwin":
        return set_macos(service, name, value)
    else:
        raise NotImplementedError("Only MacOS is supported at this time for secret storage.")

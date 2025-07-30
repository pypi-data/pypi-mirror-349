import json
import urllib.request
import warnings


import virgui

# this is a finesse and matplotlib dependency, but so far not adding it as a direct dep
try:
    from packaging.version import Version

    has_version = True
except ImportError:
    has_version = False


def check_version() -> None | tuple[Version, Version]:
    if not has_version:
        warnings.warn("Could not check for available versions")
        return

    req = urllib.request.Request(
        url="https://pypi.org/simple/virgui/",
        headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        method="GET",
    )

    ret = urllib.request.urlopen(req)

    if ret.getcode() != 200:
        warnings.warn("Could not check for available versions")

    response = json.loads(ret.read())

    newest = sorted([Version(ver) for ver in response["versions"]])[-1]
    current = Version(virgui.__version__)
    if newest > current:
        return newest, current

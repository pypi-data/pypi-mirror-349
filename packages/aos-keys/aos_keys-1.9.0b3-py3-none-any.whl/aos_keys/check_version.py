#
#  Copyright (c) 2018-2025 EPAM Systems Inc.
#

import requests
from aos_keys.common import print_error, print_message

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from packaging.version import Version

DOCS_URL = 'https://docs.aosedge.tech/docs/quick-start/set-up/'
GET_TIMEOUT = 30


def check_latest_version(package_name):
    installed_version = Version(version(package_name))
    print_message(f'Check {package_name} version ({installed_version}) is up-to-date...')

    # fetch package metadata from PyPI
    pypi_url = f'https://pypi.org/pypi/{package_name}/json'
    try:
        response = requests.get(
            url=pypi_url,
            timeout=GET_TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print_message(
            '[yellow]Cannot get latest version of package. Please check your internet connection and try again later.',
        )
        return

    resp_json = response.json()
    if installed_version.is_prerelease and resp_json.get('releases'):
        latest_version = max(Version(ver) for ver in resp_json.get('releases').keys())
    else:
        latest_version = Version(resp_json.get('info', {}).get('version', '0.0.0'))

    if max(installed_version, latest_version) == installed_version:
        print_message(f'{package_name} installed: {installed_version} latest: {latest_version} is up-to-date')
        return

    if installed_version.major != latest_version.major or installed_version.minor != latest_version.minor:
        print_error(
            f'[red]{package_name} installed: {installed_version} latest: {latest_version} have to be updated',
        )
    else:
        print_message(
            f'[yellow]{package_name} installed: {installed_version} latest: {latest_version} need to be updated',
        )
    print_message(f'Perform updating package according to AosEdge documentation: {DOCS_URL}')

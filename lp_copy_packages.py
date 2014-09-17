#!/usr/bin/python

from __future__ import print_function

from argparse import ArgumentParser
import sys

from launchpadlib.launchpad import Launchpad


def copy_packages(lp, version, from_archive_name, to_archive_name):
    packaging_team = lp.people['juju-packaging']
    build_archive = packaging_team.getPPAByName(name=from_archive_name)
    package_histories = build_archive.getPublishedSources(
        source_name='juju-core', status='Published')
    package_histories = [
        package for package in package_histories
        if package.source_package_version.startswith(version)]
    juju_team = lp.people['juju']
    public_archive = juju_team.getPPAByName(name=to_archive_name)
    for package in package_histories:
        public_archive.copyPackage(
            from_archive=build_archive,
            source_name=package.source_package_name,
            version=package.source_package_version,
            to_pocket='Release', include_binaries=True, unembargo=True)
    return 0


def get_option_parser():
    """Return the option parser for this program."""
    parser = ArgumentParser('Copy juju-core from one archive to another')
    parser.add_argument('version', help='The package version like 1.20.8')
    parser.add_argument('from_archive_name',
        help='The archive to copy source and binary packages from')
    parser.add_argument('to_archive_name',
        help='The archive to copy the source and binary packages to')
    return parser


if __name__ == '__main__':
    parser = get_option_parser()
    args = parser.parse_args()
    lp = Launchpad.login_with(
        'lp-copy-packages', service_root='https://api.launchpad.net',
        version='devel')
    sys.exit(copy_packages(
        lp, args.version, args.from_archive_name, args.to_archive_name))

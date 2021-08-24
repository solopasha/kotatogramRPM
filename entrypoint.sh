#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Please specify package to build"
    exit 1
fi

cp -r "$1"/* /home/builduser/rpmbuild

pushd /home/builduser/rpmbuild > /dev/null
chown -R builduser:builduser ./*

dnf -y builddep SPECS/*.spec
su -c 'rpmbuild -bb SPECS/*.spec' builduser
cp RPMS/x86_64/"$1"-*.rpm /github/workspace
cd /github/workspace

PACKAGE_FILE="$(echo "$1"-*.rpm)"
echo ::set-output name=package-file::"$PACKAGE_FILE"

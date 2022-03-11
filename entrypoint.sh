#!/bin/bash
set -euxo pipefail

if [ -z "$1" ]; then
    echo "Please specify package to build"
    exit 1
fi

cp -r "$1"/* /home/builduser/rpmbuild

cd /home/builduser/rpmbuild
chown -R builduser:builduser ./*
VERSION=$(awk -v ORS= '/^Version:/{print $2"-"} /^Release:/{sub(/%{\?dist}/, ""); print $2}' SPECS/kotatogram-desktop.spec)
VERSION+=$(rpm -E %dist)
echo "VERSION=$VERSION" >> $GITHUB_ENV
dnf -y builddep "SPECS/$1.spec"
su -c 'spectool -g -R SPECS/*.spec' builduser
su -c 'rpmbuild -bb SPECS/*.spec' builduser

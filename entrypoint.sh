#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Please specify package to build"
    exit 1
fi

cp -r "$1"/* /home/builduser/rpmbuild

cd /home/builduser/rpmbuild
chown -R builduser:builduser ./*
VERSION=$(awk -v ORS= '/^Version:/{print $2"-"} /^Release:/{sub(/%{\?dist}/, ""); print $2}' SPECS/kotatogram-desktop.spec)
echo "VERSION=$VERSION" >> $GITHUB_ENV
dnf -y builddep SPECS/*.spec
su -c 'rpmbuild -bb SPECS/*.spec' builduser

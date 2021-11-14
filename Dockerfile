FROM fedora:35
RUN echo -e 'max_parallel_downloads=20\nfastestmirror=True' >> /etc/dnf/dnf.conf && \
    dnf -y install fedora-packager rpmdevtools sudo && \
    dnf -y install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
    https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm && \
    dnf clean all && \
    useradd -m builduser && \
    echo 'builduser ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/builduser && \
    sudo -i -u builduser rpmdev-setuptree
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

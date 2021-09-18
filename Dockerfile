FROM fedora:34
RUN echo -e 'max_parallel_downloads=20\nfastestmirror=True' >> /etc/dnf/dnf.conf
RUN dnf -y install fedora-packager rpmdevtools sudo
RUN dnf -y install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN useradd -m builduser
RUN echo 'builduser ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/builduser
RUN sudo -i -u builduser rpmdev-setuptree
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

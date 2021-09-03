%undefine __cmake_in_source_build
%define debug_package %{nil}
%global _default_patch_fuzz 2

# Telegram Desktop's constants...
%global appname kotatogram-desktop
%global launcher kotatogramdesktop

# Applying toolchain configuration...

Name: kotatogram-desktop
Version: 1.4.3
Release: 1%{?dist}

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPLv3+ with OpenSSL exception -- main tarball;
# * rlottie - LGPLv2+ -- static dependency;
# * qt_functions.cpp - LGPLv3 -- build-time dependency.
License: GPLv3+ and LGPLv2+ and LGPLv3
URL: https://github.com/kotatogram/%{appname}
Summary: Experimental Telegram Desktop fork
Patch0: 0001-Add-an-option-to-hide-messages-from-blocked-users-in.patch

# Telegram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5XkbCommonSupport)
BuildRequires: cmake(dbusmenu-qt5)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.4)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavresample)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(opus)

BuildRequires: cmake
BuildRequires: extra-cmake-modules
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: qt5-qtbase-private-devel
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(webkit2gtk-4.0)
Requires: gtk3%{?_isa}
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(rnnoise)

BuildRequires: cmake(KF5Wayland)
BuildRequires: cmake(Qt5WaylandClient)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: qt5-qtbase-static
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xtst)


# Telegram Desktop require exact version of Qt due to Qt private API usage.
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Requires: hicolor-icon-theme
Requires: open-sans-fonts
Requires: qt5-qtimageformats%{?_isa}

# Short alias for the main package...
Provides: kotatogram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: kotatogram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Obsolete shared version of tg_owt...
Obsoletes: tg_owt < 0-8

%description
Telegram is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any number of your phones,
tablets or computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 50,000 people or
channels for broadcasting to unlimited audiences. You can write to your
phone contacts and find people by their usernames. As a result, Telegram is
like SMS and email combined — and can take care of all your personal or
business messaging needs.

%prep
rm -rf %{appname}-%{version}-full
git clone --recurse-submodules https://github.com/kotatogram/%{appname}.git %{appname}-%{version}-full
cd %{appname}-%{version}-full
/usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .
%patch0 -p1
# Unbundling libraries...
rm -rf Telegram/ThirdParty/{Catch,GSL,QR,SPMediaKeyTap,expected,fcitx-qt5,fcitx5-qt,hime,hunspell,libdbusmenu-qt,lz4,materialdecoration,minizip,nimf,qt5ct,range-v3,xxHash}


# Unbundling rlottie if build against packaged version...
#rm -rf Telegram/ThirdParty/rlottie

# Unbundling libtgvoip if build against packaged version...
#rm -rf Telegram/ThirdParty/libtgvoip

%build
cd %{appname}-%{version}-full
# Building Telegram Desktop using cmake...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTDESKTOP_API_ID=1096745 \
    -DTDESKTOP_API_HASH=d91b15bd9ad1d7cdda32345a9361586b \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
    -DTDESKTOP_LAUNCHER_BASENAME=%{launcher}
%cmake_build

%install
cd %{appname}-%{version}-full
%cmake_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{launcher}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{launcher}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{launcher}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/%{launcher}.appdata.xml

%changelog
* Sat Aug 21 2021 solopasha <1@1.ru> - 1.4.2
- Version 1.4.2

%undefine __cmake_in_source_build
%undefine _auto_set_build_flags
%global _default_patch_fuzz 2
%define debug_package %{nil}

# Telegram Desktop's constants...
%global appname kotatogram-desktop
%global launcher kotatogramdesktop
%global _name telegram-desktop
# Applying toolchain configuration...

Name: kotatogram-desktop
Version: 1.4.8
Release: 6%{?dist}

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPLv3+ with OpenSSL exception -- main tarball;
# * rlottie - LGPLv2+ -- static dependency;
# * qt_functions.cpp - LGPLv3 -- build-time dependency.
License: GPLv3+ and LGPLv2+ and LGPLv3
URL: https://github.com/kotatogram/%{appname}
Summary: Experimental Telegram Desktop fork
Source0: kotatogram-desktop.tar.zst
#Patch0: 0001-Add-an-option-to-hide-messages-from-blocked-users-in.patch
Patch0: %{_name}-desktop-validation-fix.patch
Patch1: no-add.patch
Patch2: 0007_hide-messages-from-blocked-users.patch
Patch100: %{_name}-ffmpeg5.patch

# Telegram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
BuildRequires: meson
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.4)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(webkit2gtk-4.0)

BuildRequires: cmake
BuildRequires: git
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libdispatch-devel
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
Requires: qt6-qtimageformats%{?_isa}
BuildRequires: cmake(PlasmaWaylandProtocols)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: qt6-qtbase-static
Provides: bundled(kf5-kwayland) = 5.90.0
BuildRequires: pkgconfig(wayland-client)
BuildRequires: extra-cmake-modules >= 5.90.0
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)
Requires: hicolor-icon-theme
Requires: open-sans-fonts
Requires: webkit2gtk3%{?_isa}
# Telegram Desktop can use native open/save dialogs with XDG portals.
Recommends: xdg-desktop-portal%{?_isa}
Recommends: (xdg-desktop-portal-gnome%{?_isa} if gnome-shell%{?_isa})
Recommends: (xdg-desktop-portal-kde%{?_isa} if plasma-workspace-wayland%{?_isa})
Recommends: (xdg-desktop-portal-wlr%{?_isa} if wlroots%{?_isa})


# Telegram Desktop require exact version of Qt due to Qt private API usage.


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
%autosetup -n %{appname} -p1
# Unbundling libraries...
#rm -rf Telegram/ThirdParty/{GSL,QR,SPMediaKeyTap,dispatch,expected,extra-cmake-modules,fcitx-qt5,fcitx5-qt,jemalloc,hime,hunspell,lz4,materialdecoration,minizip,nimf,plasma-wayland-protocols,qt5ct,range-v3,wayland-protocols,xxHash}


%build
%set_build_flags \
    CFLAGS="-march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -flto=auto" \
    CXXFLAGS="-march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -Wp,-D_GLIBCXX_ASSERTIONS -flto=auto -Wp,-U_GLIBCXX_ASSERTIONS" \
    LDFLAGS="-Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now -flto=auto"
# Building Telegram Desktop using cmake...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DTDESKTOP_API_TEST=ON \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
    -DTDESKTOP_LAUNCHER_BASENAME=%{launcher}

%set_build_flags \
    CFLAGS="-march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -flto=auto" \
    CXXFLAGS="-march=x86-64 -mtune=generic -O2 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=2 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -Wp,-D_GLIBCXX_ASSERTIONS -flto=auto -Wp,-U_GLIBCXX_ASSERTIONS" \
    LDFLAGS="-Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now -flto=auto"
%cmake_build

%install
%cmake_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{launcher}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{launcher}.desktop

%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/%{name}
%{_datadir}/applications/%{launcher}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/%{launcher}.metainfo.xml

%changelog
* Fri Feb 18 2022 solopasha <pasha@solopasha.ru> - 1.4.8
- Version 1.4.8
* Sat Aug 21 2021 solopasha <1@1.ru> - 1.4.2
- Version 1.4.2

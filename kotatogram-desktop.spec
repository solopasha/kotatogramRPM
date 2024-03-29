%global _default_patch_fuzz 2

%global bundled_fonts 1
%global enable_wayland 1
%global enable_x11 1
%global use_qt5 1
%global legacy_openssl 1

# Telegram Desktop's constants...
%global appname kotatogram-desktop
%global launcher kotatogramdesktop

Name: kotatogram-desktop
Version: 1.4.9
Release: 9%{?dist}

%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

%if 0%{?fedora} && 0%{?fedora} >= 38
%global optflags %(echo %{optflags} -fabi-compat-version=0)
%endif

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPLv3+ with OpenSSL exception -- main tarball;
# * rlottie - LGPLv2+ -- static dependency;
# * qt_functions.cpp - LGPLv3 -- build-time dependency.
License:    GPLv3+ and LGPLv2+ and LGPLv3
URL:        https://github.com/kotatogram/%{appname}
Summary:    Experimental Telegram Desktop fork
Source0:    https://github.com/kotatogram/kotatogram-desktop/releases/download/k%{version}/kotatogram-desktop-%{version}-full.tar.gz
Patch0:     0001-Add-an-option-to-hide-messages-from-blocked-users-in.patch
Patch1:     no-add.patch
Patch2:     https://github.com/kotatogram/kotatogram-desktop/pull/326.patch
Patch3:     https://github.com/kotatogram/kotatogram-desktop/pull/333.patch
Patch4:     https://github.com/kotatogram/kotatogram-desktop/pull/334.patch
Patch5:     https://github.com/kotatogram/kotatogram-desktop/pull/335.patch
Patch6:     https://github.com/kotatogram/kotatogram-desktop/pull/337.patch
Patch7:     25012.patch
Patch8:     telegram-desktop-ffmpeg5.patch
Patch9:     kf594.patch
Source100:  include.patch


# Telegram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64

# tg_owt deps
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xtst)
BuildRequires: yasm

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tl-expected)
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.4)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)

BuildRequires: cmake
BuildRequires: git
BuildRequires: meson
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

%if %{bundled_fonts}
Provides: bundled(open-sans-fonts) = 1.10
Provides: bundled(vazirmatn-fonts) = 27.2.2
%else
Requires: open-sans-fonts
Requires: vazirmatn-fonts
%endif

%if %{use_qt5}
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5XkbCommonSupport)
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa}}
Requires: qt5-qtimageformats%{?_isa}
%else
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
%endif

Provides: bundled(rlottie) = 0~git

%if %{enable_wayland}
%if %{use_qt5}
BuildRequires: cmake(KF5Wayland)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5WaylandClient)
BuildRequires: qt5-qtbase-static
%else
BuildRequires: cmake(PlasmaWaylandProtocols)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: qt6-qtbase-static
Provides: bundled(kf5-kwayland) = 5.90.0
%endif
BuildRequires: pkgconfig(wayland-client)
BuildRequires: extra-cmake-modules >= 5.90.0
%endif

%if %{enable_x11}
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)
%endif

%if 0%{?fedora} && 0%{?fedora} >= 37
BuildRequires: pkgconfig(webkit2gtk-4.1)
Requires: webkit2gtk4.1%{?_isa}
%else
BuildRequires: pkgconfig(webkit2gtk-4.0)
Requires: webkit2gtk3%{?_isa}
%endif

%if %{legacy_openssl}
BuildRequires: openssl1.1-devel
Requires: openssl1.1%{?_isa}
%else
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(openssl)
%endif

BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)

Requires: hicolor-icon-theme

# Telegram Desktop can use native open/save dialogs with XDG portals.
Recommends: xdg-desktop-portal%{?_isa}
Recommends: (xdg-desktop-portal-gnome%{?_isa} if gnome-shell%{?_isa})
Recommends: (xdg-desktop-portal-kde%{?_isa} if plasma-workspace-wayland%{?_isa})
Recommends: (xdg-desktop-portal-wlr%{?_isa} if wlroots%{?_isa})

# Short alias for the main package...
Provides: kotatogram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: kotatogram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

# Virtual provides for bundled libraries...
Provides: bundled(libtgvoip) = 2.4.4
Provides: bundled(rlottie) = 0~git8c69fc2

%description
%{summary}.

%prep
%autosetup -n %{appname}-%{version}-full -p1
# Unbundling libraries...
rm -rf Telegram/ThirdParty/{GSL,QR,dispatch,expected,fcitx-qt5,fcitx5-qt,hime,hunspell,jemalloc,lz4,minizip,nimf,range-v3,xxHash}

mkdir ../Libraries
cd ../Libraries
git clone --recursive https://github.com/desktop-app/tg_owt.git
cd tg_owt
git reset --hard 63a934db1ed212ebf8aaaa20f0010dd7b0d7b396
patch -Np1 -i %{SOURCE100}

%build
cd %{_builddir}/Libraries/tg_owt
cmake \
    -B build \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DTG_OWT_USE_PROTOBUF=OFF \
    -DTG_OWT_PACKAGED_BUILD=ON \
    -DBUILD_SHARED_LIBS=OFF
CXXFLAGS+=" -I/usr/include/libdrm" ninja -C build

cd %{_builddir}/%{appname}-%{version}-full
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_TEST=ON \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
    -Dtg_owt_DIR=%{_builddir}/Libraries/tg_owt/build \
%if %{bundled_fonts}
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
%else
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
%endif
%if %{use_qt5}
    -DDESKTOP_APP_QT6:BOOL=OFF \
%else
    -DDESKTOP_APP_QT6:BOOL=ON \
%endif
%if %{enable_wayland}
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
%else
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=ON \
%endif
%if %{enable_x11}
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
%else
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=ON \
%endif
    -DTDESKTOP_LAUNCHER_BASENAME=%{launcher}
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

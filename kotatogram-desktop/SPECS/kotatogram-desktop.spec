%undefine __cmake_in_source_build
%global _default_patch_fuzz 2

%global enable_wayland 1
%global enable_x11 1

# Telegram Desktop's constants...
%global appname kotatogram-desktop
%global launcher kotatogramdesktop
%global _name telegram-desktop

Name: kotatogram-desktop
Version: 1.4.9
Release: 2%{?dist}

%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPLv3+ with OpenSSL exception -- main tarball;
# * rlottie - LGPLv2+ -- static dependency;
# * qt_functions.cpp - LGPLv3 -- build-time dependency.
License: GPLv3+ and LGPLv2+ and LGPLv3
URL: https://github.com/kotatogram/%{appname}
Summary: Experimental Telegram Desktop fork
Source0: https://github.com/kotatogram/kotatogram-desktop/releases/download/k%{version}/kotatogram-desktop-%{version}-full.tar.gz
Patch0: 0001-Add-an-option-to-hide-messages-from-blocked-users-in.patch
Patch2: no-add.patch
Patch3: https://github.com/kotatogram/kotatogram-desktop/pull/326.patch
Patch4: https://github.com/kotatogram/kotatogram-desktop/pull/333.patch
Patch5: https://github.com/kotatogram/kotatogram-desktop/pull/334.patch
Patch6: https://github.com/kotatogram/kotatogram-desktop/pull/335.patch
Patch7: https://github.com/kotatogram/kotatogram-desktop/pull/337.patch
Patch100: %{_name}-ffmpeg5.patch

# Telegram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)

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
BuildRequires: qt6-qtbase-private-devel

%if %{enable_wayland}
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: qt6-qtbase-static
Provides: bundled(kf5-kwayland) = 5.91.0
Provides: bundled(plasma-wayland-protocols) = 1.6.0
%endif

%if %{enable_x11}
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)
%endif

# Fedora now has a stripped ffmpeg. Make sure we're using the full version.
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires: ffmpeg-devel
Requires: ffmpeg-libs%{?_isa}
%endif

%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
Requires: hicolor-icon-theme
Requires: open-sans-fonts
Requires: qt6-qtimageformats%{?_isa}
Requires: webkit2gtk3%{?_isa}
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
Experimental Telegram Desktop fork.

%prep
%autosetup -n %{appname}-%{version}-full -p1
# Unbundling libraries...
rm -rf Telegram/ThirdParty/{GSL,QR,dispatch,expected,fcitx-qt5,fcitx5-qt,hime,hunspell,jemalloc,lz4,minizip,nimf,range-v3,xxHash}


%build
# Building Telegram Desktop using cmake...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_TEST=ON \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=ON \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
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
* Fri Mar 11 2022 solopasha <pasha@solopasha.ru> - 1.4.9-2
- Add some patches
* Fri Mar 11 2022 solopasha <pasha@solopasha.ru> - 1.4.9-1
- Version 1.4.9 update
* Mon Feb 21 2022 solopasha <pasha@solopasha.ru> - 1.4.8-7
- Add some stuff from telegram-desktop.spec
* Fri Feb 18 2022 solopasha <pasha@solopasha.ru> - 1.4.8-6
- Version 1.4.8
* Sat Aug 21 2021 solopasha <pasha@solopasha.ru> - 1.4.2
- Version 1.4.2

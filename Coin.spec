#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	High-level, retained-mode toolkit for effective 3D graphics development
Summary(pl.UTF-8):	Wysokopoziomowy toolkit do efektywnego rozwijania grafiki 3D
Name:		Coin
Version:	3.1.3
Release:	2
License:	GPL or Coin PEL or Coin EL
Group:		X11/Libraries
Source0:	https://bitbucket.org/Coin3D/coin/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	1538682f8d92cdf03e845c786879fbea
Patch0:		%{name}-build.patch
Patch1:		%{name}-pc.patch
Patch2:		%{name}-format.patch
URL:		http://www.coin3d.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
High-level, retained-mode toolkit for effective 3D graphics
development. It's fully compatible with SGI Open Inventor 2.1.

%description -l pl.UTF-8
Wysokopoziomowy toolkit trybu przechowującego do efektywnego
rozwijania grafiki 3D. Jest w pełni kompatybilny z pakietem SGI Open
Inventor 2.1.

%package devel
Summary:	Header files for Coin3D library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Coin3D
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	openinventor-devel
Obsoletes:	sgi-OpenInventor-devel

%description devel
Header files for Coin3D library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Coin3D.

%package static
Summary:	Static Coin3D library
Summary(pl.UTF-8):	Statyczna biblioteka Coin3D
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Coin3D library.

%description static -l pl.UTF-8
Statyczna biblioteka Coin3D.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# must include COIN_INTERNAL and COIN_DEBUG in CFLAGS/CXXFLAGS, because
# internal CPPFLAGS are not propagated everywhere
CFLAGS="%{rpmcflags} -DCOIN_INTERNAL -DCOIN_DEBUG=0"
CXXFLAGS="%{rpmcxxflags} -DCOIN_INTERNAL -DCOIN_DEBUG=0"
%configure \
	--enable-3ds-import \
	--disable-debug \
	--enable-java-wrapper \
	--enable-man \
	%{?with_static_libs:--enable-static} \
	--enable-system-expat \
	--enable-threadsafe

# FIXME: don't use global LIBS to fix libCoin.la linking
# (but cannot regenerate ac/am because of missing m4 files)
%{__make} \
	LIBS="-ldl -lGL -lX11 -lpthread"

%install
rm -rf $RPM_BUILD_ROOT

# sanitize file list
%{__sed} -i -ne '/^S/p' man/man3/filelist.txt

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libCoin.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog FAQ FAQ.legal NEWS README README.UNIX RELNOTES THANKS
%attr(755,root,root) %{_libdir}/libCoin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCoin.so.60
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/conf/coin-default.cfg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libCoin.so
%attr(755,root,root) %{_bindir}/coin-config
%{_datadir}/%{name}/conf/coin-default.cfg
%dir %{_includedir}/Inventor
%{_includedir}/Inventor/C
%{_includedir}/Inventor/VRMLnodes
%{_includedir}/Inventor/actions
%{_includedir}/Inventor/annex
%{_includedir}/Inventor/bundles
%{_includedir}/Inventor/caches
%{_includedir}/Inventor/collision
%{_includedir}/Inventor/details
%{_includedir}/Inventor/draggers
%{_includedir}/Inventor/elements
%{_includedir}/Inventor/engines
%{_includedir}/Inventor/errors
%{_includedir}/Inventor/events
%{_includedir}/Inventor/fields
%{_includedir}/Inventor/lists
%{_includedir}/Inventor/lock
%{_includedir}/Inventor/manips
%{_includedir}/Inventor/misc
%{_includedir}/Inventor/nodekits
%{_includedir}/Inventor/nodes
%{_includedir}/Inventor/projectors
%{_includedir}/Inventor/scxml
%{_includedir}/Inventor/sensors
%{_includedir}/Inventor/system
%{_includedir}/Inventor/threads
%{_includedir}/Inventor/tools
%{_includedir}/Inventor/Sb*.h
%{_includedir}/Inventor/So*.h
%{_includedir}/Inventor/non_winsys.h
%{_includedir}/Inventor/oivwin32.h
%{_includedir}/SoDebug.h
%{_includedir}/SoWinEnterScope.h
%{_includedir}/SoWinLeaveScope.h
%{_pkgconfigdir}/Coin.pc
%{_aclocaldir}/coin.m4
%{_mandir}/man1/coin-config.1*
%{_mandir}/man3/Sb*.3*
%{_mandir}/man3/Sc*.3*
%{_mandir}/man3/So*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libCoin.a
%endif

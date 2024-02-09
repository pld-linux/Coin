#
# Conditional build:
%bcond_without	apidocs		# API documentation (with man pages)
%bcond_without	static_libs	# static library

Summary:	High-level, retained-mode toolkit for effective 3D graphics development
Summary(pl.UTF-8):	Wysokopoziomowy toolkit do efektywnego rozwijania grafiki 3D
Name:		Coin
Version:	4.0.2
Release:	1
License:	BSD
Group:		X11/Libraries
Source0:	https://github.com/coin3d/coin/releases/download/v%{version}/coin-%{version}-src.tar.gz
# Source0-md5:	1dd89262e2e9e44a046e803515387bdf
Patch0:		%{name}-link.patch
URL:		https://github.com/coin3d/coin/wiki
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	boost-devel
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 3.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= 1:2.2.6
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	simage-devel
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
Obsoletes:	openinventor-devel < 2.2
Obsoletes:	sgi-OpenInventor-devel < 2.2

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

%package apidocs
Summary:	API documentation for Coin library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Coin
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Coin library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Coin.

%prep
%setup -q -n coin
%patch0 -p1

%build
# COIN_HAVE_JAVASCRIPT=OFF because it relies on obsolete JS_GetStringBytes function
%define cmake_opts \\\
	-DCOIN_BUILD_TESTS=OFF \\\
	-DCOIN_HAVE_JAVASCRIPT=OFF \\\
	-DFONTCONFIG_RUNTIME_LINKING=OFF \\\
	-DFREETYPE_RUNTIME_LINKING=OFF \\\
	-DGLU_RUNTIME_LINKING=OFF \\\
	-DLIBBZIP2_RUNTIME_LINKING=OFF \\\
	-DOPENAL_RUNTIME_LINKING=OFF \\\
	-DSIMAGE_RUNTIME_LINKING=OFF \\\
	-DSPIDERMONKEY_INCLUDE_DIR=/usr/include/js187 \\\
	-DSPIDERMONKEY_RUNTIME_LINKING=OFF \\\
	-DZLIB_RUNTIME_LINKING=OFF \\\
	-DUSE_EXTERNAL_EXPAT=ON
	
install -d builddir
cd builddir
%cmake .. \
	%{cmake_opts} \
%if %{with apidocs}
	-DCOIN_BUILD_DOCUMENTATION=ON \
	-DCOIN_BUILD_DOCUMENTATION_MAN=ON
%endif

%{__make}
cd ..

%if %{with static_libs}
install -d builddir-static
cd builddir-static
%cmake .. \
	%{cmake_opts} \
	-DCOIN_BUILD_SHARED_LIBS=OFF

%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# missed by cmake suite
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/man1/coin-config.1 $RPM_BUILD_ROOT%{_mandir}/man1

%if %{with apidocs}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html
# too generic names, not public API etc.
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{_*_,[a-z]*}.3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog FAQ FAQ.legal NEWS README.UNIX README.md RELNOTES THANKS
%attr(755,root,root) %{_libdir}/libCoin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCoin.so.80
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/coin-config
%attr(755,root,root) %{_libdir}/libCoin.so
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
%{_includedir}/Inventor/navigation
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
%{_libdir}/cmake/Coin-%{version}
%{_mandir}/man1/coin-config.1*
%if %{with apidocs}
%{_mandir}/man3/Coin*.3*
%{_mandir}/man3/Sb*.3*
%{_mandir}/man3/Sc*.3*
%{_mandir}/man3/So*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libCoin.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc builddir/html/*.{css,html,js,png}
%endif

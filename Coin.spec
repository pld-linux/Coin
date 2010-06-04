#
######		Unknown group!
Summary:	High-level, retained-mode toolkit for effective 3D graphics development
Summary(pl.UTF-8):	Zbiór narzędzi wysokiego poziomu do efektywnego rozwijania grafiki 3D.
Name:		Coin
Version:	3.1.3
Release:	0.1
License:	GPL
Group:		Productivity/Other
Source0:	http://ftp.coin3d.org/coin/src/all/%{name}-%{version}.tar.gz
# Source0-md5:	1538682f8d92cdf03e845c786879fbea
URL:		http://www.coin3d.org/
#BuildRequires:	-
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Provides:	group(foo)
#Provides:	user(foo)
#Obsoletes:	-
#Conflicts:	-
#BuildArch:	noarch
#ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8



%package devel
Summary:	Header files for ... library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ...
Group:		Development/Libraries
# if base package contains shared library for which these headers are
Requires:	%{name} = %{version}-%{release}
# if -libs package contains shared library for which these headers are
#Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for ... library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ....


%prep
%setup -q
#%setup -q -c -T
#%setup -q -n %{name}
#%setup -q -n %{name}-%{version}.orig -a 1
#%patch0 -p1

# undos the source
#find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

# remove CVS control files
#find -name CVS -print0 | xargs -0 rm -rf

# you'll need this if you cp -a complete dir in source
# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__intltoolize}
#%%{__gettextize}
#%%{__libtoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
# if not running libtool or automake, but config.sub is too old:
# cp -f /usr/share/automake/config.sub .
%configure \
	  --enable-system-expat

%define specflags -DCOIN_INTERNAL -DCOIN_DEBUG=0
# %{__make}

%{__make} \
	CFLAGS="%{rpmcflags} %{specflags}" \
	CPPFLAGS="%{rpmcppflags} %{specflags}" \
	LDFLAGS="%{rpmldflags} -ldl -lGL -lX11 -lgthread"

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
%if %{with initscript}
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
%endif
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%if %{with ldconfig}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/coin-config
%{_datadir}/%{name}
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*


%files devel
%defattr(644,root,root,755)
# %doc devel-doc/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/Inventor
%{_includedir}/SoDebug.h
%{_includedir}/SoWinEnterScope.h
%{_includedir}/SoWinLeaveScope.h
%{_aclocaldir}/*.m4
%{_pkgconfigdir}/*.pc

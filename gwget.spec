#
# Conditional build:
%bcond_without	epiphany	# don't build epiphany extension
#
Summary:	A download manager for GNOME
Summary(pl):	Zarz±dca pobierania plików dla GNOME
Name:		gwget
Version:	0.95
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/gwget/0.95/%{name}-%{version}.tar.bz2
# Source0-md5:	8c268fb6c8f724f0e1971c033ada9c47
Patch0:		%{name}-desktop.patch
URL:		http://www.gnome.org/projects/gwget/
BuildRequires:	GConf2-devel
%{?with_epiphany:BuildRequires:	epiphany-devel >= 1.6.1}
BuildRequires:	gtk+2-devel >= 2:2.6.4
BuildRequires:	intltool >= 0.29
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post,preun):	GConf2
Requires:	wget
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gwget is a download manager for GNOME.

%description -l pl
Gwget to zarz±dca pobierania plików dla GNOME.

%package -n epiphany-extension-gwget
Summary:	Epiphany extension - gwget
Summary(pl):	Rozszerzenie dla Epiphany - gwget
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	epiphany >= 1.6.1

%description -n epiphany-extension-gwget
Epiphany extension that uses gwget to download files.

%description -n epiphany-extension-gwget -l pl
Rozszerzenie dla Epiphany wykorzystuj±ce gwget do pobierania plików.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-schemas-install \
	%{!?with_epiphany: --disable-epiphany-extension}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%if %{with epiphany}
rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany-*/extensions/*.{a,la}
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gwget.schemas

%preun
%gconf_schema_uninstall gwget.schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/idl/*
%{_desktopdir}/*
%{_libdir}/bonobo/servers/*
%{_sysconfdir}/gconf/schemas/*
%{_pixmapsdir}/*

%if %{with epiphany}
%files -n epiphany-extension-gwget
%defattr(644,root,root,755)
%attr(755,root,root)%{_libdir}/epiphany-*/extensions/libgwgetextension.so*
%{_libdir}/epiphany-*/extensions/gwget.xml
%endif

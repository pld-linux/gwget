#
# Conditional build:
%bcond_without	epiphany	# don't build epiphany extension
#
Summary:	A download manager for GNOME
Summary(pl):	Zarz�dca pobierania plik�w dla GNOME
Name:		gwget
Version:	0.98.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/gwget/0.98/%{name}-%{version}.tar.bz2
# Source0-md5:	26bb748aff0769321bf1fd9b65735649
Patch0:		%{name}-desktop.patch
URL:		http://www.gnome.org/projects/gwget/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.71
%{?with_epiphany:BuildRequires:	epiphany-devel >= 2.16.0}
BuildRequires:	gtk+2-devel >= 2:2.10.6
BuildRequires:	intltool >= 0.34
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post,preun):	GConf2
Requires:	libgnomeui >= 2.16.0
Requires:	wget >= 1.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gwget is a download manager for GNOME.

%description -l pl
Gwget to zarz�dca pobierania plik�w dla GNOME.

%package -n epiphany-extension-gwget
Summary:	Epiphany extension - gwget
Summary(pl):	Rozszerzenie dla Epiphany - gwget
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	epiphany >= 2.16.0

%description -n epiphany-extension-gwget
Epiphany extension that uses gwget to download files.

%description -n epiphany-extension-gwget -l pl
Rozszerzenie dla Epiphany wykorzystuj�ce gwget do pobierania plik�w.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	%{?with_epiphany: --with-epiphany-version=2.16} \
	%{!?with_epiphany: --disable-epiphany-extension}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -rf $RPM_BUILD_ROOT%{_includedir}/gwget

%if %{with epiphany}
rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/2.16/extensions/*.{a,la}
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
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_sysconfdir}/gconf/schemas/gwget.schemas

%if %{with epiphany}
%files -n epiphany-extension-gwget
%defattr(644,root,root,755)
%attr(755,root,root)%{_libdir}/epiphany/2.16/extensions/libgwgetextension.so*
%{_libdir}/epiphany/2.16/extensions/gwget.xml
%endif

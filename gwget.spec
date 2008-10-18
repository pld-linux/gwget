#
# Conditional build:
%bcond_without	epiphany	# don't build epiphany extension
#
%define	epiphany_version	2.24
#
Summary:	A download manager for GNOME
Summary(pl.UTF-8):	Zarządca pobierania plików dla GNOME
Name:		gwget
Version:	0.99
Release:	5
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://ftp.gnome.org/pub/gnome/sources/gwget/0.99/%{name}-%{version}.tar.bz2
# Source0-md5:	69f43ae6edbb7ac472c30c547fbf80e6
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-epiphany.patch
Patch2:		%{name}-libgnomeui.patch
URL:		http://www.gnome.org/projects/gwget/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.73
%{?with_epiphany:BuildRequires:	epiphany-devel >= 2.24.0}
BuildRequires:	gtk+2-devel >= 2:2.10.10
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libgnomeui-devel >= 2.18.1
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post,preun):	GConf2
Requires:	libgnomeui >= 2.18.1
Requires:	wget >= 1.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gwget is a download manager for GNOME.

%description -l pl.UTF-8
Gwget to zarządca pobierania plików dla GNOME.

%package -n epiphany-extension-gwget
Summary:	Epiphany extension - gwget
Summary(pl.UTF-8):	Rozszerzenie dla Epiphany - gwget
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	epiphany >= 2.24.0

%description -n epiphany-extension-gwget
Epiphany extension that uses gwget to download files.

%description -n epiphany-extension-gwget -l pl.UTF-8
Rozszerzenie dla Epiphany wykorzystujące gwget do pobierania plików.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
%{__intltoolize}
%{__libtoolize} --install
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	%{?with_epiphany: --with-epiphany-version=%{epiphany_version}} \
	%{!?with_epiphany: --disable-epiphany-extension}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -rf $RPM_BUILD_ROOT%{_includedir}/gwget

%if %{with epiphany}
rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/%{epiphany_version}/extensions/*.{a,la}
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
%{_datadir}/dbus-1/services/org.gnome.gwget.service
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_sysconfdir}/gconf/schemas/gwget.schemas

%if %{with epiphany}
%files -n epiphany-extension-gwget
%defattr(644,root,root,755)
%attr(755,root,root)%{_libdir}/epiphany/%{epiphany_version}/extensions/libgwgetextension.so*
%{_libdir}/epiphany/%{epiphany_version}/extensions/gwget.xml
%endif

#
# Conditional build:
%bcond_without	epiphany	# don't build epiphany extension

Summary:	A download manager for GNOME
Summary(pl):	Zarz�dca pobierania plik�w dla GNOME
Name:		gwget
Version:	0.92
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/gwget/%{name}-%{version}.tar.gz
# Source0-md5:	7e59df048afb194baf2761cb877e8920
Patch0:		%{name}-desktop.patch
URL:		http://gwget.sourceforge.net/
BuildRequires:	GConf2-devel
%{?with_epiphany:BuildRequires:	epiphany-devel >= 1.4.0}
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	intltool >= 0.11
BuildRequires:	libgnomeui-devel >= 2.0.0
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
Requires:	wget
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
Requires:	epiphany >= 1.4.0

%description -n epiphany-extension-gwget
Epiphany extension that uses gwget to download files.

%description -n epiphany-extension-gwget -l pl
Rozszerzenie dla Epiphany wykorzystuj�ce gwget do pobierania plik�w.

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
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_libdir}/epiphany-1.4/extensions}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

install pixmaps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}

%if %{with epiphany}
rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/extensions/*.{a,la}
mv $RPM_BUILD_ROOT%{_libdir}/epiphany/extensions/lib* $RPM_BUILD_ROOT%{_libdir}/epiphany-1.4/extensions
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install

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
%attr(755,root,root)%{_libdir}/epiphany-1.4/extensions/libgwgetextension.so*
%endif

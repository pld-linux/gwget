Summary:	A download manager for GNOME
Summary(pl):	Zarz±dca pobierania plików dla GNOME
Name:		gwget
Version:	0.90
Release:	0.1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/gwget/%{name}-%{version}.tar.gz
# Source0-md5:	44882057713aa64df9b94bbc6b678f29
# Source0-size:	473147
Patch0:		%{name}-desktop.patch
URL:		http://gwget.sourceforge.net/
BuildRequires:	gtk+2-devel >= 2.4.0
BuildRequires:	libgnomeui-devel >= 2.0.0
BuildRequires:	pkgconfig
BuildRequires:	perl-XML-Parser
Requires:	wget
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gwget is a download manager for GNOME.

%description -l pl
Gwget to zarz±dca pobierania plików dla GNOME.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install pixmaps/%{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_pixmapsdir}/*
%{_desktopdir}/*

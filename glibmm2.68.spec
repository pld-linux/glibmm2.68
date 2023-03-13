#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# don't build static library

%define 	glib_ver	1:2.73.2
%define		libsigc_ver	1:3.0.0
Summary:	A C++ interface for glib library
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki glib
Name:		glibmm2.68
Version:	2.74.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/glibmm/2.74/glibmm-%{version}.tar.xz
# Source0-md5:	49cbc72c28ef03d09aa630d09f894b93
URL:		https://www.gtkmm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= %{glib_ver}
BuildRequires:	libsigc++3-devel >= %{libsigc_ver}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libtool >= 2:2.0
BuildRequires:	m4
BuildRequires:	mm-common >= 0.9.12
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	doxygen >= 1:1.8.9
BuildRequires:	graphviz
BuildRequires:	libxslt-progs
%endif
Requires:	glib2 >= %{glib_ver}
Requires:	libsigc++3 >= %{libsigc_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A C++ interface for glib library.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki glib.

%package devel
Summary:	Header files for glibmm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki glibmm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= %{glib_ver}
Requires:	libsigc++3-devel >= %{libsigc_ver}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for glibmm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki glibmm.

%package static
Summary:	Static glibmm library
Summary(pl.UTF-8):	Statyczna biblioteka glibmm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static glibmm library.

%description static -l pl.UTF-8
Statyczna biblioteka glibmm.

%package apidocs
Summary:	Reference documentation for glibmm
Summary(pl.UTF-8):	Szczegółowa dokumentacja dla glibmm
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
Reference documentation for glibmm.

%description apidocs -l pl.UTF-8
Szczegółowa dokumentacja dla glibmm.

%package examples
Summary:	Examples for glibmm
Summary(pl.UTF-8):	Przykłady dla glibmm
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Examples for glibmm.

%description examples -l pl.UTF-8
Przykłady dla glibmm.

%prep
%setup -q -n glibmm-%{version}

%build
mm-common-prepare --copy --force
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-documentation} \
	--enable-maintainer-mode \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdocdir=%{_gtkdocdir}/glibmm-2.68 \
	devhelpdir=%{_gtkdocdir}/glibmm-2.68

cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Makefile* \
	$RPM_BUILD_ROOT%{_libdir}/*.la
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name .deps -type d -exec %{__rm} -r {} + -prune

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_libdir}/libgiomm-2.68.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgiomm-2.68.so.1
%attr(755,root,root) %{_libdir}/libglibmm-2.68.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglibmm-2.68.so.1
%attr(755,root,root) %{_libdir}/libglibmm_generate_extra_defs-2.68.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglibmm_generate_extra_defs-2.68.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgiomm-2.68.so
%attr(755,root,root) %{_libdir}/libglibmm-2.68.so
%attr(755,root,root) %{_libdir}/libglibmm_generate_extra_defs-2.68.so
%dir %{_libdir}/giomm-2.68
%{_libdir}/giomm-2.68/include
%dir %{_libdir}/glibmm-2.68
%{_libdir}/glibmm-2.68/include
%dir %{_libdir}/glibmm-2.68/proc
%{_libdir}/glibmm-2.68/proc/m4
%{_libdir}/glibmm-2.68/proc/pm
%attr(755,root,root) %{_libdir}/glibmm-2.68/proc/generate_wrap_init.pl
%attr(755,root,root) %{_libdir}/glibmm-2.68/proc/gmmproc
%{_includedir}/giomm-2.68
%{_includedir}/glibmm-2.68
%{_pkgconfigdir}/giomm-2.68.pc
%{_pkgconfigdir}/glibmm-2.68.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgiomm-2.68.a
%{_libdir}/libglibmm-2.68.a
%{_libdir}/libglibmm_generate_extra_defs-2.68.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/glibmm-2.68
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	A C++ interface for glib library
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki glib
Name:		glibmm
Version:	2.12.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.12/%{name}-%{version}.tar.bz2
# Source0-md5:	1bae98a3b7b6bc6e792652b800b08439
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.12.9
BuildRequires:	libsigc++-devel >= 1:2.0.17
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.12.9
Requires:	libsigc++ >= 1:2.0.17
Obsoletes:	gtkmm-glib
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
Requires:	glib2-devel >= 1:2.12.9
Requires:	libsigc++-devel >= 1:2.0.17
Requires:	libstdc++-devel
Obsoletes:	gtkmm-glib-devel

%description devel
Header files for glibmm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki glibmm.

%package static
Summary:	Static glibmm library
Summary(pl.UTF-8):	Statyczna biblioteka glibmm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	gtkmm-glib-static

%description static
Static glibmm library.

%description static -l pl.UTF-8
Statyczna biblioteka glibmm.

%package apidocs
Summary:	Reference documentation for glibmm
Summary(pl.UTF-8):	Szczegółowa dokumentacja dla glibmm
Group:		Documentation
Requires:	gtk-doc-common
Provides:	glibmm-doc
Obsoletes:	glibmm-doc

%description apidocs
Reference documentation for glibmm.

%description apidocs -l pl.UTF-8
Szczegółowa dokumentacja dla glibmm.

%package examples
Summary:	Examples for glibmm
Summary(pl.UTF-8):	Przykłady dla glibmm
Group:		Development/Libraries

%description examples
Examples for glibmm.

%description examples -l pl.UTF-8
Przykłady dla glibmm.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__automake}
%configure \
	--enable-fulldocs \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	gtkmm_docdir=%{_gtkdocdir}/%{name}-2.4 \
	glibmm_docdir=%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CHANGES NEWS README
%attr(755,root,root) %{_libdir}/libglibmm-2.4.so.*.*.*
%attr(755,root,root) %{_libdir}/libglibmm_generate_extra_defs-2.4.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglibmm-2.4.so
%attr(755,root,root) %{_libdir}/libglibmm_generate_extra_defs-2.4.so
%{_libdir}/libglibmm-2.4.la
%{_libdir}/libglibmm_generate_extra_defs-2.4.la
%dir %{_libdir}/%{name}-2.4
%{_libdir}/%{name}-2.4/include
%dir %{_libdir}/%{name}-2.4/proc
%{_libdir}/%{name}-2.4/proc/m4
%{_libdir}/%{name}-2.4/proc/pm
%attr(755,root,root) %{_libdir}/%{name}-2.4/proc/beautify_docs.pl
%attr(755,root,root) %{_libdir}/%{name}-2.4/proc/generate_wrap_init.pl
%attr(755,root,root) %{_libdir}/%{name}-2.4/proc/gmmproc
%{_includedir}/%{name}-2.4
%{_pkgconfigdir}/glibmm-2.4.pc
%{_aclocaldir}/glibmm_check_perl.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libglibmm-2.4.a
%{_libdir}/libglibmm_generate_extra_defs-2.4.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}-2.4

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

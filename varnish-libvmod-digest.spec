#
# Conditional build:
%bcond_without	tests		# build without tests

%define	vmod	digest
Summary:	Varnish Digest and HMAC Module
Name:		varnish-libvmod-%{vmod}
Version:	0.3
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://github.com/varnish/libvmod-digest/archive/3.0/%{vmod}-%{version}.tar.gz
# Source0-md5:	e28eb859075eeba82a46d8b352cbf87a
URL:		https://github.com/varnish/libvmod-digest
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-docutils
BuildRequires:	varnish-source
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-source
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
Varnish Module (vmod) for computing HMAC, message digests and working
with base64.

%prep
%setup -qc
mv libvmod-%{vmod}-*/* .

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}

VARNISHSRC=$(pkg-config --variable=srcdir varnishapi)
%configure \
	VARNISHSRC=$VARNISHSRC \
	VMODDIR=%{vmoddir} \
	--disable-static

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/varnish/vmods/libvmod_%{vmod}.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libvmod-%{vmod}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{vmoddir}/libvmod_%{vmod}.so
%{_mandir}/man3/vmod_%{vmod}.3*

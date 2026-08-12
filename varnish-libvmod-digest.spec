#
# Conditional build:
%bcond_with	tests		# tests need network

%define	vmod	digest
Summary:	Varnish Digest and HMAC Module
Name:		varnish-libvmod-%{vmod}
Version:	1.0.3
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://github.com/varnish/libvmod-digest/releases/download/libvmod-digest-%{version}/libvmod-digest-%{version}.tar.gz
# Source0-md5:	f17d332f42287920aec83f132fb91033
URL:		https://github.com/varnish/libvmod-digest
BuildRequires:	python3-docutils
BuildRequires:	varnish-devel
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
Varnish Module (vmod) for computing HMAC, message digests and working
with base64.

%prep
%setup -q -n libvmod-digest-%{version}

%build
%configure \
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

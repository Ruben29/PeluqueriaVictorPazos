%define name Peluqueria Victor Pazos
%define version 7.8
%define unmangled_version 7.8
%define release 1

Summary: Aplicacion que consulta citas en una peluqueria
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Ruben Fernandez gonzalez <rfernandezgonzalez@danielcastelao.org>
Url: http://danielcastelao.com

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version}

%build
python Setup.py build

%install
python Setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

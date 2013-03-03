%define debug_package %nil

Name:           uboot-tools
Version:        2013.01
Release:        1
Summary:        U-Boot utilities
Group:          System/Kernel and hardware
License:        GPLv2
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
Provides:	uboot-mkimage = %{version}-%{release}

%description
This package contains U-Boot utilities (for now, only mkimage).

The mkimage utility encapsulates a kernel image with header
information and other data for use with the U-Boot bootloader. It can
also be used to create ramdisk images for use with this bootloader.

%prep
%setup -q -n u-boot-%{version}

%build
make tools

%install
install -D -m755 tools/mkimage %{buildroot}/%{_bindir}/mkimage
install -D -m644 doc/mkimage.1 %{buildroot}/%{_mandir}/man1/mkimage.1

%files
%{_bindir}/mkimage
%{_mandir}/man1/mkimage.1*

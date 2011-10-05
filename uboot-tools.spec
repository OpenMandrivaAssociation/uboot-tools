Name:           uboot-tools
Version:        2011.09
Release:        %mkrel 1
Summary:        U-Boot utilities
Group:          System/Kernel and hardware
License:        GPLv2
URL:            http://www.denx.de/wiki/U-Boot
Source0:        ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
Patch0:         0001-timestamp_autogenerated.h-doesn-t-need-a-board-confi.patch
Patch1:         0002-tools-don-t-rely-on-CONFIG_SYS_UBL_BLOCK-being-defin.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
This package contains U-Boot utilities (for now, only mkimage).

The mkimage utility encapsulates a kernel image with header
information and other data for use with the U-Boot bootloader. It can
also be used to create ramdisk images for use with this bootloader.

%prep
%setup -q -n u-boot-%{version}
%patch0 -p1
%patch1 -p1

%build
make tools

%install
rm -rf %{buildroot}

install -D -m755 tools/mkimage %{buildroot}/%{_bindir}/mkimage
install -D -m644 doc/mkimage.1 %{buildroot}/%{_mandir}/man1/mkimage.1

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/mkimage
%{_mandir}/man1/mkimage.1*

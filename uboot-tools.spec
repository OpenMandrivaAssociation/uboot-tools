#global candidate rc4
%define _disable_lto %nil

Name:      uboot-tools
Version:   2019.07
Release:   3%{?candidate:.%{candidate}}%{?dist}
Summary:   U-Boot utilities
License:   GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:       http://www.denx.de/wiki/U-Boot

Source0:   ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:   arm-boards
Source2:   arm-chromebooks
Source3:   aarch64-boards
Source4:   aarch64-chromebooks
Source5:   10-devicetree.install

# Fedoraisms patches
# Needed to find DT on boot partition that's not the first partition
Patch1:    uefi-distro-load-FDT-from-any-partition-on-boot-device.patch
# Needed due to issues with shim
# replace with omv
Patch2:    uefi-use-Fedora-specific-path-name.patch

# Board fixes and enablement
Patch5:    usb-kbd-fixes.patch
Patch6:    rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch
Patch7:    dragonboard-fixes.patch
Patch8:    ARM-tegra-Add-NVIDIA-Jetson-Nano.patch
Patch9:    arm-tegra-defaine-fdtfile-for-all-devices.patch
Patch10:   rockchip-rk3399-Fix-USB3-support.patch
Patch11:   rockchip-rock960.patch
Patch12:   rock960-Enable-booting-from-eMMC-when-using-SPL.patch
Patch13:   Raspberry-Pi-32-64-support.patch

BuildRequires:  bc
BuildRequires:  dtc
BuildRequires:  make
# Added for .el7 rebuild, so newer gcc is used
BuildRequires:  gcc
BuildRequires:  flex bison
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-libfdt
BuildRequires:  python2-pyelftools
BuildRequires:  SDL2-devel
BuildRequires:  swig
%ifarch %{armx}
BuildRequires:  vboot-utils
%endif
%ifarch aarch64
BuildRequires:  arm-trusted-firmware-armv8
%endif

Requires:       dtc
Requires:       systemd
%ifarch aarch64 %{arm}
Obsoletes:      uboot-images-elf < 2019.07
Provides:       uboot-images-elf < 2019.07
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     u-boot bootloader images for aarch64 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv8
u-boot bootloader binaries for aarch64 boards
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards
%endif

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 .

sed -i 's/python/python2/' arch/arm/mach-rockchip/make_fit_atf.py

%build
mkdir builds

%ifarch %{armx}
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
  # ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(a64-olinuxino amarula_a64_relic bananapi_m2_plus_h5 bananapi_m64 libretech_all_h3_cc_h5 nanopi_a64 nanopi_neo2 nanopi_neo_plus2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus orangepi_zero_plus2 pine64-lts pine64_plus pinebook sopine_baseboard teres_i)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_a64"
    cp /usr/share/arm-trusted-firmware/sun50i_a64/* builds/$(echo $board)/
  fi
  sun50h6=(orangepi_lite2 orangepi_one_plus pine_h64)
  if [[ " ${sun50h6[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_h6"
    cp /usr/share/arm-trusted-firmware/sun50i_h6/* builds/$(echo $board)/
  fi
  rk3328=(rock64-rk3328)
  if [[ " ${rk3328[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3328"
    cp /usr/share/arm-trusted-firmware/rk3328/* builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 ficus-rk3399 firefly-rk3399 nanopc-t4-rk3399 nanopi-m4-rk3399 nanopi-neo4-rk3399 orangepi-rk3399 orangepi-rk3399 puma-rk3399 rock960-rk3399 rock-pi-4-rk3399 rockpro64-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/* builds/$(echo $board)/
  fi
  # End ATF
  make $(echo $board)_defconfig O=builds/$(echo $board)/
  make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/$(echo $board)/
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    builds/$(echo $board)/tools/mkimage -n rk3399 -T rksd  -d builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/spl_sd.img
    builds/$(echo $board)/tools/mkimage -n rk3399 -T rkspi -d builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/spl_spi.img
  fi
done

%endif

make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools-only_defconfig V=1 O=builds/
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools-all V=1 O=builds/

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb.img u-boot.img u-boot.itb spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch %{arm}
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done

done

# Bit of a hack to remove binaries we don't use as they're large
for board in $(cat %{_arch}-boards)
do
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.*
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/MLO ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/SPL ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.imx ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
done
%endif

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin spl_sd.img spl_spi.img
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

for tool in bmp_logo dumpimage easylogo/easylogo env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes
do
install -p -m 0755 builds/tools/$tool $RPM_BUILD_ROOT%{_bindir}
done
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}

# systemd kernel-install script for device tree
mkdir -p $RPM_BUILD_ROOT/lib/kernel/install.d/
install -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/lib/kernel/install.d/

# Copy sone useful docs over
mkdir -p builds/docs
cp -p board/amlogic/p200/README.odroid-c2 builds/docs/README.odroid-c2
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/Marvell/db-88f6820-gp/README builds/docs/README.mvebu-db-88f6820
cp -p board/rockchip/evb_rk3399/README builds/docs/README.evb_rk3399
cp -p board/solidrun/clearfog/README builds/docs/README.clearfog
cp -p board/solidrun/mx6cuboxi/README builds/docs/README.mx6cuboxi
cp -p board/sunxi/README.sunxi64 builds/docs/README.sunxi64
cp -p board/sunxi/README.nand builds/docs/README.sunxi-nand
cp -p board/ti/am335x/README builds/docs/README.am335x
cp -p board/ti/omap5_uevm/README builds/docs/README.omap5_uevm
cp -p board/udoo/README builds/docs/README.udoo
cp -p board/wandboard/README builds/docs/README.wandboard
cp -p board/warp/README builds/docs/README.warp
cp -p board/warp7/README builds/docs/README.warp7

%files
%doc README doc/imx doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/README.uefi doc/uImage.FIT doc/README.arm64
%doc doc/README.chromium builds/docs/*
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
/lib/kernel/install.d/10-devicetree.install
%dir %{_datadir}/uboot/
%config(noreplace) %{_sysconfdir}/fw_env.config

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
%{_datadir}/uboot/*
%endif

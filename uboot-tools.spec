%global candidate rc3

Name:		uboot-tools
Version:	2021.04
Release:	0.2%{?candidate:.%{candidate}}
Summary:	U-Boot utilities
License:	GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:		http://www.denx.de/wiki/U-Boot

Source0:	ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/arm-boards
Source2:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/arm-chromebooks
Source3:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/aarch64-boards
Source4:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/aarch64-chromebooks

# Fedoraisms patches
# Needed to find DT on boot partition that's not the first partition
Patch1:		https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/uefi-distro-load-FDT-from-any-partition-on-boot-device.patch

# RPi - uses RPI firmware device tree for HAT support
Patch3:		https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch

# Board fixes and enablement
# AllWinner improvements
Patch10:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/AllWinner-PineTab.patch
# TI fixes
Patch11:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/0001-Fix-BeagleAI-detection.patch
# Rockchips improvements
Patch12:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/rk3399-Pinebook-pro-EDP-support.patch
# Fixes for Allwinner network issues
Patch13:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/0001-arm-dts-allwinner-sync-from-linux-for-RGMII-RX-TX-de.patch

# Misc patches
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=973323
Patch100:	u-boot-2021.04-rc3-fix-booting-on-rk3399.patch
Patch101:	uboot-tools-dont-die-on-non-pe-coff-file.patch
BuildRequires:	bc
BuildRequires:	dtc
BuildRequires:	make
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(libfdt)
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	swig
%ifarch %{armx}
BuildRequires:	vboot-utils
%endif
%ifarch aarch64
BuildRequires:	arm-trusted-firmware-armv8
%endif

Requires:	dtc
Requires:	systemd
%ifarch %{armx}
Obsoletes:	uboot-images-elf < 2019.07
Provides:	uboot-images-elf < 2019.07
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package -n uboot-images-armv8
Summary:	u-boot bootloader images for aarch64 boards
Requires:	uboot-tools
BuildArch:	noarch

%description -n uboot-images-armv8
u-boot bootloader binaries for aarch64 boards.
%endif

%ifarch %{arm}
%package -n uboot-images-armv7
Summary:	u-boot bootloader images for armv7 boards
Requires:	uboot-tools
BuildArch:	noarch

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards.
%endif

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

%build
mkdir builds
%ifarch aarch64 %{arm}
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
  # ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(a64-olinuxino amarula_a64_relic bananapi_m2_plus_h5 bananapi_m64 libretech_all_h3_cc_h5 nanopi_a64 nanopi_neo2 nanopi_neo_plus2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus orangepi_zero_plus2 pine64-lts pine64_plus pinebook pinephone pinetab sopine_baseboard teres_i)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_a64"
    cp /usr/share/arm-trusted-firmware/sun50i_a64/* builds/$(echo $board)/
  fi
  sun50h6=(beelink_gs1 orangepi_3 orangepi_lite2 orangepi_one_plus orangepi_zero2 pine_h64 tanix_tx6)
  if [[ " ${sun50h6[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_h6"
    cp /usr/share/arm-trusted-firmware/sun50i_h6/* builds/$(echo $board)/
  fi
  rk3328=(evb-rk3328 nanopi-r2s-rk3328 rock64-rk3328 rock-pi-e-rk3328 roc-cc-rk3328)
  if [[ " ${rk3328[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3328"
    cp /usr/share/arm-trusted-firmware/rk3328/* builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 ficus-rk3399 firefly-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 nanopc-t4-rk3399 nanopi-m4-2gb-rk3399 nanopi-m4-rk3399 nanopi-neo4-rk3399 orangepi-rk3399 pinebook-pro-rk3399 puma-rk3399 rock960-rk3399 rock-pi-4c-rk3399 rock-pi-4-rk3399 rock-pi-n10-rk3399pro rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/* builds/$(echo $board)/
  fi
  # End ATF
  %make_build $(echo $board)_defconfig O=builds/$(echo $board)/
# (tpg) add our distribution mark
  sed -i -e '/^CONFIG_IDENT_STRING=".*"/ s/"$/  %{distribution}"/' builds/$(echo $board)/.config

  %make_build HOSTCC="%{__cc} %{optflags}" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/$(echo $board)/
done

%endif

%make_build HOSTCC="%{__cc} %{optflags}" %{?_smp_mflags} CROSS_COMPILE="" tools-only_defconfig V=1 O=builds/
%make_build HOSTCC="%{__cc} %{optflags}" %{?_smp_mflags} CROSS_COMPILE="" tools-all V=1 O=builds/

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/uboot/

%ifarch aarch64
for board in $(ls builds)
do
mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot.dtb u-boot.img u-boot-dtb.img u-boot.itb u-boot-sunxi-with-spl.bin u-boot-rockchip.bin idbloader.img spl/boot.bin spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch %{arm}
for board in $(ls builds)
do
mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-spl.kwb u-boot-rockchip.bin u-boot-sunxi-with-spl.bin spl/boot.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done

done

# Bit of a hack to remove binaries we don't use as they're large
for board in $(ls builds)
do
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.*
  fi

  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/MLO ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi

  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/SPL ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi

  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.imx ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi

  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-spl.kwb ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.*
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-spl.bin
  fi
done
%endif

for tool in bmp_logo dumpimage env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes kwboot
do
    install -p -m 0755 builds/tools/$tool %{buildroot}%{_bindir}
done
install -p -m 0644 doc/mkimage.1 %{buildroot}%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv %{buildroot}%{_bindir}
( cd %{buildroot}%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config %{buildroot}%{_sysconfdir}

# Copy some useful docs over
mkdir -p builds/docs
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
%doc README doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/uefi doc/uImage.FIT doc/arch/arm64.rst
%doc doc/README.chromium builds/docs/*
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
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

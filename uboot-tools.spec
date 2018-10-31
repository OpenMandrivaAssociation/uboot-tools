%define debug_package %nil

Name:		uboot-tools
Version:	2017.09
Release:	2
Summary:	U-Boot utilities
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://www.denx.de/wiki/U-Boot
Source0:	ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
Provides:	uboot-mkimage = %{EVRD}
Source1:	uEnv.txt

BuildRequires:	openssl-devel dtc bc netpbm
Requires:	dtc

Patch4:		0004-Add-BOOTENV_INIT_COMMAND-for-commands-that-may-be-ne.patch
Patch5:		0005-port-utilite-to-distro-generic-boot-commands.patch

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%if 0
%package -n	uboot-images-armv8
Summary:	u-boot bootloader images for armv8 boards
Requires:	uboot-tools

%description -n	uboot-images-armv8
u-boot bootloader binaries for the aarch64 vexpress_aemv8a
%endif

%ifarch %{arm}
%package -n	uboot-images-armv7
Summary:	u-boot bootloader images for armv7 boards
Requires:	uboot-tools

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards
%endif

%prep
%setup -q -n u-boot-%{version}
%apply_patches

%build
%if 0
make vexpress_aemv8a_juno_config
%%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.bin builds/u-boot.bin.vexpress_aemv8a_juno
make mrproper
%endif

%ifarch %{arm}
# AllWinner devices
make Bananapi_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Bananapi
make mrproper

make Cubieboard_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubieboard
make mrproper

make Cubieboard2_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubieboard2
make mrproper

make Cubietruck_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Cubietruck
make mrproper

make Mele_A1000G_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mele_A1000G
make mrproper

make Mele_A1000_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mele_A1000
make mrproper

make Mini-X_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mini-X
make mrproper

make Mini-X-1Gb_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.Mini-X-1Gb
make mrproper

make A10-OLinuXino-Lime_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A10-OLinuXino-Lime
make mrproper

make A10s-OLinuXino-M_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A10s-OLinuXino-M
make mrproper

make A13-OLinuXino_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A13-OLinuXino
make mrproper

make A13-OLinuXinoM_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A13-OLinuXinoM
make mrproper

make A20-OLinuXino_MICRO_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-sunxi-with-spl.bin builds/u-boot-sunxi-with-spl.bin.A20-OLinuXino_MICRO
make mrproper

# Calxeda
make highbank_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.bin builds/u-boot.bin.highbank
make mrproper

# Freescale i.MX6
make cm_fx6_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.img builds/u-boot.img.cm_fx6
cp -p SPL builds/SPL.cm_fx6
make mrproper

make riotboard_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.imx builds/u-boot.imx.riotboard
make mrproper

make udoo_quad_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.imx builds/u-boot.imx.udoo_quad
make mrproper

make wandboard_dl_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.imx builds/u-boot.imx.wandboard_dl
make mrproper

make wandboard_quad_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.imx builds/u-boot.imx.wandboard_quad
make mrproper

make wandboard_solo_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.imx builds/u-boot.imx.wandboard_solo
make mrproper

# NVidia Tegra devices
make jetson-tk1_defconfig
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.jetson-tk1
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.jetson-tk1
cp -p u-boot.map builds/u-boot.map.jetson-tk1
cp -p u-boot.dtb builds/u-boot.dtb.jetson-tk1
make mrproper

make paz00_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.paz00
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.paz00
cp -p u-boot.map builds/u-boot.map.paz00
cp -p u-boot.dtb builds/u-boot.dtb.paz00
make mrproper

make trimslice_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-dtb-tegra.bin builds/u-boot-dtb-tegra.bin.trimslice
cp -p u-boot-nodtb-tegra.bin builds/u-boot-nodtb-tegra.bin.trimslice
cp -p u-boot.map builds/u-boot.map.trimslice
cp -p u-boot.dtb builds/u-boot.dtb.trimslice
make mrproper

# Samsung Exynos devices
make arndale_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p spl/arndale-spl.bin builds/arndale-spl.bin.arndale
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.arndale
make mrproper

make origen_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p spl/origen-spl.bin builds/origen-spl.bin.origen
cp -p u-boot.bin builds/u-boot.bin.origen
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.origen
make mrproper

make smdkv310_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p spl/smdkv310-spl.bin builds/smdkv310-spl.bin.smdkv310
cp -p u-boot.bin builds/u-boot.bin.smdkv310
make mrproper

make snow_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot-dtb.bin builds/u-boot-dtb.bin.snow
make mrproper

# ST Erikson
make snowball_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p u-boot.bin builds/u-boot.bin.snowball
make mrproper

# TI devices
make am335x_evm_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p MLO builds/MLO.beaglebone
cp -p u-boot.img builds/u-boot.img.beaglebone
make mrproper

make omap3_beagle_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p MLO builds/MLO.beagle
cp -p u-boot.img builds/u-boot.img.beagle
make mrproper

make omap4_panda_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p MLO builds/MLO.panda
cp -p u-boot.img builds/u-boot.img.panda
make mrproper

make omap5_uevm_config
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" V=1
cp -p MLO builds/MLO.uevm
cp -p u-boot.img builds/u-boot.img.uevm
make mrproper

%endif

%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" defconfig V=1
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" silentoldconfig V=1
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" tools-only V=1

%ifarch %{arm}
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" sheevaplug_config V=1
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" env V=1
%endif

%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" defconfig V=1
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" silentoldconfig V=1
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" tools-only V=1

%ifarch %{arm}
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" sheevaplug_config V=1
%make HOSTCC="gcc %{optflags}" CROSS_COMPILE="" env V=1
%endif

%install
%if 0
install -p -m644 builds/u-boot.bin.vexpress_aemv8a_juno -D %{buildroot}%{_datadir}/uboot/vexpress_aemv8a_juno/u-boot.bin
%endif

%ifarch %{arm}
# AllWinner
for board in Bananapi Cubieboard Cubieboard2 Cubietruck Mele_A1000 Mele_A1000G Mini-X Mini-X-1Gb A10-OLinuXino-Lime A10s-OLinuXino-M A13-OLinuXino A13-OLinuXinoM A20-OLinuXino_MICRO
do
install -p -m644 builds/u-boot-sunxi-with-spl.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin
done

# Calxeda
install -p -m644 builds/u-boot.bin.highbank -D %{buildroot}%{_datadir}/uboot/highbank/u-boot.bin

# FreeScale
for board in cm_fx6
do
install -p -m644 builds/u-boot.img.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.img
install -p -m644 builds/SPL.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/SPL
done

for board in riotboard udoo_quad wandboard_dl wandboard_quad wandboard_solo
do
install -p -m644 builds/u-boot.imx.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.imx
done

# NVidia
for board in paz00 trimslice jetson-tk1
do
install -p -m644 builds/u-boot-nodtb-tegra.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-nodtb-tegra.bin
install -p -m644 builds/u-boot-dtb-tegra.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-dtb-tegra.bin
install -p -m644 builds/u-boot.map.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.map
install -p -m644 builds/u-boot.dtb.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.dtb
done

# Samsung
#without dtb
for board in smdkv310
do
install -p -m644 builds/$(echo $board)-spl.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/$(echo $board)-spl.bin
install -p -m644 builds/u-boot.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
done
#with dtb
for board in arndale origen
do
install -p -m644 builds/$(echo $board)-spl.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/$(echo $board)-spl.bin
install -p -m644 builds/u-boot-dtb.bin.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-dtb.bin
done

install -p -m644 builds/u-boot-dtb.bin.snow -D %{buildroot}%{_datadir}/uboot/snow/u-boot-dtb.bin

# STE
install -p -m644 builds/u-boot.bin.snowball -D %{buildroot}%{_datadir}/uboot/snowball/u-boot.bin

# TI
for board in beaglebone beagle panda uevm
do
install -p -m644 builds/u-boot.img.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.img
install -p -m644 builds/MLO.$(echo $board) -D %{buildroot}%{_datadir}/uboot/$(echo $board)/MLO
done

%endif

install -p -m755 tools/mkimage -D %{buildroot}%{_bindir}/mkimage
install -p -m644 doc/mkimage.1 -D %{buildroot}%{_mandir}/man1/mkimage.1
install -p -m755 tools/mkenvimage -D %{buildroot}%{_bindir}/mkenvimage
install -p -m755 tools/dumpimage -D %{buildroot}%{_bindir}/dumpimage
install -p -m755 tools/fit_info -D %{buildroot}%{_bindir}/fit_info
install -p -m755 tools/fit_check_sign -D %{buildroot}%{_bindir}/fit_check_sign

%ifarch %{arm}
install -p -m755 tools/env/fw_printenv -D %{buildroot}%{_bindir}/fw_printenv
ln -sf fw_printenv -D %{buildroot}%{_bindir}/fw_setenv

install -p -m644 tools/env/fw_env.config -D %{buildroot}%{_sysconfdir}/fw_env.config
%endif

%files
%doc README doc/README.imximage doc/README.kwbimage doc/uImage.FIT
%{_bindir}/fit_check_sign
%{_bindir}/fit_info
%{_bindir}/mkimage
%{_bindir}/mkenvimage
%{_bindir}/dumpimage
%{_mandir}/man1/mkimage.1*
%ifarch %{arm}
%dir %{_datadir}/uboot/
%endif
%ifarch %{arm}
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%config(noreplace) %{_sysconfdir}/fw_env.config
%endif

%if 0
%files -n uboot-images-armv8
%{_datadir}/uboot/vexpress_aemv8a_juno/
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
# AllWinner
%{_datadir}/uboot/Bananapi/
%{_datadir}/uboot/Cubieboard/
%{_datadir}/uboot/Cubieboard2/
%{_datadir}/uboot/Cubietruck/
%{_datadir}/uboot/Mele_A1000/
%{_datadir}/uboot/Mele_A1000G/
%{_datadir}/uboot/Mini-X/
%{_datadir}/uboot/Mini-X-1Gb/
%{_datadir}/uboot/A10-OLinuXino-Lime/
%{_datadir}/uboot/A10s-OLinuXino-M/
%{_datadir}/uboot/A13-OLinuXino/
%{_datadir}/uboot/A13-OLinuXinoM/
%{_datadir}/uboot/A20-OLinuXino_MICRO/
# Calxeda
%{_datadir}/uboot/highbank/
# FreeScale
%{_datadir}/uboot/cm_fx6/
%{_datadir}/uboot/riotboard/
%{_datadir}/uboot/wandboard_dl/
%{_datadir}/uboot/wandboard_quad/
%{_datadir}/uboot/wandboard_solo/
%{_datadir}/uboot/udoo_quad/
# NVidia
%{_datadir}/uboot/jetson-tk1/
%{_datadir}/uboot/paz00/
%{_datadir}/uboot/trimslice/
# Samsung
%{_datadir}/uboot/arndale/
%{_datadir}/uboot/smdkv310/
%{_datadir}/uboot/snow/
# STE
%{_datadir}/uboot/snowball/
# TI
%{_datadir}/uboot/beagle/
%{_datadir}/uboot/beaglebone/
%{_datadir}/uboot/origen/
%{_datadir}/uboot/panda/
%{_datadir}/uboot/uevm/
%endif

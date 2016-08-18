%global gittag 88eaeed872841dabce2d6385b585464d6e270e8b
%global gitshorttag 88eaeed

%global debug_package %{nil}

# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod

# name should have a -kmod suffix
Name:           razer-chroma-kmod

Version:        0.0
Release:        1.git%{gitshorttag}%{?dist}
Summary:        Kernel module(s) for Razer Chroma devices

Group:          System Environment/Kernel

License:        GPLv2
URL:            https://github.com/pez2001/razer_chroma_drivers
Source0:        https://github.com/pez2001/razer_chroma_drivers/archive/%{gittag}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{_bindir}/kmodtool
BuildRequires:	dbus-devel
%define AkmodsBuildRequires dbus-devel


# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
A collection of Linux drivers for the Razer devices.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

#%setup -q -c -T -a 0
%setup -q -n razer_chroma_drivers-%{gittag}

for kernel_version in %{?kernel_versions} ; do
    cp -a %{_builddir}/razer_chroma_drivers-%{gittag} %{_builddir}/_kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=%{_builddir}/_kmod_build_${kernel_version%%___*}/driver modules
done


%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    cd %{_builddir}/_kmod_build_${kernel_version%%___*}
    mkdir -p ${RPM_BUILD_ROOT}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -m 0644 %{_builddir}/_kmod_build_${kernel_version%%___*}/driver/{razerkbd.ko,razermouse.ko,razerfirefly.ko} ${RPM_BUILD_ROOT}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Aug 18 2016 Michael Donnelly <mike@donnellyonline.com> 0.0-1
- Initial RPM for the Razer Chroma Linux Driver

#
# Condtional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	dist_kernel	# without distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define _rel	1
Summary:	Opera file system
Summary(pl.UTF-8):	System plikÃ³w Opera
Name:		kernel%{_alt_kernel}-fs-operafs
Version:	1.1
Release:	%{_rel}@%{_kernel_ver_str}
Epoch:		0
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.stack.nl/~svdb/operafs/operafs-%{version}.tar.gz
# Source0-md5:	eedc1d7d52450c99fd2bf2bf9d6fc6e8
Patch0:		operafs-main-comment.patch
URL:		http://www.stack.nl/~svdb/operafs/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel%{_alt_kernel}}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OperaFS is a Linux implementation of the Opera file system, which is the
file system used on 3DO CD-ROM's.

%description -l pl.UTF-8
System plików Opera jest wykorzystywany do zapisu danych na p³ytach CD na
platformie 3DO.

%prep
%setup -q -n operafs-%{version}
%patch0 -p1

%build
%if %{with kernel}
%build_kernel_modules -m operafs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m operafs -d fs
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%if %{with kernel}
%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/fs/*
%endif

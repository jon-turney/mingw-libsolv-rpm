%{?mingw_package_header}

Name:           mingw-libsolv
Version:        0.7.22
Release:        2%{?dist}
Summary:        Cross-compiled package dependency solver

License:        BSD
URL:            https://github.com/openSUSE/libsolv
Source:         %{url}/archive/%{version}.tar.gz

Patch0:         0001-Fix-building-on-MinGW-w64.patch
Patch1:         0002-Ensure-duplinvolvedmap_all-is-reset-when-a-solver-is.patch

BuildArch:      noarch

BuildRequires:  cmake

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-zlib

%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

# Win32
%package -n mingw32-libsolv
Summary:        MinGW compiled libsolv

%description -n mingw32-libsolv
MinGW compiled libsolv for the Win32 target.

%package -n mingw32-libsolv-static
Summary:        MinGW libsolv (static)
Group:          Development/Libraries
Requires:       mingw32-libsolv = %{version}-%{release}

%description -n mingw32-libsolv-static
MingW compiled static libsolv for the Win32 target.

# Win64
%package -n mingw64-libsolv
Summary:        MinGW compiled libsolv

%description -n mingw64-libsolv
MinGW compiled libsolv for the Win64 target.

%package -n mingw64-libsolv-static
Summary:        MinGW libsolv (static)
Group:          Development/Libraries
Requires:       mingw64-libsolv = %{version}-%{release}

%description -n mingw64-libsolv-static
MingW compiled static libsolv for the Win64 target.

%{?mingw_debug_package}

%prep
%autosetup -p1 -n libsolv-%{version}

%build
export MINGW32_CFLAGS="%{mingw32_cflags} -fno-PIC -D__USE_MINGW_ANSI_STDIO=1"
export MINGW64_CFLAGS="%{mingw64_cflags} -fno-PIC -D__USE_MINGW_ANSI_STDIO=1"
export MINGW64_LDFLAGS="%{mingw64_ldflags} -Wl,--export-all-symbols"
export MINGW32_LDFLAGS="%{mingw32_ldflags} -Wl,--export-all-symbols"

%mingw_cmake                                     \
  -DENABLE_STATIC=ON                             \
  -DWITHOUT_COOKIEOPEN=ON                        \
  ..
%mingw_make

%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# Remove executables and scripts
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/*.{exe,sh}
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/*.{exe,sh}

# Remove manpages
rm -fr $RPM_BUILD_ROOT%{mingw32_mandir}
rm -fr $RPM_BUILD_ROOT%{mingw64_mandir}

%files -n mingw32-libsolv
%{mingw32_bindir}/*.dll
%{mingw32_libdir}/*.dll.a
%{mingw32_libdir}/pkgconfig/*.pc
%{mingw32_datadir}/cmake/Modules/*.cmake
%{mingw32_includedir}/solv/*.h

%files -n mingw32-libsolv-static
%{mingw32_libdir}/*.a
%exclude %{mingw32_libdir}/*.dll.a

%files -n mingw64-libsolv
%{mingw64_bindir}/*.dll
%{mingw64_libdir}/*.dll.a
%{mingw64_libdir}/pkgconfig/*.pc
%{mingw64_datadir}/cmake/Modules/*.cmake
%{mingw64_includedir}/solv/*.h

%files -n mingw64-libsolv-static
%{mingw64_libdir}/*.a
%exclude %{mingw64_libdir}/*.dll.a

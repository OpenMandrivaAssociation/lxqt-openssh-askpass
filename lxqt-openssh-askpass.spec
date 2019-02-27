%define git 0
Name: lxqt-openssh-askpass
Version: 0.14.1
%if %git
Release: 1.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 1
Source0: https://downloads.lxqt.org/downloads/%{name}/%{version}/%{name}-%{version}.tar.xz
%endif
Summary: OpenSSH askpass application for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake ninja
BuildRequires: qmake5
BuildRequires: git-core
BuildRequires: cmake(lxqt)
BuildRequires: cmake(lxqt-build-tools)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5LinguistTools)
Requires(post,postun): update-alternatives
Provides: ssh-askpass
Requires(post):	openssh-askpass-common

%description
OpenSSH askpass application for the LXQt desktop

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q
%endif
%cmake_qt5 \
	-DPULL_TRANSLATIONS:BOOL=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
mkdir -p %{buildroot}%{_libdir}/ssh
mv -f %{buildroot}%{_bindir}/lxqt-openssh-askpass %{buildroot}%{_libdir}/ssh/
%find_lang %{name} --with-qt --all-name

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass 50
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass 50

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass
update-alternatives --remove bssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass

%files -f %{name}.lang
%{_libdir}/ssh/%{name}
%{_mandir}/man1/*.1*

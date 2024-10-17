#define git 0
Name: lxqt-openssh-askpass
Version: 2.0.1
%if 0%{?git:1}
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 1
Source0: https://github.com/lxqt/lxqt-openssh-askpass/releases/download/%{version}/lxqt-openssh-askpass-%{version}.tar.xz
%endif
Summary: OpenSSH askpass application for the LXQt desktop
URL: https://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake ninja
BuildRequires: git-core
BuildRequires: cmake(lxqt)
BuildRequires: cmake(lxqt2-build-tools)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6LinguistTools)
Requires(post,postun): update-alternatives
Provides: ssh-askpass
Requires(post):	openssh-askpass-common

%description
OpenSSH askpass application for the LXQt desktop

%prep
%if 0%{?git:1}
%autosetup -p1 -n %{name}-%{git}
%else
%autosetup -p1
%endif
%cmake \
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
%dir %{_datadir}/lxqt/translations/lxqt-openssh-askpass

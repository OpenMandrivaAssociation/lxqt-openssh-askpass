%define git 0
Name: lxqt-openssh-askpass
Version: 0.9.0
%if %git
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 5
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
%endif
Summary: OpenSSH askpass application for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
Source1: lxqt-openssh-askpass.csh
Source2: lxqt-openssh-askpass.sh
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: cmake(lxqt)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5LinguistTools)
Requires(post,postun): update-alternatives
Provides: ssh-askpass

%description
OpenSSH askpass application for the LXQt desktop

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q
%endif
%cmake_qt5

%build
%make -C build

%install
%makeinstall_std -C build
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
mkdir -p %{buildroot}%{_libdir}/ssh
mv -f %{buildroot}%{_bindir}/lxqt-openssh-askpass %{buildroot}%{_libdir}/ssh/
for i in %{SOURCE1} %{SOURCE2}; do
	sed -e 's,/usr/libexec/openssh,%{_libdir}/ssh,g' $i >%{buildroot}%{_sysconfdir}/profile.d/$(basename $i)
done
chmod +x %{buildroot}%{_sysconfdir}/profile.d/*

%find_lang %{name} --with-qt

%post
update-alternatives --install %{_libdir}/ssh/ssh-askpass ssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass 50
update-alternatives --install %{_bindir}/ssh-askpass bssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass 50

%postun
[ $1 = 0 ] || exit 0
update-alternatives --remove ssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass
update-alternatives --remove bssh-askpass %{_libdir}/ssh/lxqt-openssh-askpass

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_libdir}/ssh/%{name}

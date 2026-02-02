Name:		mythtv-status
Version:	1.2.0
Release:	4%{?dist}
Summary:	Get the current status of your MythTV system at the command line
Summary(sv):	Hämta ett MythTV-systems status på kommandoraden
License:	GPL-3.0-only
URL:		http://www.etc.gen.nz/projects/mythtv/mythtv-status.html
Source0:	http://www.etc.gen.nz/projects/mythtv/tarballs/mythtv-status-%{version}.tar.gz
Source1:	http://www.etc.gen.nz/projects/mythtv/tarballs/mythtv-status-%{version}.tar.gz.asc
Source2:	http://www.etc.gen.nz/andrew/gpg-key-C603FC4E600F1CECD1C8D97C4B53D931E4D3E863.asc
Source3:	sysconfig
# Patch for Fedora specifics
Patch0:		mythtv-status-fedora.patch

BuildArch:	noarch

BuildRequires:	make
BuildRequires:	gnupg2
# For tests
BuildRequires: perl-Date-Manip
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-FindBin
BuildRequires: perl-libwww-perl
BuildRequires: perl-MIME-tools
BuildRequires: perl-Test-Simple
BuildRequires: perl-XML-LibXML
# For pod2man
BuildRequires:	perl-podlators
# For _unitdir and script definitions
BuildRequires:	systemd-rpm-macros

# Requires not detected automatically
Requires:	perl(MythTV)

# The backend needs to be running SOMEWHERE for mythtv-status to be useful, but
# not necessarily on the same host.
Recommends:	mythtv-backend

%description
This Perl script will display the current status of your MythTV system at the
command line. It can optionally append it to the system message of the day
(MOTD) on a regular basis.

If you want to enable motd update, enable the systemd unit
mythtv-status_update-motd.timer. The update is run quarterly. The
resulting motd is based on /etc/motd.stub, added with the output of
mythtv-status.

%description -l sv
Detta Perl-skript kommer visa den aktuella statusen för ett MythTV-system på
kommandoraden.  Möjligheten finns även att lägga till statusen till dagens
systemmeddelande (MOTD) med regelbundna intervaller.

För att aktivera motd-uppdateringar aktiverar man systemd-enheten
mythtv-status_update-motd.timer. Uppdateringen körs en gång i kvarten.
Den resulterande motd:n baseras på /etc/motd.stub med utskriften från
mythtv-status tillagd.

%prep
%{gpgverify} --keyring=%SOURCE2 --signature=%SOURCE1 --data=%SOURCE0
%autosetup -p1

%build
%make_build

%install
%make_install SBINDIR=%{_sbindir}

# Sysconfig file
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 %SOURCE3 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%systemd_post mythtv-status_health-check.timer mythtv-status_update-motd.timer

%preun
%systemd_preun mythtv-status_health-check.timer mythtv-status_update-motd.timer

%postun
%systemd_postun_with_restart mythtv-status_health-check.timer mythtv-status_update-motd.timer


%files
%doc ChangeLog FAQ README THANKS
%license COPYING
%{_bindir}/mythtv-status
%{_bindir}/mythtv_*
%{_sbindir}/mythtv-update-motd
%{_mandir}/man1/mythtv*.1.gz
%{_mandir}/man8/mythtv-update-motd.8.gz
%{_libexecdir}/%{name}
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Mon Feb 02 2026 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan  4 2025 Göran Uddeborg <goeran@uddeborg.se> - 1.2.0-1
- Update to 1.2.0
- Verify the signature of the code during the build
- Remove a lot of patches that have moved upstream

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Göran Uddeborg <goeran@uddeborg.se> - 1.1.0-3
- Undo the previous patch, a better fix is done in the base mythtv
  package.

* Sat Dec 30 2023 Göran Uddeborg <goeran@uddeborg.se> - 1.1.0-2
- Patch to expect GB in status reports, matching a patch in the base mythtv
  package

* Wed Jul 26 2023 Göran Uddeborg <goeran@uddeborg.se> - 1.1.0-1
- Update to 1.1.0
- Use the now provided make target to install rather than our own scripting
- Use the now provided systemd timers rather than our own cron configuration
- Change license tag to SPDX format
- Run tests during build

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Feb 17 2019 Göran Uddeborg <goeran@Uddeborg.se> - 1.0.1-1
- Update to 1.0.1

* Sat Jan 26 2019 Göran Uddeborg <goeran@Uddeborg.se> - 1.0.0-1
- Update to 1.0.0

* Sun Dec 23 2018 Sérgio Basto <sergio@serjux.com> - 0.10.8-1
- Update to 0.10.8

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.10.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.10.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.10.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Paul Howarth <paul@city-fan.org> - 0.10.4-6
- Perl 5.26 rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 26 2016 Paul Howarth <paul@city-fan.org> - 0.10.4-4
- BR: perl-generators for proper dependency generation
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)

* Tue Jul 26 2016 Göran Uddeborg <goeran@Uddeborg.se> - 0.10.4-3
- Make the backend dependency a recommendation only; mythtv-status is useful
  on remote servers.

* Tue Mar  8 2016 Göran Uddeborg <goeran@Uddeborg.se> - 0.10.4-2
- Tweak the update-motd script adaption slightly
- Generate a manual page for mythtv-status itself
- Add Swedish description
- Remove some specs no longer needed with current build systems.

* Thu Feb 25 2016 Antonio Trande <sagitter@fedoraproject.org> - 0.10.4-1
- Update to 0.10.4
- Use %%license tag
- Patch updated

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.0-7
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 16 2010 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.9.0-5
- Changed R: perl-net-UPnP to R: perl(MythTV).

* Mon Apr 13 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.9.0-4
- Copy motd instead of move to avoid SELinux errors.
- Fix motd update to use stub instead of motd.

* Sun Apr 12 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.9.0-3
- Modify motd update method and update script location.

* Sat Apr 11 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.9.0-2
- Fix sysconfig file location.

* Sat Apr 11 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.9.0-1
- First release.

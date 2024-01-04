Name:		mythtv-status
Version:	1.0.1
Release:	11%{?dist}
Summary:	Get the current status of your MythTV system at the command line
Summary(sv):	Hämta ett MythTV-systems status på kommandoraden
License:	GPLv3
URL:		http://www.etc.gen.nz/projects/mythtv/mythtv-status.html
Source0:	http://www.etc.gen.nz/projects/mythtv/tarballs/mythtv-status-%{version}.tar.gz
Source1:	sysconfig
# Patch for Fedora specifics
Patch0:		mythtv-status-fedora.patch
BuildArch:	noarch
# For perl dependency auto-detection
BuildRequires:	perl-generators
# For pod2man
BuildRequires:	perl-podlators

# Requires not detected automatically
Requires:	perl(MythTV)

# The backend needs to be running SOMEWHERE for mythtv-status to be useful, but
# not necessarily on the same host.
Recommends:	mythtv-backend

%description
This Perl script will display the current status of your MythTV system at the
command line. It can optionally append it to the system message of the day
(MOTD) on a regular basis.

If you want to enable motd update, edit /etc/sysconfig/mythtv-status and change
UPDATE_MOTD=no to UPDATE_MOTD=yes. The update is run hourly. The resulting motd
is based on /etc/motd.stub, added with the output of mythtv-status.

%description -l sv
Detta Perl-skript kommer visa den aktuella statusen för ett MythTV-system på
kommandoraden.  Möjligheten finns även att lägga till statusen till dagens
systemmeddelande (MOTD) med regelbundna intervaller.

För att aktivera motd-uppdateringar redigerar man
/etc/sysconfig/mythtv-status och ändrar UPDATE_MOTD=no till UPDATE_MOTD=yes.
Uppdateringen körs en gång i timmen.  Den resulterande motd:n baseras på
/etc/motd.stub med utskriften från mythtv-status tillagd.

%prep
%setup -q
%patch0 -p1 -b .orig

%build
pod2man bin/mythtv-status man/mythtv-status.1

%install
# Install scripts
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
install -p -m 755 bin/mythtv-status bin/mythtv_recording_{now,soon} %{buildroot}%{_bindir}
install -p -m 755 bin/mythtv-update-motd %{buildroot}%{_sbindir}

# Man files
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 644 man/* %{buildroot}%{_mandir}/man1

# Sysconfig file
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Cron file to update motd, doesn't do anything if not enabled in sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly
echo -e "#!/bin/sh\n%{_sbindir}/mythtv-update-motd" > %{buildroot}%{_sysconfdir}/cron.hourly/mythtv-update-motd.cron
chmod 755  %{buildroot}%{_sysconfdir}/cron.hourly/mythtv-update-motd.cron

%files
%doc ChangeLog FAQ README THANKS
%license COPYING
%{_bindir}/mythtv*
%{_sbindir}/mythtv*
%{_mandir}/man1/mythtv*.1.gz
%{_sysconfdir}/cron.hourly/mythtv-update-motd.cron
%config %{_sysconfdir}/sysconfig/%{name}

%changelog
* Thu Jan 04 2024 Göran Uddeborg <goeran@uddeborg.se> - 1.0.1-11
- Undo the previous patch, a better fix is done in the base mythtv
  package.

* Sat Dec 30 2023 Göran Uddeborg <goeran@uddeborg.se> - 1.0.1-10
- Patch to expect GB in status reports, matching a patch in the base mythtv
  package

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

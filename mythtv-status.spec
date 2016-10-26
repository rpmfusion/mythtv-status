Name:		mythtv-status
Version:	0.10.4
Release:	4%{?dist}
Summary:	Get the current status of your MythTV system at the command line
Summary(sv):	Hämta ett MythTV-systems status på kommandoraden
License:	GPLv3
URL:		http://www.etc.gen.nz/projects/mythtv/mythtv-status.html
Source0:	http://www.etc.gen.nz/projects/mythtv/tarballs/mythtv-status-%{version}.tar.gz
# Patch for Fedora specifics
Patch0:		mythtv-status-fedora.patch
Patch1:		mythtv-status-update-motd.patch
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
UPDATEMOTD=no to UPDATEMOTD=yes. The update is run hourly. The resulting motd
is based on /etc/motd.stub, added with the output of mythtv-status.

%description -l sv
Detta Perl-skript kommer visa den aktuella statusen för ett MythTV-system på
kommandoraden.  Möjligheten finns även att lägga till statusen till dagens
systemmeddelande (MOTD) med regelbundna intervaller.

För att aktivera motd-uppdateringar redigerar man
/etc/sysconfig/mythtv-status och ändrar UPDATEMOTD=no till UPDATEMOTD=yes.
Uppdateringen körs en gång i timmen.  Den resulterande motd:n baseras på
/etc/motd.stub med utskriften från mythtv-status tillagd.

%prep
%setup -q
%patch0 -p1 -b .orig
%patch1 -p1 -b .fedora

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
echo -e "HOST=127.0.0.1\nUPDATEMOTD=no" > %{buildroot}%{_sysconfdir}/sysconfig/%{name}

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
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
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

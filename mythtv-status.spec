Name:		mythtv-status
Version:	0.9.0
Release:	8%{?dist}
Summary:	Get the current status of your MythTV system at the command line
Group:		Applications/Multimedia
# Scripts claim to be under GPLv2 but COPYING and ChangeLog state license
# is GPLv3. Contacted upstream, new release coming soon.
License:	GPLv3
URL:		http://www.etc.gen.nz/projects/mythtv/mythtv-status.html
Source0:	http://www.etc.gen.nz/projects/mythtv/tarballs/mythtv-status-0.9.0.tar.gz
# Patch for Fedora specifics
Patch0:		mythtv-status-fedora.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

# Requires not detected automatically
Requires:	mythtv-backend
Requires:	perl(MythTV)

%description
This Perl script will display the current status of your MythTV system at the
command line. It can optionally append it to the system message of the day
(MOTD) on a regular basis.

If you want to enable motd update, edit /etc/sysconfig/mythtv-status and change
UPDATEMOTD=no to UPDATEMOTD=yes. The update is run hourly. The resulting motd
is based on /etc/motd.stub, added with the output of mythtv-status.

%prep
%setup -q
%patch0 -p1

%build

%install
rm -rf %{buildroot} 

# Install scripts
mkdir -p %{buildroot}/%{_bindir}  %{buildroot}/%{_sbindir}
install -p -m 755 bin/mythtv-status bin/mythtv_recording_{now,soon} %{buildroot}/%{_bindir}
install -p -m 755 bin/mythtv-update-motd %{buildroot}/%{_sbindir}

# Man files
mkdir -p %{buildroot}/%{_mandir}/man1
install -p -m 644 man/* %{buildroot}/%{_mandir}/man1

# Sysconfig file
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
echo -e "HOST=127.0.0.1\nUPDATEMOTD=no" > %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# Cron file to update motd, doesn't do anything if not enabled in sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly
echo -e "#!/bin/sh\n/usr/sbin/mythtv-update-motd" > %{buildroot}%{_sysconfdir}/cron.hourly/mythtv-update-motd.cron
chmod 755  %{buildroot}%{_sysconfdir}/cron.hourly/mythtv-update-motd.cron

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING FAQ README THANKS
%{_bindir}/mythtv*
%{_sbindir}/mythtv*
%{_mandir}/man1/mythtv*.1.gz
%{_sysconfdir}/cron.hourly/mythtv-update-motd.cron
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
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

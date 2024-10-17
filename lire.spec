Summary:	A log analyser supporting many log formats
Name:		lire
Version:	2.1
Release:	%mkrel 3
License:	GPLv2+
Group:		Monitoring
URL:		https://www.logreport.org/
Source0:	http://download.logreport.org/pub/%{name}-%{version}.tar.gz
Source1:	http://download.logreport.org/pub/%{name}-%{version}.tar.gz.asc
Source2:	lire.crontab
Source10:	lire-2.0.1-mdk-bind.cfg.bz2
Source11:	lire-2.0.1-mdk-cups.cfg.bz2
Source12:	lire-2.0.1-mdk-httpd-perl.cfg.bz2
Source13:	lire-2.0.1-mdk-httpd.cfg.bz2
Source14:	lire-2.0.1-mdk-iptables.cfg.bz2
Source15:	lire-2.0.1-mdk-mysql.cfg.bz2
Source16:	lire-2.0.1-mdk-postfix.cfg.bz2
Source17:	lire-2.0.1-mdk-postgresql.cfg.bz2
Source18:	lire-2.0.1-mdk-proftpd.cfg.bz2
Source19:	lire-2.0.1-mdk-spamassassin.cfg.bz2
Source20:	lire-2.0.1-mdk-squid.cfg.bz2
Source21:	lire-2.0.1-mdk-syslog.cfg.bz2
Requires(post): rpm-helper perl-%{name} = %{version}
Requires(preun): rpm-helper perl-%{name} = %{version}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-dsssl
BuildRequires:	docbook-style-xsl
BuildRequires:	ghostscript
BuildRequires:	jadetex
BuildRequires:	libxslt-proc
BuildRequires:	openjade
BuildRequires:	perl-Curses-UI
BuildRequires:	perl-DBD-SQLite
BuildRequires:	perl-Time-modules
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-devel
BuildRequires:	perl-libintl-perl
BuildRequires:	ploticus
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
Requires:	expat >= 1.95.6
#Requires:	perl-MIME-tools
Requires:	docbook-dtd412-xml
Requires:	docbook-style-dsssl
Requires:	docbook-style-xsl
Requires:	ghostscript
Requires:	jadetex
Requires:	openjade
Requires:	ploticus
Requires:	tetex-dvips
Requires:	tetex-latex
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Lire is the versatile log analyser. It can generate
useful reports from most of the network services you can find on the
typical internet server: email, dns, web, ftp, print services,
database, firewall, proxy, etc. More than 34 log formats are supported.

It can generate report in various output formats and can be easily
extended to support new log formats or add new reports.

It only includes the dependencies required for most of the output
formats (Text, HTML, Excel95). You need to install tetex-latex and
ghostscript packages to generate DVI, PS or PDF output formats.

%package -n	perl-%{name}
Summary:	A log analyser supporting many log formats
Group:		Development/Perl
#Requires:	perl-Curses-UI
#Requires:	perl-DBD-SQLite2 >= 0.33
#Requires:	perl-DB_File
#Requires:	perl-Spreadsheet-WriteExcel
#Requires:	perl-Time-modules
#Requires:	perl-XML-Parser
#Requires:	perl-libintl-perl

%description -n	perl-%{name}
Lire is the versatile log analyser. It can generate
useful reports from most of the network services you can find on the
typical internet server: email, dns, web, ftp, print services,
database, firewall, proxy, etc. More than 34 log formats are supported.

This package contains all the perl code for %{name}.

%package	docs
Summary:	Documentation for %{name}
Group:		System/Servers

%description	docs
Lire is the versatile log analyser. It can generate
useful reports from most of the network services you can find on the
typical internet server: email, dns, web, ftp, print services,
database, firewall, proxy, etc. More than 34 log formats are supported.

This package contains the documentation for %{name}.

%prep

%setup -q

mkdir -p Mandriva
bzcat %{SOURCE10} > Mandriva/bind.cfg
bzcat %{SOURCE11} > Mandriva/cups.cfg
bzcat %{SOURCE12} > Mandriva/httpd-perl.cfg
bzcat %{SOURCE13} > Mandriva/httpd.cfg
bzcat %{SOURCE14} > Mandriva/iptables.cfg
bzcat %{SOURCE15} > Mandriva/mysql.cfg
bzcat %{SOURCE16} > Mandriva/postfix.cfg
bzcat %{SOURCE17} > Mandriva/postgresql.cfg
bzcat %{SOURCE18} > Mandriva/proftpd.cfg
bzcat %{SOURCE19} > Mandriva/spamassassin.cfg
bzcat %{SOURCE20} > Mandriva/squid.cfg
bzcat %{SOURCE21} > Mandriva/syslog.cfg

%build

export LYNX="%{_bindir}/lynx"
export SENDMAIL="%{_sbindir}/sendmail"
export TAI64NLOCAL="%{_bindir}/tai64nlocal"

%configure2_5x \
    --with-spooldir=/var/spool/%{name} \
    --with-archivedir=%{_localstatedir}/lib/%{name} \
    --with-perl5libdir=%{perl_vendorlib}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

rm -fr %{buildroot}/%{_datadir}/doc/%{name}

# Remove fw1_lea2dlf which requires Date::Manip
#rm -f %{buildroto}/%{_libexecdir}/lire/convertors/fw1_lea2dlf

# Create directories
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/cron.d
install -d %{buildroot}%{_sysconfdir}/sysconfig/lire.d
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}/var/spool/%{name}

# Install lr_vendor_cron script and crontab
install -m0750 all/script/lr_vendor_cron %{buildroot}%{_sbindir}/
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.d/%{name}

install -m0644 Mandriva/*.cfg %{buildroot}%{_sysconfdir}/sysconfig/lire.d/

%pre
%_pre_useradd lire %{_localstatedir}/lib/%{name} /bin/sh

%postun
%_postun_userdel lire

%clean 
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* AUTHORS INSTALL NEWS THANKS
%doc doc/BUGS doc/ChangeLog* doc/TODO

%config(noreplace) %{_sysconfdir}/cron.d/lire
%dir %{_sysconfdir}/sysconfig/lire.d
%config(noreplace) %{_sysconfdir}/sysconfig/lire.d/*.cfg
%{_sbindir}/lr_vendor_cron

%dir %attr(0775,root,lire) %{_sysconfdir}/%{name}
%dir %attr(0775,root,lire) %{_sysconfdir}/%{name}/config
%dir %attr(0775,root,lire) %{_sysconfdir}/%{name}/plugins
%dir %attr(0775,root,lire) %{_sysconfdir}/%{name}/converters
%config(noreplace) %{_sysconfdir}/%{name}/plugins/*

# These "configuration files" can be overidden with a .local
%{_sysconfdir}/%{name}/address.cf
%{_sysconfdir}/%{name}/defaults
%{_sysconfdir}/%{name}/disclaimer
%{_sysconfdir}/%{name}/explanation
%{_sysconfdir}/%{name}/profile_lean
%{_sysconfdir}/%{name}/signature

%{_bindir}/*
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man7/*

%dir %attr(0770,lire,lire) /var/spool/%{name}
%dir %attr(0770,lire,lire) %{_localstatedir}/lib/%{name}

# this is to please mr. lint some
%files -n perl-%{name}
%defattr(-,root,root)
%{perl_vendorlib}/Lire/*
%{perl_vendorlib}/LocaleData/*/LC_MESSAGES/*
%{_mandir}/man3/*

%files docs
%defattr(-,root,root)
%doc doc/user-manual doc/dev-manual doc/examples doc/*.pdf doc/*.txt



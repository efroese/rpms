%define _prefix		/opt/local
%define _localstatedir	/opt/local/var
%define _mandir		/opt/local/man
%define _infodir	/opt/local/share/info
%define rubyver		1.9.2
%define rubyminorver	p0
Name:		ruby%{rubyver}%{rubyminorver}
Version:	%{rubyver}%{rubyminorver}
Release:	1%{?dist}
License:	Ruby License/GPL - see COPYING
URL:		http://www.ruby-lang.org/
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{rubyver}-%{rubyminorver}.tar.gz
Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel tk-devel libX11-devel gcc unzip openssl-devel db4-devel byacc

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -n ruby-%{rubyver}-%{rubyminorver}

%build
CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"
export CFLAGS
%configure \
--enable-shared \
--disable-rpath
make RUBY_INSTALL_NAME=ruby %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%doc README COPYING ChangeLog LEGAL ToDo
%{_prefix}/*

%changelog
* Wed Dec 22 2010 Taylor Kimball <taylor@lightcrest.com> - 1.9.2-p0-1
- Initial build for el5 based off of el5 spec.

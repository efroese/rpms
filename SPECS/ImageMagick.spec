%define VERSION  6.4.9
%define Patchlevel  10

Name:           ImageMagick
Version:        %{VERSION}
Release:        %{Patchlevel}
Summary:        ImageMagick is a software suite to create, edit, and compose bitmap images. It can read, convert and write images in a variety of formats (about 200) including GIF, JPEG, JPEG-2000, PNG, PDF, PhotoCD, TIFF, and DPX. Use ImageMagick to translate, flip, mirror, rotate, scale, shear and transform images, adjust image colors, apply various special effects, or draw text, lines, polygons, ellipses and Bezier curves.
Group:          Applications/Multimedia
License:        http://www.imagemagick.org/script/license.php
Url:            http://www.imagemagick.org/
Source0:        ftp://ftp.imagemagick.org/pub/%{name}/%{name}-%{VERSION}-%{Patchlevel}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:  libtiff-devel, giflib-devel, zlib-devel
BuildRequires:  ghostscript-devel, djvulibre-devel
BuildRequires:  libwmf-devel, jasper-devel, libtool-ltdl-devel
BuildRequires:  libX11-devel, libXext-devel, libXt-devel
BuildRequires:  lcms-devel, libxml2-devel, librsvg2-devel

%description
ImageMagick is a software suite to create, edit, and compose bitmap images. It can read, convert and write images in a variety of formats (about 100) including DPX, GIF, JPEG, JPEG-2000, PDF, PhotoCD, PNG, Postscript, SVG, and TIFF. Use ImageMagick to translate, flip, mirror, rotate, scale, shear and transform images, adjust image colors, apply various special effects, or draw text, lines, polygons, ellipses and B�zier curves.

The functionality of ImageMagick is typically utilized from the command line or you can use the features from programs written in your favorite programming language. Choose from these interfaces: G2F (Ada), MagickCore (C), MagickWand (C), ChMagick (Ch), Magick++ (C++), JMagick (Java), L-Magick (Lisp), nMagick (Neko/haXe), PascalMagick (Pascal), PerlMagick (Perl), MagickWand for PHP (PHP), PythonMagick (Python), RMagick (Ruby), or TclMagick (Tcl/TK). With a language interface, use ImageMagick to modify or create images automagically and dynamically.

ImageMagick is free software delivered as a ready-to-run binary distribution or as source code that you can freely use, copy, modify, and distribute. Its license is compatible with the GPL. It runs on all major operating systems.

%package devel
Summary: Library links and header files for ImageMagick application development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libX11-devel, libXext-devel, libXt-devel
Requires: ghostscript-devel
Requires: bzip2-devel
Requires: freetype-devel
Requires: libtiff-devel
Requires: libjpeg-devel
Requires: lcms-devel
Requires: jasper-devel
Requires: pkgconfig

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

%package doc
Summary: ImageMagick HTML documentation
Group: Documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in HTML format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/


%package perl
Summary: ImageMagick perl bindings
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.

%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: %{name}-c++ = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.

You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%setup -q -n %{name}-%{VERSION}-%{Patchlevel}
sed -i 's/libltdl.la/libltdl.so/g' configure
# for %doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples

%build
%configure --enable-shared \
           --disable-static \
           --with-modules \
           --with-perl \
           --with-x \
           --with-threads \
           --with-magick_plus_plus \
           --with-gslib \
           --with-wmf \
           --with-lcms \
           --with-rsvg \
           --with-xml \
           --with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
           --without-dps
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
cp -a www/source $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{VERSION}
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# fix weird perl Magick.so permissions
chmod 755 $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Image/Magick/Magick.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find $RPM_BUILD_ROOT -name "*.bs" |xargs rm -f
find $RPM_BUILD_ROOT -name ".packlist" |xargs rm -f
find $RPM_BUILD_ROOT -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find $RPM_BUILD_ROOT/%{_libdir}/perl* -type f -print \
        | sed "s@^$RPM_BUILD_ROOT@@g" > perl-pkg-files 
find $RPM_BUILD_ROOT%{perl_vendorarch} -type d -print \
        | sed "s@^$RPM_BUILD_ROOT@%dir @g" \
        | grep -v '^%dir %{perl_vendorarch}$' \
        | grep -v '/auto$' >> perl-pkg-files 
if [ -z perl-pkg-files ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi

# These don't belong here, we include them in %%doc
rm $RPM_BUILD_ROOT%{_datadir}/%{name}-%{VERSION}/{ChangeLog,LICENSE,NEWS.txt}

# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv $RPM_BUILD_ROOT%{_includedir}/%{name}/magick/magick-config.h \
   $RPM_BUILD_ROOT%{_includedir}/%{name}/magick/magick-config-%{wordsize}.h

cat >$RPM_BUILD_ROOT%{_includedir}/%{name}/magick/magick-config.h <<EOF
#ifndef IMAGEMAGICK_MULTILIB
#define IMAGEMAGICK_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick-config-32.h"
#elif __WORDSIZE == 64
# include "magick-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc QuickStart.txt ChangeLog Platforms.txt
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt
%{_libdir}/libMagickCore.so.*
%{_libdir}/libMagickWand.so.*
%{_bindir}/[a-z]*
%{_libdir}/%{name}-%{VERSION}
%{_datadir}/%{name}-%{VERSION}
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/MagickCore-config
%{_bindir}/Magick-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/libMagickCore.so
%{_libdir}/libMagickWand.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/Wand.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/magick
%{_includedir}/%{name}/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-%{VERSION}

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{_libdir}/libMagick++.so.*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{_bindir}/Magick++-config
%{_includedir}/%{name}/Magick++
%{_includedir}/%{name}/Magick++.h
%{_libdir}/libMagick++.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/ImageMagick++.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt


%changelog
* Sun May 01 2005 Cristy <cristy@mystic.es.dupont.com> 1.0-0
*  Port of Redhat's RPM script to support ImageMagick.

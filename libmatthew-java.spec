%define section         free
%define gcj_support     1

Name:           libmatthew-java
Version:        0.7.1
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Collection of Java libraries
License:        GPL
Group:          Development/Java
#URL:            http://www.matthew.ath.cx/projects/java/
#Source0:        http://www.matthew.ath.cx/projects/java/%{name}-%{version}.tar.gz
# XXX: somehow the Debian version is always newer than upstream
URL:            http://packages.debian.org/source/sid/libmatthew-java
Source0:        http://ftp.de.debian.org/debian/pool/main/libm/libmatthew-java/libmatthew-java_%{version}.orig.tar.gz
Patch0:         libmatthew-java-0.7-no-classpath-in-manifest.patch
Requires:       jpackage-utils
BuildRequires:  java-rpmbuild
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
%endif
BuildRequires:  java-javadoc
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
A collection of Java libraries, including:

- Unix Sockets Library: This is a collection of classes and native code to
  allow you to read and write Unix sockets in Java.
              
- Debug Library: This is a comprehensive logging and debugging solution.
              
- CGI Library: This is a collection of classes and native code to allow you to
  write CGI applications in Java.
              
- I/O Library: This provides a few much needed extensions to the Java I/O
  subsystem. Firstly, there is a class which will connect and InputStream with
  an OutputStream and copy data between them.

  Secondly there are two classes for inserting into an Input or OutputStream
  pipe a command line command, so that everything is piped through that
  command.

  Thirdly there are a pair of classes for splitting streams in two. This can
  either be to two OuputStreams, or to an OutputStream and a file. Equivelent
  to the UNIX tool tee in UNIX pipes.

- Hexdump: This class formats byte-arrays in hex and ascii for display.
              
%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1
/bin/touch Manifest
%{__perl} -pi -e 's|http://java.sun.com/j2se/1.4.2/docs/api/|%{_javadocdir}/java|' Makefile

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{__make} \
  JAVAC=%{javac} \
  JAR=%{jar} \
  JAVAH=%{java_home}/bin/javah \
  GCJ=%{gcj} \
  CC=%{__cc} \
  LD=%{__ld} \
  CFLAGS="-fPIC %{optflags} -std=c99" \
  LDFLAGS="-fPIC -shared" \
  GCJFLAGS="%{optflags} -fjni" \
  JCFLAGS="-nowarn -source 1.5" \
  JAVADOC="%{javadoc}" \
  JAVA_HOME=%{java_home} all doc

%install
%{__rm} -rf %{buildroot}

%{makeinstall_std} \
  PREFIX=%{_prefix} \
  JARDIR=%{_jnidir}/libmatthew-java-%{version} \
  LIBDIR=%{_libdir} \
  JAVAC=%{javac} \
  JAR=%{jar} \
  JAVAH=%{java_home}/bin/javah \
  GCJ=%{gcj} \
  CC=%{__cc} \
  LD=%{__ld} \
  CFLAGS="-fPIC %{optflags}" \
  LDFLAGS="-fPIC -shared" \
  GCJFLAGS="%{optflags} -fjni" \
  JCFLAGS="-nowarn -source 1.5" \
  JAVADOC="%{javadoc}" \
  JAVA_HOME=%{java_home}

%if 0
(cd %{buildroot}%{_jnidir}/libmatthew-java-%{version} && for jar in *.jar; do %{__mv} ${jar} `/bin/basename ${jar} .jar`-%{version}.jar; done)
(cd %{buildroot}%{_jnidir}/libmatthew-java-%{version} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)
%endif

%{__ln_s} libmatthew-java-%{version} %{buildroot}%{_jnidir}/libmatthew-java

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc COPYING INSTALL README
%{_jnidir}/libmatthew-java*
%{_libdir}/*.so
%{gcj_files}


%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %dir %{_javadocdir}/%{name}

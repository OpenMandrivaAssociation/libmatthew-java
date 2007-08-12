%define section         free
%define gcj_support     1

Name:           libmatthew-java
Version:        0.3
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Java bindings for D-Bus
License:        GPL
Group:          Development/Java
URL:            http://www.matthew.ath.cx/projects/java/
Source0:        http://www.matthew.ath.cx/projects/java/libmatthew-java-0.3.tar.gz
Requires:       jpackage-utils >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.6
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
A collection of Java libraries, including:

Unix Sockets Library

This is a collection of classes and native code to allow you to read and write
Unix sockets in Java.
              
Debug Library

This is a comprehensive logging and debugging solution.
              
CGI Library

This is a collection of classes and native code to allow you to write CGI
applications in Java.
              
I/O Library

This provides a few much needed extensions to the Java I/O subsystem. Firstly,
there is a class which will connect and InputStream with an OutputStream and
copy data between them.

Secondly there are two classes for inserting into an Input or OutputStream pipe
a command line command, so that everything is piped through that command.

Thirdly there are a pair of classes for splitting streams in two. This can
either be to two OuputStreams, or to an OutputStream and a file. Equivelent to
the UNIX tool tee in UNIX pipes.

Hexdump

This class formats byte-arrays in hex and ascii for display.
              
%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__mkdir_p} api

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
  CFLAGS="-fPIC %{optflags}" \
  LDFLAGS="-fPIC -shared" \
  GCJFLAGS="%{optflags} -fjni" \
  JCFLAGS="-nowarn -source 1.5" \
  JAVA_HOME=%{java_home}

%{javadoc} -d api `%{_bindir}/find . -name '*.java'`

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
  JAVA_HOME=%{java_home}

(cd %{buildroot}%{_jnidir}/libmatthew-java-%{version} && for jar in *.jar; do %{__mv} ${jar} `/bin/basename ${jar} .jar`-%{version}.jar; done)
(cd %{buildroot}%{_jnidir}/libmatthew-java-%{version} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__ln_s} libmatthew-java-%{version} %{buildroot}%{_jnidir}/libmatthew-java

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

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
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %dir %{_javadocdir}/%{name}

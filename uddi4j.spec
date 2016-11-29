%{?scl:%scl_package uddi4j}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name:		%{?scl_prefix}uddi4j
Version:	2.0.5
Release:	12.%{baserelease}%{?dist}
Summary:	Universal Description, Discovery and Integration registry API for Java
Group:		Development/Libraries
License:	IBM
URL:		http://sourceforge.net/projects/uddi4j/

Source0:	http://downloads.sf.net/project/uddi4j/uddi4j/%{version}/uddi4j-src-%{version}.zip
Source1:	%{pkg_name}-MANIFEST.MF
Source2:	http://repo1.maven.org/maven2/org/uddi4j/uddi4j/%{version}/uddi4j-%{version}.pom

# Set javac path in build.xml
Patch0:		uddi4j-set-javac-path.patch

# A couple of utf8 incompatible chars prevent compile
Patch1:		uddi4j-remove-nonutf8-chars.patch

BuildArch:	noarch

BuildRequires:	%{?scl_prefix_java_common}ant
BuildRequires:	%{?scl_prefix}axis
BuildRequires:	%{?scl_prefix_java_common}xerces-j2

BuildRequires:	%{?scl_prefix_java_common}jpackage-utils

Requires:	%{?scl_prefix}axis
Requires:	%{?scl_prefix_java_common}xerces-j2

Requires:	%{?scl_prefix_java_common}jpackage-utils

%description
UDDI4J is a Java class library that provides an API to interact with a 
UDDI (Universal Description, Discovery and Integration) registry.

%package javadoc
Summary:	Javadocs for %{pkg_name}
Group:		Documentation
Requires:	%{?scl_prefix_java_common}jpackage-utils

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}
%patch0 -p1
%patch1 -p1

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

ln -s %{_datadir}/java/axis/saaj.jar
ln -s %{_datadir}/java/axis/axis.jar
ln -s %{_datadir}/java/axis/jaxrpc.jar
ln -s %{_datadir}/java/xerces-j2.jar xerces.jar
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
ant compile javadocs
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/%{pkg_name}.jar META-INF/MANIFEST.MF

install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{pkg_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
cp -rp build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}

# POMs
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%{?scl:EOF}


%files
%doc README
%doc LICENSE.html
%doc BuildDate.txt
%doc ReleaseNotes.html
%{_javadir}/*
%{_mavenpomdir}/*

%files javadoc
%doc README
%doc LICENSE.html
%{_javadocdir}/%{pkg_name}

%changelog
* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 2.0.5-12.1
- Auto SCL-ise package for rh-eclipse46 collection

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Gerard Ryan <galileo@fedoraproject.org> - 2.0.5-10
- Remove old maven depmap stuff

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Gerard Ryan <galileo@fedoraproject.org> - 2.0.5-8
- RHBZ#1068576: Switch to java-headless requires

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.0.5-4
- Remove Bundle-Classpath from MANIFEST.MF
- Update Source0 URL so it's not just relying on one mirror

* Tue May 29 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.0.5-3
- Add line to copy javadocs

* Tue May 29 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.0.5-2
- Fix rpmlint issues: source urls; tabs and space warnings
- Remove BuildDate.txt and ReleaseNotes.html from javadoc
- Drop -version from javadoc install path
- Change group to Development/Libraries
- Remove defattr(-,root,root,-)
- Remove rm -rf RPM_BUILD_ROOT

* Mon May 28 2012 Gerard Ryan <galileo@fedoraproject.org> - 2.0.5-1
- Initial packaging
#
# Conditional build:
%bcond_with	tests	# unit tests (some failures in tarball tests?)

Summary:	Backport of compression.zstd
Summary(pl.UTF-8):	Backport modułu compression.zstd
Name:		python3-backports.zstd
Version:	1.2.0
Release:	2
License:	PSF v2, BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/backports-zstd/
Source0:	https://files.pythonhosted.org/packages/source/b/backports-zstd/backports_zstd-%{version}.tar.gz
# Source0-md5:	f78ff5bf615cf8198dadecee121b66ee
Patch0:		backports_zstd-flags.patch
URL:		https://pypi.org/project/backports.zstd/
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-devel < 1:3.14
BuildRequires:	python3-setuptools >= 1:80
BuildRequires:	zstd-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-backports
Requires:	python3-modules >= 1:3.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Backport of PEP-784 "adding Zstandard to the standard library".

%description -l pl.UTF-8
Backport PEP-784 - dodania Zstandard do biblioteki standardowej.

%prep
%setup -q -n backports_zstd-%{version}
%patch -P0 -p1

%build
%py3_build \
	--system-zstd

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m unittest discover -s tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# packaged in python3-backports (python-backports.spec)
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/backports/__init__.py
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/backports/__pycache__

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE_zstd.txt README.md
%dir %{py3_sitedir}/backports/zstd
%{py3_sitedir}/backports/zstd/*.py
%{py3_sitedir}/backports/zstd/*.pyi
%{py3_sitedir}/backports/zstd/py.typed
%{py3_sitedir}/backports/zstd/_zstd.cpython-*.so
%{py3_sitedir}/backports/zstd/__pycache__
%{py3_sitedir}/backports/zstd/_cffi
%{py3_sitedir}/backports/zstd/zipfile
%{py3_sitedir}/backports.zstd-%{version}-py*.egg-info

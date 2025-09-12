%global commit          32499573b89246385373b6288295fff830154635
%global checkout_date   20250912
%global short_commit    %(c=%{commit}; echo ${c:0:7})
%global snapshot        .%{checkout_date}git%{short_commit}

Name:       puffin-viewer
Version:    0.22.0
Release:    0.0%{?snapshot}%{?dist}
Summary:    Viewer GUI for puffin profiler data

License:    Apache-2.0 or MIT
URL:        https://github.com/EmbarkStudios/puffin
Source0:    https://github.com/EmbarkStudios/puffin/archive/%{commit}/puffin-%{commit}.tar.gz

# $ cargo vendor
# Contains puffin-$COMMIT/vendor/*.
Source1:    puffin-%{commit}.cargo-vendor.tar.xz
Source2:    config.toml
Source3:    puffin-viewer.desktop

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  desktop-file-utils

BuildRequires:  gtk3-devel
BuildRequires:  atk-devel
BuildRequires:  fontconfig-devel
BuildRequires:  wayland-devel
BuildRequires:  libxkbcommon-x11-devel

%description
Viewer GUI for puffin profiler data


%prep
%setup -q -D -T -b0 -n puffin-%{commit}
%setup -q -D -T -b1 -n puffin-%{commit}

mkdir .cargo
cp %{SOURCE2} .cargo/


%build
%{__cargo} build \
		%{?_smp_mflags} \
		-Z avoid-dev-deps \
		--frozen \
		--release \
		--features "wayland,x11" \
		--package "puffin_viewer"


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/applications
mv target/release/puffin_viewer \
        %{buildroot}/%{_bindir}/
install -Dm644 puffin_viewer/icon.png %{buildroot}%{_datadir}/pixmaps/puffin_viewer.png
desktop-file-install \
		--dir=%{buildroot}%{_datadir}/applications \
		%{SOURCE3}


%files
%{_bindir}/puffin_viewer
%{_datadir}/pixmaps/puffin_viewer.png
%{_datadir}/applications/puffin-viewer.desktop


%changelog

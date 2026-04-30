#!/usr/bin/env sh
set -eu

repo="layerbrain/layerbrain"
version="${LAYERBRAIN_VERSION:-latest}"
install_dir="${LAYERBRAIN_INSTALL_DIR:-$HOME/.layerbrain/bin}"
download_base="${LAYERBRAIN_DOWNLOAD_BASE:-https://github.com/$repo/releases/download}"

download_file() {
  url="$1"
  output="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$output"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$url" -O "$output"
  else
    echo "Install requires curl or wget." >&2
    exit 1
  fi
}

download_stdout() {
  url="$1"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$url" -O -
  else
    echo "Install requires curl or wget." >&2
    exit 1
  fi
}

os="$(uname -s | tr '[:upper:]' '[:lower:]')"
arch="$(uname -m)"

case "$os" in
  darwin) platform="macos" ;;
  linux) platform="linux" ;;
  *) echo "Unsupported operating system: $os" >&2; exit 1 ;;
esac

case "$arch" in
  x86_64|amd64) machine="x86_64" ;;
  arm64|aarch64) machine="arm64" ;;
  *) echo "Unsupported architecture: $arch" >&2; exit 1 ;;
esac

if [ "$version" = "latest" ]; then
  version="$(download_stdout "https://api.github.com/repos/$repo/releases" | awk -F '"' '/"tag_name": *"cli-v/ { print $4; exit }')"
  if [ -z "$version" ]; then
    echo "Could not find a Layerbrain CLI release." >&2
    exit 1
  fi
elif expr "$version" : '[0-9][0-9.]*$' >/dev/null; then
  version="cli-v$version"
elif expr "$version" : 'v[0-9][0-9.]*$' >/dev/null; then
  version="cli-$version"
fi

url="$download_base/$version/layerbrain-$platform-$machine.tar.gz"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT INT TERM

mkdir -p "$install_dir"
download_file "$url" "$tmp_dir/layerbrain.tar.gz"

tar -xzf "$tmp_dir/layerbrain.tar.gz" -C "$tmp_dir"
install "$tmp_dir/layerbrain" "$install_dir/layerbrain"

echo "Installed layerbrain to $install_dir/layerbrain"
case ":$PATH:" in
  *":$install_dir:"*) ;;
  *) echo "Add $install_dir to PATH to run layerbrain from any shell." ;;
esac

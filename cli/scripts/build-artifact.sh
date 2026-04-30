#!/usr/bin/env sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cli_dir="$(CDPATH= cd -- "$script_dir/.." && pwd)"
repo_root="$(CDPATH= cd -- "$cli_dir/.." && pwd)"
if [ -n "${PYTHON:-}" ]; then
  python="$PYTHON"
else
  python=""
  for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'; then
      python="$candidate"
      break
    fi
  done
  if [ -z "$python" ]; then
    echo "Python 3.10 or newer is required to build the CLI artifact." >&2
    exit 1
  fi
fi
out_dir="${LAYERBRAIN_ARTIFACT_DIR:-$cli_dir/dist}"

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

build_root="$(mktemp -d "${TMPDIR:-/tmp}/layerbrain-cli-build.XXXXXX")"
trap 'rm -rf "$build_root"' EXIT INT TERM

"$python" -m venv "$build_root/venv"
venv_python="$build_root/venv/bin/python"

"$venv_python" -m pip install --upgrade pip
"$venv_python" -m pip install pyinstaller
"$venv_python" -m pip install "$repo_root/layerbrain-python" "$cli_dir"

"$venv_python" -m PyInstaller \
  --clean \
  --onefile \
  --name layerbrain \
  --distpath "$build_root/dist" \
  --workpath "$build_root/work" \
  --specpath "$build_root/spec" \
  "$cli_dir/layerbrain_cli/__main__.py"

mkdir -p "$out_dir"
artifact="$out_dir/layerbrain-$platform-$machine.tar.gz"
tar -C "$build_root/dist" -czf "$artifact" layerbrain
printf '%s\n' "$artifact"

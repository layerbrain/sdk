from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]


def _python_version() -> str:
    raw = (ROOT / "layerbrain-python" / "layerbrain" / "_version.py").read_text()
    match = re.search(r'__version__\s*=\s*"([^"]+)"', raw)
    if not match:
        raise SystemExit("layerbrain-python/layerbrain/_version.py does not define __version__")
    return match.group(1)


def _toml_project(path: Path) -> dict:
    return tomllib.loads(path.read_text())["project"]


def _toml_version(path: Path) -> str:
    project = _toml_project(path)
    if "version" in project:
        return project["version"]
    if "dynamic" in project and "version" in project["dynamic"]:
        return _python_version()
    raise SystemExit(f"{path.relative_to(ROOT)} has no project.version")


def _node_version(path: Path) -> str:
    return json.loads(path.read_text())["version"]


def _node_runtime_version() -> str:
    raw = (ROOT / "layerbrain-node" / "src" / "version.ts").read_text()
    match = re.search(r"VERSION\s*=\s*'([^']+)'", raw)
    if not match:
        raise SystemExit("layerbrain-node/src/version.ts does not define VERSION")
    return match.group(1)


def _package_versions() -> dict[str, str]:
    return {
        "python": _python_version(),
        "node": _node_version(ROOT / "layerbrain-node" / "package.json"),
    }


def _openapi_matches() -> bool:
    source = ROOT / "openapi" / "openapi.json"
    bundled = ROOT / "layerbrain-python" / "layerbrain" / "sdk" / "openapi" / "openapi.json"
    return source.read_bytes() == bundled.read_bytes()


def _check_package_metadata() -> int:
    python_version = _python_version()
    package_versions = _package_versions()
    expected = {
        "layerbrain-python/pyproject.toml": _toml_version(
            ROOT / "layerbrain-python" / "pyproject.toml"
        ),
        "layerbrain-node/package-lock.json": json.loads(
            (ROOT / "layerbrain-node" / "package-lock.json").read_text()
        )["packages"][""]["version"],
        "layerbrain-node/src/version.ts": _node_runtime_version(),
    }
    actual = {
        "layerbrain-python/pyproject.toml": python_version,
        "layerbrain-node/package-lock.json": package_versions["node"],
        "layerbrain-node/src/version.ts": package_versions["node"],
    }
    mismatches = {
        name: version for name, version in expected.items() if version != actual[name]
    }
    if mismatches:
        print("package metadata version mismatch", file=sys.stderr)
        for name, version in mismatches.items():
            print(f"  {name}={version}, expected {actual[name]}", file=sys.stderr)
        return 1
    if not _openapi_matches():
        print(
            "openapi mismatch: openapi/openapi.json does not match "
            "layerbrain-python/layerbrain/sdk/openapi/openapi.json",
            file=sys.stderr,
        )
        return 1
    print(
        " ".join(
            f"{package}={version}" for package, version in sorted(package_versions.items())
        )
    )
    return 0


def _check_release_tag(tag: str) -> int:
    package_versions = _package_versions()
    release_prefixes = {
        "python-v": "python",
        "node-v": "node",
    }
    for prefix, package in release_prefixes.items():
        if tag.startswith(prefix):
            tag_version = tag[len(prefix) :]
            package_version = package_versions[package]
            if tag_version != package_version:
                print(
                    f"{package} release tag {tag} does not match package version "
                    f"{package_version}",
                    file=sys.stderr,
                )
                return 1
            print(f"{package}={package_version}")
            return 0
    print(
        "release tag must start with python-v or node-v",
        file=sys.stderr,
    )
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-tag", help="Validate a package-specific release tag")
    args = parser.parse_args()
    result = _check_package_metadata()
    if result:
        return result
    if args.release_tag:
        return _check_release_tag(args.release_tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

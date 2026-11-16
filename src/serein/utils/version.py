import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

from serein.utils.paths import config_dir

PKGS = ("serein-shell", "quickshell")
INDENT = "    "


def _header(text: str, suffix: str = "") -> None:
    suffix = f" {suffix}" if suffix else ""
    if sys.stdout.isatty():
        print(f"\033[1;36m{text}\033[0m{suffix}")
    else:
        print(f"{text}{suffix}")


def _rows(pairs: list[tuple[str, str]], align: bool = False) -> None:
    dim = sys.stdout.isatty()
    width = max((len(key) for key, _ in pairs), default=0) if align else 0
    for key, value in pairs:
        if dim:
            value = f"\033[2m{value}\033[0m"
        label = key.ljust(width) if align else f"{key}:"
        print(f"{INDENT}{label}  {value}" if align else f"{INDENT}{label} {value}")


def _commit(commit: str, message: str) -> str:
    sha = commit[:7]
    subject = message.splitlines()[0] if message else ""
    return f"{sha} ({subject})" if subject else sha


def _commit_from_meta(meta: tuple[str, str] | None) -> str:
    if meta:
        commit, message = meta
        return _commit(commit, message)
    return "unknown"


def fetch_git_metadata(repo_dir: Path, branch: str = "upstream/main") -> tuple[str, str] | None:
    try:
        output = subprocess.check_output(
            ["git", "-C", repo_dir, "show", "-s", "--format=%H%x00%s", branch],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    commit, separator, message = output.rstrip("\n").partition("\0")
    return (commit, message) if separator else None


def cli_version() -> str:
    """Version of this CLI (serein-cli), whether installed or run from a checkout."""
    try:
        return metadata.version("serein-cli")
    except metadata.PackageNotFoundError:
        pass
    try:
        out = subprocess.check_output(
            ["git", "-C", str(Path(__file__).resolve().parent), "describe", "--always", "--dirty"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip() or "dev"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "dev"


def pacman_query(package: str) -> tuple[str, str] | None:
    """Installed (name, version) of `package` (resolving provides), or None."""

    result = subprocess.run(["pacman", "-Q", package], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    parts = result.stdout.split()
    return (parts[0], parts[1]) if result.returncode == 0 and len(parts) >= 2 else None


def print_packages() -> None:
    own = ("serein-cli", cli_version())

    if not shutil.which("pacman"):
        _header("Packages:", "not on Arch")
        _rows([own], align=True)
        return

    _header("Packages:")
    installed = [(pkg, pacman_query(pkg)) for pkg in PKGS]
    missing = [(pkg, "not installed") for pkg, result in installed if result is None]
    present = [result for _, result in installed if result is not None]
    _rows([own] + missing + present, align=True)


def print_version() -> None:
    print_packages()

    print()
    try:
        helper = next(
            (str(p) for p in (Path("/usr/lib/serein/version"), Path.home() / ".local/lib/serein/version") if p.exists()),
            "/usr/lib/serein/version",
        )
        shell_ver = subprocess.check_output([helper, "-s"], text=True).strip()
        _header("Shell:")
        print(f"{INDENT}{shell_ver}")
    except FileNotFoundError:
        _header("Shell:", "version helper not available")

    print()
    if shutil.which("qs"):
        qs_ver = subprocess.check_output(["qs", "--version"], text=True).strip()
        _header("Quickshell:")
        print(f"{INDENT}{qs_ver}")
    else:
        _header("Quickshell:", "not in PATH")

    local_shell_dir = config_dir / "quickshell/serein"
    if local_shell_dir.exists():
        print()
        _header("Local copy of shell found:", "(takes precedence over the packaged one)")
        _rows([("Last local commit", _commit_from_meta(fetch_git_metadata(local_shell_dir, "HEAD")))])

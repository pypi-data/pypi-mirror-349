import subprocess
import sys
import tomllib
from pathlib import Path

ROOT_DIR = Path("packages")  # Default root directory


def main():
    root_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT_DIR

    for entry in root_dir.iterdir():
        if not entry.is_dir():
            continue

        pyproject_path = entry / "pyproject.toml"
        if not pyproject_path.is_file():
            continue

        print(f"\n🔍 Checking project: {entry.name}")

        try:
            with pyproject_path.open("rb") as f:
                config = tomllib.load(f)
                build_backend = config.get("build-system", {}).get("build-backend", "")
        except Exception as e:
            print(f"⚠️ Failed to parse pyproject.toml in {entry.name}: {e}")
            continue

        print(f"📦 Build backend: {build_backend}")

        if build_backend == "maturin":
            # The following line was present in the original code but is not valid Python.
            # It appears to be a comment or a command meant for manual execution for a specific package.
            # uvx --directory .\packages\fabricatio-core\ maturin publish --skip-existing
            command = ["uvx", "--directory", entry.as_posix(), "maturin", "publish", "--skip-existing"]
        else:
            command = ["uv", "publish", str(entry)]  # Assuming uv publish expects the path to the package dir

        print(f"🚀 Running command: {' '.join(command)}")

        try:
            subprocess.run(command, check=True, cwd=entry if build_backend != "maturin" else None)
        except subprocess.CalledProcessError as e:
            print(f"❌ Publishing failed for {entry.name}: {e}")
        except FileNotFoundError:
            print(f"❌ Command 'uv' not found. Make sure it's installed and in your PATH.")


if __name__ == "__main__":
    main()

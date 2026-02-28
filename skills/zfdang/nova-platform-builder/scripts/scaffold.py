#!/usr/bin/env python3
"""
scaffold.py — Create a Nova app project from the bundled template.

Usage:
    python3 scripts/scaffold.py --name my-app --desc "My secure app" --port 8000 --out ./projects

Output:
    ./projects/my-app/
    ├── Dockerfile
    └── enclave/
        ├── main.py
        ├── odyn.py
        └── requirements.txt
"""

import argparse
import os
import shutil
import sys
import textwrap
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "app-template"


def scaffold(name: str, desc: str, port: int, out: Path) -> Path:
    dest = out / name
    if dest.exists():
        print(f"[warn] Directory already exists: {dest} — files will be overwritten")

    # Copy template tree
    shutil.copytree(str(TEMPLATE_DIR), str(dest), dirs_exist_ok=True)

    # Patch main.py: replace placeholder tokens
    main_py = dest / "enclave" / "main.py"
    text = main_py.read_text()
    text = text.replace("{{APP_NAME}}", name)
    text = text.replace("{{APP_DESC}}", desc)
    text = text.replace("{{APP_PORT}}", str(port))
    main_py.write_text(text)

    # Patch Dockerfile port
    dockerfile = dest / "Dockerfile"
    df_text = dockerfile.read_text()
    df_text = df_text.replace("{{APP_PORT}}", str(port))
    dockerfile.write_text(df_text)

    # Print file tree
    print(f"\n[OK] Scaffolded Nova app → {dest}\n")
    for f in sorted(dest.rglob("*")):
        if f.is_file():
            rel = f.relative_to(dest)
            print(f"  {rel}")

    print(textwrap.dedent(f"""
    Next steps:
      1. Edit  {dest}/enclave/main.py   ← implement your app logic here
      2. Edit  {dest}/enclave/requirements.txt  ← add pip packages
      3. Test locally:
           cd {dest}/enclave
           IN_ENCLAVE=false uvicorn main:app --host 0.0.0.0 --port {port} --reload
      4. When ready:
           python3 scripts/build_push.py --name {name} --registry <docker.io/username>
    """))

    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a Nova app project")
    parser.add_argument("--name", required=True, help="App name (kebab-case, e.g. my-oracle)")
    parser.add_argument("--desc", default="A Nova Platform app", help="One-line description")
    parser.add_argument("--port", type=int, default=8000, help="App listening port (default: 8000)")
    parser.add_argument("--out", default=".", help="Output directory (default: current dir)")
    args = parser.parse_args()

    name = args.name.lower().replace(" ", "-")
    out_path = Path(args.out).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    if not TEMPLATE_DIR.exists():
        print(f"[error] Template not found at {TEMPLATE_DIR}", file=sys.stderr)
        sys.exit(1)

    scaffold(name, args.desc, args.port, out_path)


if __name__ == "__main__":
    main()

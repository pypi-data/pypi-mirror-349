import os
import subprocess
from pathlib import Path
import shutil


def main():
    thedir = Path("~/teststuff/").expanduser()
    cwd = Path.cwd()
    os.chdir(thedir)
    gh_path = shutil.which("gh")
    cmd = ["gh", "repo", "clone", "https://github.com/bsc-tace/tace-bpa"]
    response = subprocess.run(cmd, check=True)
    os.chdir(cwd)
    print(response.stdout)

if __name__ == "__main__":
    main()

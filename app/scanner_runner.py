"""
Runs the integrated scanner from the dashboard.
"""

import subprocess
import sys


def run_scanner():

    subprocess.run(
        [sys.executable, "-m", "app.integrated_scanner"]
    )


if __name__ == "__main__":
    run_scanner()

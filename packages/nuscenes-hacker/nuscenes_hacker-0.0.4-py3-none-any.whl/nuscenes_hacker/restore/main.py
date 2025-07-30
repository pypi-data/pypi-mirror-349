import shutil
import subprocess
import sys


def add_arguments(parser):
    parser.set_defaults(func=run)


def run(args, unknown_args):
    # use pip or pip3 reinstall nuscenes-devkit

    pip_path = shutil.which("pip")
    pip3_path = shutil.which("pip3")

    if pip_path is not None:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--force-reinstall",
                "nuscenes-devkit",
            ]
        )
    elif pip3_path is not None:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip3",
                "install",
                "--force-reinstall",
                "nuscenes-devkit",
            ]
        )
    else:
        print("pip3 not exists")
        return

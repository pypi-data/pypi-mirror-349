"""TrainLoop Evaluations CLI default command (studio viewer)."""

import os
import subprocess
import sys
from pathlib import Path
import signal

from .utils import load_config_for_cli, find_root, resolve_data_folder_path


def studio_command():
    """Launch local viewer (studio) for inspecting events and results."""
    print("Launching TrainLoop Evaluations Studio...")

    # Find the root directory containing trainloop.config.yaml
    # Try when the trainloop directory is in the current directory
    root_path = Path.cwd() / "trainloop"
    if not root_path.exists():
        # Try when the trainloop directory is in the parent directory
        root_path = find_root()
        if not root_path.exists():
            print(
                "Error: Could not find a trainloop folder in current directory or any parent directory."
            )
            sys.exit(1)

    # Load configuration to ensure TRAINLOOP_DATA_FOLDER is set
    load_config_for_cli(root_path)

    # Get the path to the UI directory
    # First check if UI is in the package (installed mode)
    current_file = Path(__file__)
    package_ui_dir = current_file.parent.parent / "ui"

    # If not found in package, try development mode path
    if package_ui_dir.exists():
        ui_dir = package_ui_dir
    else:
        # Development mode - look in parent directories
        cli_dir = current_file.parent.parent.parent.parent
        ui_dir = cli_dir / "ui"

    if not ui_dir.exists():
        print(f"Error: UI directory not found at {ui_dir}")
        sys.exit(1)

    # Check if the UI has a build directory
    build_exists = (ui_dir / ".next").exists()
    if not build_exists:
        print("UI build not found. The UI must be pre-built for the CLI package.")
        print(
            "If you're developing locally, run 'npm run build' in the UI directory first."
        )
        sys.exit(1)

    # Set up environment variables for the Next.js app
    env = os.environ.copy()
    # Set port for Next.js
    env["PORT"] = "8888"

    # Check if npm is available
    try:
        subprocess.run(
            ["npm", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: npm not found. Please install Node.js and npm to run the studio.")
        print("Visit https://nodejs.org/ for installation instructions.")
        sys.exit(1)

    # Resolve data folder path
    trainloop_data_folder = resolve_data_folder_path(
        os.environ.get("TRAINLOOP_DATA_FOLDER", ""), root_path / "trainloop.config.yaml"
    )

    env["TRAINLOOP_DATA_FOLDER"] = trainloop_data_folder

    # Launch the Next.js application in production mode
    try:
        print(f"Starting studio viewer on http://localhost:{env['PORT']}")
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=str(ui_dir),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,  # Line buffered
        )

        # Set up signal handler to gracefully exit
        def handle_exit(sig, frame):
            print("\nShutting down TrainLoop Evaluations Studio...")
            process.terminate()
            process.wait(timeout=5)
            sys.exit(0)

        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)

        # Print the output from the Next.js process
        for line in process.stdout:
            print(line, end="")

        # Wait for the process to complete
        process.wait()

    except KeyboardInterrupt:
        print("\nShutting down TrainLoop Evaluations Studio...")
        process.terminate()
        process.wait(timeout=5)
    except Exception as e:
        print(f"Error launching TrainLoop Evaluations Studio: {e}")
        sys.exit(1)

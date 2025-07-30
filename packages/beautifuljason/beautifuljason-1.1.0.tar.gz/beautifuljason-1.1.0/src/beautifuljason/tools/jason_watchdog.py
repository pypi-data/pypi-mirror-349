##
##-----------------------------------------------------------------------------
##
## Copyright (c) 2025 JEOL Ltd.
## 1-2 Musashino 3-Chome
## Akishima Tokyo 196-8558 Japan
##
## This software is provided under the MIT License. For full license information,
## see the LICENSE file in the project root or visit https://opensource.org/licenses/MIT
##
##++---------------------------------------------------------------------------
##
## ModuleName : JASON
## ModuleType : Listener to monitor a directory and send new files to JASON
## Purpose : Automate processing, analysis, and report generation with JASON
## Author : Iain Day
## Language : Python
##
####---------------------------------------------------------------------------
##

import os
import logging
import threading
import time
import beautifuljason as bjason
import importlib
import importlib.util

from argparse import ArgumentParser
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("The 'watchdog' package is not installed. Please install it using 'pip install watchdog' and try again.")
    exit(1)

class JASONEventHandler(FileSystemEventHandler):
    """Handles file system events for the JASON watchdog."""

    def __init__(self, outdir, file_extensions, rules, formats, shutdown_flag, metadata_handler=None):
        super().__init__()
        self.outdir = outdir
        self.file_extensions = file_extensions
        self.rules = rules
        self.formats = formats
        self.shutdown_flag = shutdown_flag
        self.metadata_handler = metadata_handler  # Custom handler for metadata
        self.jason = bjason.JASON()

    def on_created(self, event):
        """Called when a file is created in the monitored directory."""
        if any(event.src_path.endswith(ext) for ext in self.file_extensions):
            self.run_jason(event)

    def generate_unique_path(self, basepath, extension):
        """Generate a unique file path by appending a numeric suffix if the file exists."""
        counter = 1
        unique_path = f"{basepath}.{extension}"
        while os.path.exists(unique_path):
            unique_path = f"{basepath}({counter}).{extension}"
            counter += 1
        return unique_path

    def run_jason(self, event):
        """Process the created file with JASON."""
        basename = os.path.basename(event.src_path)
        basepath = os.path.join(self.outdir, os.path.splitext(basename)[0])
        try:
            with self.jason.create_document(event.src_path, rules=self.rules) as doc:
                output_paths = [
                    self.generate_unique_path(basepath, fmt) for fmt in self.formats
                ]
                # Call the metadata handler if provided
                if self.metadata_handler:
                    self.metadata_handler.process(doc, event.src_path, output_paths)
                self.jason.save(doc, output_paths)
                logging.info(f"File processed: {basename}")
        except Exception as e:
            logging.error(f"Fatal error processing file {basename}: {e}", exc_info=True)
            self.shutdown_flag.set()  # Set the shutdown flag to stop the observer

def load_metadata_handler(handler_path):
    """
    Dynamically load a metadata handler module from the specified file path.
    """
    if not handler_path:
        return None

    # Ensure the file exists
    if not os.path.isfile(handler_path):
        raise FileNotFoundError(f"Metadata handler file not found: {handler_path}")

    # Load the module from the file path
    module_name = os.path.splitext(os.path.basename(handler_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, handler_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Check if the module has the required methods: initialize, process, and finalize
    required_methods = ['initialize', 'process', 'finalize']
    for method in required_methods:
        if not hasattr(module, method):
            raise AttributeError(f"Metadata handler module must have a '{method}' method.")

    return module

def get_cmdline_arguments():
    """Parse command line arguments."""
    parser = ArgumentParser()

    parser.add_argument("indir", help="Directory to monitor")
    parser.add_argument("outdir", help="Directory to store output files")
    parser.add_argument('-r', '--rules',
                        default='off',
                        help="Rules file to use, defaults to 'off' (no rules)")
    parser.add_argument('-f', '--formats',
                        default=['pdf', 'jjh5'],
                        nargs='+',
                        choices=['pdf', 'jjh5'],
                        help="Output formats: pdf, jjh5, or both (default: both)")
    parser.add_argument('-e', '--extensions', default=['jdf'],
                        nargs='+',
                        help="File extensions to monitor (default: jdf)")
    parser.add_argument('--metadata-handler', default=None,
                        help="Path to a custom metadata handler module (e.g., /path/to/dbwriter.py)")

    return parser.parse_args()

def main():
    """Main entry point for the jason_watchdog tool."""
    args = get_cmdline_arguments()
    args.indir = os.path.abspath(args.indir)
    args.outdir = os.path.abspath(args.outdir)
    # For convenience, ensure extensions start with a dot
    args.extensions = [ext if ext.startswith('.') else '.' + ext for ext in args.extensions]

    # Load the metadata handler module if specified
    metadata_handler = None
    if args.metadata_handler:
        metadata_handler = load_metadata_handler(args.metadata_handler)

    # Configure logging
    timenow = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = os.path.join(args.outdir, 'logs', timenow + '.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,  # Show INFO messages by default
        format="%(asctime)s:%(levelname)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, mode='w'),  # Save logs to file
            logging.StreamHandler()  # Print logs to console
        ]
    )

    # Initialize the metadata handler if provided
    if metadata_handler:
        metadata_handler.initialize(args.outdir, logging)

    shutdown_flag = threading.Event()
    event_handler = JASONEventHandler(
        args.outdir, args.extensions, args.rules, args.formats, shutdown_flag, metadata_handler=metadata_handler
    )

    observer = Observer()
    observer.schedule(event_handler, args.indir, recursive=True)
    observer.start()
    logging.info(f"Observer for '{args.indir}' folder has started.")
    logging.info(f"Monitoring file extensions: {', '.join(args.extensions)}")
    logging.info(f"Output files will be saved to '{args.outdir}' folder.")
    logging.info(f"Using output formats: '{', '.join(args.formats)}'")
    logging.info(f"Logging to file: '{log_file}'")
    logging.info(f"The rules is set to: '{args.rules}'")
    if metadata_handler:
        logging.info(f"Using custom metadata handler: '{args.metadata_handler}'")
    logging.info("Press Ctrl+C to stop cleanly.")

    try:
        while not shutdown_flag.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopped by user (Ctrl+C).")
    except Exception as e:
        logging.error("Unexpected error occurred:", exc_info=True)
    finally:
        observer.stop()
        observer.join()
        # Finalize the metadata handler if provided
        if metadata_handler:
            metadata_handler.finalize()

if __name__ == "__main__":
    main()
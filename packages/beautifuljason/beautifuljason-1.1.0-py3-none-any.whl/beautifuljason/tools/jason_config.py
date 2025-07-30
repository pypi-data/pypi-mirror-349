##
##-----------------------------------------------------------------------------
##
## Copyright (c) 2023 JEOL Ltd.
## 1-2 Musashino 3-Chome
## Akishima Tokyo 196-8558 Japan
##
## This software is provided under the MIT License. For full license information,
## see the LICENSE file in the project root or visit https://opensource.org/licenses/MIT
##
##++---------------------------------------------------------------------------
##
## ModuleName : BeautifulJASON
## ModuleType : Python API for JASON desktop application and JJH5 documents
## Purpose : Automate processing, analysis, and report generation with JASON
## Author : Nikolay Larin
## Language : Python
##
####---------------------------------------------------------------------------
##

import argparse
import os
from beautifuljason.jason import config, JASON
from colorama import Fore, init

def display_config():
    """Display the JASON application."""

    def path_status(path):
        if os.path.exists(path):
            return f"{Fore.GREEN}OK"
        else:
            return f"{Fore.RED}NOT FOUND"

    print("JASON Configuration")
    print(f"├─Work Path: {config.work_path}")
    print(f"├─Temp Path: {config.temp_path}")
    print(f"└─JASON Paths")
    print(f"  ├─Operational: ", end="") 
    if config.app_path is None:
        print(f"{Fore.RED}NOT FOUND")
    else:
        print(config.app_path)

    preferred_path_index = config.preferred_path_index
    print("  └─ All Known Paths")
    all_paths = config.all_paths
    for i, index_path in enumerate(all_paths):
        index, path = index_path
        symbol = "└─" if i == len(all_paths)-1 else "├─"
        preferred_symbol = f"{Fore.CYAN}*{Fore.RESET}" if index == preferred_path_index else " "
        print(f"     {symbol}[{index}]{preferred_symbol}{path} - {path_status(path)}")

    # Check for the current JASON path validity
    if not config.app_path:
        print()
        print(f"{Fore.RED}ERROR: JASON application is not detected at any known location.")
        print("Suggestions:")
        print("- Install JASON from https://www.jeoljason.com/, in which case the path will be found automatically.")
        print("- Add a path to an existing JASON installation with the --add_path option.")

def add_path_to_config(new_path):
    """Add a new path for the JASON application."""

    # Check if the path exists
    if not os.path.exists(new_path):
        print(f"{Fore.RED}ERROR: The provided path does not exist.")
        return
    
    # Check if the path is already in the configuration
    path_index = config.find_path(new_path)
    if path_index is not None:
        print(f"{Fore.YELLOW}WARNING: The specified path already exists in the configuration at index [{path_index}].")
        return

    try:
        # Check if the path is a valid JASON application
        print(f"Checking if {new_path} is a valid JASON application...", end="")
        jason = JASON(new_path)
        print(f"{Fore.GREEN}OK: JASON v.{'.'.join(map(str, jason.version))} found.")
        index = config.add_path(new_path)
        print(f"Path added as [{index}]: {new_path}")
        confirmation = input("Do you want to set this path as the preferred JASON path? (y/n): ").strip().lower()
        if confirmation == 'y':
            config.set_preferred_path_index(index)
            print(f"Preferred JASON path set to [{index}]: {new_path}")
    except Exception as e:
        # If the path is not a valid JASON application, print the error
        print(f"{Fore.RED}ERROR: {e}")

def set_preferred_by_index(index):
    """Set the preferred JASON path by index."""
    try:
        config.set_preferred_path_index(index)
        print(f"Preferred JASON path set to [{index}]")
    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}")

def reset_config():
    """Reset the JASON application path configuration to defaults."""
    confirmation = input("This operation will reset the JASON configuration to default settings. Are you sure? (y/n): ").strip().lower()
    if confirmation == 'y':
        config.reset()
        print("Configuration reset to default settings.")
    else:
        print("Reset operation cancelled.")

def delete_path_by_index(index):
    """Delete a JASON path by its index."""
    try:
        config.delete_path_by_index(index)
        print(f"Path [{index}] deleted.")
    except Exception as e:
        print(f"{Fore.RED}ERROR: {e}")

def main():
    init(autoreset=True)  # Initialize colorama

    parser = argparse.ArgumentParser(description="Manage BeautifulJASON's JASON application configuration.")
    
    parser.add_argument("--display", action="store_true", help="Display the JASON configuration.")
    parser.add_argument("--add_path", type=str, help="Add a new path for the JASON application.")
    parser.add_argument('--del_path', type=int, help="Delete a JASON path by its index")
    parser.add_argument("--set_preferred", type=int, help="Set the preferred JASON path by index. You may need to add the path first with --add_path. Use --display to see all paths and their indexes.")
    parser.add_argument("--reset", action="store_true", help="Reset the JASON configuration to default settings.")
    
    args = parser.parse_args()

    if args.display:
        display_config()
    elif args.add_path:
        add_path_to_config(args.add_path)
    elif args.reset:
        reset_config()
    elif args.set_preferred:
        set_preferred_by_index(args.set_preferred)
    elif args.del_path:
        delete_path_by_index(args.del_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

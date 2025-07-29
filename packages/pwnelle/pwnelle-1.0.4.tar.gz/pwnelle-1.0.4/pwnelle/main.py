#!/usr/bin/env python3
"""
Main entry point for pwnelle.
"""
import sys

def main():
    """Entry point for the application."""
    try:
        from .cli import main as cli_main
        return cli_main()
    except ImportError as e:
        print(f"Error importing pwnelle modules: {e}")
        print("Please make sure pwnelle is installed correctly.")
        print("You need to install the following dependencies:")
        print("  pip install pwntools python-Levenshtein capstone pyelftools")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
#!/usr/bin/env python3
"""
CLI interface for pwnelle.
"""

import argparse
import os
import sys
from pathlib import Path
from .analyzer import BinaryAnalyzer
from .exploiter import ExploitGenerator
from . import __version__


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="pwnelle - Advanced Binary-Exploitation Assistant",
        usage="pwnelle <binary> [options]"
    )

    parser.add_argument(
        "binary", 
        help="Path to the ELF binary to analyze"
    )
    
    parser.add_argument(
        "-o", "--output", 
        default=None,
        help="Output directory (default: pwnelle-out/<binary_name>)"
    )
    
    parser.add_argument(
        "--depth", 
        type=int, 
        default=2,
        help="Nested decode depth for smart strings (default: 2)"
    )
    
    parser.add_argument(
        "--stride", 
        type=int, 
        default=3,
        help="Levenshtein distance for gadget clustering (default: 3)"
    )
    
    parser.add_argument(
        "--budget", 
        type=int, 
        default=100000,
        help="Cap total strings kept (default: 100000)"
    )
    
    parser.add_argument(
        "--min", 
        type=int, 
        default=4,
        help="Min printable-string length to keep (default: 4)"
    )
    
    parser.add_argument(
        "--max", 
        type=int, 
        default=256,
        help="Max printable-string length to keep (default: 256)"
    )
    
    parser.add_argument(
        "--no-objdump", 
        action="store_true",
        help="Skip objdump -s extraction (speed)"
    )
    
    parser.add_argument(
        "--no-gadgets", 
        action="store_true",
        help="Skip ROPgadget run"
    )
    
    parser.add_argument(
        "--no-strings", 
        action="store_true",
        help="Skip smart-strings scan"
    )
    
    parser.add_argument(
        "--json-only", 
        action="store_true",
        help="Generate analysis.json only, no md/html/template"
    )
    
    parser.add_argument(
        "--extra", 
        help="Comma-list: ropper, one_gadget, checksec"
    )

    # Exploit generation options
    exploit_group = parser.add_argument_group('Exploit Generation')
    
    exploit_group.add_argument(
        "--auto-exploit",
        action="store_true",
        help="[DEPRECATED] Generate exploit template only (auto-exploitation removed)"
    )
    
    exploit_group.add_argument(
        "--bof-only",
        action="store_true",
        help="[DEPRECATED] Generate buffer overflow template only (auto-exploitation removed)"
    )
    
    exploit_group.add_argument(
        "--max-length",
        type=int,
        default=2000,
        help="Maximum suggested payload length for template (default: 2000)"
    )
    
    exploit_group.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Suggested timeout for exploit testing in seconds (default: 10)"
    )
    
    exploit_group.add_argument(
        "--flag-regex",
        default=r"(flag\{[^}]*\}|CTF\{[^}]*\})",
        help="Regex pattern to identify flags in template (default: flag{...} or CTF{...})"
    )
    
    # Remote exploitation options
    remote_group = parser.add_argument_group('Remote Exploitation')
    
    remote_group.add_argument(
        "--remote",
        help="[DEPRECATED] Generate template for remote server (format: HOST:PORT)"
    )
    
    remote_group.add_argument(
        "--remote-protocol",
        choices=["tcp", "udp"],
        default="tcp",
        help="Protocol to use for remote connection (default: tcp)"
    )
    
    remote_group.add_argument(
        "--remote-delay",
        type=float,
        default=0.5,
        help="Delay before sending payloads to remote server in seconds (default: 0.5)"
    )
    
    remote_group.add_argument(
        "--remote-retries",
        type=int,
        default=3,
        help="Number of connection retries for remote server (default: 3)"
    )
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Show progress bars, extra diagnostics"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"pwnelle v{__version__}"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the CLI."""
    try:
        args = parse_args()
        
        # Create output directory if not specified
        if not args.output:
            binary_name = os.path.basename(args.binary)
            output_dir = os.path.join("pwnelle-out", binary_name)
        else:
            output_dir = args.output
        
        # Create the output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Parse remote connection options
        remote_options = None
        if args.remote:
            try:
                host, port = args.remote.split(":")
                remote_options = {
                    "host": host,
                    "port": int(port),
                    "protocol": "tcp",  # Default to TCP
                    "delay": 1.0,       # Default delay
                    "retries": 3        # Default retries
                }
                print(f"Remote mode: Will connect to {host}:{port}")
                print("NOTE: CTF servers may have rate limiting or specific requirements.")
                print("      It's recommended to analyze the binary locally first before using remote mode.")
                print("      Remote exploitation may require multiple attempts or manual adjustments.")
            except ValueError:
                print("Error: Invalid remote format. Please use 'host:port'")
                return 1
        
        print(f"Analyzing {os.path.basename(args.binary)}...")
        
        # Analyze the binary
        analyzer = BinaryAnalyzer(
            binary_path=args.binary,
            output_dir=output_dir,
            depth=args.depth,
            stride=args.stride,
            budget=args.budget,
            min_string_len=args.min,
            max_string_len=args.max,
            skip_objdump=args.no_objdump,
            skip_gadgets=args.no_gadgets,
            skip_strings=args.no_strings,
            json_only=args.json_only,
            verbose=args.verbose
        )
        
        analysis_results = analyzer.analyze()
        
        # Auto-exploit if requested
        if args.auto_exploit:
            print(f"Auto-exploitation removed - generating template only for {os.path.basename(args.binary)}...")
            
            # Note: ExploitGenerator is kept only to generate templates, not for exploitation
            exploiter = ExploitGenerator(
                binary_path=args.binary,
                analysis_results=analysis_results,
                output_dir=output_dir,
                verbose=args.verbose,
                timeout=args.timeout,
                flag_regex=args.flag_regex,
                remote_options=remote_options
            )
            
            # Only generate the template, no exploitation
            template_path = os.path.join(output_dir, "exploit_template.py")
            print(f"Template generated at: {template_path}")
            print("\nPwnelle no longer performs auto-exploitation.")
            print("Use the template and your knowledge to exploit the binary manually.")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        if args and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    main() 
"""
ROP gadget finder module for pwnelle.
"""

import subprocess
import tempfile
import os
import re
import json
from typing import Dict, List, Any, Tuple, Optional, Set


class ROPGadgetFinder:
    """Find and categorize ROP gadgets in binaries."""
    
    # Key ROP gadgets to look for
    TARGET_GADGETS = {
        # x86_64 gadgets
        "pop_rdi": r"pop rdi\s*;\s*ret",
        "pop_rsi_r15": r"pop rsi\s*;\s*pop r15\s*;\s*ret",
        "pop_rdx": r"pop rdx\s*;\s*ret",
        "pop_rcx": r"pop rcx\s*;\s*ret",
        "pop_rax": r"pop rax\s*;\s*ret",
        "pop_rbp": r"pop rbp\s*;\s*ret",
        "syscall": r"syscall\s*;\s*ret",
        "int_0x80": r"int 0x80\s*;\s*ret",
        "leave_ret": r"leave\s*;\s*ret",
        "ret": r"ret",
        
        # x86 (32-bit) gadgets
        "pop_eax": r"pop eax\s*;\s*ret",
        "pop_ebx": r"pop ebx\s*;\s*ret",
        "pop_ecx": r"pop ecx\s*;\s*ret",
        "pop_edx": r"pop edx\s*;\s*ret",
        "pop_esi": r"pop esi\s*;\s*ret",
        "pop_edi": r"pop edi\s*;\s*ret",
        "pop_ebp": r"pop ebp\s*;\s*ret",
    }
    
    def __init__(
        self,
        binary_path: str,
        stride: int = 3,
        extra_tools: bool = False,
        verbose: bool = False
    ):
        """
        Initialize the ROP gadget finder.
        
        Args:
            binary_path: Path to the binary to analyze
            stride: Levenshtein distance for gadget clustering
            extra_tools: Whether to use additional tools like ropper
            verbose: Whether to show verbose output
        """
        self.binary_path = binary_path
        self.stride = stride
        self.extra_tools = extra_tools
        self.verbose = verbose
        
        # Results
        self.all_gadgets = []
        self.key_gadgets = {}
    
    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def find_gadgets(self) -> Dict[str, Any]:
        """Find ROP gadgets in the binary."""
        self.log(f"Finding ROP gadgets in {self.binary_path}")
        
        # Run ROPgadget
        self._run_ropgadget()
        
        # Run ropper if enabled
        if self.extra_tools:
            self._run_ropper()
        
        # Extract key gadgets
        self._extract_key_gadgets()
        
        return {
            "key_gadgets": self.key_gadgets,
            "gadget_count": len(self.all_gadgets),
        }
    
    def _run_ropgadget(self) -> None:
        """Run ROPgadget on the binary."""
        self.log("Running ROPgadget...")
        
        try:
            # Check if ROPgadget is installed as a Python module
            from ROPgadget.ROPgadget import main as ropgadget_main
            
            # Create a temporary file to capture output
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
                tmp_filename = tmp.name
            
            # Redirect stdout to our temp file
            import sys
            original_stdout = sys.stdout
            sys.stdout = open(tmp_filename, 'w')
            
            # Run ROPgadget
            try:
                ropgadget_main(['--binary', self.binary_path, '--all'])
            except SystemExit:
                pass  # ROPgadget calls sys.exit()
            
            # Restore stdout
            sys.stdout.close()
            sys.stdout = original_stdout
            
            # Read results
            with open(tmp_filename, 'r') as f:
                output = f.read()
            
            # Clean up
            os.unlink(tmp_filename)
            
        except ImportError:
            # Fall back to command-line
            self.log("ROPgadget Python module not found, trying command line")
            try:
                output = subprocess.check_output(
                    ['ROPgadget', '--binary', self.binary_path, '--all'],
                    universal_newlines=True
                )
            except subprocess.CalledProcessError as e:
                self.log(f"Error running ROPgadget: {e}")
                return
            except FileNotFoundError:
                self.log("ROPgadget executable not found")
                return
        
        # Parse output
        self._parse_ropgadget_output(output)
    
    def _parse_ropgadget_output(self, output: str) -> None:
        """Parse ROPgadget output and extract gadgets."""
        # ROPgadget format: 0x0000000000401016 : pop rdi ; ret
        gadget_pattern = re.compile(r'(0x[0-9a-f]+)\s+:\s+(.*)')
        
        for line in output.splitlines():
            match = gadget_pattern.search(line)
            if match:
                address = int(match.group(1), 16)
                gadget = match.group(2).strip()
                
                self.all_gadgets.append({
                    'address': address,
                    'gadget': gadget
                })
    
    def _run_ropper(self) -> None:
        """Run ropper as an additional tool."""
        self.log("Running ropper for additional gadgets...")
        
        try:
            output = subprocess.check_output(
                ['ropper', '--file', self.binary_path, '--search', "pop,leave,syscall,int"],
                universal_newlines=True
            )
            
            # Parse output - ropper format is different
            # Example: 0x00000000004011df: pop rdi; ret;
            gadget_pattern = re.compile(r'(0x[0-9a-f]+):\s+(.*)')
            
            for line in output.splitlines():
                match = gadget_pattern.search(line)
                if match:
                    address = int(match.group(1), 16)
                    gadget = match.group(2).strip()
                    
                    # Convert semicolons to the format used by ROPgadget
                    gadget = gadget.replace(';', ' ;')
                    
                    # Check if this is a new gadget
                    if not any(g['address'] == address and g['gadget'] == gadget for g in self.all_gadgets):
                        self.all_gadgets.append({
                            'address': address,
                            'gadget': gadget
                        })
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.log(f"Error running ropper: {e}")
    
    def _extract_key_gadgets(self) -> None:
        """Extract key gadgets from all found gadgets."""
        if not self.all_gadgets:
            self.log("No gadgets found")
            return
        
        # Sort by address for deterministic output
        self.all_gadgets.sort(key=lambda g: g['address'])
        
        # Match against our target patterns
        for name, pattern in self.TARGET_GADGETS.items():
            for gadget in self.all_gadgets:
                if re.search(pattern, gadget['gadget'], re.IGNORECASE):
                    # Store only the relative offset (for PIE binaries)
                    self.key_gadgets[name] = gadget['address']
                    break
        
        self.log(f"Found {len(self.key_gadgets)}/{len(self.TARGET_GADGETS)} key gadgets")
        if self.verbose:
            for name, addr in self.key_gadgets.items():
                self.log(f"  {name}: {addr:#x}") 
"""
Core binary analysis engine for pwnelle.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
import re
import shutil
from typing import Dict, List, Any, Tuple, Optional, Set

try:
    import Levenshtein
    FAST_LEVENSHTEIN = True
except ImportError:
    FAST_LEVENSHTEIN = False
    print("Warning: 'python-Levenshtein' not found – using slow fallback")

try:
    from pwn import *
    context.update(log_level='error')  # Suppress pwntools logging unless verbose
except ImportError:
    print("Error: pwntools not installed. Run: pip install pwntools", file=sys.stderr)
    sys.exit(1)

try:
    import elftools
    from elftools.elf.elffile import ELFFile
    from elftools.elf.sections import SymbolTableSection
except ImportError:
    print("Error: pyelftools not installed. Run: pip install pyelftools", file=sys.stderr)
    sys.exit(1)

try:
    from capstone import *
    from capstone.x86 import *
except ImportError:
    print("Error: capstone not installed. Run: pip install capstone", file=sys.stderr)
    sys.exit(1)

from .templates.template_generator import TemplateGenerator
from .gadgets.rop_finder import ROPGadgetFinder
from .strings.string_finder import StringFinder
from .report.report_generator import ReportGenerator


class BinaryAnalyzer:
    """Main binary analysis engine."""
    
    def __init__(
        self,
        binary_path: str,
        output_dir: str,
        depth: int = 2,
        stride: int = 3,
        budget: int = 100000,
        min_string_len: int = 4,
        max_string_len: int = 256,
        skip_objdump: bool = False,
        skip_gadgets: bool = False, 
        skip_strings: bool = False,
        json_only: bool = False,
        extra_tools: List[str] = None,
        verbose: bool = False
    ):
        """Initialize the BinaryAnalyzer.
        
        Args:
            binary_path: Path to the binary to analyze
            output_dir: Directory to write output files
            depth: Nested decode depth for smart strings
            stride: Levenshtein distance for gadget clustering
            budget: Cap total strings kept
            min_string_len: Min printable-string length to keep
            max_string_len: Max printable-string length to keep
            skip_objdump: Skip objdump -s extraction
            skip_gadgets: Skip ROPgadget run
            skip_strings: Skip smart-strings scan
            json_only: Generate analysis.json only, no md/html/template
            extra_tools: List of extra tools to run
            verbose: Show progress bars, extra diagnostics
        """
        self.binary_path = binary_path
        self.output_dir = output_dir
        self.depth = depth
        self.stride = stride
        self.budget = budget
        self.min_string_len = min_string_len
        self.max_string_len = max_string_len
        self.skip_objdump = skip_objdump
        self.skip_gadgets = skip_gadgets
        self.skip_strings = skip_strings
        self.json_only = json_only
        self.extra_tools = extra_tools or []
        self.verbose = verbose
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.elf = None
        self.analysis_results = {}
        
        # Component instances
        self.rop_finder = None
        self.string_finder = None
        self.template_generator = None
        self.report_generator = None
    
    def log(self, message: str) -> None:
        """Print log message if verbose is enabled."""
        if self.verbose:
            print(message)
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis on the binary."""
        self.log(f"Starting analysis of {self.binary_path}")
        
        # Load the binary
        try:
            self.elf = ELF(self.binary_path)
        except Exception as e:
            print(f"Error loading binary: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Gather basic information
        self.analyze_basic_info()
        
        # Analyze security features
        self.analyze_security_features()
        
        # Analyze symbols
        self.analyze_symbols()
        
        # Analyze interesting functions
        self.analyze_functions()
        
        # Extract strings if not skipped
        if not self.skip_strings:
            self.extract_strings()
        
        # Find ROP gadgets if not skipped
        if not self.skip_gadgets:
            self.find_rop_gadgets()
        
        # Predict exploit paths
        self.predict_exploit_paths()
        
        # Save analysis results
        self.save_analysis_json()
        
        # Generate report and template files if not json-only
        if not self.json_only:
            self.generate_report()
            self.generate_gadgets_file()
            self.generate_exploit_template()
        
        return self.analysis_results
    
    def analyze_basic_info(self) -> None:
        """Gather basic information about the binary."""
        self.log("Analyzing basic binary information")
        
        self.analysis_results["basic_info"] = {
            "file_name": os.path.basename(self.binary_path),
            "file_size": os.path.getsize(self.binary_path),
            "sha256": sha256sum(self.binary_path),
            "architecture": self.elf.arch,
            "bits": self.elf.bits,
            "endian": "little" if self.elf.little_endian else "big",
            "type": self.elf.elftype,
        }
    
    def analyze_security_features(self) -> None:
        """Analyze security features of the binary."""
        self.log("Analyzing security features")
        
        self.analysis_results["security"] = {
            "nx": self.elf.nx,
            "pie": self.elf.pie,
            "canary": self.has_canary(),
            "relro": self.get_relro(),
        }
    
    def has_canary(self) -> bool:
        """Check if the binary has stack canary protection."""
        # Check for __stack_chk_fail
        for section in self.elf.sections:
            if not isinstance(section, SymbolTableSection):
                continue
            
            for symbol in section.iter_symbols():
                if symbol.name == "__stack_chk_fail":
                    return True
        
        return False
    
    def get_relro(self) -> str:
        """Get RELRO status."""
        if self.elf.relro == "Full":
            return "Full"
        elif self.elf.relro == "Partial":
            return "Partial"
        else:
            return "None"
    
    def analyze_symbols(self) -> None:
        """Analyze symbols in the binary."""
        self.log("Analyzing symbols")
        
        # Extract imports
        imports = []
        try:
            # Handle different attribute names in different pwntools versions
            if hasattr(self.elf, 'relocs'):
                relocs = self.elf.relocs
            elif hasattr(self.elf, 'got'):
                # Alternative approach using GOT entries
                relocs = []
                for name, addr in self.elf.got.items():
                    relocs.append({"symbol": {"name": name}, "address": addr})
            else:
                # Fallback for other versions
                relocs = []
                for sec in self.elf.sections:
                    if sec.name.startswith('.rel') or sec.name.startswith('.rela'):
                        for sym in self.elf.get_section_objects(sec.name):
                            if hasattr(sym, 'name') and sym.name:
                                relocs.append({"symbol": {"name": sym.name}, "address": sym.entry.st_value})

            for reloc in relocs:
                if hasattr(reloc, 'symbol') and reloc.symbol and reloc.symbol.name:
                    imports.append({
                        "name": reloc.symbol.name,
                        "address": reloc.address,
                    })
                elif isinstance(reloc, dict) and "symbol" in reloc and "name" in reloc["symbol"]:
                    imports.append({
                        "name": reloc["symbol"]["name"],
                        "address": reloc["address"],
                    })
        except Exception as e:
            self.log(f"Error extracting imports: {e}")
            # Continue with empty imports list
            pass
        
        # Extract exports
        exports = []
        try:
            for symbol in self.elf.symbols:
                if symbol.name and symbol.type == "STT_FUNC" and symbol.binding == "STB_GLOBAL":
                    exports.append({
                        "name": symbol.name,
                        "address": symbol.address,
                    })
        except Exception as e:
            self.log(f"Error extracting exports: {e}")
            # Continue with empty exports list
            pass
        
        self.analysis_results["symbols"] = {
            "imports": imports,
            "exports": exports,
        }
    
    def analyze_functions(self) -> None:
        """Analyze interesting functions in the binary."""
        self.log("Analyzing interesting functions")
        
        interesting_functions = {}
        
        # Check for main function
        try:
            if hasattr(self.elf, 'functions') and "main" in self.elf.functions:
                interesting_functions["main"] = {
                    "address": self.elf.functions["main"].address,
                    "size": self.elf.functions["main"].size,
                }
            elif hasattr(self.elf, 'symbols') and "main" in self.elf.symbols:
                # Alternative way to access main if functions attribute is not available
                interesting_functions["main"] = {
                    "address": self.elf.symbols["main"],
                    "size": 0,  # We don't know the size without function information
                }
        except Exception as e:
            self.log(f"Error finding main function: {e}")
        
        # Check for potentially vulnerable functions
        vuln_patterns = ["vuln", "win", "shell", "get_flag", "print_flag"]
        try:
            if hasattr(self.elf, 'functions'):
                for func_name in self.elf.functions:
                    for pattern in vuln_patterns:
                        if pattern in func_name.lower():
                            interesting_functions[func_name] = {
                                "address": self.elf.functions[func_name].address,
                                "size": self.elf.functions[func_name].size,
                            }
                            break
            elif hasattr(self.elf, 'symbols'):
                # Alternative approach using symbols
                for func_name, addr in self.elf.symbols.items():
                    for pattern in vuln_patterns:
                        if pattern in func_name.lower():
                            interesting_functions[func_name] = {
                                "address": addr,
                                "size": 0,  # We don't know the size without function information
                            }
                            break
        except Exception as e:
            self.log(f"Error finding vulnerable functions: {e}")
        
        # Check for format string vulnerabilities in code
        format_string_funcs = ["printf", "fprintf", "sprintf", "snprintf", "vprintf", 
                              "vfprintf", "vsprintf", "vsnprintf"]
        
        format_string_vulns = []
        for func_name, func_info in interesting_functions.items():
            if func_info["size"] == 0:
                # Skip functions where we don't know the size
                continue
                
            try:
                if self.elf.pie:
                    # If PIE, we need to disassemble relative to 0
                    func_addr = func_info["address"] - self.elf.load_addr
                else:
                    func_addr = func_info["address"]
                
                # Get function bytes
                func_bytes = self.elf.read(func_addr, func_info["size"])
                
                # Disassemble
                md = Cs(CS_ARCH_X86, CS_MODE_64 if self.elf.bits == 64 else CS_MODE_32)
                md.detail = True
                
                for insn in md.disasm(func_bytes, func_addr):
                    if insn.mnemonic == "call":
                        # Check if calling a format string function
                        for fmt_func in format_string_funcs:
                            # Simple pattern matching for calls
                            # In a real implementation, this would need to be more sophisticated
                            if fmt_func in str(insn.op_str):
                                format_string_vulns.append({
                                    "function": func_name,
                                    "address": insn.address,
                                    "instruction": f"{insn.mnemonic} {insn.op_str}",
                                })
            except Exception as e:
                if self.verbose:
                    print(f"Warning: Error disassembling {func_name}: {e}")
        
        self.analysis_results["interesting_functions"] = interesting_functions
        self.analysis_results["format_string_vulns"] = format_string_vulns
    
    def extract_strings(self) -> None:
        """Extract interesting strings from the binary."""
        self.log("Extracting and analyzing strings")
        
        self.string_finder = StringFinder(
            binary_path=self.binary_path,
            depth=self.depth,
            min_len=self.min_string_len,
            max_len=self.max_string_len,
            budget=self.budget,
            skip_objdump=self.skip_objdump,
            verbose=self.verbose
        )
        
        strings_result = self.string_finder.find_strings()
        self.analysis_results["strings"] = strings_result
    
    def find_rop_gadgets(self) -> None:
        """Find ROP gadgets in the binary."""
        self.log("Finding ROP gadgets")
        
        self.rop_finder = ROPGadgetFinder(
            binary_path=self.binary_path,
            stride=self.stride,
            extra_tools="ropper" in self.extra_tools,
            verbose=self.verbose
        )
        
        gadgets_result = self.rop_finder.find_gadgets()
        self.analysis_results["rop_gadgets"] = gadgets_result
    
    def predict_exploit_paths(self) -> None:
        """Predict potential exploit paths based on analysis."""
        self.log("Predicting exploit paths")
        
        exploit_paths = []
        
        # Check for ret2win
        for func_name in self.analysis_results.get("interesting_functions", {}):
            if "win" in func_name.lower() or "shell" in func_name.lower() or "flag" in func_name.lower():
                exploit_paths.append({
                    "type": "ret2win",
                    "confidence": "high",
                    "target": func_name,
                })
        
        # Check for format string
        if self.analysis_results.get("format_string_vulns", []):
            exploit_paths.append({
                "type": "format_string",
                "confidence": "high",
                "locations": len(self.analysis_results["format_string_vulns"]),
            })
        
        # Check for ROP potential
        if self.analysis_results.get("rop_gadgets", {}).get("key_gadgets", {}):
            key_gadgets = self.analysis_results["rop_gadgets"]["key_gadgets"]
            
            # Classic ROP
            if key_gadgets.get("pop_rdi") and key_gadgets.get("syscall"):
                exploit_paths.append({
                    "type": "rop_chain",
                    "confidence": "medium",
                    "note": "syscall gadget and argument gadgets available",
                })
            
            # Stack pivot potential
            if key_gadgets.get("leave_ret"):
                exploit_paths.append({
                    "type": "stack_pivot",
                    "confidence": "medium",
                    "note": "leave; ret gadget available",
                })
        
        # Check for shellcode possibility
        if "security" in self.analysis_results and not self.analysis_results["security"]["nx"]:
            exploit_paths.append({
                "type": "shellcode",
                "confidence": "high",
                "note": "NX disabled, shellcode execution possible",
            })
        
        # Check for one_gadget if libc is available
        if "symbols" in self.analysis_results:
            libc_funcs = ["system", "__libc_start_main", "malloc", "free"]
            has_libc = any(imp["name"] in libc_funcs for imp in self.analysis_results["symbols"].get("imports", []))
            
            if has_libc:
                exploit_paths.append({
                    "type": "libc_leak",
                    "confidence": "medium",
                    "note": "Potential for libc leak and ret2libc/one_gadget",
                })
        
        self.analysis_results["exploit_paths"] = exploit_paths
    
    def save_analysis_json(self) -> None:
        """Save analysis results to JSON file."""
        json_path = os.path.join(self.output_dir, "analysis.json")
        
        with open(json_path, "w") as f:
            json.dump(self.analysis_results, f, indent=2)
        
        self.log(f"Analysis results saved to {json_path}")
    
    def generate_report(self) -> None:
        """Generate human-readable report."""
        self.log("Generating report")
        
        self.report_generator = ReportGenerator(
            analysis_results=self.analysis_results,
            binary_path=self.binary_path,
            output_dir=self.output_dir
        )
        
        self.report_generator.generate_report()
    
    def generate_gadgets_file(self) -> None:
        """Generate gadgets.py file."""
        self.log("Generating gadgets.py")
        
        if "rop_gadgets" not in self.analysis_results:
            self.log("No ROP gadgets found, skipping gadgets.py generation")
            return
        
        gadgets_py_path = os.path.join(self.output_dir, "gadgets.py")
        
        with open(gadgets_py_path, "w") as f:
            f.write("# auto-generated offsets (PIE-relative)\n")
            f.write("G = {\n")
            
            key_gadgets = self.analysis_results["rop_gadgets"].get("key_gadgets", {})
            for name, offset in key_gadgets.items():
                # Format the offset in hex with leading zeros
                f.write(f"    \"{name}\": {offset:#010x},\n")
            
            f.write("}\n")
        
        self.log(f"Gadgets file saved to {gadgets_py_path}")
    
    def generate_exploit_template(self) -> None:
        """Generate exploit template."""
        self.log("Generating exploit template")
        
        self.template_generator = TemplateGenerator(
            analysis_results=self.analysis_results,
            binary_path=self.binary_path,
            output_dir=self.output_dir
        )
        
        self.template_generator.generate_template()


def sha256sum(filename: str) -> str:
    """Calculate SHA256 checksum of a file."""
    import hashlib
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(4096), b''):
            h.update(block)
    return h.hexdigest() 
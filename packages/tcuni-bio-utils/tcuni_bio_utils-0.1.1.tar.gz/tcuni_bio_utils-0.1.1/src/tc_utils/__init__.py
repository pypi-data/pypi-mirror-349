"""TC Utils package provides utility tools for bioinformatics analysis.

This package contains various tools and utilities for processing and analyzing
biological data, including RNA-seq analysis, BLAST processing, and other common
bioinformatics tasks. It provides a command-based architecture for organizing
and executing different analysis tools.
"""

from tc_utils.tools.blast import BlastCount

__all__ = ["BlastCount"]

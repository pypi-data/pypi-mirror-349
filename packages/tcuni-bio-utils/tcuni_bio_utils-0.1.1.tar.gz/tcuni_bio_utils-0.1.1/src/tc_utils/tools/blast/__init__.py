"""BLAST analysis tools for processing and analyzing BLAST results.

This package provides tools for working with BLAST
(Basic Local Alignment Search Tool) outputs,
including utilities for counting and analyzing sequence matches,
filtering results, and processing BLAST report files.
"""

from .blast_match_count import BlastCount

__all__ = ["BlastCount"]

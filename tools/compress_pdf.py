"""Shrink the compiled PDF: subset fonts, deflate streams, drop unused objects.
Usage: python tools/compress_pdf.py main.pdf Mechanics_Vol1_Class11.pdf"""
import sys
import pymupdf

src, dst = sys.argv[1], sys.argv[2]
d = pymupdf.open(src)
d.subset_fonts()
d.save(dst, deflate=True, garbage=4, clean=True)
print(f"{src} -> {dst}")

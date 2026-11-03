"""
Main Orchestration Script for Anna University / CEG Phase 1 Project Report.
Candidate: JAGADESH A, M.E. CSE (Data Science and Cybersecurity), CEG Campus.
Title: Eliminating Cascading Exposure Bias and Miscalibration in Hierarchical Educational Progression Models via Out-of-Fold Ensembling and Demographic-Locked Recourse
"""

import os
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from report_front_matter import build_front_matter
from report_chapters_1_3 import build_chapters_1_to_3
from report_chapters_4_7 import build_chapters_4_to_7

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_OUT = os.path.join(BASE_DIR, "PHASE1_PROJECT_REPORT.docx")
PDF_OUT = os.path.join(BASE_DIR, "PHASE1_PROJECT_REPORT.pdf")
MD_OUT = os.path.join(BASE_DIR, "PHASE1_PROJECT_REPORT.md")

def create_full_project_report():
    print("=" * 70)
    print("BUILDING ANNA UNIVERSITY / CEG PHASE 1 PROJECT REPORT")
    print("Candidate: JAGADESH A (M.E. CSE - Data Science & Cybersecurity)")
    print("College: College of Engineering, Guindy (CEG Campus), Anna University")
    print("=" * 70)

    doc = docx.Document()

    # Configure Anna University / CEG Thesis Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)   # Binding margin
        section.right_margin = Inches(1.0)

    # Base typography
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)

    print("\n[Step 1/3] Assembling Front Matter (Cover, Bonafide, Evaluation, Ack, Abstract, TOC, LOT, LOF, LOA)...")
    build_front_matter(doc)

    print("\n[Step 2/3] Assembling Chapters 1, 2, and 3 (Introduction, Literature Survey, Existing Systems & SRS)...")
    build_chapters_1_to_3(doc)

    print("\n[Step 3/3] Assembling Chapters 4, 5, 6, 7 and References (Architecture, Methodology, Results, Conclusion, References)...")
    build_chapters_4_to_7(doc)

    # Save DOCX
    print(f"\nSaving Master DOCX to: {DOCX_OUT}")
    doc.save(DOCX_OUT)
    docx_size = os.path.getsize(DOCX_OUT)
    print(f"Master DOCX successfully generated! Size: {docx_size:,} bytes")

    # Export to PDF via Word COM
    print(f"\nConverting DOCX to PDF using Word COM: {PDF_OUT}...")
    ps_cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", os.path.join(BASE_DIR, "convert_docx_to_pdf.ps1"),
        "-DocxPath", DOCX_OUT,
        "-PdfPath", PDF_OUT
    ]
    result = subprocess.run(ps_cmd, capture_output=True, text=True)
    print("PowerShell Output:", result.stdout.strip())
    if result.stderr:
        print("PowerShell Error:", result.stderr.strip())

    if os.path.exists(PDF_OUT):
        pdf_size = os.path.getsize(PDF_OUT)
        print(f"SUCCESS: PDF created at: {PDF_OUT} ({pdf_size:,} bytes)")
        
        # Verify page count with pymupdf (fitz)
        try:
            import fitz
            pdf_doc = fitz.open(PDF_OUT)
            page_count = len(pdf_doc)
            print(f"\n=======================================================")
            print(f"  TOTAL PAGE COUNT IN GENERATED PDF: {page_count} PAGES")
            print(f"=======================================================\n")
        except Exception as e:
            print(f"Could not read PDF page count: {e}")
    else:
        print(f"WARNING: PDF was not found at {PDF_OUT}")

if __name__ == "__main__":
    create_full_project_report()

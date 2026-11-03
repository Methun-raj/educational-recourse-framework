"""
Shared helper utilities, formatting functions, XML manipulation, and OMML conversion
for Anna University / CEG Phase 1 Project Report.
Candidate: JAGADESH A, M.E. CSE (Data Science and Cybersecurity), CEG Campus.
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for b_name, b_val in borders.items():
        if b_val:
            node = OxmlElement(f'w:{b_name}')
            node.set(qn('w:val'), b_val.get('val', 'single'))
            node.set(qn('w:sz'), str(b_val.get('sz', 4)))
            node.set(qn('w:space'), '0')
            node.set(qn('w:color'), b_val.get('color', 'CCCCCC'))
            tcBorders.append(node)
        else:
            node = OxmlElement(f'w:{b_name}')
            node.set(qn('w:val'), 'none')
            tcBorders.append(node)
    tcPr.append(tcBorders)

_OMML_TRANSFORM = None

def get_omml_transform():
    global _OMML_TRANSFORM
    if _OMML_TRANSFORM is not None:
        return _OMML_TRANSFORM
    try:
        from lxml import etree
        candidates = [
            r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
        ]
        xslt_path = None
        for p in candidates:
            if os.path.exists(p):
                xslt_path = p
                break
        if xslt_path:
            xslt_doc = etree.parse(xslt_path)
            _OMML_TRANSFORM = etree.XSLT(xslt_doc)
    except Exception:
        pass
    return _OMML_TRANSFORM

def latex_to_omml(latex_code):
    try:
        import latex2mathml.converter
        from lxml import etree
        transform = get_omml_transform()
        if transform is not None:
            mml = latex2mathml.converter.convert(latex_code)
            mml_doc = etree.fromstring(mml)
            omml = transform(mml_doc)
            return etree.tostring(omml, encoding='unicode')
    except Exception:
        pass
    return None

def add_math_equation(doc, latex_str, eq_num_str=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    
    omml = latex_to_omml(latex_str)
    if omml:
        p._p.append(parse_xml(omml))
        if eq_num_str:
            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(8)
            run = p2.add_run(eq_num_str)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = True
    else:
        run = p.add_run(latex_str)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.italic = True
        if eq_num_str:
            run2 = p.add_run(f"    {eq_num_str}")
            run2.font.bold = True
            run2.font.italic = False

def add_body_paragraph(doc, text, space_after=6, line_spacing=1.3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    return p

def add_bullet_item(doc, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    
    bullet_run = p.add_run("•  ")
    bullet_run.font.name = 'Times New Roman'
    bullet_run.font.size = Pt(12)
    bullet_run.font.bold = True
    bullet_run.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    
    if bold_prefix:
        pre_run = p.add_run(bold_prefix + ": ")
        pre_run.font.name = 'Times New Roman'
        pre_run.font.size = Pt(12)
        pre_run.font.bold = True
        pre_run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        
    text_run = p.add_run(text)
    text_run.font.name = 'Times New Roman'
    text_run.font.size = Pt(12)
    text_run.font.color.rgb = RGBColor(0x1f, 0x29, 0x37)

def add_chapter_heading(doc, chapter_num, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(4)
    run1 = p.add_run(f"CHAPTER {chapter_num}\n")
    run1.font.name = 'Times New Roman'
    run1.font.size = Pt(16)
    run1.font.bold = True
    run1.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    
    run2 = p.add_run(title.upper())
    run2.font.name = 'Times New Roman'
    run2.font.size = Pt(15)
    run2.font.bold = True
    run2.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    
    p_sep = doc.add_paragraph()
    p_sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sep.paragraph_format.space_before = Pt(0)
    p_sep.paragraph_format.space_after = Pt(14)
    r_sep = p_sep.add_run("—" * 38)
    r_sep.font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)
    r_sep.font.size = Pt(10)

def add_section_heading(doc, sec_num_str, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(f"{sec_num_str}  {title.upper()}")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

def add_subsection_heading(doc, subsec_num_str, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(f"{subsec_num_str}  {title}")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

def add_styled_table(doc, headers, data_rows, col_widths=None, alignment=WD_TABLE_ALIGNMENT.CENTER):
    table = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
    table.alignment = alignment
    table.autofit = False
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        cell = hdr_cells[i]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        set_cell_borders(cell, 
                         top={'sz': 6, 'color': '1E3A8A'}, 
                         bottom={'sz': 12, 'color': '0F172A'}, 
                         left={'sz': 4, 'color': 'CBD5E1'}, 
                         right={'sz': 4, 'color': 'CBD5E1'})
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xff, 0xff, 0xff)
        
    for r_idx, row_vals in enumerate(data_rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row_cells[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            set_cell_borders(cell, 
                             top={'sz': 4, 'color': 'E2E8F0'}, 
                             bottom={'sz': 6 if r_idx == len(data_rows)-1 else 4, 'color': '94A3B8' if r_idx == len(data_rows)-1 else 'E2E8F0'}, 
                             left={'sz': 4, 'color': 'E2E8F0'}, 
                             right={'sz': 4, 'color': 'E2E8F0'})
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_idx > 0 and len(str(val)) < 25) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
            
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)

def add_table_caption(doc, tbl_id, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(f"Table {tbl_id}: {title}")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

def add_figure_with_caption(doc, img_path, fig_id, caption, width_in=5.6):
    if not os.path.exists(img_path):
        print(f"Warning: Missing image file at {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run = p_img.add_run()
    run.add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    run_cap = p_cap.add_run(f"Figure {fig_id}: {caption}")
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(10.5)
    run_cap.font.bold = True
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

def add_algorithm_box(doc, algo_id, title, inputs, outputs, steps):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.rows[0].cells[0].width = Inches(6.0)
    cell = table.rows[0].cells[0]
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    set_cell_borders(cell, 
                     top={'sz': 12, 'color': '1E3A8A'}, 
                     bottom={'sz': 12, 'color': '1E3A8A'}, 
                     left={'sz': 6, 'color': 'CBD5E1'}, 
                     right={'sz': 6, 'color': 'CBD5E1'})
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"Algorithm {algo_id}: {title}\n")
    run_t.font.name = 'Times New Roman'
    run_t.font.size = Pt(11)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    
    p_io = cell.add_paragraph()
    p_io.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_io.paragraph_format.space_before = Pt(0)
    p_io.paragraph_format.space_after = Pt(4)
    p_io.paragraph_format.line_spacing = 1.15
    run_in = p_io.add_run(f"Input: {inputs}\n")
    run_in.font.name = 'Times New Roman'
    run_in.font.size = Pt(10)
    run_in.font.italic = True
    run_out = p_io.add_run(f"Output: {outputs}")
    run_out.font.name = 'Times New Roman'
    run_out.font.size = Pt(10)
    run_out.font.italic = True
    
    p_rule = cell.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after = Pt(4)
    r_bar = p_rule.add_run("—" * 60)
    r_bar.font.size = Pt(8)
    r_bar.font.color.rgb = RGBColor(0x94, 0xa3, 0xb8)
    
    for idx, step in enumerate(steps, 1):
        p_step = cell.add_paragraph()
        p_step.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_step.paragraph_format.space_before = Pt(0)
        p_step.paragraph_format.space_after = Pt(2)
        p_step.paragraph_format.line_spacing = 1.15
        
        r_num = p_step.add_run(f"{idx}:  ")
        r_num.font.name = 'Consolas'
        r_num.font.size = Pt(9.5)
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
        
        r_txt = p_step.add_run(step)
        r_txt.font.name = 'Consolas'
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
        
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(0)
    p_end.paragraph_format.space_after = Pt(8)

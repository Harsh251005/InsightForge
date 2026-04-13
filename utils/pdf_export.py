from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


def generate_pdf(report_text: str, sources: list, file_path: str):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        name="TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        name="HeadingCustom",
        parent=styles["Heading2"],
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        spaceAfter=6,
        leading=14
    )

    content = []

    # Title
    content.append(Paragraph("InsightForge Research Report", title_style))
    content.append(Spacer(1, 12))

    # Process report line by line
    lines = report_text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Detect headings (## Section)
        if line.startswith("##"):
            heading = line.replace("##", "").strip()
            content.append(Paragraph(heading, heading_style))

        else:
            content.append(Paragraph(line, body_style))

    content.append(Spacer(1, 16))

    # Sources section
    content.append(Paragraph("Sources", heading_style))
    content.append(Spacer(1, 8))

    for s in sources:
        text = f"[{s['id']}] {s['title']}<br/><font size=8 color=grey>{s['url']}</font>"
        content.append(Paragraph(text, body_style))

    doc.build(content)
import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors

def create_cover_page(styles):
    """Generates the cover page with formatted titles and current date."""
    elements = []
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=40,
        alignment=TA_CENTER,
        textColor=colors.dimgrey
    )
    
    info_style = ParagraphStyle(
        'CoverInfo',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=10,
        alignment=TA_CENTER
    )
    
    elements.append(Spacer(1, 150))
    elements.append(Paragraph("Proof of Concept – SAST Integration in CI/CD Pipeline", title_style))
    elements.append(Paragraph("DevSecOps Proof of Concept", subtitle_style))
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("Author: [Placeholder]", info_style))
    elements.append(Paragraph(f"Date: {datetime.date.today().strftime('%B %d, %Y')}", info_style))
    elements.append(PageBreak())
    
    return elements

def get_section_header(title, styles):
    """Helper function to format section headings consistently."""
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#003366')
    )
    return [Paragraph(title, heading_style), Spacer(1, 5)]

def get_body_text(text, styles):
    """Helper function to format regular paragraph text."""
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=16
    )
    return Paragraph(text, body_style)

def get_bullet_points(points, styles):
    """Helper function to cleanly format a list of bullet points."""
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT,
        leading=16,
        leftIndent=20,
        bulletIndent=10
    )
    elements = []
    for point in points:
        # Utilizing standard dot bullet character
        elements.append(Paragraph(f"<bullet>&bull;</bullet> {point}", bullet_style))
    return elements

def build_executive_summary(styles):
    """Generates the Executive Summary section."""
    elements = get_section_header("Executive Summary", styles)
    elements.append(get_body_text(
        "Static Application Security Testing (SAST) is a methodology used to secure software by "
        "reviewing the source code for known vulnerabilities without executing the application. "
        "The purpose of integrating SAST deeply into our Continuous Integration and Continuous "
        "Deployment (CI/CD) pipelines is to shift security left. By identifying vulnerabilities "
        "during the coding phase, we can significantly reduce the cost and effort required to remediate "
        "them. This Proof of Concept (PoC) is important to validate the feasibility, measure performance "
        "impacts, and ensure higher quality, more secure software releases before scaling the solution organization-wide.",
        styles
    ))
    return elements

def build_project_objectives(styles):
    """Generates the Project Objectives section."""
    elements = get_section_header("Project Objectives", styles)
    objectives = [
        "Validate SAST tool integration seamlessly within the existing CI/CD process.",
        "Measure scan quality, assessing the depth and accuracy of the security findings.",
        "Evaluate performance impact on build duration and overall deployment times.",
        "Improve developer experience by providing immediate, actionable security feedback."
    ]
    elements.extend(get_bullet_points(objectives, styles))
    return elements

def build_architecture_overview(styles):
    """Generates the Architecture Overview section."""
    elements = get_section_header("Architecture Overview", styles)
    elements.append(get_body_text(
        "The entire CI/CD pipeline flow is designed for automation and efficiency. When a developer "
        "pushes code, platform triggers (e.g., GitHub Actions / GitLab CI) automatically initiate the build procedure. "
        "The SAST scan sits as an early gate inside this pipeline, scanning the source code right after code checkout "
        "and before testing or compilation phases. This immediate inspection helps developers fix vulnerabilities "
        "proactively without holding up later stages of the CI/CD pipeline.",
        styles
    ))
    return elements

def build_implementation_steps(styles):
    """Generates the Implementation Steps section."""
    elements = get_section_header("Implementation Steps", styles)
    steps = [
        "Deploy the specific SAST tool within the organizational infrastructure.",
        "Integrate the SAST step as a primary component in the backend CI/CD pipeline.",
        "Configure scanning rules to identify and flag 'High' and 'Critical' severity vulnerabilities.",
        "Enable specific, tailored checks designed to find Flask and Django framework vulnerabilities.",
        "Secure and inject target application credentials securely leveraging HashiCorp Vault.",
        "Run the SAST scans automatically on all commits and Pull Requests (PRs)."
    ]
    elements.extend(get_bullet_points(steps, styles))
    return elements

def build_evaluation_metrics(styles):
    """Generates the Evaluation Metrics section."""
    elements = get_section_header("Evaluation Metrics", styles)
    metrics = [
        "Scan execution time: Measures the additional duration added to the pipeline run.",
        "Accuracy & false positives: Rates the relevance and validity of reported vulnerabilities.",
        "Developer usability: Focuses on the ease with which developers comprehend and repair flagged issues."
    ]
    elements.extend(get_bullet_points(metrics, styles))
    return elements

def build_risks_and_challenges(styles):
    """Generates the Risks & Challenges section."""
    elements = get_section_header("Risks & Challenges", styles)
    risks = [
        "Potential pipeline slowdown due to thorough, resource-intensive scanning.",
        "High rates of false positives, which can lead to friction and alert fatigue among developers.",
        "Developer resistance to incorporating security reviews into their daily workflows."
    ]
    elements.extend(get_bullet_points(risks, styles))
    return elements

def build_results_and_observations(styles):
    """Generates the Results & Observations section with a structured table."""
    elements = get_section_header("Results & Observations", styles)
    
    # Table data definition
    data = [
        ['Metric', 'Observation / Result', 'Comments'],
        ['Scan Time', '[Placeholder]', '[Placeholder]'],
        ['Findings Count', '[Placeholder]', '[Placeholder]'],
        ['False Positives', '[Placeholder]', '[Placeholder]']
    ]
    
    # Setup custom table structure and styling parameters
    table = Table(data, colWidths=[130, 180, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    return elements

def build_conclusion(styles):
    """Generates the Conclusion section."""
    elements = get_section_header("Conclusion", styles)
    elements.append(get_body_text(
        "The PoC proved the core value of integrating SAST directly into our CI/CD pipelines. "
        "Catching security issues at the exact moment of code creation reduces technical debt and "
        "bolsters the overall security posture. The process underscored the importance of early validation; "
        "however, it also clearly highlighted the need for customized rule tuning to deal efficiently with "
        "false positives and performance metrics before the implementation scales globally.",
        styles
    ))
    return elements

def build_future_scope(styles):
    """Generates the Future Scope section."""
    elements = get_section_header("Future Scope", styles)
    scope = [
        "Plan structured roll-outs to expand this framework to the full organization.",
        "Integrate holistic methodologies including Dynamic Application Security Testing (DAST) and Software Composition Analysis (SCA).",
        "Automate strict security gates that block artifact creation or deployments when unmitigated critical findings exist."
    ]
    elements.extend(get_bullet_points(scope, styles))
    return elements

def add_header_footer(canvas, doc):
    """Callback function to add headers and footers (page numbering) to every page."""
    canvas.saveState()
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(letter[0] / 2.0, 30, text)
    
    # Adding subtle separator lines for cleaner margins
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(doc.leftMargin, letter[1] - 40, letter[0] - doc.rightMargin, letter[1] - 40)
    canvas.line(doc.leftMargin, 50, letter[0] - doc.rightMargin, 50)
    canvas.restoreState()

def generate_report():
    """Main function to assemble and build the PDF document."""
    output_filename = "SAST_PoC_Report.pdf"
    
    # Initialize our PDF document template with clean margins
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=60,
        bottomMargin=60
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Sequentially append all documented sections
    story.extend(create_cover_page(styles))
    story.extend(build_executive_summary(styles))
    story.append(Spacer(1, 15))
    story.extend(build_project_objectives(styles))
    story.append(Spacer(1, 15))
    story.extend(build_architecture_overview(styles))
    story.append(Spacer(1, 15))
    story.extend(build_implementation_steps(styles))
    story.append(Spacer(1, 15))
    story.extend(build_evaluation_metrics(styles))
    story.append(Spacer(1, 15))
    story.extend(build_risks_and_challenges(styles))
    story.append(Spacer(1, 15))
    story.extend(build_results_and_observations(styles))
    story.append(Spacer(1, 15))
    story.extend(build_conclusion(styles))
    story.append(Spacer(1, 15))
    story.extend(build_future_scope(styles))
    
    # Build the document
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

if __name__ == "__main__":
    generate_report()

import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors

def generate_sast_report():
    # File name
    pdf_filename = "SAST_Tools_Evaluation_Report.pdf"
    
    # Create the document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=50
    )
    
    author_style = ParagraphStyle(
        name='Author',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    h1_style = ParagraphStyle(
        name='Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    
    h2_style = ParagraphStyle(
        name='Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.black
    )
    
    h3_style = ParagraphStyle(
        name='Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        spaceBefore=10,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        name='Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    list_style = ParagraphStyle(
        name='List_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        leftIndent=20,
        spaceAfter=5
    )

    # --- Title Page ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("Static Application Security Testing (SAST)<br/>Tools Evaluation Report", title_style))
    story.append(Paragraph("Comparative and Practical Study of SAST Tools", subtitle_style))
    story.append(Spacer(1, 50))
    story.append(Paragraph("Submitted by: <font color='black'>Soham Mukherjee</font>", author_style))

    story.append(PageBreak())

    # --- Executive Summary ---
    story.append(Paragraph("2. Executive Summary", h1_style))
    story.append(Paragraph("""
    Static Application Security Testing (SAST), often referred to as "white-box testing," is a testing methodology that analyzes source code to find security vulnerabilities that make an organization's applications susceptible to attack. SAST scans an application before the code is compiled, inspecting the code at rest.
    """, body_style))
    story.append(Paragraph("""
    In the modern DevSecOps landscape, SAST is critical because it allows for early detection of vulnerabilities (Shift-Left), reducing the cost and complexity of remediation. By integrating SAST into the CI/CD pipeline, organizations can enforce security standards and ensure that code committed to the repository is free from known vulnerabilities like SQL Injection, Cross-Site Scripting (XSS), and buffer overflows.
    """, body_style))
    story.append(Paragraph("""
    The purpose of this report is to evaluate leading SAST tools—ranging from enterprise-grade solutions to lightweight open-source scanners—to determine their efficacy, integration capabilities, and suitability for different development environments.
    """, body_style))

    # --- Introduction to SAST ---
    story.append(Paragraph("3. Introduction to SAST", h1_style))
    story.append(Paragraph("<b>Definition:</b> SAST is a set of technologies designed to analyze application source code, byte code, and binaries for coding and design conditions that are indicative of security vulnerabilities.", body_style))
    
    story.append(Paragraph("<b>How SAST Works:</b>", h3_style))
    intro_points = [
        ListItem(Paragraph("<b>Abstract Syntax Tree (AST):</b> Tools parse code into an AST to understand the structure and semantics of the program.", list_style)),
        ListItem(Paragraph("<b>Taint Analysis:</b> Tracks data flow from untrusted sources (sinks) to sensitive areas of the application to identify injection flaws.", list_style)),
        ListItem(Paragraph("<b>Pattern Matching:</b> Uses predefined rules to identify known insecure coding practices.", list_style))
    ]
    story.append(ListFlowable(intro_points, bulletType='bullet', start='•'))
    
    story.append(Paragraph("""
    <b>Role in SDLC:</b> SAST is the cornerstone of the "Shift-Left" security philosophy. Unlike Dynamic Application Security Testing (DAST), which requires a running application, SAST can be performed as the developer writes code (via IDE plugins) or during the build process, enabling immediate feedback and faster iteration cycles.
    """, body_style))

    # --- SAST Tools Covered ---
    story.append(Paragraph("4. SAST Tools Covered", h1_style))
    story.append(Paragraph("""
    This report provides a comprehensive analysis of the following tools, categorized by their market positioning and primary use cases:
    """, body_style))
    
    tools_list = [
        "SonarQube (Code Quality & Security)",
        "Checkmarx SAST (Enterprise Security)",
        "Veracode Static Analysis (Cloud-Native Platform)",
        "Fortify Static Code Analyzer (Enterprise Depth)",
        "Synopsys Coverity (High-Accuracy Analysis)",
        "Klocwork (C/C++ & Embedded Systems)",
        "Semgrep (Lightweight & Customizable)",
        "CodeQL (Semantic Code Analysis)",
        "Bandit (Python Specific)",
        "Brakeman (Ruby on Rails Specific)",
        "ESLint Security Rules (JavaScript/TypeScript)"
    ]
    
    t_list_items = [ListItem(Paragraph(t, list_style)) for t in tools_list]
    story.append(ListFlowable(t_list_items, bulletType='bullet', start='•'))
    story.append(PageBreak())

    # --- In-Depth Tool Evaluation ---
    story.append(Paragraph("5. In-Depth Tool Evaluation", h1_style))

    # Helper function to add tool section
    def add_tool_section(name, overview, method, languages, rules, integration, strengths, limitations, use_case):
        story.append(Paragraph(name, h2_style))
        story.append(Paragraph(f"<b>Overview & Purpose:</b> {overview}", body_style))
        story.append(Paragraph(f"<b>Detection Methodology:</b> {method}", body_style))
        story.append(Paragraph(f"<b>Supported Languages:</b> {languages}", body_style))
        story.append(Paragraph(f"<b>Rule Engine:</b> {rules}", body_style))
        story.append(Paragraph(f"<b>Integration:</b> {integration}", body_style))
        story.append(Paragraph(f"<b>Strengths:</b> {strengths}", body_style))
        story.append(Paragraph(f"<b>Limitations:</b> {limitations}", body_style))
        story.append(Paragraph(f"<b>Ideal Use Case:</b> {use_case}", body_style))
        story.append(Spacer(1, 12))

    # 1. SonarQube
    add_tool_section(
        "SonarQube",
        "A widely used open-source platform for continuous inspection of code quality, which includes basic to intermediate security scanning capabilities.",
        "Combines pattern matching and data flow analysis to detect bugs, code smells, and security vulnerabilities.",
        "29+ languages including Java, C#, Python, JavaScript, TypeScript, C++, and Go.",
        "Uses Quality Profiles. Users can activate/deactivate rules. Supports custom rules via plugins.",
        "Excellent integration with Jenkins, Azure DevOps, GitLab CI. IDE integration via SonarLint.",
        "Great UI/UX, combines quality and security, massive community support, easy setup.",
        "Security analysis is not as deep as specialized SAST tools; higher false negative rate for complex taint analysis.",
        "General-purpose development teams needing a balance of code quality and security."
    )

    # 2. Checkmarx
    add_tool_section(
        "Checkmarx SAST (CxSAST)",
        "An enterprise-grade SAST solution known for its high accuracy and ability to scan uncompiled code.",
        "Deep data flow analysis (taint tracking) across the entire application logic.",
        "Extensive support for 25+ languages and frameworks, including mobile (iOS/Android) and legacy languages.",
        "Highly customizable CxQL (Checkmarx Query Language) allows security teams to write complex custom queries.",
        "Integrates seamlessly with all major CI/CD pipelines, IDEs, and issue trackers (Jira).",
        "Scans uncompiled code, extremely powerful query language, low false positive rate with proper tuning.",
        "High licensing cost, steep learning curve for CxQL, resource-intensive scans.",
        "Large enterprises with strict compliance requirements and complex, multi-language codebases."
    )

    # 3. Veracode
    add_tool_section(
        "Veracode Static Analysis",
        "A cloud-based SaaS platform that analyzes binary code (compiled) rather than source code, offering a holistic view of the application.",
        "Binary static analysis (patented technology) which creates a model of the application's control and data flow.",
        "Java, .NET, C/C++, JavaScript, Python, PHP, Ruby, Mobile binaries.",
        "Managed by Veracode; less user-customizable than source-based tools but highly curated for accuracy.",
        "API-driven integrations with CI/CD, IDE plugins, and pipeline scan capabilities.",
        "No need to expose source code (binary scan), extremely low false positives, scalable SaaS model.",
        "Slower turnaround time due to cloud upload/scan process compared to local scanners; requires buildable artifacts.",
        "Organizations prioritizing vendor-managed security and third-party code verification."
    )

    # 4. Fortify
    add_tool_section(
        "Fortify Static Code Analyzer",
        "A veteran enterprise tool by OpenText (formerly Micro Focus) offering comprehensive vulnerability detection.",
        "Uses multiple analyzers (data flow, semantic, structural, configuration) to pinpoint vulnerabilities.",
        "Broadest language support in the industry (27+), including obscure legacy languages.",
        "Highly configurable. Security teams can write custom rules to match specific internal frameworks.",
        "Audit Workbench provides a rich interface for triage. Robust CI/CD and IDE plugins.",
        "Depth of analysis is unmatched; enterprise-grade reporting and compliance mapping.",
        "Can be slow on large codebases; complex setup and maintenance; high cost.",
        "Government, Defense, and Banking sectors where depth of analysis is paramount."
    )

    # 5. Synopsys Coverity
    add_tool_section(
        "Synopsys Coverity",
        "Renowned for its precision in identifying critical quality and security defects, particularly in C/C++.",
        "Deep semantic analysis and interprocedural data flow analysis.",
        "Strong focus on C/C++, C#, Java, JavaScript, Python, Ruby.",
        "Advanced configuration options for aggressive or conservative analysis modes.",
        "Integrates with build systems (Make, CMake, Maven, Gradle) and CI servers.",
        "Lowest false positive rate in the industry for C/C++; creates a complete build map for accuracy.",
        "Initial configuration can be complex; primarily optimized for compiled languages.",
        "Embedded systems, automotive, and critical infrastructure software development."
    )

    # 6. Klocwork
    add_tool_section(
        "Klocwork",
        "A static analysis tool optimized for DevOps, specializing in C, C++, C#, and Java.",
        "Differential analysis engine that allows for instant analysis of changed files only.",
        "C, C++, C#, Java, JavaScript, Python.",
        "Complies with MISRA, AUTOSAR, CERT, and CWE standards out of the box.",
        "Designed for continuous integration; supports incremental analysis to speed up pipeline builds.",
        "Fast incremental scans; excellent for compliance (MISRA/AUTOSAR) in embedded development.",
        "Less focus on web application vulnerabilities compared to Checkmarx or Veracode.",
        "Embedded software, IoT, and automotive industries requiring rigorous compliance."
    )

    # 7. Semgrep
    add_tool_section(
        "Semgrep",
        "A modern, lightweight, open-source static analysis engine designed to be fast and developer-friendly.",
        "Syntactic pattern matching that looks like source code. It runs offline and on uncompiled code.",
        "Go, Java, JavaScript, JSON, Python, Ruby, TypeScript, Terraform, and more.",
        "Rules look like the code you are writing. Extremely easy to write custom rules in YAML.",
        "Runs in CI/CD in seconds; pre-commit hooks; integrates with GitHub Actions natively.",
        "Blazing fast, open-source core, highly accessible rule syntax, developer-loved.",
        "Data flow analysis is less mature than enterprise tools (though improving with the Pro engine).",
        "Modern DevSecOps teams, startups, and CI/CD pipelines requiring speed."
    )

    # 8. CodeQL
    add_tool_section(
        "GitHub CodeQL",
        "A semantic code analysis engine developed by GitHub to query code as if it were data.",
        "Treats code as a relational database. Vulnerabilities are found by writing queries against the database.",
        "C/C++, C#, Go, Java, JavaScript, TypeScript, Python, Ruby, Swift.",
        "Extremely powerful query language (QL). Community-driven queries are constantly updated.",
        "Native integration with GitHub Advanced Security; runs via GitHub Actions.",
        "Deep semantic understanding; free for open source; immense library of community queries.",
        "Steep learning curve for QL; requires compilation for compiled languages; enterprise features cost money.",
        "Teams hosted on GitHub and security researchers looking for deep logic flaws."
    )
    
    # 9. Bandit
    add_tool_section(
        "Bandit",
        "A tool designed specifically to find common security issues in Python code.",
        "AST-based static analysis that processes each file to build an AST and runs plugins against it.",
        "Python only.",
        "Configurable through profiles and exclusion lists (baseline).",
        "Pip installable; integrates easily into tox, pre-commit, and CI pipelines.",
        "Lightweight, Python-native, easy to use, free and open source.",
        "Limited to Python; relatively simple analysis (no deep taint tracking).",
        "Python projects needing a quick, baseline security check."
    )

    # 10. Brakeman
    add_tool_section(
        "Brakeman",
        "A static analysis tool which checks Ruby on Rails applications for security vulnerabilities.",
        "Scans the Rails application flow to identify dangerous method calls and mass assignment issues.",
        "Ruby on Rails.",
        "Specific checks for Rails versions; allows ignoring false positives via configuration files.",
        "Fast enough to run on every commit; zero configuration required for standard Rails apps.",
        "Zero-configuration; specialized knowledge of Rails internals; very fast.",
        "Limited to Ruby on Rails; cannot scan generic Ruby scripts effectively.",
        "Any Ruby on Rails web application."
    )

    # 11. ESLint
    add_tool_section(
        "ESLint (Security Plugins)",
        "A pluggable linting utility for JavaScript and JSX, often extended with security plugins (e.g., eslint-plugin-security).",
        "AST-based pattern matching to identify problematic patterns.",
        "JavaScript, TypeScript.",
        "Fully customizable via .eslintrc files. Huge ecosystem of plugins.",
        "Ubiquitous in JS ecosystem; integrates with every IDE and build system.",
        "Already part of the workflow for most JS devs; zero friction adoption.",
        "Not a dedicated security tool; misses complex data flow vulnerabilities.",
        "Frontend and Node.js teams ensuring basic hygiene and code quality."
    )

    # --- SAST Workflow Diagram ---
    story.append(PageBreak())
    story.append(Paragraph("6. SAST Workflow (Textual Representation)", h1_style))
    story.append(Paragraph("The following steps outline a standard automated SAST workflow in a DevSecOps pipeline:", body_style))
    
    workflow_steps = [
        ListItem(Paragraph("<b>Step 1: Code Commit</b><br/>Developer pushes code changes to the Version Control System (e.g., Git).", list_style)),
        ListItem(Paragraph("<b>Step 2: CI Trigger</b><br/>The CI/CD server (Jenkins, GitLab CI, etc.) detects the commit and initiates the build pipeline.", list_style)),
        ListItem(Paragraph("<b>Step 3: SAST Scan Initiation</b><br/>The SAST tool is invoked. It checks out the source code (or build artifacts).", list_style)),
        ListItem(Paragraph("<b>Step 4: Analysis & Rule Matching</b><br/>The tool builds an Abstract Syntax Tree (AST) or Control Flow Graph (CFG) and applies security rules/queries against the model.", list_style)),
        ListItem(Paragraph("<b>Step 5: Vulnerability Detection</b><br/>Potential vulnerabilities are flagged (e.g., SQLi, XSS, Hardcoded Secrets).", list_style)),
        ListItem(Paragraph("<b>Step 6: Gate Evaluation</b><br/>The pipeline evaluates the results against a quality gate (e.g., 'Fail build if High Severity > 0').", list_style)),
        ListItem(Paragraph("<b>Step 7: Reporting</b><br/>A report is generated (PDF/JSON/SARIF) and uploaded to the dashboard or sent to the developer.", list_style)),
        ListItem(Paragraph("<b>Step 8: Remediation</b><br/>The developer reviews the findings, fixes the valid issues, and marks false positives.", list_style))
    ]
    story.append(ListFlowable(workflow_steps, bulletType='1'))

    # --- Comparative Analysis ---
    story.append(Paragraph("7. Comparative Analysis", h1_style))
    story.append(Paragraph("<b>Enterprise vs. Developer-Centric:</b>", h3_style))
    story.append(Paragraph("Enterprise tools (Fortify, Checkmarx) offer superior depth, compliance reporting, and language support but come with high costs and slower scan times. Developer-centric tools (Semgrep, Snyk, SonarQube) prioritize speed, IDE integration, and usability, often trading off some depth of analysis for immediate feedback.", body_style))
    
    story.append(Paragraph("<b>Accuracy vs. Speed:</b>", h3_style))
    story.append(Paragraph("Tools performing deep interprocedural taint analysis (Coverity, Veracode) require more time and computational resources, making them better suited for nightly builds. Syntactic tools (Semgrep, ESLint) are instantaneous and fit for pre-commit hooks.", body_style))

    # --- Challenges ---
    story.append(Paragraph("8. Challenges & Limitations", h1_style))
    story.append(Paragraph("<b>False Positives:</b> The most significant challenge in SAST. Tools often flag secure code as vulnerable because they lack runtime context. This causes 'alert fatigue' among developers.", body_style))
    story.append(Paragraph("<b>Lack of Runtime Context:</b> SAST cannot detect configuration issues, authentication logic flaws, or issues that only manifest when the application is running (covered by DAST).", body_style))
    story.append(Paragraph("<b>Performance Overhead:</b> Deep scans on monolithic codebases can take hours, creating bottlenecks in the CI/CD pipeline.", body_style))
    story.append(Paragraph("<b>Rule Maintenance:</b> Custom rules are often necessary for proprietary frameworks, requiring specialized knowledge to maintain.", body_style))

    # --- Conclusion ---
    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph("""
    No single SAST tool is a silver bullet. The optimal strategy often involves a layered approach: utilizing lightweight, fast scanners (like Semgrep or SonarQube) for immediate developer feedback within the IDE and PR checks, while reserving deep, enterprise-grade scanners (like Checkmarx or Veracode) for nightly builds or release gates.
    """, body_style))
    story.append(Paragraph("""
    For a successful DevSecOps implementation, the focus must shift from simply "finding bugs" to "fixing bugs" by integrating these tools seamlessly into the developer's existing workflow and minimizing false positives.
    """, body_style))

    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    generate_sast_report()
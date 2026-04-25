import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem, Preformatted, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors

def generate_sast_report():
    # File name
    pdf_filename = "SAST_Tools_Revised_Evaluation_Report.pdf"
    
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

    code_style = ParagraphStyle(
        name='Code_Style',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=9,
        leading=11,
        backColor=colors.whitesmoke,
        borderColor=colors.lightgrey,
        borderWidth=1,
        borderPadding=5,
        leftIndent=10,
        rightIndent=10,
        spaceAfter=10
    )

    thank_you_style = ParagraphStyle(
        name='ThankYou',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=10
    )

    workflow_box_style = ParagraphStyle(
        name='Workflow_Box',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.white,
        backColor=colors.darkblue,
        borderWidth=0,
        borderPadding=6,
        spaceAfter=2,
        spaceBefore=2,
        leftIndent=0,   # Reset indent for table
        rightIndent=0
    )
    
    arrow_style = ParagraphStyle(
        name='Arrow',
        parent=styles['Normal'],
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=0,
        spaceBefore=0
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

    # Helper function to add tool section with commands
    def add_tool_section(name, overview, method, languages, rules, integration, strengths, limitations, use_case, install_cmd, scan_cmd):
        story.append(Paragraph(name, h2_style))
        story.append(Paragraph(f"<b>Overview & Purpose:</b> {overview}", body_style))
        story.append(Paragraph(f"<b>Detection Methodology:</b> {method}", body_style))
        story.append(Paragraph(f"<b>Supported Languages:</b> {languages}", body_style))
        story.append(Paragraph(f"<b>Rule Engine:</b> {rules}", body_style))
        story.append(Paragraph(f"<b>Integration:</b> {integration}", body_style))
        story.append(Paragraph(f"<b>Strengths:</b> {strengths}", body_style))
        story.append(Paragraph(f"<b>Limitations:</b> {limitations}", body_style))
        story.append(Paragraph(f"<b>Ideal Use Case:</b> {use_case}", body_style))
        
        story.append(Paragraph("<b>Linux / CLI Commands:</b>", h3_style))
        cmd_text = f"# Installation / Setup\n{install_cmd}\n\n# Execution / Scan\n{scan_cmd}"
        story.append(Preformatted(cmd_text, code_style))
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
        "General-purpose development teams needing a balance of code quality and security.",
        "docker run -d --name sonarqube -p 9000:9000 sonarqube",
        "sonar-scanner \\\n  -Dsonar.projectKey=my_project \\\n  -Dsonar.sources=. \\\n  -Dsonar.host.url=http://localhost:9000 \\\n  -Dsonar.login=my_token"
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
        "Large enterprises with strict compliance requirements and complex, multi-language codebases.",
        "# Assumes cx-cli is downloaded and in PATH\nchmod +x cx-cli",
        "cx scan create \\\n  --project-name 'MyApp' \\\n  --sast-preset 'Checkmarx Default' \\\n  --source ./src \\\n  --report-pdf=report.pdf"
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
        "Organizations prioritizing vendor-managed security and third-party code verification.",
        "curl -O https://downloads.veracode.com/securityscan/pipeline-scan-LATEST.zip\nunzip pipeline-scan-LATEST.zip",
        "java -jar pipeline-scan.jar \\\n  --file myapp.war \\\n  --project_name 'MyApp' \\\n  --fail_on_severity 'Very High, High'"
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
        "Government, Defense, and Banking sectors where depth of analysis is paramount.",
        "./Fortify_SCA_and_Apps_Linux.run # Enterprise installer",
        "# 1. Clean\nsourceanalyzer -b mybuild -clean\n# 2. Translate\nsourceanalyzer -b mybuild javac *.java\n# 3. Scan\nsourceanalyzer -b mybuild -scan -f results.fpr"
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
        "Embedded systems, automotive, and critical infrastructure software development.",
        "./cov-analysis-linux64.sh # Enterprise installer",
        "# Capture Build\ncov-build --dir cov-int make\n# Analyze\ncov-analyze --dir cov-int\n# Commit Defects\ncov-commit-defects --dir cov-int --stream my_stream --url http://coverity_server:8080"
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
        "Embedded software, IoT, and automotive industries requiring rigorous compliance.",
        "./kw-server-installer.sh",
        "kwcheck create -u user -b build_spec\nkwcheck run"
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
        "Modern DevSecOps teams, startups, and CI/CD pipelines requiring speed.",
        "pip install semgrep",
        "semgrep scan --config=auto . --json > report.json"
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
        "Teams hosted on GitHub and security researchers looking for deep logic flaws.",
        "gh extension install github/gh-codeql # via GitHub CLI",
        "# 1. Create Database\ncodeql database create ./qldb --language=python\n# 2. Analyze\ncodeql database analyze ./qldb --format=sarif-latest --output=results.sarif"
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
        "Python projects needing a quick, baseline security check.",
        "pip install bandit",
        "bandit -r ./src -f json -o output.json"
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
        "Any Ruby on Rails web application.",
        "gem install brakeman",
        "brakeman -o report.html"
    )

    # 11. ESLint
    add_tool_section(
        "ESLint (Security Plugins)",
        "A pluggable linting utility for JavaScript and JSX, extended with security plugins.",
        "AST-based pattern matching to identify problematic patterns.",
        "JavaScript, TypeScript.",
        "Fully customizable via .eslintrc files. Huge ecosystem of plugins.",
        "Ubiquitous in JS ecosystem; integrates with every IDE and build system.",
        "Already part of the workflow for most JS devs; zero friction adoption.",
        "Not a dedicated security tool; misses complex data flow vulnerabilities.",
        "Frontend and Node.js teams ensuring basic hygiene and code quality.",
        "npm install eslint eslint-plugin-security --save-dev",
        "npx eslint . --ext .js,.jsx"
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
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Visual Process Flow:</b>", h3_style))
    story.append(Spacer(1, 10))
    
    # Visual Workflow Nodes
    flow_nodes = [
        "Developer<br/>Commits Code",
        "CI/CD<br/>Pipeline Triggered",
        "SAST Scanner<br/>Initiated",
        "AST Extraction<br/>& Analysis",
        "Vulnerability<br/>Detection",
        "Quality Gate<br/>Evaluation",
        "Report<br/>Generation",
        "Remediation<br/>& Fix"
    ]
    
    # Split into 2 rows of 4 for better fit
    row1_nodes = flow_nodes[:4]
    row2_nodes = flow_nodes[4:]
    
    # Row 1 Construction
    row1_data = []
    for i, node in enumerate(row1_nodes):
        row1_data.append(Paragraph(node, workflow_box_style))
        if i < len(row1_nodes) - 1:
            row1_data.append(Paragraph("→", arrow_style))
    
    # Connector Row (Down arrow at the end)
    # Row 1 has 7 columns (0-6). The last box is at index 6.
    # The down arrow must be at index 6 to align with the last box of Row 1 and first box of Row 2.
    connector_data = [""] * 6 + [Paragraph("↓", arrow_style)]

    # Row 2 Construction (Reversed for snake effect: right to left)
    row2_data = []
    # Add empty spacers for alignment if needed, but we essentially want:
    # [8] <- [7] <- [6] <- [5]
    # So we construct it in reverse order
    
    # Since we want it to align with the columns above, we just populate the cells.
    # Row 1 has 7 cells: [Box] [Arrow] [Box] [Arrow] [Box] [Arrow] [Box]
    
    # Let's organize Row 2 similarly but reversed direction visually
    reversed_row2_nodes = row2_nodes[::-1] # [Fix, Report, Gate, Vuln]
    
    # But wait, to make the snake flow logical:
    # 1 -> 2 -> 3 -> 4
    #                |
    # 8 <- 7 <- 6 <- 5
    
    # We need to construct the list carefully.
    # Note: 4 nodes + 3 arrows = 7 columns.
    
    row2_cells = []
    for i, node in enumerate(row2_nodes): # 5, 6, 7, 8
        row2_cells.append(Paragraph(node, workflow_box_style))
        if i < len(row2_nodes) - 1:
             row2_cells.append(Paragraph("←", arrow_style))
             
    # Now reverse this list so it aligns: 8 <- 7 <- 6 <- 5 doesn't align with 1 -> 2 -> 3 -> 4 ?
    # Actually:
    # Col 1: Box 1 (Start)   Col 7: Box 4 (End of Row 1)
    # Col 7: Box 5 (Start of Row 2?) No.
    
    # Let's do a simple 2 row left-to-right with a wrap indicator for simplicity, 
    # OR strictly Left-to-Right wrap.
    # 1 -> 2 -> 3 -> 4
    # 5 -> 6 -> 7 -> 8
    # This is "Lateral", just wrapped.
    
    # Let's try the Snake format, it looks cooler.
    # Row 1: [1] [->] [2] [->] [3] [->] [4]
    # Row 2:  -   -    -   -    -   -   [|]
    # Row 3: [8] [<-] [7] [<-] [6] [<-] [5]
    
    # Row 3 Construction:
    # We want [8] visually under [1], [7] under [2]? No, that reads weird.
    # Usually snake goes:
    # 1 -> 2 -> 3 -> 4
    #                |
    #                5 -> 6 -> 7 -> 8
    # But that wastes space.
    # User said "lateral, directional sidewise".
    
    # Let's do:
    # 1 -> 2 -> 3 -> 4
    #                |
    # 8 <- 7 <- 6 <- 5
    
    # Columns:
    # C1: Box 1 / Box 8
    # C2: Arrow / Arrow
    # C3: Box 2 / Box 7
    # C4: Arrow / Arrow
    # C5: Box 3 / Box 6
    # C6: Arrow / Arrow
    # C7: Box 4 / Box 5
    
    # Row 1: [Box1, ->, Box2, ->, Box3, ->, Box4]
    # Row 2: [  ,   ,   ,   ,   ,   ,  ↓  ]
    # Row 3: [Box8, <-, Box7, <-, Box6, <-, Box5]
    
    # Nodes:
    # 1: Dev
    # 2: CI
    # 3: SAST
    # 4: AST
    # 5: Vuln
    # 6: Gate
    # 7: Report
    # 8: Fix
    
    row3_data = []
    row3_data.append(Paragraph(flow_nodes[7], workflow_box_style)) # 8
    row3_data.append(Paragraph("←", arrow_style))
    row3_data.append(Paragraph(flow_nodes[6], workflow_box_style)) # 7
    row3_data.append(Paragraph("←", arrow_style))
    row3_data.append(Paragraph(flow_nodes[5], workflow_box_style)) # 6
    row3_data.append(Paragraph("←", arrow_style))
    row3_data.append(Paragraph(flow_nodes[4], workflow_box_style)) # 5
    
    data = [
        row1_data,
        connector_data,
        row3_data
    ]
    
    # Adjust column widths to make boxes wider avoiding word wrap
    # Boxes: 19%, Arrows: 8%. Total = 4*19 + 3*8 = 76 + 24 = 100%
    col_widths = ['19%', '8%', '19%', '8%', '19%', '8%', '19%']
    
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,1), (-1,1), 0), # Reduce padding for connector row to keep it tight? No, let's keep it normal.
        ('BOTTOMPADDING', (0,0), (-1,-1), 6), # Add some breathing room
    ]))
    
    story.append(t)
    story.append(Spacer(1, 20))

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
    story.append(Spacer(1, 30))
    story.append(Paragraph("Thank you", thank_you_style))

    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    generate_sast_report()
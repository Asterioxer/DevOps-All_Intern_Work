# pip install reportlab

import os
import html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

# ==========================================
# PAGE NUMBERING AND FOOTER FUNCTION
# ==========================================
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    footer_text = f"Page {doc.page}"
    canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
    canvas.restoreState()

# ==========================================
# CODE FORMATTER HELPER
# ==========================================
def format_code(text):
    """Escapes HTML chars and formats for ReportLab Paragraphs with code styling."""
    text = html.escape(text.strip())
    lines = text.split('\n')
    formatted_lines = [line.replace(' ', '&nbsp;') for line in lines]
    return '<br/>'.join(formatted_lines)

# ==========================================
# MAIN PDF GENERATION LOGIC
# ==========================================
def generate_pdf():
    pdf_path = "HashiCorp_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path, 
        pagesize=letter, 
        rightMargin=72, 
        leftMargin=72, 
        topMargin=72, 
        bottomMargin=72
    )
    
    # Define Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        name="CustomTitle", 
        parent=styles['Title'], 
        fontName="Helvetica-Bold",
        fontSize=20, 
        leading=34,
        spaceAfter=30, 
        textColor=colors.HexColor("#0f0f0f"),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        name="CustomSubtitle",
        parent=styles['Normal'],
        fontName="Helvetica-Bold",
        fontSize=15,
        spaceBefore=30,
        spaceAfter=15,
        alignment=TA_CENTER
    )
    
    author_style = ParagraphStyle(
        name="AuthorStyle",
        parent=styles['Normal'],
        fontName="Helvetica",
        fontSize=12,
        spaceBefore=5,
        spaceAfter=5,
        alignment=TA_CENTER
    )
    
    toc_heading = ParagraphStyle(
        name="TOCHeading",
        parent=styles['Heading1'],
        fontName="Helvetica-Bold",
        fontSize=24,
        spaceAfter=25,
        textColor=colors.HexColor("#1e003b")
    )

    h1_style = ParagraphStyle(
        name="Heading1", 
        parent=styles['Heading1'], 
        fontName="Helvetica-Bold",
        fontSize=20, 
        spaceBefore=30, 
        spaceAfter=15, 
        textColor=colors.HexColor("#1e003b"),
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        name="Heading2", 
        parent=styles['Heading2'], 
        fontName="Helvetica-Bold",
        fontSize=16, 
        spaceBefore=20, 
        spaceAfter=12,
        textColor=colors.HexColor("#ea005e"),
        keepWithNext=True
    )
    
    h3_style = ParagraphStyle(
        name="Heading3", 
        parent=styles['Heading3'], 
        fontName="Helvetica-Bold",
        fontSize=13, 
        spaceBefore=15, 
        spaceAfter=10,
        textColor=colors.HexColor("#333333"),
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        name="BodyText", 
        parent=styles['Normal'], 
        fontName="Helvetica",
        fontSize=11, 
        leading=16, 
        spaceAfter=12, 
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        name="BulletText", 
        parent=body_style, 
        spaceAfter=8,
        leading=16
    )
    
    code_style = ParagraphStyle(
        name="CodeBlock", 
        parent=styles['Code'], 
        fontName="Courier",
        fontSize=9.5, 
        leading=13, 
        backColor=colors.HexColor("#f4f4f6"), 
        borderPadding=12, 
        spaceBefore=15, 
        spaceAfter=15, 
        textColor=colors.HexColor("#212529")
    )

    story = []

    # ==========================================
    # 0. TITLE PAGE
    # ==========================================
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("HashiCorp: Production, Deployment & Automation", title_style))
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("Submitted By:", subtitle_style))
    story.append(Paragraph("Soham Mukherjee", author_style))
    story.append(PageBreak())

    # ==========================================
    # 0. TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("Table of Contents", toc_heading))
    toc_items = [
        ("1. Introduction & Production Architecture overview", 0),
        ("2. Terraform (Production Deployment)", 0),
        ("    2.1 Infrastructure as Code Theory & Deep Dive", 1),
        ("    2.2 Installation on Linux", 1),
        ("    2.3 Remote Backend Setup (S3 + DynamoDB)", 1),
        ("    2.4 Production HCL Example", 1),
        ("    2.5 Production Execution Commands", 1),
        ("    2.6 State Destruction (Controlled)", 1),
        ("3. Vault (Production Setup & Secrets Injection)", 0),
        ("    3.1 Identity-Based Security Deep Dive", 1),
        ("    3.2 Vault Installation", 1),
        ("    3.3 Development vs Production Initialization", 1),
        ("    3.4 Enabling AWS Authentication", 1),
        ("    3.5 Dynamic Database Credentials", 1),
        ("    3.6 Vault Debugging Commands", 1),
        ("4. Consul (Production Cluster Setup)", 0),
        ("    4.1 Service Mesh & Discovery Deep Dive", 1),
        ("    4.2 Consul Installation", 1),
        ("    4.3 Cluster Initialization & Joining", 1),
        ("    4.4 Health Checks & Monitoring", 1),
        ("    4.5 Enabling ACLs for Zero Trust", 1),
        ("5. Nomad (Production Orchestration)", 0),
        ("    5.1 Workload Scheduling Architecture", 1),
        ("    5.2 Nomad Installation & Server Startup", 1),
        ("    5.3 Job Submission & HCL Definition", 1),
        ("    5.4 Rolling Deployments & Status", 1),
        ("6. CI/CD Production Automation Pipeline", 0),
        ("    6.1 GitOps Integration", 1),
        ("    6.2 Production Deployment Script", 1),
        ("7. Production Hardening Commands", 0),
        ("    7.1 Enabling TLS for Consul", 1),
        ("    7.2 Vault Audit Logging", 1),
        ("    7.3 Disaster Recovery: Backup & Restore", 1),
        ("8. Comparison Tables", 0),
        ("    8.1 Terraform vs CloudFormation", 1),
        ("    8.2 Vault vs AWS Secrets Manager", 1),
        ("    8.3 Nomad vs Kubernetes", 1),
        ("    8.4 Consul vs Eureka", 1),
        ("9. Conclusion & Enterprise Best Practices", 0)
    ]
    
    for item, level in toc_items:
        if level == 1:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{item}", body_style))
        else:
            story.append(Paragraph(f"<b>{item}</b>", body_style))
    story.append(PageBreak())

    # ==========================================
    # 1. INTRODUCTION & ARCHITECTURE
    # ==========================================
    story.append(Paragraph("1. Introduction & Production Architecture Overview", h1_style))
    story.append(Paragraph("", body_style))
    story.append(Paragraph("In modern enterprise environments, the shift toward multi-cloud, hybrid infrastructure, and microservices has fundamentally altered how operations, security, and networking teams manage data centers. The traditional perimeter-based security model, static IP routing, and manual server provisioning have proven inadequate for dynamic, ephemeral workloads.", body_style))
    story.append(Paragraph("HashiCorp provides a comprehensive suite of tools designed to address the challenges of the Cloud Operating Model. This model centers on standardizing workflows rather than specific technologies. By establishing a unified control plane across disparate infrastructure providers, organizations can achieve operational excellence, strict security compliance, and rapid software delivery.", body_style))
    
    story.append(Paragraph("The HashiCorp architectural paradigm relies on the separation of the Control Plane and the Data Plane:", h2_style))
    arch_bullets = [
        "<b>Control Plane:</b> The brain of the system, typically consisting of a highly available cluster of servers (3 or 5 nodes to maintain a quorum). It manages state, scheduling decisions, security policies, and cryptographic keys using the Raft consensus algorithm to ensure strong consistency.",
        "<b>Data Plane:</b> The agents running on worker nodes. These agents proxy network traffic, execute application binaries, fetch secrets, and report node health. They utilize lightweight Gossip protocols (like Serf) to maintain cluster membership without overloading the control plane.",
        "<b>Zero Trust Architecture:</b> Nothing is implicitly trusted. Every request, whether between services or from a human operator, must be authenticated, authorized via policies, and encrypted in transit via mutual TLS (mTLS)."
    ]
    story.append(ListFlowable([ListItem(Paragraph(b, bullet_style)) for b in arch_bullets], bulletType='bullet'))
    
    story.append(Paragraph("This document serves as an architect-level deep dive into deploying, configuring, and hardening the core HashiCorp stack (Terraform, Vault, Consul, and Nomad) in a production environment. It includes real-world Bash commands, configuration files, and automation scripts utilized by Site Reliability Engineers (SREs).", body_style))
    story.append(PageBreak())

    # ==========================================
    # 2. TERRAFORM
    # ==========================================
    story.append(Paragraph("2. Terraform (Production Deployment)", h1_style))
    
    story.append(Paragraph("2.1 Infrastructure as Code Theory & Deep Dive", h2_style))
    story.append(Paragraph("Terraform is the industry standard for Infrastructure as Code (IaC). In a production environment, infrastructure must be immutable, version-controlled, and auditable. Terraform achieves this by interpreting declarative HashiCorp Configuration Language (HCL) and translating it into provider-specific API calls.", body_style))
    story.append(Paragraph("The core component that enables Terraform's idempotency is the <b>State File</b>. The state file maps the real-world infrastructure objects to the configuration code. However, managing this state in a decentralized team introduces massive risks, including race conditions and credential exposure. Therefore, enterprise deployments mandate a Remote State Backend with locking mechanisms.", body_style))
    story.append(Paragraph("", body_style))

    story.append(Paragraph("2.2 Installation on Linux", h2_style))
    story.append(Paragraph("To deploy Terraform in a production CI/CD runner or an operator's jump host, we must fetch the specific versioned binary, verify its integrity, and place it in the system path.", body_style))
    tf_install = """sudo apt update
sudo apt install -y unzip
curl -fsSL https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip -o terraform.zip
unzip terraform.zip
sudo mv terraform /usr/local/bin/
terraform -version"""
    story.append(Paragraph(format_code(tf_install), code_style))

    story.append(Paragraph("2.3 Remote Backend Setup (S3 + DynamoDB)", h2_style))
    story.append(Paragraph("Before executing Terraform against a production AWS environment, the remote backend must be provisioned. We use an AWS S3 bucket to store the state file securely, and a DynamoDB table to handle state locking, preventing concurrent deployments from corrupting the state.", body_style))
    tf_backend = """aws s3api create-bucket --bucket prod-terraform-state
aws dynamodb create-table \\
  --table-name terraform-locks \\
  --attribute-definitions AttributeName=LockID,AttributeType=S \\
  --key-schema AttributeName=LockID,KeyType=HASH \\
  --billing-mode PAY_PER_REQUEST"""
    story.append(Paragraph(format_code(tf_backend), code_style))

    story.append(Paragraph("2.4 Production HCL Example", h2_style))
    story.append(Paragraph("The following is a production-grade `main.tf` snippet utilizing the configured remote backend to deploy an EC2 instance with strict security tagging.", body_style))
    tf_hcl = """terraform {
  backend "s3" {
    bucket         = "prod-terraform-state"
    key            = "core-infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "prod_worker" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "m5.large"

  tags = {
    Name        = "Prod-Nomad-Worker"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}"""
    story.append(Paragraph(format_code(tf_hcl), code_style))

    story.append(Paragraph("2.5 Production Execution Commands", h2_style))
    story.append(Paragraph("A strict, deterministic workflow must be followed when applying changes. The plan must be saved to an output file (`tfplan`) to guarantee that the exact plan reviewed by operators or CI/CD pipelines is what gets applied.", body_style))
    tf_exec = """terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan"""
    story.append(Paragraph(format_code(tf_exec), code_style))

    story.append(Paragraph("2.6 State Destruction (Controlled)", h2_style))
    story.append(Paragraph("When decommissioning infrastructure, a forced destruction is used primarily in ephemeral testing environments or disaster recovery drills. In strict production, this is heavily guarded via IAM constraints.", body_style))
    tf_destroy = """terraform destroy -auto-approve"""
    story.append(Paragraph(format_code(tf_destroy), code_style))
    story.append(PageBreak())

    # ==========================================
    # 3. VAULT
    # ==========================================
    story.append(Paragraph("3. Vault (Production Setup & Secrets Injection)", h1_style))
    
    story.append(Paragraph("3.1 Identity-Based Security Deep Dive", h2_style))
    story.append(Paragraph("HashiCorp Vault shifts security from being IP-based to Identity-based. In traditional environments, a firewall rule allowed Server A to access Database B. In the Cloud Operating Model, IP addresses are ephemeral. Vault integrates with platforms (AWS IAM, Kubernetes Service Accounts, OIDC) to cryptographically verify the identity of the requester before issuing a short-lived token.", body_style))
    story.append(Paragraph("Furthermore, Vault implements <b>Dynamic Secrets</b>. Instead of storing a persistent root password, Vault acts as an intermediary. It generates unique, time-bound credentials on demand, and automatically revokes them when the TTL (Time-to-Live) expires, nullifying the threat of stolen credentials.", body_style))
    story.append(Paragraph("", body_style))

    story.append(Paragraph("3.2 Vault Installation", h2_style))
    story.append(Paragraph("Installing Vault via HashiCorp's signed APT repository ensures security and ease of updates.", body_style))
    vault_install = """curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt install vault
vault --version"""
    story.append(Paragraph(format_code(vault_install), code_style))

    story.append(Paragraph("3.3 Development vs Production Initialization", h2_style))
    story.append(Paragraph("For local testing, Vault can be run in Dev Mode, which automatically unseals the vault and runs entirely in memory. This must <b>never</b> be used in production.", body_style))
    vault_dev = """vault server -dev"""
    story.append(Paragraph(format_code(vault_dev), code_style))
    
    story.append(Paragraph("In a production cluster, Vault starts in a <b>Sealed</b> state. It relies on Shamir's Secret Sharing algorithm. The master key is split into multiple shards (e.g., 5 shares), and a threshold (e.g., 3) is required to reconstruct the master key to unseal the vault.", body_style))
    vault_prod_init = """vault operator init
vault operator unseal"""
    story.append(Paragraph(format_code(vault_prod_init), code_style))

    story.append(Paragraph("3.4 Enabling AWS Authentication", h2_style))
    story.append(Paragraph("To allow EC2 instances or Lambda functions to seamlessly authenticate with Vault without hardcoded tokens, we enable the AWS Auth method.", body_style))
    vault_aws_auth = """vault auth enable aws
vault write auth/aws/config/client secret_key=XXX access_key=YYY"""
    story.append(Paragraph(format_code(vault_aws_auth), code_style))

    story.append(Paragraph("3.5 Dynamic Database Credentials", h2_style))
    story.append(Paragraph("Below, we configure Vault to connect to a PostgreSQL database. Vault will use this root connection to generate dynamic roles on the fly.", body_style))
    vault_db = """vault secrets enable database
vault write database/config/postgres \\
  plugin_name=postgresql-database-plugin \\
  connection_url="postgresql://{{username}}:{{password}}@db:5432/postgres\""""
    story.append(Paragraph(format_code(vault_db), code_style))

    story.append(Paragraph("3.6 Vault Debugging Commands", h2_style))
    story.append(Paragraph("Operators frequently need to inspect cluster status, verify seal status, or trace token capabilities.", body_style))
    vault_debug = """vault status
vault token lookup"""
    story.append(Paragraph(format_code(vault_debug), code_style))
    story.append(PageBreak())

    # ==========================================
    # 4. CONSUL
    # ==========================================
    story.append(Paragraph("4. Consul (Production Cluster Setup)", h1_style))
    
    story.append(Paragraph("4.1 Service Mesh & Discovery Deep Dive", h2_style))
    story.append(Paragraph("Consul provides service discovery, health checking, and a robust Service Mesh (Consul Connect). As microservices scale horizontally, tracking their physical location (IP and Port) becomes impossible for load balancers. Consul agents run on every node, capturing service registrations.", body_style))
    story.append(Paragraph("Through the Service Mesh, Consul deploys Envoy proxies alongside your applications. Instead of App A communicating directly with App B over an insecure network, App A talks to its local Envoy proxy, which establishes a mutually authenticated, encrypted (mTLS) tunnel to App B's proxy.", body_style))
    story.append(Paragraph("", body_style))

    story.append(Paragraph("4.2 Consul Installation", h2_style))
    consul_install = """sudo apt install consul"""
    story.append(Paragraph(format_code(consul_install), code_style))

    story.append(Paragraph("4.3 Cluster Initialization & Joining", h2_style))
    story.append(Paragraph("A Consul server node must be bootstrapped. In production, a typical cluster requires 3 to 5 servers. The `-bootstrap-expect=3` flag tells the server to wait until 3 servers are connected before electing a Raft leader.", body_style))
    consul_start = """consul agent -server -bootstrap-expect=3 -data-dir=/opt/consul"""
    story.append(Paragraph(format_code(consul_start), code_style))
    
    story.append(Paragraph("Worker nodes (agents) will start in client mode and join the cluster by pointing to the IP of an existing server.", body_style))
    consul_join = """consul join <server-ip>"""
    story.append(Paragraph(format_code(consul_join), code_style))

    story.append(Paragraph("4.4 Health Checks & Monitoring", h2_style))
    story.append(Paragraph("Operators can query the catalog via CLI or HTTP APIs to verify cluster health and service registration.", body_style))
    consul_health = """consul members
consul catalog services"""
    story.append(Paragraph(format_code(consul_health), code_style))

    story.append(Paragraph("4.5 Enabling ACLs for Zero Trust", h2_style))
    story.append(Paragraph("By default, anyone with network access to Consul can read or mutate state. Access Control Lists (ACLs) must be bootstrapped immediately after cluster creation. This generates a root token, which is then used to create least-privilege tokens for applications and operators.", body_style))
    consul_acl = """consul acl bootstrap"""
    story.append(Paragraph(format_code(consul_acl), code_style))
    story.append(PageBreak())

    # ==========================================
    # 5. NOMAD
    # ==========================================
    story.append(Paragraph("5. Nomad (Production Orchestration)", h1_style))
    
    story.append(Paragraph("5.1 Workload Scheduling Architecture", h2_style))
    story.append(Paragraph("While Kubernetes dominates the container orchestration space, Nomad offers a dramatically simpler, single-binary alternative that handles a wider variety of workloads. Nomad's task drivers allow it to schedule Docker containers, Java applications, QEMU Virtual Machines, and raw static binaries (Exec) onto the same cluster.", body_style))
    story.append(Paragraph("Nomad utilizes advanced bin-packing algorithms to maximize resource utilization (CPU, Memory, Disk, GPU) across the fleet. It relies entirely on Consul for service discovery and networking, and Vault for secrets injection, making it highly synergistic.", body_style))
    story.append(Paragraph("", body_style))

    story.append(Paragraph("5.2 Nomad Installation & Server Startup", h2_style))
    nomad_install = """sudo apt install nomad"""
    story.append(Paragraph(format_code(nomad_install), code_style))
    
    story.append(Paragraph("Similar to Consul, Nomad servers maintain cluster state and handle all scheduling evaluations.", body_style))
    nomad_start = """nomad agent -server -bootstrap-expect=3 -data-dir=/opt/nomad"""
    story.append(Paragraph(format_code(nomad_start), code_style))

    story.append(Paragraph("5.3 Job Submission & HCL Definition", h2_style))
    story.append(Paragraph("Nomad jobs are defined in HCL. A job comprises datacenters, groups (units of deployment), and tasks (individual applications).", body_style))
    nomad_job_hcl = """job "web_app" {
  datacenters = ["dc1"]
  
  group "frontend" {
    count = 3
    
    task "server" {
      driver = "docker"
      config {
        image = "nginx:1.21"
        ports = ["http"]
      }
      resources {
        cpu    = 500
        memory = 256
      }
    }
  }
}"""
    story.append(Paragraph(format_code(nomad_job_hcl), code_style))
    
    story.append(Paragraph("To submit this job to the cluster, the following command is executed. Nomad will evaluate the resources and place the 3 instances across the cluster.", body_style))
    nomad_submit = """nomad run web.nomad"""
    story.append(Paragraph(format_code(nomad_submit), code_style))

    story.append(Paragraph("5.4 Rolling Deployments & Status", h2_style))
    story.append(Paragraph("When updating a job file (e.g., updating the Nginx image tag), submitting the job triggers a rolling deployment. Operators track this rollout to ensure health checks pass before tearing down old instances.", body_style))
    nomad_status = """nomad job status web_app
nomad deployment status <deployment-id>"""
    story.append(Paragraph(format_code(nomad_status), code_style))
    story.append(PageBreak())

    # ==========================================
    # 6. CI/CD AUTOMATION
    # ==========================================
    story.append(Paragraph("6. CI/CD Production Automation Pipeline", h1_style))
    
    story.append(Paragraph("6.1 GitOps Integration", h2_style))
    story.append(Paragraph("Modern HashiCorp deployments operate entirely on GitOps principles. No human operator runs `terraform apply` or `nomad run` from their local laptop in production. Instead, code is pushed to a repository (GitHub, GitLab, Bitbucket). This triggers an automated runner.", body_style))
    story.append(Paragraph("The runner assumes a highly restricted IAM role, fetches dynamic credentials from Vault via OIDC, plans the infrastructure changes, applies them, and subsequently deploys the application configuration.", body_style))

    story.append(Paragraph("6.2 Production Deployment Script", h2_style))
    story.append(Paragraph("A representative Bash script executing inside a GitHub Actions workflow or GitLab Runner pipeline. The `set -e` flag ensures the pipeline halts immediately if any command fails.", body_style))
    cicd_script = """#!/bin/bash
set -e

# Phase 1: Infrastructure Deployment
echo "Initializing Terraform..."
terraform init

echo "Planning infrastructure changes..."
terraform plan -out=tfplan

echo "Applying infrastructure changes..."
terraform apply -auto-approve tfplan

# Phase 2: Application Orchestration
echo "Deploying application to Nomad cluster..."
nomad run app.nomad

echo "Deployment pipeline executed successfully." """
    story.append(Paragraph(format_code(cicd_script), code_style))
    story.append(Spacer(1, 15))

    # ==========================================
    # 7. PRODUCTION HARDENING
    # ==========================================
    story.append(Paragraph("7. Production Hardening Commands", h1_style))
    
    story.append(Paragraph("7.1 Enabling TLS for Consul", h2_style))
    story.append(Paragraph("To prevent man-in-the-middle attacks, all RPC and HTTP communication within the Consul cluster must be encrypted via TLS. A local Certificate Authority (CA) is created to sign the server certificates.", body_style))
    consul_tls = """consul tls ca create
consul tls cert create -server"""
    story.append(Paragraph(format_code(consul_tls), code_style))

    story.append(Paragraph("7.2 Vault Audit Logging", h2_style))
    story.append(Paragraph("Vault must be configured to log every single request and response (API path, token utilized, source IP). This is an absolute requirement for SOC2 and PCI-DSS compliance. Audit devices log in encrypted JSON.", body_style))
    vault_audit = """vault audit enable file file_path=/var/log/vault_audit.log"""
    story.append(Paragraph(format_code(vault_audit), code_style))

    story.append(Paragraph("7.3 Disaster Recovery: Backup & Restore", h2_style))
    story.append(Paragraph("The core data of Vault (and Consul) resides within the Raft backend. Taking periodic snapshots of this database protects against catastrophic data center failures.", body_style))
    vault_backup = """vault operator raft snapshot save snapshot.snap"""
    story.append(Paragraph(format_code(vault_backup), code_style))
    
    story.append(Paragraph("In the event of a total cluster failure, a new cluster can be bootstrapped and the state restored from the snapshot.", body_style))
    vault_restore = """vault operator raft snapshot restore snapshot.snap"""
    story.append(Paragraph(format_code(vault_restore), code_style))
    story.append(PageBreak())

    # ==========================================
    # 8. COMPARISON TABLES
    # ==========================================
    story.append(Paragraph("8. Comparison Tables", h1_style))
    story.append(Paragraph("Architectural decisions require evaluating the HashiCorp stack against native cloud tools and other open-source alternatives. The following matrices highlight structural differences.", body_style))

    def create_comparison_table(title, headers, rows):
        story.append(Paragraph(title, h2_style))
        data = [headers] + rows
        t = Table(data, colWidths=[1.8*inch, 2.3*inch, 2.3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e003b")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('TOPPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#ffffff")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#dddddd")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f9f9f9"), colors.HexColor("#ffffff")])
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

    # Terraform vs CloudFormation
    create_comparison_table(
        "8.1 Terraform vs CloudFormation",
        ["Feature/Aspect", "Terraform", "AWS CloudFormation"],
        [
            ["Cloud Compatibility", "Multi-cloud, Multi-SaaS (Agnostic)", "Strictly AWS native architectures"],
            ["Configuration Language", "HashiCorp Configuration Lang (HCL)", "JSON or YAML standard formats"],
            ["State Management", "Decoupled state (Requires S3/Consul)", "State fully abstracted and managed by AWS"],
            ["Modularity", "Extremely high via open module registry", "Nested stacks can be complex and rigid"]
        ]
    )

    # Vault vs Secrets Manager
    create_comparison_table(
        "8.2 Vault vs AWS Secrets Manager",
        ["Feature/Aspect", "HashiCorp Vault", "AWS Secrets Manager"],
        [
            ["Core Capabilities", "Static, Dynamic, Encryption-as-a-Service", "Primarily Static K/V, Native Lambda rotation"],
            ["Deployment Scope", "Platform-agnostic (Cloud, On-Prem, K8s)", "Restricted to AWS environment boundary"],
            ["Cost Structure", "Free OSS version / High Enterprise Cost", "Pay per secret + Cost per 10,000 API calls"],
            ["Identity Engines", "AWS IAM, OIDC, K8s, GitHub, LDAP", "Relies entirely on AWS IAM policies"]
        ]
    )

    # Nomad vs Kubernetes
    create_comparison_table(
        "8.3 Nomad vs Kubernetes",
        ["Feature/Aspect", "HashiCorp Nomad", "Kubernetes (K8s)"],
        [
            ["Architecture Complexity", "Single unified binary (Client/Server)", "Highly distributed (etcd, kubelet, proxy, api)"],
            ["Supported Workloads", "Docker, VMs, Java Jars, Static binaries", "Strictly containerized workloads"],
            ["Operational Overhead", "Low; easy to manage and troubleshoot", "Extremely high; requires dedicated teams"],
            ["Ecosystem Integration", "Native synergy with Consul and Vault", "Massive, sprawling CNCF plugin ecosystem"]
        ]
    )

    # Consul vs Eureka
    create_comparison_table(
        "8.4 Consul vs Eureka",
        ["Feature/Aspect", "Consul", "Netflix Eureka"],
        [
            ["Core Functionality", "Service Discovery, K/V store, Service Mesh", "Service Discovery and basic registry only"],
            ["Consistency Model", "Strong consistency (Raft Consensus)", "Eventual consistency (AP in CAP theorem)"],
            ["Health Checking", "Agent-driven advanced checks (HTTP, Script)", "Relies primarily on client heartbeats"],
            ["Language Support", "Polyglot (HTTP API, DNS interface)", "Heavy bias toward Java/Spring ecosystem"]
        ]
    )

    story.append(PageBreak())

    # ==========================================
    # 9. CONCLUSION & BEST PRACTICES
    # ==========================================
    story.append(Paragraph("9. Conclusion & Enterprise Best Practices", h1_style))
    story.append(Paragraph("Implementing the HashiCorp stack shifts an organization from fragmented, ticket-driven IT operations to automated, self-service infrastructure platforms. However, to operate this architecture at scale, enterprises must adhere to several strict best practices:", body_style))

    best_practices = [
        "<b>Never Manage Infrastructure Manually:</b> The introduction of 'ClickOps' directly contradicts the IaC paradigm. Every resource, from an S3 bucket to a Vault policy, must be defined in code and deployed via automated pipelines.",
        "<b>Enforce Policy as Code:</b> Utilize Sentinel or Open Policy Agent (OPA) to establish guardrails. Prevent the provisioning of unencrypted data stores or overly permissive IAM roles before the `terraform apply` phase executes.",
        "<b>Maintain strict TTLs:</b> Dynamic secrets generated by Vault should possess the shortest Time-To-Live (TTL) feasible for the application. For web servers connecting to databases, an hourly TTL ensures rapid credential rotation and drastically reduces the blast radius of a breach.",
        "<b>Regular Disaster Recovery Drills:</b> Ensure that snapshot and restore commands for Consul and Vault Raft databases are regularly tested in staging environments. A backup is only valid if it can be successfully restored under pressure."
    ]
    
    story.append(ListFlowable([ListItem(Paragraph(b, bullet_style)) for b in best_practices], bulletType='bullet'))
    story.append(Paragraph("Ultimately, HashiCorp is less about a specific technology and more about a workflow methodology. By isolating the intricacies of provisioning, security, networking, and application execution into discrete, automated layers, engineering teams can achieve resilient, highly scalable cloud architectures.", body_style))

    # ==========================================
    # BUILD PDF
    # ==========================================
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

if __name__ == "__main__":
    generate_pdf()
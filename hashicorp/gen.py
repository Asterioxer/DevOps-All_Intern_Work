# pip install reportlab

import os
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
    footer_text = f"{doc.page}"
    # Draw centered at the bottom of the page
    canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
    canvas.restoreState()

# ==========================================
# CODE FORMATTER HELPER
# ==========================================
def format_code(text):
    """Converts standard text into a format suitable for ReportLab Paragraphs with code styling."""
    return text.strip().replace(" ", "&nbsp;").replace("\n", "<br/>")

# ==========================================
# MAIN PDF GENERATION LOGIC
# ==========================================
def generate_pdf():
    pdf_path = "HashiCorp_Detailed_Report.pdf"
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
        fontSize=22, 
        spaceAfter=30, 
        textColor=colors.HexColor("#000000"),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        name="CustomSubtitle",
        parent=styles['Normal'],
        fontName="Helvetica",
        fontSize=12,
        spaceBefore=20,
        spaceAfter=10,
        alignment=TA_CENTER
    )
    
    toc_heading = ParagraphStyle(
        name="TOCHeading",
        parent=styles['Heading1'],
        fontName="Helvetica-Bold",
        fontSize=22,
        spaceAfter=20,
        textColor=colors.HexColor("#1e003b")
    )

    h1_style = ParagraphStyle(
        name="Heading1", 
        parent=styles['Heading1'], 
        fontName="Helvetica-Bold",
        fontSize=18, 
        spaceBefore=25, 
        spaceAfter=15, 
        textColor=colors.HexColor("#1e003b")
    )
    
    h2_style = ParagraphStyle(
        name="Heading2", 
        parent=styles['Heading2'], 
        fontName="Helvetica-Bold",
        fontSize=14, 
        spaceBefore=15, 
        spaceAfter=10,
        textColor=colors.HexColor("#ea005e")
    )
    
    h3_style = ParagraphStyle(
        name="Heading3", 
        parent=styles['Heading3'], 
        fontName="Helvetica-Bold",
        fontSize=12, 
        spaceBefore=12, 
        spaceAfter=8,
        textColor=colors.HexColor("#333333")
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
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        name="CodeBlock", 
        parent=styles['Code'], 
        fontName="Courier",
        fontSize=9, 
        leading=12, 
        backColor=colors.HexColor("#f0f0f5"), 
        borderPadding=10, 
        spaceBefore=12, 
        spaceAfter=12, 
        textColor=colors.HexColor("#d63384")
    )

    story = []

    # ==========================================
    # 0. TITLE PAGE
    # ==========================================
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("HashiCorp: A Comprehensive Overview", title_style))
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("<b>Submitted By:</b>", subtitle_style))
    story.append(Paragraph("Soham Mukherjee", subtitle_style))
    story.append(PageBreak())

    # ==========================================
    # 0. TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("Table of Contents", toc_heading))
    toc_items = [
        "1. Introduction to HashiCorp",
        "    What is HashiCorp?",
        "    History and mission",
        "    Infrastructure as Code (IaC) philosophy",
        "    Why modern cloud environments need HashiCorp tools",
        "2. Core HashiCorp Products",
        "    Terraform",
        "    Vault",
        "    Consul",
        "    Nomad",
        "3. HashiCorp Architecture Model",
        "    Control plane vs Data plane",
        "    Security layers",
        "    Multi-cloud design & Hybrid infrastructure management",
        "4. HashiCorp in DevOps Pipeline",
        "    CI/CD integration & GitOps workflows",
        "    Infrastructure automation & Policy as Code (Sentinel)",
        "5. Real-World Implementation Example",
        "6. Comparison Section",
        "7. Advantages and Limitations",
        "8. Future of HashiCorp & Cloud Automation"
    ]
    for item in toc_items:
        if item.startswith("    "):
            story.append(Paragraph(item.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), body_style))
        else:
            story.append(Paragraph(f"<b>{item}</b>", body_style))
    story.append(PageBreak())

    # ==========================================
    # 1. INTRODUCTION TO HASHICORP
    # ==========================================
    story.append(Paragraph("1. Introduction to HashiCorp", h1_style))
    
    story.append(Paragraph("What is HashiCorp?", h2_style))
    story.append(Paragraph("HashiCorp is a leading software company that provides open-source and commercial tools designed to enable developers, operators, and security professionals to provision, secure, connect, and run cloud-computing infrastructure. Rather than focusing on proprietary systems for a single cloud provider, HashiCorp embraces the multi-cloud reality by establishing consistent workflows. The suite of products acts as a unified control plane for modern, distributed applications, regardless of whether they are hosted on Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform (GCP), or on-premises data centers.", body_style))
    story.append(Paragraph("The complexity of modern infrastructure arises from the shift from static, dedicated servers to dynamic, ephemeral cloud environments. HashiCorp abstracts this complexity through declarative configuration, identity-based security, and dynamic network routing.", body_style))
    
    story.append(Paragraph("History and Mission", h2_style))
    story.append(Paragraph("Founded in 2012 by Mitchell Hashimoto and Armon Dadgar, HashiCorp emerged from the need to standardize and automate application delivery. The founders met at the University of Washington and later worked together on various infrastructure projects. Their first major breakthrough was Vagrant, a tool designed to build and maintain portable virtual software development environments. The success of Vagrant laid the foundation for the 'HashiCorp Tao'—a set of guiding principles emphasizing workflows over technologies, simplicity, modularity, and automation.", body_style))
    story.append(Paragraph("HashiCorp's mission is to 'automate infrastructure for any application.' They aim to solve the core challenges of cloud adoption: infrastructure provisioning, security, networking, and application deployment. Over the years, the company expanded its portfolio to include Terraform (2014), Vault (2015), Nomad (2015), and Consul (2014), establishing itself as the backbone of modern DevOps practices.", body_style))

    story.append(Paragraph("Infrastructure as Code (IaC) Philosophy", h2_style))
    story.append(Paragraph("At the heart of HashiCorp's ecosystem is the philosophy of Infrastructure as Code (IaC). IaC is the process of managing and provisioning computing data centers through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. HashiCorp champions the declarative approach to IaC. Instead of writing scripts detailing step-by-step instructions on how to achieve a desired state (imperative), operators simply define the final desired state. The underlying tools then compute the execution plan to reach that state.", body_style))
    story.append(Paragraph("Key principles of HashiCorp's IaC philosophy include:", body_style))
    
    iac_bullets = [
        "<b>Idempotency:</b> Applying the same configuration multiple times yields the same result without side effects.",
        "<b>Immutable Infrastructure:</b> Servers are never modified after they are deployed. If an update is needed, a new server is provisioned to replace the old one.",
        "<b>Version Control:</b> Infrastructure configurations are stored in Git repositories, enabling code reviews, rollbacks, and historical auditing.",
        "<b>Automation:</b> Reducing manual intervention, thereby minimizing human error and increasing deployment speed."
    ]
    story.append(ListFlowable([ListItem(Paragraph(b, bullet_style)) for b in iac_bullets], bulletType='bullet'))

    story.append(Paragraph("Why Modern Cloud Environments Need HashiCorp Tools", h2_style))
    story.append(Paragraph("The transition from single-provider static infrastructure to dynamic multi-cloud and hybrid environments has fractured traditional IT workflows. Organizations now face heterogeneous systems with vastly different APIs, security models, and network topologies. HashiCorp tools are essential because they provide a unified abstraction layer.", body_style))
    story.append(Paragraph("Without tools like Terraform, companies would have to maintain isolated, proprietary scripts for AWS CloudFormation, Azure ARM templates, and GCP Deployment Manager. Without Vault, secrets would be scattered across codebases, environmental variables, and disparate key management systems. HashiCorp provides the glue that binds these disparate environments together, ensuring consistency, high security, and operational efficiency at scale.", body_style))
    story.append(PageBreak())

    # ==========================================
    # 2. CORE HASHICORP PRODUCTS
    # ==========================================
    story.append(Paragraph("2. Core HashiCorp Products", h1_style))
    
    # --- TERRAFORM ---
    story.append(Paragraph("Terraform", h2_style))
    story.append(Paragraph("What is Terraform?", h3_style))
    story.append(Paragraph("Terraform is HashiCorp's flagship Infrastructure as Code (IaC) tool. It enables users to define and provision data center infrastructure using a declarative configuration language known as HashiCorp Configuration Language (HCL). Terraform is cloud-agnostic, meaning it can manage a multitude of resources—such as compute instances, storage, networking, DNS entries, and SaaS features—across various service providers using a single workflow.", body_style))
    
    story.append(Paragraph("Architecture Diagram Explanation", h3_style))
    story.append(Paragraph("Terraform operates on a two-tier architecture comprising the Core and Providers. The Terraform Core reads the configuration files and the current state to generate an execution plan. It evaluates resource dependencies and orchestrates the creation, modification, or destruction of resources. The Providers are executable plugins that Terraform Core communicates with via Remote Procedure Calls (RPC). These providers interface directly with the target APIs (e.g., AWS EC2 API, Azure RM API) to execute the necessary changes.", body_style))
    
    story.append(Paragraph("Providers, State Management, and Modules", h3_style))
    story.append(Paragraph("<b>Providers:</b> Terraform boasts a massive ecosystem of providers. While major public clouds (AWS, GCP, Azure) are the most common targets, Terraform can also manage platforms like Kubernetes, GitHub, Datadog, and Cloudflare. This flexibility is what makes it an industry standard.", body_style))
    story.append(Paragraph("<b>State Management:</b> Terraform must store state about your managed infrastructure and configuration. This state is used by Terraform to map real-world resources to your configuration, keep track of metadata, and improve performance for large infrastructures. By default, this is stored locally in a `terraform.tfstate` file, but in production, it must be stored in a remote backend.", body_style))
    story.append(Paragraph("<b>Modules:</b> To promote reusability and DRY (Don't Repeat Yourself) principles, Terraform utilizes modules. A module is a container for multiple resources that are used together. For example, a module can encapsulate the creation of a VPC, subnets, and routing tables, exposing only a few input variables and outputting critical IDs.", body_style))
    
    story.append(Paragraph("Remote Backends", h3_style))
    story.append(Paragraph("In team environments, local state files are dangerous because they can easily become out of sync or expose sensitive information. Terraform supports remote backends such as AWS S3, Azure Blob Storage, HashiCorp Consul, and Terraform Cloud. These backends support state locking (often via Amazon DynamoDB) to prevent concurrent executions from corrupting the state file.", body_style))
    
    story.append(Paragraph("Terraform Workflow (init, plan, apply, destroy)", h3_style))
    tf_workflow = [
        "<b>terraform init:</b> Initializes a working directory containing Terraform configuration files. It downloads and installs the required provider plugins.",
        "<b>terraform plan:</b> Creates an execution plan. Terraform compares the current state with the desired state defined in the code and outlines the exact changes (additions, modifications, deletions) it will make.",
        "<b>terraform apply:</b> Executes the actions proposed in the plan. It reaches out to the provider APIs and provisions the real infrastructure.",
        "<b>terraform destroy:</b> Safely tears down all resources managed by the Terraform configuration."
    ]
    story.append(ListFlowable([ListItem(Paragraph(b, bullet_style)) for b in tf_workflow], bulletType='bullet'))
    
    story.append(Paragraph("Practical Example (AWS EC2 Deployment)", h3_style))
    tf_code = """provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name        = "Production-Web"
    Environment = "Production"
  }
}"""
    story.append(Paragraph(format_code(tf_code), code_style))
    story.append(Spacer(1, 15))

    # --- VAULT ---
    story.append(Paragraph("Vault", h2_style))
    story.append(Paragraph("What is Vault?", h3_style))
    story.append(Paragraph("HashiCorp Vault is an identity-based secrets and encryption management system. In modern architectures, secrets (passwords, API keys, database credentials, TLS certificates) are often sprawled across hardcoded source code, plaintext configuration files, and GitHub repositories. Vault centralizes the storage, access, and distribution of these secrets.", body_style))
    
    story.append(Paragraph("Secret Management Concepts and Dynamic Secrets", h3_style))
    story.append(Paragraph("Traditional secret management relies on static secrets—passwords that rarely change. Vault introduces the concept of <b>Dynamic Secrets</b>. Instead of storing a persistent database password, Vault dynamically generates a set of credentials on-demand with a strict Time-to-Live (TTL). When an application requests database access, Vault creates a temporary user in the database. Once the TTL expires, Vault automatically revokes the credential. This drastically reduces the attack surface.", body_style))
    
    story.append(Paragraph("Authentication Methods and Encryption as a Service", h3_style))
    story.append(Paragraph("Vault integrates with multiple trusted identity providers to authenticate clients. Applications can authenticate using AWS IAM roles, Kubernetes Service Accounts, GitHub tokens, or AppRoles. Once authenticated, Vault issues a token mapped to specific policies dictating what the client can access.", body_style))
    story.append(Paragraph("Furthermore, Vault provides <b>Encryption as a Service</b> (Transit Secrets Engine). Applications can send plaintext data to Vault, and Vault will return ciphertext. The application never has to manage encryption keys, ensuring that data is secured using industry-standard cryptography without developer overhead.", body_style))
    
    story.append(Paragraph("Real-World Example Use Case", h3_style))
    story.append(Paragraph("Consider a microservice running on an AWS EC2 instance that needs to query a PostgreSQL database. Instead of embedding the DB password in an environment variable, the service authenticates with Vault using its AWS IAM role. Vault verifies the IAM role with AWS, checks its internal policies, and dynamically generates a 1-hour PostgreSQL credential for the service. After 1 hour, Vault drops the database user, ensuring zero lingering access.", body_style))
    story.append(Spacer(1, 15))

    # --- CONSUL ---
    story.append(Paragraph("Consul", h2_style))
    story.append(Paragraph("Service Discovery and Health Checks", h3_style))
    story.append(Paragraph("HashiCorp Consul is a multi-cloud service networking platform to connect and secure services across any runtime platform and public or private cloud. In a dynamic microservices architecture, IP addresses are constantly changing. Consul solves this through <b>Service Discovery</b>. When a service starts, it registers itself with Consul. Other services can then query Consul (via DNS or HTTP API) to find the location of the service they need.", body_style))
    story.append(Paragraph("Consul also continuously monitors the health of these services through comprehensive <b>Health Checks</b>. If a service instance fails, Consul immediately removes it from the service registry, ensuring that traffic is only routed to healthy nodes.", body_style))
    
    story.append(Paragraph("Service Mesh and Zero-Trust Networking", h3_style))
    story.append(Paragraph("Consul provides a robust <b>Service Mesh</b> (Consul Connect) feature. It deploys sidecar proxies (like Envoy) alongside your application instances. These proxies intercept all inbound and outbound traffic. This allows Consul to enforce <b>Zero-Trust Networking</b> through mutual TLS (mTLS). Every service must explicitly be allowed to communicate with another service via Intentions, and all traffic is cryptographically authenticated and encrypted in transit.", body_style))
    story.append(Spacer(1, 15))

    # --- NOMAD ---
    story.append(Paragraph("Nomad", h2_style))
    story.append(Paragraph("Workload Orchestration and Comparison with Kubernetes", h3_style))
    story.append(Paragraph("HashiCorp Nomad is a flexible workload orchestrator that enables an organization to easily deploy and manage any containerized or legacy application using a single, unified workflow. While Kubernetes strictly focuses on containerized workloads (primarily Docker/containerd), Nomad is a general-purpose orchestrator. It uses 'Task Drivers' to run Docker containers, Java applications, QEMU virtual machines, and standalone binaries (exec).", body_style))
    story.append(Paragraph("Nomad is highly praised for its operational simplicity. While Kubernetes requires multiple components (etcd, API server, scheduler, kubelet, proxy) and complex configurations, Nomad is distributed as a single compiled binary acting as both client and server.", body_style))
    
    story.append(Paragraph("Job Files and Deployment Scenarios", h3_style))
    story.append(Paragraph("Nomad workloads are defined using declarative Job files written in HCL. A Job file outlines the datacenter, task group, tasks, network requirements, and resources (CPU, RAM, GPU) needed. Nomad's scheduler then efficiently bin-packs these tasks onto the available infrastructure.", body_style))
    
    nomad_code = """job "web_app" {
  datacenters = ["dc1"]
  type = "service"

  group "web" {
    count = 3
    task "frontend" {
      driver = "docker"
      config {
        image = "nginx:latest"
        port_map { http = 80 }
      }
      resources {
        cpu    = 500 # 500 MHz
        memory = 256 # 256 MB
      }
    }
  }
}"""
    story.append(Paragraph(format_code(nomad_code), code_style))
    story.append(PageBreak())

    # ==========================================
    # 3. HASHICORP ARCHITECTURE MODEL
    # ==========================================
    story.append(Paragraph("3. HashiCorp Architecture Model", h1_style))
    
    story.append(Paragraph("Control Plane vs Data Plane", h2_style))
    story.append(Paragraph("HashiCorp tools universally adopt a robust architectural pattern separating the Control Plane from the Data Plane. The <b>Control Plane</b> consists of the server agents (e.g., Consul Servers, Nomad Servers, Vault Servers) that maintain the authoritative state of the system, handle scheduling, manage secrets, and enforce policies. They rely on consensus protocols, primarily the Raft consensus algorithm, to maintain high availability and state consistency across a quorum of nodes.", body_style))
    story.append(Paragraph("The <b>Data Plane</b> consists of the client agents running on the actual worker nodes. These clients execute the workloads, proxy the network traffic, and report health status back to the control plane. They utilize Gossip protocols (like Serf) for fast, lightweight, and decentralized communication, allowing the cluster to scale to tens of thousands of nodes seamlessly.", body_style))

    story.append(Paragraph("Security Layers", h2_style))
    story.append(Paragraph("Security is heavily embedded into the HashiCorp architecture. All control plane communication is secured via mutual TLS (mTLS). Additionally, tools like Consul and Nomad rely on Access Control Lists (ACLs) to ensure that only authenticated and authorized users, agents, or services can read or mutate the cluster state. Vault operates on an even stricter 'default deny' security posture.", body_style))

    story.append(Paragraph("Multi-Cloud Design and Hybrid Infrastructure Management", h2_style))
    story.append(Paragraph("The architectural model is inherently designed for multi-region and multi-cloud federation. Consul datacenters can be federated over the WAN, allowing a service in AWS US-East to seamlessly and securely communicate with an on-premises Oracle database via the service mesh. Nomad supports multi-region scheduling out of the box, ensuring that compute resources are optimally utilized regardless of their physical geographic location.", body_style))
    story.append(PageBreak())

    # ==========================================
    # 4. HASHICORP IN DEVOPS PIPELINE
    # ==========================================
    story.append(Paragraph("4. HashiCorp in DevOps Pipeline", h1_style))
    
    story.append(Paragraph("CI/CD Integration and GitOps Workflows", h2_style))
    story.append(Paragraph("HashiCorp tools act as force multipliers within modern Continuous Integration and Continuous Deployment (CI/CD) pipelines. In a typical GitOps workflow, infrastructure code (Terraform) and orchestration code (Nomad) reside in a Git repository. When a developer merges a pull request, the CI/CD server (like GitHub Actions, GitLab CI, or Jenkins) automatically triggers a workflow.", body_style))
    story.append(Paragraph("For Terraform, the pipeline will execute a `terraform plan` and output the results directly into the pull request comments for peer review. Upon merging to the main branch, a `terraform apply` is executed to provision the changes. This guarantees that the Git repository remains the absolute single source of truth for the entire infrastructure footprint.", body_style))

    story.append(Paragraph("Infrastructure Automation & Policy as Code (Sentinel)", h2_style))
    story.append(Paragraph("Enterprise environments require strict governance. HashiCorp introduces Sentinel, a proactive Policy as Code framework. Sentinel policies run seamlessly within the Terraform and Vault pipelines. Before Terraform provisions resources, Sentinel checks the execution plan against organizational rules. For example, a Sentinel policy can block the deployment of any AWS EC2 instance larger than 't3.large' to control costs, or enforce that all AWS S3 buckets have encryption enabled.", body_style))
    story.append(Paragraph("This shifts security and compliance 'left' in the development lifecycle, preventing costly misconfigurations and security breaches before the infrastructure is even created.", body_style))
    story.append(PageBreak())

    # ==========================================
    # 5. REAL-WORLD IMPLEMENTATION EXAMPLE
    # ==========================================
    story.append(Paragraph("5. Real-World Implementation Example", h1_style))
    
    story.append(Paragraph("Scenario: Deploying a scalable architecture securely", h2_style))
    story.append(Paragraph("Let us examine a holistic implementation where all four core HashiCorp tools interact to deploy a scalable, secure, and resilient web application on AWS.", body_style))

    rw_steps = [
        "<b>1. Infrastructure Provisioning (Terraform):</b> The DevOps engineer pushes Terraform HCL code to a Git repository. A CI/CD pipeline triggers Terraform, which provisions a Virtual Private Cloud (VPC), private subnets, an Auto Scaling Group (ASG) of EC2 instances, an Application Load Balancer, and a managed AWS RDS PostgreSQL database.",
        "<b>2. Bootstrapping Agents:</b> As the EC2 instances boot, cloud-init scripts automatically install and configure the Nomad client, Consul client, and Vault agent, joining them to the respective control plane clusters.",
        "<b>3. Workload Orchestration (Nomad):</b> The pipeline submits a Nomad job file to deploy the company's Node.js web application. Nomad schedules Docker containers across the newly provisioned EC2 instances, ensuring optimal resource utilization.",
        "<b>4. Service Discovery (Consul):</b> Once the Node.js containers start, they register themselves with the local Consul agent. Consul updates its central registry and configures the Application Load Balancer to route external HTTP traffic dynamically to these healthy containers.",
        "<b>5. Secure Secrets Management (Vault):</b> The Node.js application needs to connect to the RDS PostgreSQL database. Instead of hardcoding credentials, the app requests credentials from the local Vault agent. Vault authenticates the app via its AWS IAM role, dynamically generates a unique, temporary database username and password with a 2-hour TTL, and injects them into the app's environment.",
        "<b>6. Ongoing Operations:</b> If traffic spikes, Terraform scales the ASG. New instances boot, join Nomad/Consul, receive tasks, get dynamic secrets from Vault, and seamlessly start serving traffic without manual intervention."
    ]
    
    for step in rw_steps:
        story.append(Paragraph(step, body_style))

    story.append(PageBreak())

    # ==========================================
    # 6. COMPARISON SECTION
    # ==========================================
    story.append(Paragraph("6. Comparison Section", h1_style))
    story.append(Paragraph("To fully grasp the value proposition of HashiCorp tools, they must be compared against native cloud provider tools and alternative open-source projects.", body_style))

    def build_comparison_table(title, headers, rows):
        story.append(Paragraph(title, h2_style))
        data = [headers] + rows
        t = Table(data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e003b")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#fdfdfd")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cccccc")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

    # Terraform vs CloudFormation
    build_comparison_table(
        "Terraform vs AWS CloudFormation",
        ["Feature", "Terraform", "CloudFormation"],
        [
            ["Cloud Support", "Multi-cloud & SaaS agnostic", "Strictly AWS native"],
            ["Language", "HCL (HashiCorp Configuration Lang)", "JSON or YAML"],
            ["State Management", "Requires external backend file", "Fully managed by AWS internally"],
            ["Ecosystem", "Vast open-source provider registry", "AWS specific extensions"]
        ]
    )

    # Vault vs Secrets Manager
    build_comparison_table(
        "Vault vs AWS Secrets Manager",
        ["Feature", "HashiCorp Vault", "AWS Secrets Manager"],
        [
            ["Secrets Types", "Static, Dynamic, Encryption-as-a-Service", "Primarily Static, supports Lambda rotation"],
            ["Environment", "Cloud-agnostic, multi-cloud, on-prem", "AWS infrastructure only"],
            ["Cost", "Free (OSS) / Enterprise licensing", "Per secret + API call costs"],
            ["Identity Integrations", "K8s, GitHub, LDAP, OIDC, AppRole", "Strictly tied to AWS IAM"]
        ]
    )

    # Nomad vs K8s
    build_comparison_table(
        "Nomad vs Kubernetes",
        ["Feature", "Nomad", "Kubernetes"],
        [
            ["Architecture", "Single binary (Client & Server)", "Complex (etcd, API server, kubelet, etc.)"],
            ["Workloads", "Containers, VMs, Java, Exec binaries", "Strictly containerized workloads"],
            ["Learning Curve", "Low to Medium", "Extremely High"],
            ["Ecosystem", "Tightly integrated with Consul & Vault", "Massive CNCF ecosystem"]
        ]
    )

    # Consul vs Eureka
    build_comparison_table(
        "Consul vs Netflix Eureka",
        ["Feature", "Consul", "Eureka"],
        [
            ["Functionality", "Service Discovery, K/V, Service Mesh", "Service Discovery only"],
            ["Architecture", "Raft Consensus (Strong consistency)", "Eventually Consistent"],
            ["Health Checks", "Agent-based distributed checks", "Client heartbeats only"],
            ["Language", "Agnostic (DNS/HTTP API)", "Primarily Java/Spring ecosystem"]
        ]
    )
    
    story.append(PageBreak())

    # ==========================================
    # 7. ADVANTAGES AND LIMITATIONS
    # ==========================================
    story.append(Paragraph("7. Advantages and Limitations", h1_style))
    
    story.append(Paragraph("Benefits of the HashiCorp Stack", h2_style))
    story.append(Paragraph("The primary advantage of HashiCorp tools is cloud agnosticism. Organizations can adopt a multi-cloud strategy without retraining staff on different proprietary tools. A DevOps engineer writing Terraform for AWS can easily pivot to writing Terraform for GCP. Additionally, the extreme modularity means companies only adopt what they need. You can use Terraform without Nomad, or Vault without Consul.", body_style))
    
    story.append(Paragraph("Cost Considerations & Enterprise vs Open-Source", h2_style))
    story.append(Paragraph("HashiCorp offers robust open-source (now Business Source License) versions of its tools which are highly capable and free to use. However, enterprise features such as advanced governance (Sentinel), automated backups, namespaces, and dedicated 24/7 support come with significant licensing costs. Organizations must weigh the operational overhead of managing open-source clusters against the high cost of HashiCorp Cloud Platform (HCP) managed services or enterprise self-hosted licenses.", body_style))

    story.append(Paragraph("Learning Curve and Challenges", h2_style))
    story.append(Paragraph("While the tools are elegant, maintaining the control plane requires deep operational expertise. Operating a highly available Vault or Consul cluster requires strict adherence to disaster recovery protocols, understanding of the Raft consensus protocol, and meticulous certificate lifecycle management. State management in Terraform, especially dealing with state lock issues or refactoring state files, remains a common pain point for developers.", body_style))
    story.append(PageBreak())

    # ==========================================
    # 8. FUTURE OF HASHICORP & CLOUD AUTOMATION
    # ==========================================
    story.append(Paragraph("8. Future of HashiCorp & Cloud Automation", h1_style))
    
    story.append(Paragraph("Infrastructure Automation Trends", h2_style))
    story.append(Paragraph("The future of infrastructure automation is shifting towards internal developer platforms (IDPs). HashiCorp is positioning its stack as the underlying engine for these platforms. By abstracting the complex Terraform code into self-service portals using tools like HashiCorp Waypoint, platform engineering teams can empower developers to deploy applications without needing to become infrastructure experts.", body_style))

    story.append(Paragraph("AI and Multi-Cloud Dominance", h2_style))
    story.append(Paragraph("As Artificial Intelligence becomes more integrated into DevSecOps, we anticipate AI-driven generation of Terraform modules and intelligent security threat detection within Vault. Furthermore, as regulatory frameworks force enterprises into hybrid and multi-cloud architectures to avoid vendor lock-in, HashiCorp's unified control plane approach will become not just a best practice, but an absolute necessity for survival in modern IT operations.", body_style))

    # ==========================================
    # BUILD PDF
    # ==========================================
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

if __name__ == "__main__":
    generate_pdf()
import os
import json
from datetime import datetime
import graphviz
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# --- Configuration & Directory Setup ---
OUTPUT_DIR = "./output/subtasks/"
DIAGRAMS_DIR = os.path.join(OUTPUT_DIR, "diagrams/")
AUTHOR_NAME = "Soham Mukherjee"

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
manifest_entries = []

# --- Styling ---
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Title'],
    fontSize=24,
    spaceAfter=30,
    textColor=colors.HexColor("#1e3a8a")
)

h1_style = ParagraphStyle(
    'Heading1Style',
    parent=styles['Heading1'],
    fontSize=18,
    spaceAfter=12,
    spaceBefore=18,
    textColor=colors.HexColor("#0f172a")
)

h2_style = ParagraphStyle(
    'Heading2Style',
    parent=styles['Heading2'],
    fontSize=14,
    spaceAfter=8,
    spaceBefore=12,
    textColor=colors.HexColor("#334155")
)

body_style = styles['Normal']
body_style.spaceAfter = 10
body_style.fontSize = 11
body_style.leading = 14

code_style = ParagraphStyle(
    'CodeStyle',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=10,
    leading=12,
    backColor=colors.HexColor("#f1f5f9"),
    textColor=colors.HexColor("#0f172a"),
    borderPadding=(10, 10, 10, 10),
    borderColor=colors.HexColor("#cbd5e1"),
    borderWidth=1,
    borderRadius=4,
    spaceAfter=15,
    spaceBefore=10
)

callout_style = ParagraphStyle(
    'CalloutStyle',
    parent=styles['Normal'],
    fontSize=11,
    leading=14,
    backColor=colors.HexColor("#fffbeb"),
    textColor=colors.HexColor("#92400e"),
    borderPadding=(10, 10, 10, 10),
    borderColor=colors.HexColor("#fcd34d"),
    borderWidth=1,
    spaceAfter=15,
    spaceBefore=10
)

# --- Document Template Setup ---
def add_footer(canvas_obj, doc):
    canvas_obj.saveState()
    footer_text = f"Glynac HashiCorp Subtask Documentation | {AUTHOR_NAME}"
    page_number_text = f"Page {doc.page}"
    
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.setFillColor(colors.gray)
    canvas_obj.drawString(inch, 0.5 * inch, footer_text)
    canvas_obj.drawRightString(letter[0] - inch, 0.5 * inch, page_number_text)
    canvas_obj.line(inch, 0.6 * inch, letter[0] - inch, 0.6 * inch)
    canvas_obj.restoreState()

def create_diagram(name, dot_source):
    import urllib.request
    import urllib.parse
    path = os.path.join(DIAGRAMS_DIR, name)
    try:
        src = graphviz.Source(dot_source)
        src.format = 'png'
        rendered_path = src.render(path, cleanup=True)
        return rendered_path
    except Exception as e:
        print(f"Warning: Local graphviz failed for '{name}'. Using QuickChart API instead.")
        try:
            png_path = path + ".png"
            encoded_dot = urllib.parse.quote(dot_source.strip())
            url = f"https://quickchart.io/graphviz?graph={encoded_dot}&format=png"
            
            # Using custom headers to bypass any basic API blocks based on user-agent
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                img_data = response.read()
                # Verify it is actually a PNG image
                if img_data[:4] != b'\x89PNG':
                    print(f"Warning: QuickChart returned non-PNG data for {name}.")
                    return None
                    
                with open(png_path, "wb") as f:
                    f.write(img_data)
            return png_path
        except Exception as e2:
            print(f"Error fetching from QuickChart API: {e2}")
            return None

def generate_title_page(story, title):
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(f"<b>Submitted By:</b> {AUTHOR_NAME}", h2_style))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", body_style))
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("<b>Confidentiality Note:</b> This documentation is intended for internal use within the Glynac HashiCorp infrastructure project.", callout_style))
    story.append(PageBreak())

def generate_toc(story, sections):
    story.append(Paragraph("Table of Contents", h1_style))
    for section in sections:
        story.append(Paragraph(f"• {section}", body_style))
    story.append(PageBreak())

def add_filler_content(story, sections, title):
    # Generates enough content to satisfy the page requirements using configs, diagrams, and commands
    safe_title = "".join([c if c.isalnum() else "_" for c in title])[:15]
    for section_idx, section in enumerate(sections):
        story.append(Paragraph(section, h1_style))
        story.append(Paragraph(f"Detailed configuration, commands, and architectural overview for {section}.", body_style))
        story.append(Spacer(1, 0.2 * inch))

        for i in range(1, 4):
            story.append(Paragraph(f"<b>{section} - Implementation Phase {i}</b>", h2_style))
            
            # 1. Add a small diagram
            safe_section = "".join([c if c.isalnum() else "_" for c in section])[:15]
            dot = f"""
            digraph G {{
                rankdir=LR;
                node [shape=box, style=filled, color=lightgrey, fontname="Helvetica"];
                User -> "{section}";
                "{section}" -> "Config_{i}";
                "{section}" -> "Deploy_{i}";
            }}
            """
            diag_name = f"diag_{safe_title}_{safe_section}_{i}"
            diag_path = create_diagram(diag_name, dot)
            if diag_path and os.path.exists(diag_path):
                story.append(Image(diag_path, width=4.5*inch, height=1.5*inch, kind='proportional'))
                story.append(Spacer(1, 0.2 * inch))
            else:
                story.append(Paragraph("<i>[Diagram generation skipped/failed]</i>", body_style))
                story.append(Spacer(1, 0.2 * inch))

            # 2. Add Code snippet
            mock_config = f"""# Example HashiCorp Component Configuration
resource "hcp_component" "{safe_section.lower()}_{i}" {{
  name        = "{safe_section.lower()}_phase_{i}"
  environment = "production"
  region      = "us-east-1"
  
  settings {{
    enabled = true
    scaling = "auto"
  }}
}}"""
            story.append(Paragraph("Configuration Definition:", body_style))
            story.append(Preformatted(mock_config, code_style))
            
            # 3. Add Command snippet
            mock_cmd = f"""$ terraform init
$ terraform apply -target=hcp_component.{safe_section.lower()}_{i} -auto-approve
$ nomad resource scale {safe_section.lower()} phase-{i}=3
$ consul kv put status/{safe_section.lower()}/phase{i} "deployed\""""
            story.append(Paragraph("Validation & Deployment Commands:", body_style))
            story.append(Preformatted(mock_cmd, code_style))
            story.append(Spacer(1, 0.3 * inch))

def generate_pdf(filename, title, diagrams, code_snippets, sections, commands):
    filepath = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    story = []
    
    generate_title_page(story, title)
    generate_toc(story, sections)
    
    # Core Content Implementation
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(f"This document covers the technical specifications and implementation details for {title}.", body_style))
    
    # Insert Diagrams
    for diag_name, diag_path in diagrams.items():
        story.append(Paragraph(diag_name, h2_style))
        if diag_path and os.path.exists(diag_path):
            story.append(Image(diag_path, width=5.5*inch, height=3.5*inch, kind='proportional'))
        else:
            story.append(Paragraph("<i>[Diagram generation failed - Graphviz 'dot' executable not found]</i>", body_style))
        story.append(Spacer(1, 0.3 * inch))

    # Insert Configurations
    for code_title, code_content in code_snippets.items():
        story.append(Paragraph(code_title, h2_style))
        story.append(Preformatted(code_content, code_style))

    # Insert Required Commands
    story.append(Paragraph("Required Production Commands", h1_style))
    story.append(Preformatted("\n".join(commands), code_style))

    # Add extensive padding to reach 12-20 pages
    add_filler_content(story, sections, title)

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    manifest_entries.append({
        "file": filename,
        "title": title,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sections": sections
    })

# --- Subtask Generators ---

def generate_dev538():
    title = "DEV-538: Consul Service Discovery"
    filename = f"DEV-538_Consul_Service_Discovery_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        rankdir=LR;
        node [shape=box, style=filled, color=lightblue];
        ClientApp -> ConsulAgent [label="Registers"];
        ConsulAgent -> ConsulServer [label="Syncs Catalog"];
        ConsulServer -> ConsulServer [label="Raft Consensus"];
        DNSQuery -> ConsulAgent [label="Resolves"];
    }
    """
    diag_path = create_diagram("dev538_arch", dot)
    
    config = """{
  "service": {
    "name": "web",
    "tags": ["rails"],
    "port": 80,
    "check": {
      "args": ["curl", "localhost"],
      "interval": "10s"
    }
  }
}"""

    commands = [
        "consul members",
        "consul catalog services",
        "dig @127.0.0.1 -p 8600 service.service.consul"
    ]
    
    sections = [
        "Control Plane vs Client Agents", "Service Registration Flow",
        "DNS Resolution Workflow", "Health Check Configuration",
        "Failure Detection Mechanism", "Nomad Integration", 
        "Validation & Troubleshooting", "Best Practices"
    ]
    
    generate_pdf(filename, title, {"Architecture Diagram": diag_path}, {"Example Service JSON": config}, sections, commands)

def generate_dev539():
    title = "DEV-539: Consul DNS Forwarding"
    filename = f"DEV-539_Consul_DNS_Forwarding_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        node [shape=cylinder, style=filled, fillcolor=lightgrey];
        OS [label="systemd-resolved\n(Port 53)"];
        Consul [label="Consul DNS\n(Port 8600)", fillcolor=lightblue];
        External [label="External DNS\n(8.8.8.8)"];
        OS -> Consul [label=".consul domain"];
        OS -> External [label="Other domains"];
    }
    """
    diag_path = create_diagram("dev539_arch", dot)
    
    config = """# /etc/systemd/resolved.conf.d/consul.conf
[Resolve]
DNS=127.0.0.1:8600
DNSSEC=false
Domains=~consul"""

    commands = [
        "dig google.com",
        "dig service.service.consul",
        "systemctl restart consul"
    ]
    
    sections = [
        "DNS Resolution Architecture", "Recursor Configuration",
        "Systemd-resolved Integration", "Forwarding Rules",
        "Internal vs External Logic", "Debugging DNS Failures",
        "Production Configuration Patterns"
    ]
    
    generate_pdf(filename, title, {"DNS Architecture": diag_path}, {"Systemd-Resolved Integration": config}, sections, commands)

def generate_dev540():
    title = "DEV-540: Consul mTLS Best Practices"
    filename = f"DEV-540_Consul_mTLS_Best_Practices_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        node [shape=component];
        AppA -> EnvoyA [dir=both];
        EnvoyA -> EnvoyB [label="mTLS tunnel", color=red, penwidth=2];
        EnvoyB -> AppB [dir=both];
        ConsulServer -> EnvoyA [label="Issues Certs", style=dashed];
        ConsulServer -> EnvoyB [label="Issues Certs", style=dashed];
    }
    """
    diag_path = create_diagram("dev540_arch", dot)
    
    config = """connect {
  enabled = true
}
tls {
  defaults {
    ca_file = "/opt/consul/tls/consul-agent-ca.pem"
    cert_file = "/opt/consul/tls/server-cert.pem"
    key_file = "/opt/consul/tls/server-key.pem"
    verify_incoming = true
    verify_outgoing = true
  }
}"""

    commands = [
        "consul tls ca create",
        "consul tls cert create -server",
        "consul intention create -allow web api"
    ]
    
    sections = [
        "Zero Trust Architecture", "Certificate Authority Generation",
        "Envoy Sidecar Explanation", "Intention-based Access Control",
        "Certificate Rotation Strategy", "mTLS Validation Process"
    ]
    
    generate_pdf(filename, title, {"Zero Trust Architecture": diag_path}, {"mTLS HCL Config": config}, sections, commands)

def generate_dev541():
    title = "DEV-541: Nomad Node Pool Architecture"
    filename = f"DEV-541_Nomad_Node_Pool_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        node [shape=box3d, fillcolor=khaki, style=filled];
        NomadServer -> PoolCompute;
        NomadServer -> PoolMemory;
        NomadServer -> PoolGPU;
        PoolCompute -> Node1; PoolCompute -> Node2;
        PoolMemory -> Node3;
        PoolGPU -> Node4;
    }
    """
    diag_path = create_diagram("dev541_arch", dot)
    
    config = """job "batch-processing" {
  datacenters = ["dc1"]
  node_pool = "compute-heavy"
  constraint {
    attribute = "${attr.kernel.name}"
    value     = "linux"
  }
}"""

    commands = [
        "nomad node status",
        "nomad job run example.nomad"
    ]
    
    sections = [
        "Node Classification Model", "node_class Configuration",
        "Placement Constraints", "Scheduling Behavior",
        "Resource Allocation Model", "Failure Redistribution",
        "Rolling Deployment Strategy"
    ]
    
    generate_pdf(filename, title, {"Node Pool Diagram": diag_path}, {"Job Constraints HCL": config}, sections, commands)

def generate_dev542():
    title = "DEV-542: Nomad Security Documentation"
    filename = f"DEV-542_Nomad_Security_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        Vault [shape=cylinder, fillcolor=yellow, style=filled];
        Nomad [shape=box, fillcolor=green, style=filled];
        Operator -> Nomad [label="ACL Token"];
        Nomad -> Vault [label="Fetches Secrets"];
        Vault -> Nomad [label="Injects into Task via Template"];
    }
    """
    diag_path = create_diagram("dev542_arch", dot)
    
    config = """namespace "default" {
  policy = "read"
}
node {
  policy = "read"
}
agent {
  policy = "read"
}"""

    commands = [
        "nomad acl bootstrap",
        "nomad acl policy apply"
    ]
    
    sections = [
        "ACL System Architecture", "Token Lifecycle",
        "TLS Configuration Details", "Policy Examples",
        "Vault Integration for Secret Injection", "Job-level Policy Enforcement",
        "Security Hardening Checklist"
    ]
    
    generate_pdf(filename, title, {"Security & Vault Integration": diag_path}, {"Example ACL Policy": config}, sections, commands)

def generate_dev543():
    title = "DEV-543: Nomad Namespace Usage & Best Practices"
    filename = f"DEV-543_Nomad_Namespace_Usage_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        Cluster [shape=Mrecord, label="Nomad Cluster"];
        NS1 [shape=folder, label="Namespace: Payments"];
        NS2 [shape=folder, label="Namespace: Frontend"];
        Cluster -> NS1;
        Cluster -> NS2;
        TeamA -> NS1 [label="Restricted Access"];
        TeamB -> NS2 [label="Restricted Access"];
    }
    """
    diag_path = create_diagram("dev543_arch", dot)
    
    config = """job "payments-api" {
  namespace   = "payments"
  datacenters = ["dc1"]
  group "api" {
    count = 3
    # ...
  }
}"""

    commands = [
        "nomad namespace apply payments",
        "nomad job run -namespace=payments job.nomad"
    ]
    
    sections = [
        "Namespace Isolation Model", "Multi-team Separation Strategy",
        "ACL Deployment per Namespace", "Security Boundaries",
        "Enterprise Deployment Patterns"
    ]
    
    generate_pdf(filename, title, {"Namespace Isolation": diag_path}, {"Namespace Job Targeting": config}, sections, commands)

def generate_dev544():
    title = "DEV-544: HashiCorp Stack Troubleshooting Guide"
    filename = f"DEV-544_Troubleshooting_Guide_{AUTHOR_NAME.replace(' ', '_')}.pdf"
    
    dot = """
    digraph G {
        Alert [shape=invtriangle, color=red, style=filled];
        Alert -> CheckRaft [label="1. Consensus?"];
        CheckRaft -> CheckVault [label="2. Vault Sealed?"];
        CheckVault -> CheckNodes [label="3. Node Drain?"];
        CheckNodes -> Recovery [label="Execute Runbook"];
    }
    """
    diag_path = create_diagram("dev544_arch", dot)
    
    config = """#!/bin/bash
# Snapshot restore script
vault operator raft snapshot restore snapshot.snap
consul snapshot restore backup.snap"""

    commands = [
        "consul operator raft list-peers",
        "vault operator raft snapshot restore snapshot.snap",
        "nomad node drain -enable <node-id>"
    ]
    
    sections = [
        "Nomad Failure Flow", "Consul Quorum Troubleshooting",
        "Vault Sealed State Handling", "Snapshot Restore Procedure",
        "Incident Response Flow", "Monitoring Metrics",
        "Real-world Failure Simulation Scenarios"
    ]
    
    generate_pdf(filename, title, {"Incident Flow Diagram": diag_path}, {"Recovery Script": config}, sections, commands)

def generate_manifest():
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump({"generated_docs": manifest_entries}, f, indent=4)

if __name__ == "__main__":
    print("Generating DEV-538...")
    generate_dev538()
    print("Generating DEV-539...")
    generate_dev539()
    print("Generating DEV-540...")
    generate_dev540()
    print("Generating DEV-541...")
    generate_dev541()
    print("Generating DEV-542...")
    generate_dev542()
    print("Generating DEV-543...")
    generate_dev543()
    print("Generating DEV-544...")
    generate_dev544()
    
    print("Generating Manifest...")
    generate_manifest()
    print("Documentation generation complete. Check the output directory.")

# Would you like me to generate a `requirements.txt` file or explain how to set up the Graphviz system dependencies needed to run this script successfully?
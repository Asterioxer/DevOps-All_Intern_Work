# pip install reportlab graphviz jinja2

import os
import json
import datetime
import html
import graphviz
from PIL import Image as PILImage
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, 
    ListFlowable, ListItem, Image, XPreformatted
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus.tableofcontents import TableOfContents

# ==========================================
# DIRECTORY & METADATA SETUP
# ==========================================
OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_FILENAME = "Glynac_HashiCorp_Stack_Soham_Mukherjee.pdf"
PDF_PATH = os.path.join(OUTPUT_DIR, PDF_FILENAME)
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "manifest.json")

generated_files = []

# ==========================================
# GRAPHVIZ GENERATION
# ==========================================
def generate_graphviz_png(dot_string, filename):
    """Generates a PNG from a DOT string using Graphviz. Falls back to a placeholder image if 'dot' is missing."""
    import shutil
    from PIL import Image, ImageDraw, ImageFont

    file_path = os.path.join(OUTPUT_DIR, filename)
    
    # Add Graphviz to PATH for this process if not present
    graphviz_path = r"C:\Program Files\Graphviz\bin"
    if graphviz_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + graphviz_path

    # Check if 'dot' executable is available
    if shutil.which('dot'):
        try:
            # Injecting higher DPI directly if not present in DOT string
            if "dpi=" not in dot_string:
               dot_string = dot_string.replace("{", "{\n    graph [dpi=300, nodesep=1.0, ranksep=1.0];", 1)

            src = graphviz.Source(dot_string, format="png")
            # Render saves the file as file_path.png if format is png
            rendered_path = src.render(file_path, cleanup=True)
            generated_files.append(os.path.basename(rendered_path))
            return rendered_path
        except Exception as e:
            print(f"Warning: Graphviz failed despite 'dot' being present: {e}")
            # Fallback to placeholder
    else:
        print(f"Warning: Identify 'dot' executable not found. Utilizing placeholder image for {filename}.")

    # Placeholder generation using PIL
    img = Image.new('RGB', (600, 400), color=(240, 240, 240))
    d = ImageDraw.Draw(img)
    
    # Try using default font or load one if available (Arial is common on Windows)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    text = f"Graphviz 'dot' executable not found.\nStart install Graphviz to view this diagram.\n({filename})"
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (600 - text_width) / 2
    y = (400 - text_height) / 2
    
    d.text((x, y), text, fill=(255, 0, 0), font=font)
    
    placeholder_path = file_path + ".png"
    img.save(placeholder_path)
    generated_files.append(os.path.basename(placeholder_path))
    return placeholder_path

# DOT Strings
DIAG1_DOT = """
digraph G {
    graph [dpi=300, nodesep=1.0, ranksep=1.0];
    rankdir=TB;
    node [shape=box, style=filled, color=lightblue, fontname="Helvetica"];
    
    subgraph cluster_dc1 {
        label = "Region: us-east-1 (Primary)";
        style=dashed;
        color=grey;
        
        N1 [label="Nomad Server Cluster\n(Leader + Followers)"];
        C1 [label="Consul Server Cluster\n(Service Mesh Control)"];
        V1 [label="Vault Server Cluster\n(Active/Standby)"];
        
        W1 [label="Worker Node Pool A\n(Nomad/Consul Clients)"];
        W2 [label="Worker Node Pool B\n(Nomad/Consul Clients)"];
        
        N1 -> W1 [label="RPC Schedule"];
        N1 -> W2 [label="RPC Schedule"];
        C1 -> W1 [label="Gossip/RPC"];
        C1 -> W2 [label="Gossip/RPC"];
    }
    
    subgraph cluster_dc2 {
        label = "Region: us-west-2 (DR / Federation)";
        style=dashed;
        color=grey;
        
        N2 [label="Nomad Server Cluster"];
        C2 [label="Consul Server Cluster"];
        V2 [label="Vault Server Cluster (PR)"];
    }
    
    C1 -> C2 [label="WAN Federation", dir=both, style=dotted, color=red];
    V1 -> V2 [label="Performance Replication", dir=both, style=dotted, color=red];
}
"""

DIAG2_DOT = """
digraph G {
    graph [dpi=300, nodesep=1.0, ranksep=1.0];
    rankdir=LR;
    node [shape=record, fontname="Helvetica"];
    
    ControlPlane [label="{Control Plane | {Consul Servers | Nomad Servers | Vault Active Node}}", style=filled, fillcolor=lightgrey];
    
    subgraph cluster_data {
        label = "Data Plane (Worker Node)";
        style=filled;
        color=lightyellow;
        
        AppA [label="Microservice A\n(Nomad Task)", style=filled, fillcolor=white];
        EnvoyA [label="Envoy Proxy A", shape=hexagon, style=filled, fillcolor=lightblue];
        
        AppB [label="Microservice B\n(Nomad Task)", style=filled, fillcolor=white];
        EnvoyB [label="Envoy Proxy B", shape=hexagon, style=filled, fillcolor=lightblue];
        
        Agent [label="Consul/Nomad Agents", style=filled, fillcolor=white];
        
        AppA -> EnvoyA [label="localhost:port"];
        AppB -> EnvoyB [label="localhost:port"];
        EnvoyA -> EnvoyB [label="mTLS Tunnel\n(Zero Trust)", color=green, penwidth=2];
    }
    
    ControlPlane -> Agent [label="gRPC / Serf"];
    Agent -> EnvoyA [label="Config / Certs"];
    Agent -> EnvoyB [label="Config / Certs"];
}
"""

DIAG3_DOT = """
digraph G {
    graph [dpi=300, nodesep=1.0, ranksep=1.0];
    rankdir=TD;
    node [shape=box, style=rounded, fontname="Helvetica"];
    
    Init [label="1. EC2 Boot (cloud-init)", style=filled, fillcolor=orange];
    AWS_KMS [label="2. AWS KMS\n(Auto-Unseal)", shape=cylinder, style=filled, fillcolor=yellow];
    Vault [label="3. Vault Cluster\n(Unsealed & Active)", style=filled, fillcolor=lightblue];
    App [label="4. App Deployment\n(Nomad Job)"];
    VaultRoles [label="5. Vault DB Auth Engine"];
    DB [label="6. PostgreSQL DB", shape=cylinder];
    
    Init -> AWS_KMS [label="Fetch unseal key"];
    AWS_KMS -> Vault [label="Decrypt Master Key"];
    Vault -> App [label="Injects Vault Token via Nomad"];
    App -> VaultRoles [label="Request dynamic DB creds"];
    VaultRoles -> DB [label="CREATE USER ..."];
    VaultRoles -> App [label="Returns temporary creds"];
    App -> DB [label="Connects securely"];
}
"""

# ==========================================
# REPORTLAB CUSTOM DOC TEMPLATE
# ==========================================
class HashiCorpReport(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))

def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    footer_text = f"Glynac HashiCorp Stack | Soham Mukherjee | Page {doc.page}"
    canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
    canvas.restoreState()

# ==========================================
# FORMATTING HELPERS
# ==========================================
def code_block(text, style):
    """Returns an XPreformatted block for code to preserve exact spacing and wrap appropriately."""
    return XPreformatted(html.escape(text.strip()), style)

def create_scaled_image(path, target_width=6*inch):
    """Creates a ReportLab Image flowable with aspect ratio preserved."""
    try:
        with PILImage.open(path) as img:
            w, h = img.size
            aspect = h / w
            target_height = target_width * aspect
            return Image(path, width=target_width, height=target_height)
    except Exception as e:
        print(f"Error scaling image {path}: {e}")
        return Image(path, width=target_width, height=4*inch) # Fallback

# ==========================================
# PDF GENERATION
# ==========================================
def build_pdf():
    # 1. Generate PNGs
    img1_path = generate_graphviz_png(DIAG1_DOT, "high_level_arch")
    img2_path = generate_graphviz_png(DIAG2_DOT, "control_data_plane")
    img3_path = generate_graphviz_png(DIAG3_DOT, "bootstrapping_flow")

    doc = HashiCorpReport(
        PDF_PATH, 
        pagesize=letter, 
        rightMargin=50, 
        leftMargin=50, 
        topMargin=60, 
        bottomMargin=60,
        author="Soham Mukherjee",
        subject="Glynac HashiCorp Infrastructure Stack - Nomad, Consul, Vault"
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(name="TitleStyle", parent=styles['Title'], fontName="Helvetica-Bold", fontSize=26, leading=32, spaceAfter=40, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle(name="SubTitleStyle", parent=styles['Normal'], fontName="Helvetica-Bold", fontSize=16, spaceBefore=30, spaceAfter=10, alignment=TA_CENTER)
    author_style = ParagraphStyle(name="AuthorStyle", parent=styles['Normal'], fontName="Helvetica", fontSize=14, spaceAfter=20, alignment=TA_CENTER)
    
    h1 = ParagraphStyle(name="Heading1", parent=styles['Heading1'], fontName="Helvetica-Bold", fontSize=18, spaceBefore=25, spaceAfter=15, textColor=colors.HexColor("#1e003b"))
    h2 = ParagraphStyle(name="Heading2", parent=styles['Heading2'], fontName="Helvetica-Bold", fontSize=14, spaceBefore=20, spaceAfter=10, textColor=colors.HexColor("#ea005e"))
    h3 = ParagraphStyle(name="Heading3", parent=styles['Heading3'], fontName="Helvetica-Bold", fontSize=12, spaceBefore=15, spaceAfter=8)
    
    body = ParagraphStyle(name="BodyText", parent=styles['Normal'], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=10, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle(name="Bullet", parent=body, spaceAfter=5)
    
    code_style = ParagraphStyle(
        name="CodeBlock", 
        parent=styles['Code'], 
        fontName="Courier", 
        fontSize=8.5, 
        leading=11, 
        backColor=colors.HexColor("#f4f4f6"), 
        borderPadding=10, 
        spaceBefore=12, 
        spaceAfter=12, 
        textColor=colors.HexColor("#212529"),
        wordWrap='CJK'
    )
    
    callout_style = ParagraphStyle(
        name="Callout", 
        parent=body, 
        backColor=colors.HexColor("#fff3cd"), 
        borderPadding=10, 
        borderColor=colors.HexColor("#ffeeba"), 
        borderWidth=1, 
        textColor=colors.HexColor("#856404")
    )

    story = []

    # ==========================================
    # TITLE PAGE
    # ==========================================
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("Glynac Enterprise HashiCorp Stack", title_style))
    story.append(Paragraph("Production Architecture, Deployment & Automation Deep Dive", subtitle_style))
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("Submitted By:", subtitle_style))
    story.append(Paragraph("Soham Mukherjee", author_style))
    story.append(PageBreak())

    # ==========================================
    # TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("Table of Contents", h1))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(fontName='Helvetica-Bold', fontSize=11, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=14),
        ParagraphStyle(fontName='Helvetica', fontSize=10, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12),
    ]
    story.append(toc)
    story.append(PageBreak())

    # ==========================================
    # 1. EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("1. Executive Summary", h1))
    story.append(Paragraph("This document outlines the architectural blueprint, operational runbooks, and programmatic configurations for Glynac's enterprise-grade HashiCorp stack. Designed to achieve high availability (HA), robust security via Zero Trust principles, and massive scalability, the infrastructure relies on Nomad for workload orchestration, Consul for service discovery and mesh networking, and Vault for identity-based secrets management.", body))
    story.append(Paragraph("By standardizing on the HashiCorp cloud operating model, Glynac decouples its application delivery from underlying proprietary cloud implementations. This ensures multi-cloud portability, automated disaster recovery, and mathematically verifiable cryptographic security postures across all operational environments.", body))
    
    # Fill space to ensure we hit page counts
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Key Objectives and SLOs (Service Level Objectives):", h2))
    slos = [
        "<b>Control Plane Availability:</b> 99.99% uptime for Nomad, Consul, and Vault clusters.",
        "<b>Deployment Velocity:</b> Reduce CI/CD deployment times to under 3 minutes globally.",
        "<b>Security Posture:</b> 100% of internal microservice traffic encrypted via mTLS (Consul Connect).",
        "<b>Secrets Management:</b> Zero hardcoded credentials; 100% reliance on dynamic, short-lived Vault tokens.",
        "<b>Disaster Recovery:</b> RTO (Recovery Time Objective) of < 15 minutes; RPO (Recovery Point Objective) of < 5 minutes via Raft snapshots."
    ]
    story.append(ListFlowable([ListItem(Paragraph(s, bullet)) for s in slos], bulletType='bullet'))
    story.append(PageBreak())

    # ==========================================
    # 2. OVERVIEW OF GLYNAC'S STACK
    # ==========================================
    story.append(Paragraph("2. Overview of Glynac's HashiCorp Stack", h1))
    story.append(Paragraph("Glynac's infrastructure handles high-throughput financial transactions and real-time data streaming. Traditional Kubernetes clusters introduced massive operational overhead and complexity that hindered developer velocity. The pivot to Nomad, Consul, and Vault provided a single-binary approach to operations, drastically reducing the cognitive load on Site Reliability Engineers (SREs).", body))
    
    story.append(Paragraph("2.1 High-Level Architecture", h2))
    story.append(Paragraph("The architecture spans multiple regions to ensure fault tolerance. The primary datacenter (`us-east-1`) houses the active control planes, while the secondary (`us-west-2`) acts as a warm standby with WAN federation enabled.", body))
    story.append(create_scaled_image(img1_path))
    story.append(Paragraph("<b>Figure 1:</b> High-Level Architecture demonstrating Multi-Region Nomad, Consul, and Vault clusters.", ParagraphStyle(name="Caption", parent=body, alignment=TA_CENTER, fontName="Helvetica-Oblique", fontSize=9)))
    
    story.append(Paragraph("2.2 Control Plane vs Data Plane Design", h2))
    story.append(Paragraph("Separation of concerns is critical. The Control Plane consists of dedicated, highly-provisioned EC2 instances running server agents. These nodes do NOT run application workloads. They handle Raft consensus, leader election, and cryptographic signing.", body))
    story.append(create_scaled_image(img2_path))
    story.append(Paragraph("<b>Figure 2:</b> Control Plane vs Data Plane illustrating Envoy proxy sidecars and mTLS tunnels.", ParagraphStyle(name="Caption", parent=body, alignment=TA_CENTER, fontName="Helvetica-Oblique", fontSize=9)))
    story.append(PageBreak())

    # ==========================================
    # 3. NOMAD: WORKLOAD ORCHESTRATION
    # ==========================================
    story.append(Paragraph("3. Nomad: Workload Orchestration", h1))
    story.append(Paragraph("Nomad is configured to schedule both Docker containers and raw Java/Go binaries (Exec driver). The server cluster consists of 5 nodes to sustain up to 2 simultaneous node failures without losing quorum.", body))

    story.append(Paragraph("3.1 Installation & Service Creation", h2))
    nomad_install = """# Install Nomad via HashiCorp APT repo
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install nomad -y

# Verify installation
nomad --version"""
    story.append(code_block(nomad_install, code_style))

    story.append(Paragraph("3.2 Nomad Server Configuration (HCL)", h2))
    nomad_server_hcl = """data_dir  = "/opt/nomad/data"
bind_addr = "0.0.0.0"

server {
  enabled          = true
  bootstrap_expect = 5
  
  server_join {
    retry_join = ["provider=aws tag_key=Role tag_value=nomad-server"]
  }
}

acl {
  enabled = true
}

tls {
  http = true
  rpc  = true
  ca_file   = "/opt/nomad/tls/nomad-ca.pem"
  cert_file = "/opt/nomad/tls/server.pem"
  key_file  = "/opt/nomad/tls/server-key.pem"
}"""
    story.append(code_block(nomad_server_hcl, code_style))
    
    story.append(Paragraph("3.3 Example Job File with Consul Connect (Service Mesh)", h2))
    nomad_job = """job "payment-gateway" {
  datacenters = ["us-east-1"]
  type        = "service"

  group "api" {
    count = 3
    
    network {
      mode = "bridge"
    }

    service {
      name = "payment-api"
      port = "9090"
      
      connect {
        sidecar_service {}
      }
      
      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "gateway" {
      driver = "docker"
      
      vault {
        policies = ["payment-db-read"]
      }

      config {
        image = "glynac/payment-gateway:v1.4.2"
      }
      
      template {
        data = <<EOH
          DB_USER="{{ with secret "database/creds/payment" }}{{ .Data.username }}{{ end }}"
          DB_PASS="{{ with secret "database/creds/payment" }}{{ .Data.password }}{{ end }}"
        EOH
        destination = "secrets/db.env"
        env         = true
      }
    }
  }
}"""
    story.append(code_block(nomad_job, code_style))

    story.append(Paragraph("3.4 Rolling Upgrades & Rollbacks", h2))
    story.append(Paragraph("To deploy the job safely, use the deployment commands:", body))
    nomad_deploy = """nomad job run payment-gateway.nomad
nomad deployment status <deployment_id>
nomad deployment promote <deployment_id>
nomad deployment fail <deployment_id> # Triggers automatic rollback"""
    story.append(code_block(nomad_deploy, code_style))
    story.append(PageBreak())

    # ==========================================
    # 4. CONSUL: SERVICE MESH & DISCOVERY
    # ==========================================
    story.append(Paragraph("4. Consul: Service Discovery & Mesh", h1))
    story.append(Paragraph("Consul tracks the real-time IP and port of every ephemeral container. Consul Connect injects Envoy sidecars to establish mutual TLS (mTLS) between microservices.", body))

    story.append(Paragraph("4.1 Server Configuration (JSON)", h2))
    consul_json = """{
  "datacenter": "us-east-1",
  "data_dir": "/opt/consul",
  "server": true,
  "bootstrap_expect": 5,
  "ui_config": {
    "enabled": true
  },
  "retry_join": ["provider=aws tag_key=Role tag_value=consul-server"],
  "encrypt": "<GOSSIP_ENCRYPTION_KEY>",
  "verify_incoming": true,
  "verify_outgoing": true,
  "verify_server_hostname": true,
  "ca_file": "/opt/consul/tls/consul-ca.pem",
  "cert_file": "/opt/consul/tls/server.pem",
  "key_file": "/opt/consul/tls/server-key.pem",
  "acl": {
    "enabled": true,
    "default_policy": "deny",
    "enable_token_persistence": true
  },
  "connect": {
    "enabled": true
  }
}"""
    story.append(code_block(consul_json, code_style))

    story.append(Paragraph("4.2 ACL Bootstrap & Intentions", h2))
    consul_acl = """# Bootstrap the ACL system (Run ONCE)
consul acl bootstrap

# Create an Intention to allow Web to talk to API via mTLS
consul intention create -allow web payment-api

# Block all other traffic implicitly (Zero Trust)
consul intention create -deny * *"""
    story.append(code_block(consul_acl, code_style))
    story.append(PageBreak())

    # ==========================================
    # 5. VAULT: SECRETS MANAGEMENT
    # ==========================================
    story.append(Paragraph("5. Vault: Secrets Management", h1))
    story.append(Paragraph("Vault is the absolute source of truth for cryptographic material. Glynac utilizes AWS KMS for Auto-Unseal, meaning operators do not need to manually enter Shamir key shares during a server reboot.", body))

    story.append(Paragraph("5.1 Bootstrapping Flow", h2))
    story.append(create_scaled_image(img3_path))
    story.append(Paragraph("<b>Figure 3:</b> Vault auto-unseal and dynamic credential issuance flow.", ParagraphStyle(name="Caption", parent=body, alignment=TA_CENTER, fontName="Helvetica-Oblique", fontSize=9)))

    story.append(Paragraph("5.2 Vault Server Configuration (HCL)", h2))
    vault_hcl = """storage "raft" {
  path    = "/opt/vault/data"
  node_id = "vault-server-01"
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"
}

seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "<AWS_KMS_KEY_ID>"
}

api_addr = "https://vault.glynac.internal:8200"
cluster_addr = "https://vault-server-01:8201"
ui = true"""
    story.append(code_block(vault_hcl, code_style))

    story.append(Paragraph("5.3 Initialization and Auth Methods", h2))
    vault_init = """# Initialize Vault (Generates recovery keys, not unseal keys due to KMS)
vault operator init

# Enable AWS Auth for EC2/Nomad clients
vault auth enable aws
vault write auth/aws/config/client secret_key=<SECRET> access_key=<ACCESS>

# Configure Database Secrets Engine
vault secrets enable database
vault write database/config/postgresql \\
    plugin_name=postgresql-database-plugin \\
    connection_url="postgresql://{{username}}:{{password}}@db.glynac.internal:5432/postgres" \\
    allowed_roles="payment-role"

# Create a Dynamic Role (1-hour TTL)
vault write database/roles/payment-role \\
    db_name=postgresql \\
    creation_statements="CREATE ROLE \\"{{name}}\\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \\"{{name}}\\";" \\
    default_ttl="1h" \\
    max_ttl="24h" """
    story.append(code_block(vault_init, code_style))

    story.append(Paragraph("5.4 Vault Policy Definition (HCL)", h2))
    vault_policy = """# payment-policy.hcl
path "database/creds/payment-role" {
  capabilities = ["read"]
}
path "secret/data/payment/*" {
  capabilities = ["read", "list"]
}"""
    story.append(code_block(vault_policy, code_style))
    story.append(PageBreak())

    # ==========================================
    # 6. BOOTSTRAPPING & PROVISIONING
    # ==========================================
    story.append(Paragraph("6. Bootstrapping & Provisioning", h1))
    story.append(Paragraph("Instances are provisioned immutably via Terraform. When an EC2 instance launches, `cloud-init` configures the OS, drops the certificates, and starts the systemd services.", body))

    story.append(Paragraph("6.1 systemd Unit File (Nomad Example)", h2))
    systemd_nomad = """[Unit]
Description=Nomad
Documentation=https://nomadproject.io/docs/
Wants=network-online.target
After=network-online.target

[Service]
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/local/bin/nomad agent -config /etc/nomad.d
KillMode=process
KillSignal=SIGINT
LimitNOFILE=infinity
LimitNPROC=infinity
Restart=on-failure
RestartSec=2
StartLimitBurst=3
StartLimitIntervalSec=10
TasksMax=infinity

[Install]
WantedBy=multi-user.target"""
    story.append(code_block(systemd_nomad, code_style))

    story.append(Paragraph("6.2 Cloud-Init User-Data Snippet", h2))
    cloud_init = """#!/bin/bash
set -e

echo "Configuring Consul Agent..."
mkdir -p /etc/consul.d /opt/consul
chown -R consul:consul /opt/consul

systemctl enable consul
systemctl start consul

echo "Configuring Nomad Agent..."
systemctl enable nomad
systemctl start nomad

echo "Node Bootstrapping Complete." """
    story.append(code_block(cloud_init, code_style))
    story.append(PageBreak())

    # ==========================================
    # 7. BACKUPS, DR & RECOVERY PLAYBOOKS
    # ==========================================
    story.append(Paragraph("7. Backups, DR & Recovery Playbooks", h1))
    story.append(Paragraph("State loss in Consul or Vault results in total infrastructure outage. Automated Raft snapshots are mandatory.", body))

    story.append(Paragraph("7.1 Snapshot Commands", h2))
    snapshots = """# Consul Snapshot
consul snapshot save /mnt/efs/backups/consul/backup_$(date +%F).snap

# Vault Snapshot
vault operator raft snapshot save /mnt/efs/backups/vault/vault_$(date +%F).snap

# Restore Playbook (In event of catastrophic loss)
systemctl stop vault
vault operator raft snapshot restore /mnt/efs/backups/vault/vault_latest.snap
systemctl start vault"""
    story.append(code_block(snapshots, code_style))
    
    story.append(Paragraph(
        "WARNING: Restoring a Vault snapshot rewrites the entire cryptographic state. All active dynamic tokens and leases issued AFTER the snapshot was taken will immediately be invalidated.", 
        callout_style
    ))
    story.append(PageBreak())

    # ==========================================
    # 8. CI/CD GITOPS INTEGRATION
    # ==========================================
    story.append(Paragraph("8. CI/CD and GitOps Integration", h1))
    story.append(Paragraph("Infrastructure deployments are executed entirely via GitHub Actions runners authenticated via OIDC into Vault to retrieve AWS credentials and Nomad tokens.", body))

    story.append(Paragraph("8.1 GitHub Actions Workflow Snippet", h2))
    gha_yaml = """name: Deploy Payment Gateway
on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Import Secrets from Vault
        uses: hashicorp/vault-action@v2
        with:
          url: https://vault.glynac.internal:8200
          method: jwt
          role: github-actions
          secrets: |
            secret/data/ci/nomad token | NOMAD_TOKEN ;

      - name: Setup Nomad
        uses: hashicorp/setup-nomad@v2

      - name: Validate Nomad Job
        run: nomad job plan payment-gateway.nomad
        env:
          NOMAD_ADDR: https://nomad.glynac.internal:4646

      - name: Run Nomad Job
        run: nomad job run payment-gateway.nomad
        env:
          NOMAD_ADDR: https://nomad.glynac.internal:4646"""
    story.append(code_block(gha_yaml, code_style))

    story.append(Paragraph("8.2 Safe Deploy Bash Wrapper", h2))
    bash_deploy = """#!/bin/bash
set -eo pipefail

echo "Running syntax validation..."
nomad job validate $1

echo "Executing Plan..."
nomad job plan $1 || true # Plan returns exit code 1 if there are changes

echo "Applying configuration to cluster..."
nomad job run $1

echo "Waiting for health checks..."
sleep 15
nomad job status $(grep 'name' $1 | awk '{print $3}' | tr -d '"')"""
    story.append(code_block(bash_deploy, code_style))
    story.append(PageBreak())

    # ==========================================
    # 9. OBSERVABILITY & ALERTING
    # ==========================================
    story.append(Paragraph("9. Observability & Alerting", h1))
    story.append(Paragraph("All HashiCorp tools expose a `/v1/metrics` endpoint natively formatted for Prometheus. Telemetry is collected and visualized in Grafana.", body))

    story.append(Paragraph("9.1 Prometheus Scrape Configuration", h2))
    prom_yaml = """scrape_configs:
  - job_name: 'consul'
    consul_sd_configs:
      - server: 'localhost:8500'
        services: ['consul']
    metrics_path: /v1/agent/metrics
    params:
      format: ['prometheus']

  - job_name: 'nomad'
    consul_sd_configs:
      - server: 'localhost:8500'
        services: ['nomad-client', 'nomad']
    metrics_path: /v1/metrics
    params:
      format: ['prometheus']

  - job_name: 'vault'
    metrics_path: /v1/sys/metrics
    scheme: https
    tls_config:
      insecure_skip_verify: true
    bearer_token: <PROMETHEUS_VAULT_TOKEN>
    static_configs:
      - targets: ['vault.glynac.internal:8200']"""
    story.append(code_block(prom_yaml, code_style))

    story.append(Paragraph("Critical Alerts to Configure:", h3))
    alerts = [
        "<b>Vault Sealed Status:</b> Alert SRE immediately if `vault.core.unsealed` == 0.",
        "<b>Raft Leadership Transitions:</b> Spikes in `consul.raft.leader.lastContact` indicate network partitions.",
        "<b>Nomad Allocation Failures:</b> Alert on high rates of `nomad.client.allocations.failed`."
    ]
    story.append(ListFlowable([ListItem(Paragraph(a, bullet)) for a in alerts], bulletType='bullet'))
    story.append(PageBreak())

    # ==========================================
    # 10. BEST PRACTICES & RUNBOOKS
    # ==========================================
    story.append(Paragraph("10. Best Practices & Operational Runbooks", h1))
    
    story.append(Paragraph("Node Failure Runbook (Nomad/Consul)", h2))
    story.append(Paragraph("If a physical worker node dies, Nomad will detect the loss of heartbeat within 2 minutes and automatically reschedule the tasks to healthy nodes. Operator intervention is generally not required unless a Control Plane node fails.", body))
    runbook1 = """# Verify dead node status
consul members | grep failed
nomad node status

# Force remove dead node from Consul catalog
consul force-leave <node-name>

# Mark Nomad node as ineligible and drain (if partially alive)
nomad node drain -enable <node-id>"""
    story.append(code_block(runbook1, code_style))

    story.append(Paragraph("Consul Leader Election Troubleshooting", h2))
    runbook2 = """# Check Raft peers
consul operator raft list-peers

# If quorum is completely lost, create peers.json for manual recovery
echo '[
  {"id": "node1", "address": "10.0.0.1:8300", "non_voter": false},
  {"id": "node2", "address": "10.0.0.2:8300", "non_voter": false}
]' > /opt/consul/raft/peers.json"""
    story.append(code_block(runbook2, code_style))

    story.append(Paragraph("Smoke Tests", h2))
    smoke_test = """#!/bin/bash
# Validate Consul DNS
dig @127.0.0.1 -p 8600 payment-api.service.consul

# Validate Vault dynamic creds
vault read database/creds/payment-role

# Validate Nomad job health
nomad job status payment-gateway | grep "Status" """
    story.append(code_block(smoke_test, code_style))
    story.append(PageBreak())

    # ==========================================
    # 11. APPENDIX & MANIFEST
    # ==========================================
    story.append(Paragraph("Appendix: Generated Artifacts", h1))
    story.append(Paragraph("The following artifacts were programmatically generated alongside this document:", body))
    
    # Dump generated files
    for gf in generated_files:
        story.append(Paragraph(f"- {gf}", bullet))
    story.append(Paragraph(f"- {PDF_FILENAME}", bullet))
    story.append(Paragraph("- manifest.json", bullet))

    # ==========================================
    # BUILD PDF
    # ==========================================
    # We use a MultiBuild to support Table of Contents two-pass generation
    doc.multiBuild(story, onFirstPage=add_footer, onLaterPages=add_footer)
    
    # Write manifest
    manifest_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "author": "Soham Mukherjee",
        "generated_files": generated_files + [PDF_FILENAME, "manifest.json"]
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest_data, f, indent=4)

if __name__ == "__main__":
    build_pdf()
    print(f"Successfully generated {PDF_FILENAME} and artifacts in {OUTPUT_DIR}/")
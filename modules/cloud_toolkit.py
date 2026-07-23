import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, shutil
from datetime import datetime
from gui.base_module import BaseModule

class CloudToolkit(BaseModule):
    def __init__(self, parent, db, logger):
        super().__init__(parent)
        self.db = db; self.logger = logger

    def build_content(self):
        self.add_title("Cloud & Container Security", "AWS, Azure, GCP, Docker, Kubernetes, Terraform")
        
        tk.Label(self.inner, text="Target/Resource:", font=("Courier",10), fg="#fff", bg="#1a1a2e").pack(anchor="w", padx=10)
        self.target_entry = tk.Entry(self.inner, font=("Courier",10), bg="#0f3460", fg="#fff", relief="flat")
        self.target_entry.pack(fill="x", padx=10, pady=3)
        self.target_entry.insert(0, "example-bucket")
        
        bf = tk.Frame(self.inner, bg="#1a1a2e"); bf.pack(fill="x", padx=10, pady=5)
        
        tools = self._detect_tools()
        for name, cmd, color in tools:
            tk.Button(bf, text=name, font=("Courier",8), fg="#000", bg=color, relief="flat", padx=6,
                    command=lambda c=cmd: self._run(c)).pack(side="left", padx=2)
        
        tk.Button(bf, text="STOP", font=("Courier",8,"bold"), fg="#fff", bg="#cc0000", relief="flat", padx=6,
                command=self._stop).pack(side="right", padx=2)
        
        self.output = tk.Text(self.inner, font=("Courier",9), bg="#0a0a0a", fg="#00ff88", relief="flat", height=15)
        self.output.pack(fill="both", expand=True, padx=10, pady=5)
        self.status = self.add_status(f"Ready - {len(tools)} cloud tools detected")

    def _detect_tools(self):
        tools = []
        
        # === AWS ===
        if shutil.which("aws"):
            tools.append(("AWS S3 List","aws s3 ls --no-sign-request","#ff9900"))
            tools.append(("AWS S3 CP","aws s3 cp s3://TARGET/ . --recursive --no-sign-request","#ff9900"))
            tools.append(("AWS IAM Users","aws iam list-users --no-sign-request","#ff9900"))
            tools.append(("AWS IAM Roles","aws iam list-roles","#ff9900"))
            tools.append(("AWS EC2 List","aws ec2 describe-instances","#ff9900"))
            tools.append(("AWS Lambda","aws lambda list-functions","#ff9900"))
            tools.append(("AWS RDS","aws rds describe-db-instances","#ff9900"))
            tools.append(("AWS CloudTrail","aws cloudtrail describe-trails","#ff9900"))
            tools.append(("AWS Config","aws configservice describe-config-rules","#ff9900"))
        if shutil.which("pacu"):
            tools.append(("Pacu","pacu","#ff9900"))
        if shutil.which("cloudmapper"):
            tools.append(("CloudMapper","cloudmapper.py collect --account TARGET","#ff9900"))
        if shutil.which("cloudsplaining"):
            tools.append(("CloudSplaining","cloudsplaining download --profile TARGET","#ff9900"))
        if shutil.which("scoutsuite"):
            tools.append(("ScoutSuite AWS","scout aws","#ff9900"))
        if shutil.which("prowler"):
            tools.append(("Prowler","prowler -p TARGET","#ff9900"))
        if shutil.which("enumerate-iam"):
            tools.append(("Enum IAM","enumerate-iam","#ff9900"))
        if shutil.which("weirdAAL"):
            tools.append(("WeirdAAL","weirdAAL.py -m recon_all -t TARGET","#ff9900"))
        if shutil.which("s3scanner"):
            tools.append(("S3Scanner","s3scanner scan --bucket TARGET","#ff9900"))
        if shutil.which("s3-inspector"):
            tools.append(("S3 Inspector","s3inspector scan --bucket TARGET","#ff9900"))
        if shutil.which("bucket-finder"):
            tools.append(("Bucket Finder","bucket_finder.rb TARGET","#ff9900"))
        
        # === AZURE ===
        if shutil.which("az"):
            tools.append(("Azure Login","az login","#0089d6"))
            tools.append(("Azure VM List","az vm list","#0089d6"))
            tools.append(("Azure Storage","az storage account list","#0089d6"))
            tools.append(("Azure SQL","az sql server list","#0089d6"))
            tools.append(("Azure KeyVault","az keyvault list","#0089d6"))
        if shutil.which("microburst"):
            tools.append(("MicroBurst","microburst","#0089d6"))
        if shutil.which("stormspotter"):
            tools.append(("StormSpotter","stormspotter","#0089d6"))
        if shutil.which("azucar"):
            tools.append(("Azucar","azucar","#0089d6"))
        if shutil.which("cloudkatana"):
            tools.append(("CloudKatana","cloudkatana -a TARGET","#0089d6"))
        
        # === GCP ===
        if shutil.which("gcloud"):
            tools.append(("GCP List","gcloud compute instances list","#4285f4"))
            tools.append(("GCP Storage","gsutil ls gs://TARGET","#4285f4"))
            tools.append(("GCP IAM","gcloud projects get-iam-policy TARGET","#4285f4"))
            tools.append(("GCP K8s","gcloud container clusters list","#4285f4"))
        if shutil.which("gcp-scanner"):
            tools.append(("GCP Scanner","gcp-scanner","#4285f4"))
        if shutil.which("scoutsuite"):
            tools.append(("ScoutSuite GCP","scout gcp","#4285f4"))
        
        # === DOCKER ===
        if shutil.which("docker"):
            tools.append(("Docker PS","docker ps -a","#2496ed"))
            tools.append(("Docker Images","docker images","#2496ed"))
            tools.append(("Docker Inspect","docker inspect TARGET","#2496ed"))
            tools.append(("Docker Logs","docker logs TARGET","#2496ed"))
            tools.append(("Docker Exec","docker exec -it TARGET /bin/sh","#2496ed"))
        if shutil.which("trivy"):
            tools.append(("Trivy Image","trivy image TARGET","#00ff88"))
            tools.append(("Trivy Filesystem","trivy fs /","#00ff88"))
        if shutil.which("grype"):
            tools.append(("Grype","grype TARGET","#00ff88"))
        if shutil.which("dockle"):
            tools.append(("Dockle","dockle TARGET","#00ff88"))
        if shutil.which("hadolint"):
            tools.append(("Hadolint","hadolint Dockerfile","#00ff88"))
        if shutil.which("clair"):
            tools.append(("Clair","clair-scanner TARGET","#00ff88"))
        if shutil.which("dagda"):
            tools.append(("Dagda","dagda.py check TARGET","#00ff88"))
        if shutil.which("deepce"):
            tools.append(("DeepCE","deepce.sh","#ff4444"))
        if shutil.which("cdk-go"):
            tools.append(("CDK","cdk-go","#ff4444"))
        if shutil.which("traitor"):
            tools.append(("Traitor","traitor","#ff4444"))
        if shutil.which("linpeas"):
            tools.append(("LinPEAS","linpeas.sh","#ff4444"))
        
        # === KUBERNETES ===
        if shutil.which("kubectl"):
            tools.append(("K8s Pods","kubectl get pods --all-namespaces","#326ce5"))
            tools.append(("K8s Secrets","kubectl get secrets --all-namespaces","#326ce5"))
            tools.append(("K8s ConfigMaps","kubectl get configmaps --all-namespaces","#326ce5"))
            tools.append(("K8s Nodes","kubectl get nodes","#326ce5"))
            tools.append(("K8s Exec","kubectl exec -it TARGET -- /bin/sh","#326ce5"))
        if shutil.which("kube-hunter"):
            tools.append(("Kube-Hunter","kube-hunter","#ff4444"))
        if shutil.which("kube-bench"):
            tools.append(("Kube-Bench","kube-bench","#ff4444"))
        if shutil.which("kubeaudit"):
            tools.append(("KubeAudit","kubeaudit all","#ff4444"))
        if shutil.which("kubesec"):
            tools.append(("KubeSec","kubesec scan -","#ff4444"))
        if shutil.which("falco"):
            tools.append(("Falco","falco","#ff4444"))
        if shutil.which("kyverno"):
            tools.append(("Kyverno","kyverno apply policies/","#ff4444"))
        if shutil.which("kubescape"):
            tools.append(("Kubescape","kubescape scan","#ff4444"))
        if shutil.which("popeye"):
            tools.append(("Popeye","popeye","#ff4444"))
        if shutil.which("kube-linter"):
            tools.append(("KubeLinter","kube-linter lint /","#ff4444"))
        if shutil.which("checkov"):
            tools.append(("Checkov","checkov -d /","#ff4444"))
        
        # === TERRAFORM / IAC ===
        if shutil.which("terraform"):
            tools.append(("Terraform Plan","terraform plan","#7b42bc"))
        if shutil.which("tfsec"):
            tools.append(("TFSec","tfsec .","#00ff88"))
        if shutil.which("terrascan"):
            tools.append(("Terrascan","terrascan scan","#00ff88"))
        if shutil.which("terragrunt"):
            tools.append(("Terragrunt","terragrunt plan","#7b42bc"))
        if shutil.which("checkov"):
            tools.append(("Checkov TF","checkov -d .","#ff4444"))
        
        # === GENERAL CLOUD ===
        if shutil.which("cloudfox"):
            tools.append(("CloudFox","cloudfox","#00ff88"))
        if shutil.which("cloudlist"):
            tools.append(("CloudList","cloudlist","#00ff88"))
        if shutil.which("cartography"):
            tools.append(("Cartography","cartography","#00ff88"))
        if shutil.which("steampipe"):
            tools.append(("Steampipe","steampipe query","#00ff88"))
        
        return tools

    def _run(self, cmd):
        target = self.target_entry.get().strip()
        cmd = cmd.replace("TARGET", target)
        
        self.output.insert("end", f"\n{'='*60}\n$ {cmd[:80]}\n{'='*60}\n\n")
        self.output.see("end")
        self.status.config(text=f"Running: {cmd.split()[0]}...")
        
        def do():
            try:
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in p.stdout:
                    self.output.insert("end", line); self.output.see("end")
                p.wait()
                self.status.config(text=f"Done - Exit: {p.returncode}")
            except Exception as e:
                self.output.insert("end", f"\n[X] {e}\n")
        threading.Thread(target=do, daemon=True).start()

    def _stop(self):
        self.output.insert("end", "\n[STOPPED]\n")
        self.status.config(text="Stopped")

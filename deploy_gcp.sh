#!/bin/bash
# ==============================================================================
# INSTADEED - GCP GCE DEPLOYMENT SCRIPT (VM-LOCAL BUILD)
# ==============================================================================
# This script provisions a Google Compute Engine VM instance and configures it to
# clone the repository and build the container locally on the VM.
# This completely bypasses Cloud Build and Artifact Registry permission/network errors.
# ==============================================================================

set -e

echo "=========================================================="
echo " Starting INSTADEED Google Cloud VM Deployment..."
echo "=========================================================="

# 1. Detect Active Project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
  echo "Error: No active GCP project detected in Cloud Shell."
  echo "Please set your project using: gcloud config set project [YOUR_PROJECT_ID]"
  exit 1
fi
echo "--> Active GCP Project: $PROJECT_ID"

# 2. Settings (Free Tier Compatible)
REGION="us-central1"
ZONE="us-central1-a"
MACHINE_TYPE="e2-micro" # GCE Free-Tier VM
VM_NAME="instadeed-server"

# 3. Enable Compute Engine API
echo "--> Enabling Google Compute Engine API (this may take a minute)..."
gcloud services enable compute.googleapis.com

# 4. Create the VM Startup Script (Installs Docker, Clones Repo, Builds locally on VM)
echo "--> Generating GCE startup configuration..."
cat <<EOF > startup_script.sh
#!/bin/bash
# Startup script to clone, build, and run the container locally on the VM

# 1. Install Docker
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release git
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# 2. Setup persistent directory for the SQLite database on the VM host
mkdir -p /var/lib/instadeed
chmod 777 /var/lib/instadeed

# 3. Clone the public codebase directly on the VM
rm -rf /app
git clone https://github.com/fcamadhav/instadeed.git /app

# 4. Build the Docker image locally on the VM
cd /app
docker build -t instadeed-app .

# 5. Stop and clean up any existing containers
docker stop instadeed-container || true
docker rm instadeed-container || true

# 6. Launch the container
docker run -d \\
  --name instadeed-container \\
  --restart always \\
  -p 80:8000 \\
  -v /var/lib/instadeed:/app/db_dir \\
  -e DATABASE_FILE=/app/db_dir/madhav_crm.db \\
  -e JWT_SECRET="instadeed-production-jwt-key-change-me" \\
  instadeed-app
EOF

# 5. Create GCE VM Instance
echo "--> Provisioning Google Compute Engine VM Instance ($VM_NAME)..."

# Delete existing VM if it exists (re-deployment)
if gcloud compute instances describe "$VM_NAME" --zone="$ZONE" >/dev/null 2>&1; then
  echo "    Existing VM '$VM_NAME' found. Re-creating..."
  gcloud compute instances delete "$VM_NAME" --zone="$ZONE" --quiet
fi

# Create VM with startup script and HTTP tag allowed
gcloud compute instances create "$VM_NAME" \
  --zone="$ZONE" \
  --machine-type="$MACHINE_TYPE" \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --metadata-from-file=startup-script=startup_script.sh \
  --tags=http-server

# Allow HTTP Web Traffic through the Firewall
echo "--> Configuring firewall to allow public web access on port 80..."
if gcloud compute firewall-rules describe default-allow-http >/dev/null 2>&1; then
  echo "    Firewall rule already exists."
else
  gcloud compute firewall-rules create default-allow-http \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:80 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server
fi

# Cleanup local startup script file
rm -f startup_script.sh

# Get VM IP Address
VM_IP=$(gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].nativeApnIp)' 2>/dev/null || gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "=========================================================="
echo "   DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=========================================================="
echo " Your server is launching."
echo " Since it is compiling locally, please wait 3-4 minutes"
echo " for the VM to install Docker and build the app."
echo ""
echo " Access your website at: http://${VM_IP}"
echo "=========================================================="

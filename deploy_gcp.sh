#!/bin/bash
# ==============================================================================
# INSTADEED - GCP GCE DEPLOYMENT SCRIPT
# ==============================================================================
# This script builds the Instadeed application container and deploys it to a
# Google Compute Engine (VM) instance. It configures the VM to automatically
# run the container on startup with persistent storage for the SQLite database.
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
MACHINE_TYPE="e2-micro" # GCE Free-Tier eligible VM
VM_NAME="instadeed-server"
REPO_NAME="instadeed-repo"
IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/instadeed-app:latest"

# 3. Enable Required Google Cloud APIs
echo "--> Enabling Google Cloud APIs (this may take a minute)..."
gcloud services enable \
  compute.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com

# 4. Create Artifact Registry Repository (if not exists)
echo "--> Setting up Artifact Registry repository..."
if gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" >/dev/null 2>&1; then
  echo "    Repository '$REPO_NAME' already exists."
else
  gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Instadeed Application Registry"
  echo "    Repository created successfully."
fi

# 5. Build and Push Docker Image locally in Cloud Shell
echo "--> Authenticating Docker with Artifact Registry..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

echo "--> Building Docker image locally in Cloud Shell (this may take a few minutes)..."
docker build -t "$IMAGE_TAG" .

echo "--> Pushing Docker image to Artifact Registry..."
docker push "$IMAGE_TAG"
echo "    Docker image built and pushed successfully."

# 6. Create the VM Startup Script
echo "--> Generating GCE startup configuration..."
cat <<EOF > startup_script.sh
#!/bin/bash
# Startup script to configure Docker and launch the Instadeed container

# Update package manager and install Docker
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# Create persistent directory for the SQLite database on the host machine
mkdir -p /var/lib/instadeed
chmod 777 /var/lib/instadeed

# Authenticate Docker with Google Artifact Registry
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

# Pull the latest image
docker pull $IMAGE_TAG

# Stop and remove any existing container
docker stop instadeed-container || true
docker rm instadeed-container || true

# Run the container
# - Mounts /var/lib/instadeed on the VM host to the app inside the container to persist SQLite
# - Maps container port 8000 to host port 80 (standard HTTP web port)
docker run -d \\
  --name instadeed-container \\
  --restart always \\
  -p 80:8000 \\
  -v /var/lib/instadeed:/app/db_dir \\
  -e DATABASE_FILE=/app/db_dir/madhav_crm.db \\
  -e JWT_SECRET="instadeed-production-jwt-key-change-me" \\
  $IMAGE_TAG
EOF

# 7. Create GCE VM Instance
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
VM_IP=\$(gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].nativeApnIp)' 2>/dev/null || gcloud compute instances describe "$VM_NAME" --zone="$ZONE" --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "=========================================================="
echo "   DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=========================================================="
echo " Your server is starting up."
echo " It may take 2-3 minutes for Docker to initialize."
echo ""
echo " Access your website at: http://\${VM_IP}"
echo "=========================================================="

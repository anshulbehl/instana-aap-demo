# Instana + AAP AIOps Demo

Ansible playbooks and EDA rulebooks for the Instana + Ansible Automation Platform
AIOps integration demo. Covers automated incident remediation triggered by
Instana Smart Alerts via Event-Driven Ansible.

## Repository Structure

```
playbooks/
  demo_setup_aws_infra.yml       - Provision AWS VPC, subnet, SG, RHEL EC2 instance
  demo_setup_app.yml             - Install Flask demo app + Instana agent + load generator
  demo_setup_latency.yml         - Inject or clear simulated latency
  demo_setup_teardown.yml        - Tear down all AWS demo resources
  remediate_service_latency.yml  - Remediation: restart service, verify health, annotate Instana

rulebooks/
  instana_remediation.yml        - EDA rulebook for Instana webhook events

inventory/
  demo.yml                       - Dynamic inventory for demo hosts
  group_vars/
    all.yml                      - Shared variables

files/
  demo-app.py                   - Flask checkout service source
  demo-app.service              - Systemd unit file
  load-gen.sh                   - Background load generator script
```

## Quick Start

### 1. Set up demo infrastructure

```bash
# Set required variables (or use extra-vars)
export AWS_REGION=us-east-1
export AWS_KEY_NAME=your-keypair
export OWNER_TAG=your-name

# Provision AWS infrastructure
ansible-playbook playbooks/demo_setup_aws_infra.yml

# Install app and Instana agent
ansible-playbook playbooks/demo_setup_app.yml \
  -e instana_agent_key=YOUR_KEY \
  -e instana_download_key=YOUR_KEY \
  -e instana_endpoint=ingress-red-saas.instana.io:443
```

### 2. Manual Instana configuration

After the app is running and Instana discovers the service (~5 min):

1. Create an Application Perspective for `demo-app.py`
2. Create a Smart Alert for latency (p90 > 2000ms)
3. Create a Generic Webhook alert channel pointing to EDA controller
4. Attach the webhook channel to the Smart Alert

### 3. Set up AAP

1. Create a Project pointing to this Git repo
2. Create an Inventory with the demo host
3. Create a Job Template using `playbooks/remediate_service_latency.yml`
4. Create an EDA Rulebook Activation using `rulebooks/instana_remediation.yml`

### 4. Test the cycle

```bash
# Inject latency
ansible-playbook playbooks/demo_setup_latency.yml -e latency_state=on

# Watch Instana detect -> EDA trigger -> AAP remediate -> Instana recover

# Or manually clear
ansible-playbook playbooks/demo_setup_latency.yml -e latency_state=off
```

## Use Cases

| # | Use Case | Playbook | Instana Trigger |
|---|----------|----------|-----------------|
| 1 | Service Latency Spike | `remediate_service_latency.yml` | Smart Alert on p90 latency |
| 2 | Database Performance | `remediate_database_performance.yml` | Entity match on db/mysql |
| 3 | Bad Deployment Rollback | `remediate_deployment_rollback.yml` | Error rate spike + change correlation |

## Requirements

- Ansible 2.15+
- `amazon.aws` collection
- `ibm.instana` collection (for EDA rulebook)
- AWS credentials configured
- Instana SaaS/self-hosted instance
- AAP 2.5+ with EDA controller

# AWS Direct Connect Terraform Configuration

This Terraform configuration sets up AWS Direct Connect infrastructure including VPC, Transit Gateway, Direct Connect Gateway, and Transit Virtual Interfaces.

## ⚠️ Important: Two-Step Deployment Process

This configuration requires a **two-step deployment process** due to AWS Direct Connect connection acceptance requirements.

---

## 📋 Prerequisites

- Terraform >= 1.1.0
- AWS CLI configured with appropriate credentials
- Direct Connect connection ID provided by Graphiant
- Direct Connect connection must be created by Graphiant (you cannot create it via Terraform)

---

## 🚀 Deployment Steps

### **STEP 1: Pre-Manual Step (Initial Deployment)**

This step creates all infrastructure that doesn't require the Direct Connect connection to be accepted.

1. **Configure variables** in `configs/terraform/aws_config.tfvars`:
   ```hcl
   skip_manual_steps = false
   ```

2. **Initialize Terraform**:
   ```bash
   cd terraform/AWS/directConnect
   terraform init
   ```

3. **Review the plan**:
   ```bash
   terraform plan -var-file="../../../configs/terraform/aws_config.tfvars"
   ```

4. **Apply Step 1**:
   ```bash
   terraform apply -var-file="../../../configs/terraform/aws_config.tfvars"
   ```

   **This creates:**
   - VPC (or uses existing)
   - Subnet (or uses existing)
   - Route Table (or uses existing)
   - Transit Gateway
   - Transit Gateway VPC Attachment
   - TGW Route
   - DirectConnect Gateway

---

### **🔧 MANUAL STEP: Accept Direct Connect Connection**

**⚠️ CRITICAL: You must complete this step before proceeding to Step 2!**

1. **Go to AWS Console**:
   - Navigate to: **Direct Connect** → **Connections**
   - Find the connection with ID specified in your `dx_connection_id` variable

2. **Check Connection State**:
   - **"ordering"**: Click **"Accept"** button
   - **"requested"**: Connection may need approval from provider
   - **"available"** or **"pending"**: Connection is ready, proceed to Step 2

3. **Verify Connection State** (using AWS CLI):
   ```bash
   aws directconnect describe-connections \
     --connection-id <your-connection-id> \
     --query 'connections[0].connectionState' \
     --output text
   ```

4. **Wait for Connection**:
   - Connection state should be **"available"** or **"pending"** before proceeding
   - This may take a few minutes

---

### **STEP 2: Post-Manual Step (Final Deployment)**

This step creates resources that require the Direct Connect connection to be accepted.

1. **Update configuration** in `configs/terraform/aws_config.tfvars`:
   ```hcl
   skip_manual_steps = true  # ⚠️ Change to true after accepting connection
   ```

2. **Review the plan**:
   ```bash
   terraform plan -var-file="../../../configs/terraform/aws_config.tfvars"
   ```

3. **Apply Step 2**:
   ```bash
   terraform apply -var-file="../../../configs/terraform/aws_config.tfvars"
   ```

   **This creates:**
   - DirectConnect Gateway Association (TGW ↔ DX Gateway)
   - Transit Virtual Interface

4. **Get BGP Configuration**:
   ```bash
   terraform output
   ```
   
   Important outputs:
   - `amazon_side_asn`: Amazon's BGP ASN
   - `bgp_authentication_key`: BGP authentication key
   - `customer_router_peer_ip`: Your router's peer IP
   - `amazon_router_peer_ip`: Amazon's router peer IP

---

## 📝 Configuration Variables

### Key Variables in `aws_config.tfvars`:

| Variable | Description |
|----------|-------------|
| `skip_manual_steps` | Controls two-step deployment. Set to `false` for Step 1, `true` for Step 2 |
| `dx_connection_id` | Direct Connect connection ID provided by Graphiant |
| `dx_connection_vlan` | VLAN ID for transit VIF |
| `customer_bgp_asn` | Your BGP ASN for peering |
| `dxgw_allowed_prefixes` | List of CIDR prefixes allowed through the Direct Connect Gateway |

---

## 🔍 Troubleshooting

### Connection Does Not Exist Error

**Error**: `The specified Physical Connection does not exist`

**Solution**: 
1. **Verify the connection ID** is correct in your `aws_config.tfvars`:
   ```bash
   aws directconnect describe-connections --query 'connections[*].[connectionId,connectionName,connectionState]' --output table
   ```
2. **Check if connection exists in your AWS account**:
   ```bash
   aws directconnect describe-connections --connection-id <your-connection-id>
   ```
3. **Verify the connection was created by Graphiant** and is visible in your account
4. **Check AWS account/region** - ensure you're using the correct AWS account and region
5. **Connection may need to be shared** - if Graphiant created it in a different account, it may need to be shared with your account first

### Connection Not Accepted Error

**Error**: `Connection is not in a valid state`

**Solution**: 
1. Verify connection state: `aws directconnect describe-connections --connection-id <your-connection-id>`
2. Ensure connection is in "available" or "pending" state
3. If in "ordering" state, accept it in AWS Console

### Resources Not Created in Step 2

**Issue**: DX Gateway Association and Transit VIF not created

**Solution**:
1. Check `skip_manual_steps = true` in tfvars
2. Verify connection exists and is accepted
3. Check Terraform plan output
4. Verify connection ID is correct

### BGP Configuration Missing

**Issue**: Outputs show "Run Step 2 with skip_manual_steps = true"

**Solution**: Complete Step 2 with `skip_manual_steps = true`

---

## 📊 Resource Dependencies

```
Step 1 (skip_manual_steps = false):
  VPC → Subnet → Route Table
  Transit Gateway → TGW VPC Attachment → TGW Route
  DirectConnect Gateway

Step 2 (skip_manual_steps = true):
  DX Gateway Association (requires: DX Gateway, TGW, Connection accepted)
  Transit VIF (requires: DX Gateway, Connection accepted)
```

---

## 🧹 Cleanup

To destroy all resources:

1. **Destroy Step 2 resources first**:
   ```bash
   # Set skip_manual_steps = true
   terraform destroy -var-file="../../../configs/terraform/aws_config.tfvars"
   ```

2. **Then destroy Step 1 resources**:
   ```bash
   # Set skip_manual_steps = false
   terraform destroy -var-file="../../../configs/terraform/aws_config.tfvars"
   ```

---

## 📚 Additional Resources

- [AWS Direct Connect Documentation](https://docs.aws.amazon.com/directconnect/)
- [Terraform AWS Provider - Direct Connect](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dx_gateway)

---

## ✅ Verification Checklist

After Step 2 completion, verify:

- [ ] Direct Connect connection is in "available" state
- [ ] DX Gateway Association is created
- [ ] Transit VIF is created and in "available" state
- [ ] BGP peer IPs are assigned
- [ ] Transit Gateway routes are configured
- [ ] All Terraform outputs are available

---

**Need Help?** Check the inline comments in `main.tf` for detailed explanations of each resource.


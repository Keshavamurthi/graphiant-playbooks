# Cloud-Init Interactive Generator

This Bash script is an interactive tool for generating a valid `cloud-init` configuration (`user-data` and `meta-data`) and outputting it in a supported image format such as `cloud.iso`.

The script is designed to onboard network devices using parameters required by Graphiant's onboarding system and is compatible with both DHCP and static IP environments.

## 📦 What It Does

- Prompts the user step-by-step to enter relevant onboarding and networking configuration values.
- Supports default or custom local management and WAN interfaces.
- Allows use of DHCP or static IPs for the WAN interface.
- Can optionally include an onboarding token.
- Outputs a cloud-init ISO.

## 🛠️ Requirements

- Bash shell (Linux/macOS)
- `mkisofs` installed and available in your system path

## ▶️ How to Run

### Install Required Packages
```bash
# Linux/macOS: install cdrtools
brew install cdrtools
```

### Start Cloud Init Generation Script
```bash
# Make script executable
chmod +x generate-cloud-init.sh

# Run the script
./generate-cloud-init.sh
```

## ▶️ Example Run
```commandline
./generate-cloud-init.sh 

=== Cloud-Init local management and ztp Configurator ===
Enter onboarding environment [prod,test, default: prod]: test
Enter device role [cpe,gateway,core, default: cpe]: core
Do you want to include an onboarding token? [y,n, default: n]: y
Enter onboarding token [default: ]: hjfdhjklfdhjklfdahjklfda
Do you want to change the default local management interface from GigabitEthernet2? [y,n, default: n]: y
Enter custom local management interface name [default: GigabitEthernet2]: GigabitEthernet2/0/0
Do you want to change the default onboarding WAN interface from GigabitEthernet1? [y,n, default: n]: 1
Invalid option. Please choose one of: y,n
Do you want to change the default onboarding WAN interface from GigabitEthernet1? [y,n, default: n]: y
Enter custom onboarding WAN interface name [default: GigabitEthernet1]: GigabitEthernet1/0/0
Do you want to use DHCP for GigabitEthernet1/0/0? [y,n, default: n]: n
Enter WAN IP address (CIDR) for GigabitEthernet1/0/0 [default: ]: 123.123.123.2/24
Enter WAN Gateway for GigabitEthernet1/0/0 [default: ]: 123.123.123.1
Do you want to customize DNS servers? [y,n, default: n]: 
Enter local web server password [default: ]: 1234qwerasdf
Enter custom hostname [default: ]: 
Enter output disk file name (e.g., cloud.iso, myimage.qcow2) [default: cloud.iso]: ccccloud.iso
Generating cloud image...
Total translation table size: 0
Total rockridge attributes bytes: 363
Total directory bytes: 0
Path table size(bytes): 10
Max brk space used 0
183 extents written (0 MB)
✅ Cloud-init image created: ccccloud.iso
```

## Configuration Options

### Onboarding Environment
- **prod**: Production environment
- **test**: Test environment

### Device Role
- **cpe**: Customer Premises Equipment
- **gateway**: Gateway device
- **core**: Core network device

### Interface Configuration
- **Local Management Interface**: Default is `GigabitEthernet2`
- **WAN Interface**: Default is `GigabitEthernet1`
- **IP Configuration**: DHCP or static IP assignment

### Network Settings
- **WAN IP Address**: CIDR format (e.g., `123.123.123.2/24`)
- **WAN Gateway**: Gateway IP address
- **DNS Servers**: Optional custom DNS configuration
- **Hostname**: Optional custom hostname

### Security
- **Onboarding Token**: Optional token for secure onboarding
- **Local Web Server Password**: Password for local management interface

## Output Files

The script generates:
- **Cloud-init ISO**: Bootable image with cloud-init configuration
- **User-data**: Cloud-init user data configuration
- **Meta-data**: Cloud-init metadata configuration

## Troubleshooting

### Common Issues

1. **mkisofs not found**: Install cdrtools package
   ```bash
   # macOS
   brew install cdrtools
   
   # Ubuntu/Debian
   sudo apt-get install genisoimage
   ```

2. **Permission denied**: Make script executable
   ```bash
   chmod +x generate-cloud-init.sh
   ```

3. **Invalid interface names**: Use standard interface naming conventions
   - Example: `GigabitEthernet1/0/0`, `Ethernet0/0/1`

### Validation

The script includes built-in validation for:
- Interface name format
- IP address format (CIDR)
- Gateway IP format
- Required field completion

## Integration with Graphiant Playbooks

The generated cloud-init ISO can be used with Graphiant Edge devices for automated onboarding:

1. **Generate ISO**: Use this script to create the cloud-init image
2. **Deploy to Device**: Boot the device with the generated ISO
3. **Configure Network**: Use Graphiant Playbooks to configure the device
4. **Manage Infrastructure**: Use Terraform modules for cloud connectivity

## Additional Resources

- [Cloud-init Documentation](https://cloudinit.readthedocs.io/)
- [Graphiant Playbooks Main Documentation](../../README.md)
- [Terraform Infrastructure Documentation](../../terraform/README.md)
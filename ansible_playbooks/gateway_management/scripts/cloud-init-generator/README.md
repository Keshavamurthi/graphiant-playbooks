# Cloud-Init Interactive Generator

This Bash script is an interactive and command-line tool for generating a valid `cloud-init` configuration (`user-data` and `meta-data`) and outputting it in supported image formats such as `cloud.iso`, `qcow2`, or `vdi`.

The script is designed to onboard network devices using parameters required by Graphiant's onboarding system and is compatible with both DHCP and static IP environments.

---

## 📦 What It Does

- **Interactive Mode**: Prompts the user step-by-step to enter relevant onboarding and networking configuration values
- **Command-Line Mode**: Accepts all parameters as command-line arguments for automation
- Supports default or custom local management and WAN interfaces
- Allows use of DHCP or static IPs for the WAN interface
- Can optionally include an onboarding token
- Supports multiple output formats (ISO, QCOW2, VDI)
- Outputs a cloud-init image in the specified format

---

## 🛠️ Requirements

- Bash shell (Linux/macOS)
- `mkisofs` (for ISO format) - install via `brew install cdrtools` on macOS
- `cloud-localds` (for QCOW2/VDI formats) - part of cloud-utils package

---

## ▶️ How to Run

### Prerequisites
```bash
# macOS
brew install cdrtools cloud-utils

# Linux (Ubuntu/Debian)
sudo apt-get install cdrtools cloud-utils

# Linux (CentOS/RHEL)
sudo yum install cdrtools cloud-utils
```

### Interactive Mode
```bash
chmod +x generate-cloud-init.sh
./generate-cloud-init.sh
```

### Command-Line Mode
```bash
# Basic CPE with DHCP
./generate-cloud-init.sh -e prod -r cpe -d -p mypassword -o mycloud.iso

# CPE with static IP
./generate-cloud-init.sh -e prod -r cpe -i 192.168.100.10/24 -g 192.168.100.1 -p mypassword -o mycloud.iso

# With onboarding token
./generate-cloud-init.sh -e test -r cpe -t mytoken -d -p mypassword -n mydevice -o mycloud.iso

# Gateway role (maps to CPE internally)
./generate-cloud-init.sh -e prod -r gateway -d -p mypassword -o gateway.iso

# Core device
./generate-cloud-init.sh -e prod -r core -d -p mypassword -o core.iso
```

---

## 📋 Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-e, --env ENV` | Onboarding environment (prod\|test) | prod |
| `-r, --role ROLE` | Device role (cpe\|gateway\|core) | cpe |
| `-t, --token TOKEN` | Onboarding token (optional) | - |
| `-m, --mgmt-iface IFACE` | Local management interface | GigabitEthernet2 |
| `-w, --wan-iface IFACE` | WAN interface | GigabitEthernet1 |
| `-d, --dhcp` | Use DHCP for WAN interface | n |
| `-i, --wan-ip IP` | WAN IP address (CIDR format) | - |
| `-g, --wan-gateway GW` | WAN gateway | - |
| `--dns1 DNS1` | Primary DNS server | 8.8.8.8 |
| `--dns2 DNS2` | Secondary DNS server | 1.1.1.1 |
| `-p, --password PASSWORD` | Local web server password | - |
| `-n, --hostname HOSTNAME` | Custom hostname | - |
| `-c, --cloud-init-dir DIR` | Cloud-init directory | . |
| `-o, --output FILE` | Output file | cloud_init.qcow2 |
| `-h, --help` | Show help message | - |

---

## ▶️ Example Interactive Run
```bash
./generate-cloud-init.sh 

=== Cloud-Init local management and ztp Configurator (Interactive Mode) ===
Enter onboarding environment [prod,test, default: prod]: test
Enter device role [cpe,gateway,core, default: cpe]: core
Do you want to include an onboarding token? [y,n, default: n]: y
Enter onboarding token [default: ]: hjfdhjklfdhjklfdahjklfda
Do you want to change the default local management interface from GigabitEthernet2? [y,n, default: n]: y
Enter custom local management interface name [default: GigabitEthernet2]: GigabitEthernet2/0/0
Do you want to change the default onboarding WAN interface from GigabitEthernet1? [y,n, default: n]: y
Enter custom onboarding WAN interface name [default: GigabitEthernet1]: GigabitEthernet1/0/0
Do you want to use DHCP for GigabitEthernet1/0/0? [y,n, default: n]: n
Enter WAN IP address (CIDR) for GigabitEthernet1/0/0 [default: ]: 123.123.123.2/24
Enter WAN Gateway for GigabitEthernet1/0/0 [default: ]: 123.123.123.1
Do you want to customize DNS servers? [y,n, default: n]: 
Enter local web server password [default: ]: 1234qwerasdf
Enter custom hostname [default: ]: 
Enter output disk file name (e.g., cloud.iso, myimage.qcow2) [default: cloud.iso]: ccccloud.iso

Generating cloud image with below settings...
Hostname: 
Environment: test
Role: core
Token: hjfdhjklfdhjklfdahjklfda
Management Interface: GigabitEthernet2/0/0
WAN Interface: GigabitEthernet1/0/0
WAN DHCP: n
WAN IP: 123.123.123.2/24
WAN Gateway: 123.123.123.1
DNS: 8.8.8.8, 1.1.1.1
Cloud-init directory: .
Cloud-init userdata: user-data
Cloud-init metadata: meta-data
Cloud-init disk: ccccloud.iso

Total translation table size: 0
Total rockridge attributes bytes: 363
Total directory bytes: 0
Path table size(bytes): 10
Max brk space used 0
183 extents written (0 MB)
✅ Cloud-init image created: ccccloud.iso
```

---

## 🔧 Output Formats

The script supports multiple output formats based on the file extension:

- **`.iso`**: Creates a cloud-init ISO using `mkisofs`
- **`.qcow2`**: Creates a QCOW2 disk image using `cloud-localds`
- **`.vdi`**: Creates a VDI disk image using `cloud-localds`

---

## 📁 Generated Files

The script creates the following files in the specified cloud-init directory:

- `user-data` (or `userdata` for non-ISO formats): Cloud-init user data configuration
- `meta-data` (or `metadata` for non-ISO formats): Cloud-init metadata
- Output disk image in the specified format

---

## 🔍 Validation

The script includes validation for:
- Required parameters when not using DHCP (WAN IP and gateway)
- Valid environment values (prod/test)
- Valid role values (cpe/gateway/core)
- File format support
- Output file creation success

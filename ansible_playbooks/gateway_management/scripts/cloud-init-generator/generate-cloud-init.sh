#!/usr/bin/env bash

# Default values
DEFAULT_GCS_ENV="production"
DEFAULT_ROLE="cpe"
DEFAULT_USE_TOKEN="y"
DEFAULT_TOKEN=""
DEFAULT_LOCAL_MGMT_IFACE="GigabitEthernet2"
DEFAULT_WAN_IFACE="GigabitEthernet1"
DEFAULT_USE_DHCP="n"
DEFAULT_WAN_IP=""
DEFAULT_WAN_GATEWAY=""
DEFAULT_USE_CUSTOM_DNS="n"
DEFAULT_DNS1="8.8.8.8"
DEFAULT_DNS2="1.1.1.1"
DEFAULT_LWS_PASSWORD=""
DEFAULT_HOSTNAME=""
DEFAULT_CLOUD_INIT_DIR="."
DEFAULT_DISK="cloud_init.qcow2"

# Global variables (will be set by parse_args or interactive mode)
gcs_env=""
role=""
use_token=""
token=""
local_mgmt_iface=""
wan_iface=""
use_dhcp=""
wan_ip=""
wan_gateway=""
use_custom_dns=""
dns1=""
dns2=""
lws_password=""
hostname=""
cloud_init_dir=""
disk=""

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] [OUTPUT_FILE]

Generate cloud-init configuration for Graphiant devices.

OPTIONS:
    -e, --env ENV              Onboarding environment (production|systest) [default: $DEFAULT_GCS_ENV]
    -r, --role ROLE            Device role (cpe|gateway|core) [default: $DEFAULT_ROLE]
    -t, --token TOKEN          Onboarding token (optional)
    -m, --mgmt-iface IFACE     Local management interface [default: $DEFAULT_LOCAL_MGMT_IFACE]
    -w, --wan-iface IFACE      WAN interface [default: $DEFAULT_WAN_IFACE]
    -d, --dhcp                 Use DHCP for WAN interface
    -i, --wan-ip IP            WAN IP address (CIDR format, required if not using DHCP)
    -g, --wan-gateway GW       WAN gateway (required if not using DHCP)
    --dns1 DNS1                Primary DNS server [default: $DEFAULT_DNS1]
    --dns2 DNS2                Secondary DNS server [default: $DEFAULT_DNS2]
    -p, --password PASSWORD    Local web server password
    -n, --hostname HOSTNAME    Custom hostname
    -c, --cloud-init-dir DIR   Cloud-init directory [default: $DEFAULT_CLOUD_INIT_DIR]
    -o, --output FILE          Output file [default: $DEFAULT_DISK]
    -h, --help                 Show this help message

EXAMPLES:
    # Interactive mode
    $0

    # Command line mode - basic CPE with DHCP
    $0 -e production -r cpe -d -p mypassword -o mycloud.iso

    # Command line mode - CPE with static IP
    $0 -e production -r cpe -i 192.168.100.10/24 -g 192.168.100.1 -p mypassword -o mycloud.iso

    # Command line mode - with token
    $0 -e systest -r cpe -t mytoken -d -p mypassword -n mydevice -o mycloud.iso

EOF
}

# Parse command line arguments
parse_args() {
    # Initialize with default values
    gcs_env="$DEFAULT_GCS_ENV"
    role="$DEFAULT_ROLE"
    use_token="$DEFAULT_USE_TOKEN"
    token="$DEFAULT_TOKEN"
    local_mgmt_iface="$DEFAULT_LOCAL_MGMT_IFACE"
    wan_iface="$DEFAULT_WAN_IFACE"
    use_dhcp="$DEFAULT_USE_DHCP"
    wan_ip="$DEFAULT_WAN_IP"
    wan_gateway="$DEFAULT_WAN_GATEWAY"
    use_custom_dns="$DEFAULT_USE_CUSTOM_DNS"
    dns1="$DEFAULT_DNS1"
    dns2="$DEFAULT_DNS2"
    lws_password="$DEFAULT_LWS_PASSWORD"
    hostname="$DEFAULT_HOSTNAME"
    cloud_init_dir="$DEFAULT_CLOUD_INIT_DIR"
    disk="$DEFAULT_DISK"

    # Check if any arguments provided
    if [[ $# -eq 0 ]]; then
        # No arguments, use interactive mode
        return 1
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--env)
                gcs_env="$2"
                shift 2
                ;;
            -r|--role)
                role="$2"
                shift 2
                ;;
            -t|--token)
                token="$2"
                use_token="y"
                shift 2
                ;;
            -m|--mgmt-iface)
                local_mgmt_iface="$2"
                shift 2
                ;;
            -w|--wan-iface)
                wan_iface="$2"
                shift 2
                ;;
            -d|--dhcp)
                use_dhcp="y"
                shift
                ;;
            -i|--wan-ip)
                wan_ip="$2"
                shift 2
                ;;
            -g|--wan-gateway)
                wan_gateway="$2"
                shift 2
                ;;
            --dns1)
                dns1="$2"
                use_custom_dns="y"
                shift 2
                ;;
            --dns2)
                dns2="$2"
                use_custom_dns="y"
                shift 2
                ;;
            -p|--password)
                lws_password="$2"
                shift 2
                ;;
            -n|--hostname)
                hostname="$2"
                shift 2
                ;;
            -c|--cloud-init-dir)
                cloud_init_dir="$2"
                disk="$cloud_init_dir/$disk"
                shift 2
                ;;
            -o|--output)
                disk="$cloud_init_dir/$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            -*)
                echo "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                # Assume it's the output file
                disk="$1"
                shift
                ;;
        esac
    done

    # Validate required parameters
    if [[ "$use_dhcp" == "n" && (-z "$wan_ip" || -z "$wan_gateway") ]]; then
        echo "Error: WAN IP and gateway are required when not using DHCP"
        exit 1
    fi

    return 0
}

function prompt() {
    local var_name=$1
    local prompt_text=$2
    local default_value=$3
    local allow_empty=${4:-false}

    while true; do
        read -rp "$prompt_text [default: $default_value]: " input
        input="${input:-$default_value}"

        if [[ -z "$input" && "$allow_empty" == "false" ]]; then
            echo "This field cannot be empty."
        else
            eval "$var_name='$input'"
            break
        fi
    done
}

function prompt_choice() {
    local var_name=$1
    local prompt_text=$2
    local valid_options=$3
    local default_value=$4

    local input
    local IFS=','
    read -r -a options <<< "$valid_options"

    while true; do
        read -rp "$prompt_text [$valid_options, default: $default_value]: " input
        input="${input:-$default_value}"
        for opt in "${options[@]}"; do
            if [[ "$input" == "$opt" ]]; then
                eval "$var_name='$input'"
                return
            fi
        done
        echo "Invalid option. Please choose one of: $valid_options"
    done
}

# Declare arrays for both modes
declare -A ONBOARDING_AUTH_URL
ONBOARDING_AUTH_URL["production"]="https://api.graphiant.com/v1/devices/oauth"

declare -A ONBOARDING_GW
ONBOARDING_GW["production"]="onboarding-gateway.graphiant.com:16000"

# Try to parse command line arguments
if parse_args "$@"; then
    # Command line mode - variables are already set
    echo "=== Cloud-Init local management and ztp Configurator (Command Line Mode) ==="
else
    # Interactive mode
    echo "=== Cloud-Init local management and ztp Configurator (Interactive Mode) ==="

    prompt_choice gcs_env "Enter onboarding environment" "production,systest" "production"

    prompt_choice role "Enter device role" "cpe,gateway,core" "cpe"
    # Map 'gateway' to 'cpe' internally
    if [[ "$role" == "gateway" ]]; then
        role="cpe"
    fi

    prompt_choice use_token "Do you want to include an onboarding token?" "y,n" "n"
    include_token="false"

    if [[ "$use_token" == "y" ]]; then
        prompt token "Enter onboarding token" "" false
        include_token="true"
    fi

    # Local management interface (ask if they want to change the default interface name)
    default_mgmt_iface="GigabitEthernet2"
    prompt_choice change_mgmt_iface "Do you want to change the default local management interface from $default_mgmt_iface?" "y,n" "n"

    if [[ "$change_mgmt_iface" == "y" ]]; then
        prompt local_mgmt_iface "Enter custom local management interface name" "$default_mgmt_iface" true
    else
        local_mgmt_iface="$default_mgmt_iface"
    fi

    default_wan_iface="GigabitEthernet1"
    prompt_choice change_wan_iface "Do you want to change the default onboarding WAN interface from $default_wan_iface?" "y,n" "n"
    if [[ "$change_wan_iface" == "y" ]]; then
        prompt wan_iface "Enter custom onboarding WAN interface name" "$default_wan_iface" true
    else
        wan_iface="$default_wan_iface"
    fi

    prompt_choice use_dhcp "Do you want to use DHCP for $wan_iface?" "y,n" "n"
    wan_use_dhcp="false"

    if [[ "$use_dhcp" == "y" ]]; then
        wan_use_dhcp="true"
    else
        # No default values shown, and empty input not allowed
        prompt wan_ip "Enter WAN IP address (CIDR) for $wan_iface" "" false
        prompt wan_gateway "Enter WAN Gateway for $wan_iface" "" false
    fi

    prompt_choice use_custom_dns "Do you want to customize DNS servers?" "y,n" "n"

    if [[ "$use_custom_dns" == "y" ]]; then
        read -rp "Enter primary DNS server (or press enter to skip): " dns1
        read -rp "Enter secondary DNS server (or press enter to skip): " dns2
    else
        dns1="8.8.8.8"
        dns2="1.1.1.1"
    fi

    # local web server password
    prompt lws_password "Enter local web server password" "" true

    # hostname
    prompt hostname "Enter custom hostname" "" true

    prompt disk "Enter output disk file name (e.g., cloud.iso, myimage.qcow2)" "cloud.iso"
fi

# Common variables for both modes

# Map 'gateway' to 'cpe' internally
if [[ "$role" == "gateway" ]]; then
    role="cpe"
fi

# Set include_token based on use_token
if [[ "$use_token" == "y" ]]; then
    include_token="true"
else
    include_token="false"
fi

# Set wan_use_dhcp based on use_dhcp
if [[ "$use_dhcp" == "y" ]]; then
    wan_use_dhcp="true"
else
    wan_use_dhcp="false"
fi

format="${disk##*.}"
userdata="$cloud_init_dir/userdata"
metadata="$cloud_init_dir/metadata"

if [[ -d "$cloud_init_dir" ]]; then
    echo "Cloud-init directory already exists: $cloud_init_dir"
else    
    mkdir -p "$cloud_init_dir"
fi

[[ "$format" == "iso" ]] && { userdata='user-data'; metadata='meta-data'; }

# Validate required variables
if [[ -z "$gcs_env" ]]; then
    echo "Error: Environment not set"
    exit 1
fi

if [[ -z "$role" ]]; then
    echo "Error: Role not set"
    exit 1
fi

if [[ -z "$disk" ]]; then
    echo "Error: Output file not set"
    exit 1
fi

cat > "$userdata" <<EOF
#cloud-config
graphnos:
  role: $role
  onboarding-auth-url: ${ONBOARDING_AUTH_URL[${gcs_env}]}
  onboarding-gw: ${ONBOARDING_GW[${gcs_env}]}
EOF

if [[ "$include_token" == "true" ]]; then
    echo "  token: \"$token\"" >> "$userdata"
fi

cat >> "$userdata" <<EOF

graphnos-network:
  local-management-interface:
    name: "$local_mgmt_iface"
    ipv4:
      address: "192.168.1.1/24"
  wan-interfaces:
    "$wan_iface":
      ipv4:
EOF

if [[ "$wan_use_dhcp" == "true" ]]; then
    echo "        address: dhcp" >> "$userdata"
else
    echo "        address: \"$wan_ip\"" >> "$userdata"
    echo "        gateway: \"$wan_gateway\"" >> "$userdata"
fi

if [[ -n "$dns1" || -n "$dns2" ]]; then
    echo "      dns-servers: [${dns1:+\"$dns1\"}${dns1:+, }${dns2:+\"$dns2\"}]" >> "$userdata"
fi

cat >> "$userdata" <<EOF

  local-web-password: "$lws_password"
  hostname: "$hostname"
EOF

cat >> "$userdata" <<EOF
users:
  - name: gnos
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    lock_passwd: false
    groups: sudo
    shell: /bin/bash
EOF

echo -e "local-hostname: gnos\ninstance-id: gnos" > "$metadata"

if [[ "$disk" == "nodisk" ]]; then
    echo "No disk image created."
    exit 0
fi

echo "Generating cloud image with below settings..."
echo "Hostname: $hostname"
echo "Environment: $gcs_env"
echo "Role: $role"
echo "Token: ${use_token:+$token}"
echo "Management Interface: $local_mgmt_iface"
echo "WAN Interface: $wan_iface"
echo "WAN DHCP: $use_dhcp"
if [[ "$use_dhcp" == "n" ]]; then
    echo "WAN IP: $wan_ip"
    echo "WAN Gateway: $wan_gateway"
fi
echo "DNS: $dns1, $dns2"
echo "Cloud-init directory: $cloud_init_dir"
echo "Cloud-init userdata: $userdata"
echo "Cloud-init metadata: $metadata"
echo "Cloud-init disk: $disk"
echo ""
if [[ "$format" == "iso" ]]; then
    mkisofs -output "$disk" -volid cidata -joliet -rock "$userdata" "$metadata"
elif [[ "$format" == "qcow2" || "$format" == "vdi" ]]; then
    cloud-localds --disk-format "$format" "$disk" "$userdata" "$metadata"
else
    echo "Unsupported disk format: $format"
    exit 1
fi
if [[ -f "$disk" ]]; then
    echo "✅ Cloud-init image created: $disk"
else
    echo "❌ Cloud-init image creation failed"
    exit 1
fi

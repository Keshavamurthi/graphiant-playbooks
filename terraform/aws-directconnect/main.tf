# Terraform configuration for AWS Direct Connect
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.1.0"
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.project_name}-igw"
    Environment = var.environment
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.project_name}-public-subnet"
    Environment = var.environment
  }
}

# Private Subnet
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = var.availability_zone

  tags = {
    Name        = "${var.project_name}-private-subnet"
    Environment = var.environment
  }
}

# Route Table for Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "${var.project_name}-public-rt"
    Environment = var.environment
  }
}

# Route Table Association for Public Subnet
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Direct Connect Gateway
resource "aws_dx_gateway" "main" {
  count = var.enable_direct_connect ? 1 : 0

  name            = "${var.project_name}-dx-gateway"
  amazon_side_asn = var.dx_gateway_asn

  tags = {
    Name        = "${var.project_name}-dx-gateway"
    Environment = var.environment
  }
}

# Direct Connect Connection
resource "aws_dx_connection" "main" {
  count = var.enable_direct_connect ? 1 : 0

  name      = "${var.project_name}-dx-connection"
  bandwidth = var.dx_bandwidth
  location  = var.dx_location

  tags = {
    Name        = "${var.project_name}-dx-connection"
    Environment = var.environment
  }
}

# Direct Connect Gateway Association
resource "aws_dx_gateway_association" "main" {
  count = var.enable_direct_connect ? 1 : 0

  dx_gateway_id         = aws_dx_gateway.main[0].id
  associated_gateway_id = aws_vpn_gateway.main[0].id

  depends_on = [aws_vpn_gateway.main]
}

# VPN Gateway
resource "aws_vpn_gateway" "main" {
  count = var.enable_direct_connect ? 1 : 0

  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.project_name}-vpn-gateway"
    Environment = var.environment
  }
}

# Route Table for Private Subnet (with Direct Connect route)
resource "aws_route_table" "private" {
  count = var.enable_direct_connect ? 1 : 0

  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[0].id
  }

  tags = {
    Name        = "${var.project_name}-private-rt"
    Environment = var.environment
  }
}

# Route Table Association for Private Subnet
resource "aws_route_table_association" "private" {
  count = var.enable_direct_connect ? 1 : 0

  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private[0].id
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  count = var.enable_direct_connect ? 1 : 0

  domain = "vpc"

  tags = {
    Name        = "${var.project_name}-nat-eip"
    Environment = var.environment
  }
}

# NAT Gateway
resource "aws_nat_gateway" "main" {
  count = var.enable_direct_connect ? 1 : 0

  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public.id

  tags = {
    Name        = "${var.project_name}-nat-gateway"
    Environment = var.environment
  }

  depends_on = [aws_internet_gateway.main]
}

# Security Group for Direct Connect
resource "aws_security_group" "dx" {
  count = var.enable_direct_connect ? 1 : 0

  name        = "${var.project_name}-dx-sg"
  description = "Security group for Direct Connect"
  vpc_id      = aws_vpc.main.id

  # Allow all traffic within VPC
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr_block]
  }

  # Allow BGP traffic
  ingress {
    from_port   = 179
    to_port     = 179
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-dx-sg"
    Environment = var.environment
  }
}

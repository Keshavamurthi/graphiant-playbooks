# Docker Support

Graphiant Playbooks includes Docker support for consistent development and deployment environments.

## Building the Docker Image

```bash
# Build the Docker image
docker build -t graphiant-playbooks .

# Build with specific commit SHA
docker build --build-arg COMMIT_SHA=$(git rev-parse HEAD) -t graphiant-playbooks .
```

## Running with Docker

```bash
# Run interactive container
docker run -it graphiant-playbooks

# Run with volume mount for development
docker run -it -v $(pwd):/home/graphiant-playbooks graphiant-playbooks

# Run with environment variables
docker run -it -e GRAPHIANT_API_URL=https://api.graphiant.com graphiant-playbooks
```

## Docker Features

- **Multi-stage build** for optimized image size
- **Python 3.11.5** runtime environment
- **Pre-installed dependencies** from requirements.txt
- **Development tools** (vim, git, sshpass)
- **Version tracking** via COMMIT_SHA build arg

## Development with Docker

### Interactive Development
```bash
# Run with volume mount for live development
docker run -it -v $(pwd):/home/graphiant-playbooks graphiant-playbooks

# Inside the container, you can:
# - Edit files with vim
# - Run tests
# - Install additional packages
```

### Environment Variables
```bash
# Set Graphiant API URL
docker run -it -e GRAPHIANT_API_URL=https://api.graphiant.com graphiant-playbooks

# Set multiple environment variables
docker run -it \
  -e GRAPHIANT_API_URL=https://api.graphiant.com \
  -e GRAPHIANT_USERNAME=your_username \
  -e GRAPHIANT_PASSWORD=your_password \
  graphiant-playbooks
```

### Volume Mounts
```bash
# Mount current directory for development
docker run -it -v $(pwd):/home/graphiant-playbooks graphiant-playbooks

# Mount specific directories
docker run -it \
  -v $(pwd)/configs:/home/graphiant-playbooks/configs \
  -v $(pwd)/logs:/home/graphiant-playbooks/logs \
  graphiant-playbooks
```

## Docker Compose (Optional)

Create a `docker-compose.yml` for easier management:

```yaml
version: '3.8'
services:
  graphiant-playbooks:
    build: .
    container_name: graphiant-playbooks
    volumes:
      - .:/home/graphiant-playbooks
    environment:
      - GRAPHIANT_API_URL=https://api.graphiant.com
    stdin_open: true
    tty: true
```

Then run:
```bash
docker-compose up -d
docker-compose exec graphiant-playbooks bash
```

## Troubleshooting

### Common Issues

1. **Permission Issues**: Ensure Docker has access to mounted volumes
2. **Build Failures**: Check Dockerfile syntax and dependencies
3. **Network Issues**: Verify internet connectivity for package downloads

### Useful Commands

```bash
# Check Docker version
docker --version

# List running containers
docker ps

# View container logs
docker logs graphiant-playbooks

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Graphiant Playbooks Main Documentation](README.md)

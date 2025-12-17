# Docker Support

Run Graphiant Playbooks in a containerized environment.

## Building

```bash
# Build the image
docker build -t graphiant-playbooks .

# Build with version tag
docker build --build-arg COMMIT_SHA=$(git rev-parse HEAD) -t graphiant-playbooks .
```

## Running

```bash
# Interactive shell
docker run -it graphiant-playbooks

# With environment variables
docker run -it \
  -e GRAPHIANT_HOST=https://api.graphiant.com \
  -e GRAPHIANT_USERNAME=user \
  -e GRAPHIANT_PASSWORD=pass \
  graphiant-playbooks

# With custom configs directory (override collection's built-in configs)
docker run -it \
  -e GRAPHIANT_CONFIGS_PATH=/app/my-configs \
  -v $(pwd)/my-configs:/app/my-configs \
  graphiant-playbooks

# With custom templates directory
docker run -it \
  -e GRAPHIANT_TEMPLATES_PATH=/app/my-templates \
  -v $(pwd)/my-templates:/app/my-templates \
  graphiant-playbooks
```

## Running Playbooks

```bash
# Test the collection installation
docker run -it \
  -e GRAPHIANT_HOST=https://api.graphiant.com \
  -e GRAPHIANT_USERNAME=user \
  -e GRAPHIANT_PASSWORD=pass \
  graphiant-playbooks \
  ansible-playbook /root/.ansible/collections/ansible_collections/graphiant/naas/playbooks/hello_test.yml

# Run any playbook from the installed collection
docker run -it \
  -e GRAPHIANT_HOST=https://api.graphiant.com \
  -e GRAPHIANT_USERNAME=user \
  -e GRAPHIANT_PASSWORD=pass \
  graphiant-playbooks \
  ansible-playbook /root/.ansible/collections/ansible_collections/graphiant/naas/playbooks/complete_network_setup.yml
```

## Docker Compose

```yaml
version: '3.8'
services:
  graphiant-playbooks:
    build: .
    container_name: graphiant-playbooks
    environment:
      - GRAPHIANT_HOST=https://api.graphiant.com
      - GRAPHIANT_USERNAME=${GRAPHIANT_USERNAME}
      - GRAPHIANT_PASSWORD=${GRAPHIANT_PASSWORD}
    stdin_open: true
    tty: true
```

```bash
docker-compose up -d
docker-compose exec graphiant-playbooks bash
```

## Container Contents

- **Python 3.12** runtime
- **Ansible collection** installed at `/root/.ansible/collections/`
- **Source collection** at `/app/ansible_collections/`
- **Tools**: vim, git, sshpass

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GRAPHIANT_HOST` | Graphiant API host URL |
| `GRAPHIANT_USERNAME` | API username |
| `GRAPHIANT_PASSWORD` | API password |
| `GRAPHIANT_CONFIGS_PATH` | Custom configs directory path (optional) |
| `GRAPHIANT_TEMPLATES_PATH` | Custom templates directory path (optional) |

## Troubleshooting

```bash
# Check container logs
docker logs graphiant-playbooks

# Verify collection
docker run -it graphiant-playbooks ansible-galaxy collection list graphiant.naas
```

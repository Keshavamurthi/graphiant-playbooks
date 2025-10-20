# CI/CD Pipelines

The project includes pre-configured CI/CD pipelines for automated testing and deployment.

## Pipeline Structure

| Pipeline | Purpose | Triggers |
|----------|---------|----------|
| **`docker.yml`** | Docker image build and push | Push to main branch |
| **`lint.yml`** | Code quality checks | Pull requests |
| **`run.yml`** | Test execution | Pull requests, pushes |

## Pipeline Features

- **Automated Testing**: Runs test suite on every PR
- **Code Quality**: Flake8 and Pylint checks
- **Template Validation**: Jinja2 template linting
- **Docker Builds**: Automated container image creation
- **Multi-Environment**: Support for different deployment targets

## Local Pipeline Testing

```bash
# Run linting checks locally
flake8 ./libs ./test
pylint --errors-only ./libs
djlint configs -e yaml
djlint templates -e yaml

# Run tests
python3 test/test.py
```

## Pipeline Configuration

### Docker Pipeline (`docker.yml`)
- Builds Docker images on main branch pushes
- Tags images with commit SHA and version
- Pushes to container registry

### Lint Pipeline (`lint.yml`)
- Runs on pull requests
- Checks code quality with flake8 and pylint
- Validates Jinja2 templates
- Ensures code style consistency

### Test Pipeline (`run.yml`)
- Runs on pull requests and pushes
- Executes full test suite
- Validates configuration files
- Checks integration tests

## Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
# ... your code changes ...

# Run local checks
flake8 ./libs ./test
python3 test/test.py
```

### 2. Pull Request
```bash
# Push feature branch
git push origin feature/your-feature

# Create pull request
# Pipelines will automatically run:
# - Lint checks
# - Test execution
# - Code quality validation
```

### 3. Merge to Main
```bash
# After PR approval and merge
# Docker pipeline will automatically:
# - Build new Docker image
# - Tag with commit SHA
# - Push to registry
```

## Pipeline Triggers

### Automatic Triggers
- **Push to main**: Triggers Docker build pipeline
- **Pull requests**: Triggers lint and test pipelines
- **Push to any branch**: Triggers test pipeline

### Manual Triggers
- **Re-run failed jobs**: Available in CI/CD interface
- **Scheduled runs**: Can be configured for nightly builds
- **Custom triggers**: For specific deployment scenarios

## Environment Variables

### Required Variables
- `DOCKER_REGISTRY`: Container registry URL
- `DOCKER_USERNAME`: Registry username
- `DOCKER_PASSWORD`: Registry password

### Optional Variables
- `PYTHON_VERSION`: Python version for testing
- `TERRAFORM_VERSION`: Terraform version for infrastructure tests
- `AZURE_CLI_VERSION`: Azure CLI version for cloud tests

## Troubleshooting

### Common Issues

1. **Lint Failures**: Fix code style issues reported by flake8/pylint
2. **Test Failures**: Ensure all tests pass locally before pushing
3. **Docker Build Failures**: Check Dockerfile syntax and dependencies
4. **Permission Issues**: Verify CI/CD service account permissions

### Debugging

```bash
# Run pipeline steps locally
docker build -t graphiant-playbooks .

# Test specific components
python3 -m unittest test.test.TestGraphiantPlaybooks.test_get_enterprise_id

# Check linting issues
flake8 ./libs --show-source --statistics
```

## Customization

### Adding New Pipelines
1. Create new `.yml` file in `pipelines/` directory
2. Define pipeline steps and triggers
3. Update documentation

### Modifying Existing Pipelines
1. Edit the relevant `.yml` file
2. Test changes locally
3. Update documentation if needed

## Best Practices

### Code Quality
- Run linting checks before committing
- Fix all linting issues before creating PR
- Use pre-commit hooks for automatic checks

### Testing
- Write comprehensive tests for new features
- Ensure all tests pass before pushing
- Add integration tests for complex workflows

### Documentation
- Update README files for new features
- Document pipeline changes
- Keep configuration examples up to date

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Testing Guide](https://docs.python.org/3/library/unittest.html)
- [Graphiant Playbooks Main Documentation](../README.md)
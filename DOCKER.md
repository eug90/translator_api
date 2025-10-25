# Docker Setup for Translation API

## Quick Start

### 1. Setup Docker
```bash
chmod +x docker-setup.sh
./docker-setup.sh
```

### 2. Start the Service
```bash
make up
```

### 3. Access the API
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/hello

## Available Commands

```bash
make build       # Build Docker image
make up          # Start containers
make down        # Stop containers
make restart     # Restart containers
make logs        # View logs
make ps          # Show running containers
make test        # Run tests
make lint        # Run linting
make type-check  # Run type checking
make format      # Format code
make shell       # Open shell in container
make clean       # Clean up Docker resources
make help        # Show all commands
```

## Configuration

### Environment Variables
Edit `.env` file with your configuration:
```properties
DEEPL_API_KEY=your-key-here
API_DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=docker
```

### Files
- **Dockerfile** - Container image definition
- **docker-compose.yml** - Multi-container orchestration
- **.dockerignore** - Exclude files from Docker build
- **Makefile** - Convenient command shortcuts
- **docker-setup.sh** - One-time setup script

## Development Workflow

```bash
# Start containers
make up

# View logs in real-time
make logs

# Run tests
make test

# Open shell in container
make shell

# Format code
make format

# Stop containers
make down
```

## Production Deployment

For production, update `docker-compose.yml`:

```yaml
services:
  translator-api:
    # Remove volumes
    # Remove --reload from command
    # Set environment variables appropriately
    restart: on-failure
```

Then deploy with Docker Swarm or Kubernetes.

## Troubleshooting

### Container won't start
```bash
docker-compose logs translator-api
```

### Port already in use
Change port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Need to rebuild
```bash
make clean
make build
make up
```

## Health Check

The container includes a health check:
```bash
make ps  # Shows health status
```

## Notes

- Volumes are mounted for development (hot-reload enabled)
- Health check ensures container is ready
- Automatic restart on failure
- Network isolation with custom bridge network

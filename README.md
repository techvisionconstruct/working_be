# Service

## Docker Usage

Specify which environment's requirements to use when building the Docker image:

```bash
# For development
docker build --build-arg ENVIRONMENT=dev -t myapp:dev .

# For staging
docker build --build-arg ENVIRONMENT=staging -t myapp:staging .

# For production (default)
docker build -t myapp:prod .
```
FROM python:3.13.3-apline3.21

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies based on environment
ARG ENVIRONMENT=prod
COPY requirements /app/requirements/
RUN pip install --upgrade pip
RUN pip install -r requirements/${ENVIRONMENT}.txt

# Copy project
COPY . /app/

# Create a non-root user to run the app
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /app
USER app

# Run the entrypoint script
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
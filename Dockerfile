# ---- Builder Stage ----
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Using --no-cache-dir to keep this stage smaller if intermediate caching is not crucial, Prevents pip from saving downloaded packages in its cache,
# This makes it easy to copy them to the standard location in the final image.
RUN pip3 install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Final Stage ----
FROM python:3.9-slim

WORKDIR /app

# Create a non-root user and group for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin -c "App User" appuser

# Copy installed Python packages from the builder stage
COPY --from=builder /install /usr/local 

# Copy the application code
COPY . .

# Ensure wait-for-it.sh is executable
RUN chmod +x /app/wait-for-it.sh

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Command to run the application
# Note: --reload is typically for development. For production, you might remove
CMD ["uvicorn", "time-api:app", "--host=0.0.0.0", "--port=8000", "--reload"]

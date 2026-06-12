# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy dependencies list and install with --user to isolate in .local
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Create a non-root group and user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code
COPY . /app/

# Set ownership of app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose server port
EXPOSE 8000

# Add liveness check instruction for platform monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start backend server
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8000"]

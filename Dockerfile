# Use the Playwright image
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

# Set the working directory in the container
WORKDIR /workspace

# Copy the current directory contents into the container at /workspace
COPY . /workspace

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install webkit

# Default command (can be overridden)
CMD ["python", "main.py"]
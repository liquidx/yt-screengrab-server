FROM python:alpine

# Install ffmpeg
RUN apk add --no-cache ffmpeg

# Install uv
RUN pip install uv

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv venv && uv pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 7777

# Run the application
CMD ["uv", "run", "main.py"]

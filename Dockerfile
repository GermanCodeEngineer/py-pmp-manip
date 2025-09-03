FROM python:3.12-slim

# Install ffmpeg and dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy wheel(s) and test script
COPY dist/*.whl .
COPY docker_test.py .

# Install latest pip and the wheel (whatever version is in dist/)
RUN pip install --upgrade pip
RUN pip install ./*.whl

# Run the test script
CMD ["python", "docker_test.py"]

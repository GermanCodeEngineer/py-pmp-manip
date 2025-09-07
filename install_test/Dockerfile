FROM python:3.12-slim

# Install ffmpeg and dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Build the package
RUN pip install --upgrade build
RUN python -m build

# Copy wheel(s) and test script
COPY dist/*.whl .
COPY install_test/docker_test.py .

# Install latest pip and the wheel
RUN pip install --upgrade pip
RUN pip install ./*.whl

# Run the test script
CMD ["python", "docker_test.py"]

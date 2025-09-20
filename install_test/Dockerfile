FROM python:3.12-slim

# Install ffmpeg, nodejs and dependencies
RUN apt-get update && apt-get install -y ffmpeg nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy necessary files for build
COPY pyproject.toml ./
COPY MANIFEST.in ./
COPY pmp_manip/ ./pmp_manip/
COPY builtin_extension_source/ ./builtin_extension_source/

# Build the package
RUN pip install --upgrade build
RUN python -m build

# Copy test script
COPY install_test/docker_test.py .

# Install latest pip and the wheel (from the build we just did)
RUN pip install --upgrade pip
RUN pip install dist/*.whl

# Run the test script
CMD ["python", "docker_test.py"]

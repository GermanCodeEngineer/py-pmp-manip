FROM python:3.12-slim

# Install ffmpeg and dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy wheel and test script
COPY dist/py_pmp_manip-1.0.1-py3-none-any.whl .
COPY docker_test.py .

# Install wheel
RUN pip install --upgrade pip
RUN pip install py_pmp_manip-1.0.1-py3-none-any.whl

# Run the test script
CMD ["python", "docker_test.py"]

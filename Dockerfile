FROM python:3.12-slim

# Create app user and working directory
RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /home/app

# Copy only requirements first (for layer caching)
COPY app/requirements.txt .

# Install dependencies as root
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Now switch to non-root user
USER app

# Copy the rest of the app
COPY app .

# Expose the port (adjust based on your app, e.g. 8080 or 3838)
EXPOSE 8080

# Run your app (adjust if using something else like gunicorn, uvicorn, shiny, etc.)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

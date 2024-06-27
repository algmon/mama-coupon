# TODO: Fix
# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Start the application
CMD ["uvicorn", "app:app", "--reload"]
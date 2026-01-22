# Use Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt gunicorn

# Copy all files
COPY . .

# Create data directory explicitly to avoid path errors
RUN mkdir -p data

# Add this line to ensure the output folder exists
RUN mkdir -p backend/saved_models

# --- CRITICAL FIX: Retrain models inside the container ---
# We switch to the backend directory so relative paths (../data) work correctly
RUN cd backend && python preprocess.py
RUN cd backend && python model_lr.py
RUN cd backend && python model_lstm.py

# Create writable directory for matplotlib (required for some cloud envs)
ENV MPLCONFIGDIR=/tmp/matplotlib
RUN mkdir -p /tmp/matplotlib && chmod -R 777 /tmp/matplotlib

# Expose port
EXPOSE 7860

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "backend.app:app"]
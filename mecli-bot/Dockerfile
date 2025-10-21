FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git and other dependencies
RUN apt-get update && apt-get install -y \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Clone the me-cli repository
RUN git clone https://github.com/purplemashu/me-cli /app/me-cli

# Change to me-cli directory and run setup
WORKDIR /app/me-cli
RUN bash setup.sh

# Copy bot files to app directory
WORKDIR /app
COPY telegram_bot.py .
COPY requirements.txt .

# Install bot requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "telegram_bot.py"]
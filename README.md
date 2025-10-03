# 🚀 py-secrets-cache - Simple Caching for AWS Secrets

## 💻 Download

[![Download py-secrets-cache](https://img.shields.io/badge/Download-py--secrets--cache-blue.svg)](https://github.com/sachin31198/py-secrets-cache/releases)

## 🎯 Overview

py-secrets-cache offers in-memory caching for AWS Secrets Manager and AWS Systems Manager Parameter Store. This tool helps you access your secrets quickly and efficiently in AWS Lambda functions. For local development, it also supports an optional file-based cache. This reduces the need for repeated API calls, speeding up your applications while securing your sensitive data.

## 🚀 Getting Started

This guide will help you download and run py-secrets-cache with ease.

### 🔗 Download & Install

To download the application, simply visit the following link:

[Download py-secrets-cache](https://github.com/sachin31198/py-secrets-cache/releases)

1. Go to the Releases page by clicking the link above.
2. Look for the latest version of py-secrets-cache.
3. Select the file that best fits your operating system and download it.

### 🖥️ System Requirements

Ensure you meet the following requirements before proceeding:

- **Operating System:** Windows, macOS, or a Linux distribution.
- **Python Version:** Python 3.6 or later is required to run this application.
- **AWS Account:** You will need an AWS account with permissions to access AWS Secrets Manager and Systems Manager.

### 🛠️ Installation Steps

1. After downloading, locate the file on your computer.
2. If it’s a ZIP file, extract the contents to a preferred directory.
3. Open a command prompt or terminal window in that directory, depending on your operating system.
4. Install necessary dependencies by running:
   ```
   pip install -r requirements.txt
   ```
5. Follow the configuration steps outlined in the next section.

### ⚙️ Configuration

Configure py-secrets-cache to store and retrieve secrets securely. Here’s a simple setup to prepare the application:

1. Create a configuration file named `config.json` in the same directory as the application.
2. Include the following JSON structure in your `config.json`:
   ```json
   {
     "aws_access_key_id": "YOUR_ACCESS_KEY",
     "aws_secret_access_key": "YOUR_SECRET_KEY",
     "region": "YOUR_AWS_REGION",
     "cache_type": "in_memory" // or "file" for file-based caching
   }
   ```
3. Replace the placeholders with your actual AWS credentials and preferred region.

### 🏃 Running the Application

To run py-secrets-cache:

1. Open the command prompt or terminal in the application directory.
2. Execute the following command:
   ```
   python main.py
   ```
3. Your application will start and begin retrieving secrets as configured.

### 🌐 Additional Features

- **In-Memory Caching:** Speed up operations by storing secrets in memory.
- **File-Based Caching:** Save secrets to a file for local use, particularly useful during development.
- **AWS Integration:** Seamlessly integrate with AWS services to manage your secrets.

### 📄 Documentation

For detailed documentation and advanced features, refer to our [official documentation](https://github.com/sachin31198/py-secrets-cache/wiki).

## 💬 Support

If you encounter any issues or need assistance, please open an issue in this repository. Our community and maintainers are here to help. 

## 🔗 Useful Links

- [Releases Page](https://github.com/sachin31198/py-secrets-cache/releases)
- [Documentation](https://github.com/sachin31198/py-secrets-cache/wiki)
- [Source Code](https://github.com/sachin31198/py-secrets-cache)

Thank you for using py-secrets-cache! We hope it simplifies your AWS Secrets management.
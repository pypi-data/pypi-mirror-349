# PyPI Setup Guide

This guide explains how to set up your environment for publishing to PyPI.

## Creating a PyPI Account

1. Go to [PyPI](https://pypi.org/) and create an account if you don't have one
2. Verify your email address

## Creating an API Token

1. Log in to your PyPI account
2. Go to your account settings
3. Navigate to the "API tokens" section
4. Click "Add API token"
5. Give your token a name (e.g., "GitHub Actions")
6. Select the scope "Upload to project" and choose the project name
7. Click "Create token"
8. Copy the token value (you won't be able to see it again)

## Adding the Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Name the secret `PYPI_API_TOKEN`
5. Paste the token value
6. Click "Add secret"

## Manual Publishing (if needed)

If you need to publish manually, you can use the following steps:

1. Install the required tools:
   ```bash
   pip install build twine
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

   You'll be prompted for your PyPI username and password (or token).

## Using a .pypirc File (Optional)

For convenience during manual uploads, you can create a `.pypirc` file in your home directory:

```
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-your-token-here
```

Replace `pypi-your-token-here` with your actual PyPI token.

This file should be kept secure with restricted permissions:

```bash
chmod 600 ~/.pypirc
```


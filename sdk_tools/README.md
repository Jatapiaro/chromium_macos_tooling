# SDK Tools

## Setting up the repo

### 1. Create a virtual environment

    python3 -m venv env
    source env/bin/activate

### 2. Install the requirements

    pip install -r requirements.txt

### 3. Configure your .env file

    cp .env.example .env

## Uploading an SDK

This is a public repo. SDK must be managed in a private repository.
First you need to make sure that you have dev tools installed in your macOS
machine.

    xcode-select --install

After that you can run

    python generate_sdk_tar

The last step will upload the macOS SDK to the repo that you have specified
in your `.env` file.

## Downloading an SDK
#!/bin/bash

# Define variables
REPO_URL="https://github.com/StevenSU4/Asclepius/releases/download"
RELEASE_TAG="v1.0.0"
ZIP_FILE="images.zip"

# Download the dataset
echo "Downloading images from GitHub Releases..."
wget "$REPO_URL/$RELEASE_TAG/$ZIP_FILE"

# Unzip and clean up
echo "Unzipping..."
unzip -q "$ZIP_FILE" -d bench_data/
rm "$ZIP_FILE"
echo "Images ready in the 'bench_data/images' directory!"
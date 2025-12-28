#!/bin/bash

# Repository Migration Script
# This script updates the git remote origin for this repository

set -e

echo "Repository Migration Script"
echo "=========================="
echo ""

# Check if arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <organization> <repository-name>"
    echo ""
    echo "Example: $0 myorg my-dealfinder"
    echo ""
    echo "This will set the remote to: https://github.com/myorg/my-dealfinder.git"
    exit 1
fi

ORG=$1
REPO=$2
NEW_REMOTE="https://github.com/$ORG/$REPO.git"

echo "This script will:"
echo "  1. Remove the existing origin remote"
echo "  2. Add new origin: $NEW_REMOTE"
echo "  3. Rename current branch to 'main'"
echo "  4. Push to the new origin"
echo ""

read -p "Do you want to continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Migration cancelled."
    exit 1
fi

echo ""
echo "Step 1: Removing existing origin remote..."
git remote remove origin

echo "Step 2: Adding new origin remote..."
git remote add origin "$NEW_REMOTE"

echo "Step 3: Renaming current branch to main..."
git branch -M main

echo "Step 4: Pushing to new origin..."
git push -u origin main

echo ""
echo "Migration completed successfully!"
echo "New remote origin: $NEW_REMOTE"
echo ""
echo "Verify with: git remote -v"

#!/bin/bash

# Repository Migration Script
# This script updates the git remote origin for this repository

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
if git remote get-url origin &>/dev/null; then
    git remote remove origin
    echo "  ✓ Removed existing origin remote"
else
    echo "  ℹ No existing origin remote found, skipping removal"
fi

echo "Step 2: Adding new origin remote..."
if ! git remote add origin "$NEW_REMOTE" 2>/dev/null; then
    echo "  ⚠ Failed to add new origin remote (it may already exist)"
    echo "  Attempting to update existing remote..."
    git remote set-url origin "$NEW_REMOTE"
    echo "  ✓ Updated existing origin remote to: $NEW_REMOTE"
else
    echo "  ✓ Added new origin remote: $NEW_REMOTE"
fi

echo "Step 3: Renaming current branch to main..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    git branch -M main
    echo "  ✓ Renamed branch '$CURRENT_BRANCH' to 'main'"
else
    echo "  ℹ Current branch is already 'main', no rename needed"
fi

echo "Step 4: Pushing to new origin..."
if git push -u origin main; then
    echo "  ✓ Pushed to new origin"
else
    echo "  ⚠ Push failed. This may be due to upstream divergence or authentication issues."
    echo "  Please resolve manually and retry with: git push -u origin main"
    exit 1
fi

echo ""
echo "Migration completed successfully!"
echo "New remote origin: $NEW_REMOTE"
echo ""
echo "Verify with: git remote -v"

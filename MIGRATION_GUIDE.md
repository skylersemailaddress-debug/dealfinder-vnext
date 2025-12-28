# Repository Migration Guide

This guide explains how to update the git remote origin for this repository.

## Steps to Update Git Remote

Follow these steps to change the repository's remote origin:

### 1. Remove the existing origin remote

```bash
git remote remove origin
```

### 2. Add the new origin remote

Replace `ORG` and `NEW_REPO_NAME` with your organization and repository name:

```bash
git remote add origin https://github.com/ORG/NEW_REPO_NAME.git
```

### 3. Rename the current branch to main

```bash
git branch -M main
```

### 4. Push to the new origin

```bash
git push -u origin main
```

## Verification

After completing the steps above, verify the remote was updated correctly:

```bash
git remote -v
```

You should see the new origin URL pointing to your new repository.

## Example

If you're migrating to a repository named `my-dealfinder` under the organization `myorg`:

```bash
git remote remove origin
git remote add origin https://github.com/myorg/my-dealfinder.git
git branch -M main
git push -u origin main
```

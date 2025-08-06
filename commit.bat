@echo off
setlocal enabledelayedexpansion

echo ================================
echo Git + GitHub Setup Script
echo ================================

:: Step 1: Set your Git identity (optional if already set)
git config --global user.name "HDanke"

git config --global user.email "dankethegamer@gmail.com"

:: Step 2: Initialize Git
echo.
git init

:: Step 3: Add all files
git add .

:: Step 4: Commit
set /p commitmsg="Enter your commit message: "
git commit -m "%commitmsg%"

:: Step 5: Connect to GitHub
set /p repo="Paste your GitHub repo URL (e.g. https://github.com/username/repo.git): "
git remote add origin %repo%

:: Step 6: Rename to main (in case it's still 'master')
git branch -M main

:: Step 7: Push to GitHub
git push -u origin main

echo.
echo ================================
echo ✅ GitHub Push Completed!
pause

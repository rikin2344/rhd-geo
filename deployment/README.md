# Deployment Scripts

This directory contains scripts and documentation for deploying RHD Bearings web pages.

## Files

### Scripts
- **`create_separate_page.py`** - Generates self-contained HTML files from the webpage components
- **`direct_cpanel_upload.py`** - Uploads HTML files directly to the server via FTP

### Documentation
- **`UploadToFTP.md`** - Comprehensive guide for FTP upload process

## Usage

### Quick Deployment
```bash
# Navigate to deployment directory
cd deployment

# Generate the HTML file
python create_separate_page.py

# Upload to server
python direct_cpanel_upload.py
```

### Requirements
- Python 3.7+
- Required packages: `python-dotenv`, `ftplib`
- FTP credentials configured in `.env` file (in project root)

## File Paths
The scripts automatically reference the correct paths:
- Source files: `../webpages/MiniatureBearingsWebPage/`
- Output files: `../` (project root)
- Upload target: Server's `public_html` directory

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

# Generate the HTML files (creates clean URL structure)
python3 create_separate_page.py --page miniature

# Upload to server (automated - may require manual upload if FTP issues)
python3 direct_cpanel_upload.py --page miniature
```

### Clean URLs Generated
- **Miniature Series**: `https://rhdbearings.com/miniature-series/`
- **6000 Series**: `https://rhdbearings.com/6000-series/`

### Manual Upload (If Automated Fails)
1. Login to cPanel → File Manager
2. Go to `public_html`
3. Upload the entire `miniature-series/` directory
4. Visit: `https://rhdbearings.com/miniature-series/`

### Requirements
- Python 3.7+
- Required packages: `python-dotenv`, `ftplib`
- FTP credentials configured in `.env` file (in project root)

## File Paths
The scripts automatically reference the correct paths:
- Source files: `../webpages/MiniatureBearingsWebPage/`
- Output files: `../` (project root)
- Upload target: Server's `public_html` directory

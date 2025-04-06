# Instagram Follower Analysis Tool

This tool helps you analyze your Instagram followers and following lists to identify:
1. Users who don't follow you back
2. Users who follow you but you don't follow them

## Prerequisites
- Python 3.x
- Required Python packages (will be installed automatically)

## How to Use

1. Export your Instagram data:
   - Go to your Instagram profile
   - Click on "Settings and privacy"
   - Click on "Accounts Center"
   - Click on "Your information and permissions"
   - Click on "Download your information"
   - Select "Followers and following"
   - Request download
   - Once ready, download the zip file
   - Extract the zip file
   - Look for `followers_1.html` and `following.html` files

2. Place the HTML files:
   - Copy both `followers_1.html` and `following.html` files into the same directory as this script
   - Rename `followers.html` to `followers_1.html` (if needed)

3. Run the analysis:
   ```bash
   python analyze_followers.py
   ```

4. View results:
   - The script will generate two Excel files:
     - `not_following_back.xlsx`: Users who you follow but don't follow you back
     - `followers_you_dont_follow.xlsx`: Users who follow you but you don't follow them

## Output Files
Each Excel file contains:
- username: Instagram username
- profile_link: Direct link to their Instagram profile
- name: Display name (if available)

## Requirements
The script will automatically install required packages. If you want to install them manually:
```bash
pip install -r requirements.txt
``` 
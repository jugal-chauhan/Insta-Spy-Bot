import subprocess
import sys
import os
from bs4 import BeautifulSoup
import pandas as pd

def install_requirements():
    """Install required packages if not already installed."""
    print("Checking and installing required packages...")
    try:
        import beautifulsoup4
        import pandas
        import openpyxl
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully!")

def extract_usernames_from_html(file_path):
    """Extract usernames and profile links from Instagram HTML file."""
    print(f"\nProcessing file: {file_path}")
    
    users = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all Instagram profile links
        links = soup.find_all('a', href=lambda x: x and 'instagram.com' in x)
        print(f"Found {len(links)} Instagram profile links")
        
        for link in links:
            href = link.get('href', '')
            username = link.text.strip()
            
            # Skip any non-profile links
            if '/p/' in href or '/explore/' in href or '/stories/' in href:
                continue
                
            if username:
                user_data = {
                    'username': username,
                    'profile_link': href,
                    'name': username  # Since we don't have display names, using username as name
                }
                users.append(user_data)
                
        print(f"Extracted {len(users)} valid usernames")
        print("Sample usernames:", [user['username'] for user in users[:5]])
        
    return users

def analyze_followers(followers_file, following_file):
    """Analyze follower and following lists to find who doesn't follow back."""
    print("\n=== Starting Analysis ===")
    
    print("\n--- Processing Followers ---")
    followers = extract_usernames_from_html(followers_file)
    
    print("\n--- Processing Following ---")
    following = extract_usernames_from_html(following_file)
    
    # Create sets of usernames for comparison
    follower_usernames = {user['username'] for user in followers}
    following_usernames = {user['username'] for user in following}
    
    # Find who doesn't follow back (following - followers)
    not_following_back = following_usernames - follower_usernames
    
    # Find who follows you but you don't follow them (followers - following)
    followers_you_dont_follow = follower_usernames - following_usernames
    
    # Create lists with full details
    not_following_back_details = [
        user for user in following 
        if user['username'] in not_following_back
    ]
    
    followers_you_dont_follow_details = [
        user for user in followers
        if user['username'] in followers_you_dont_follow
    ]
    
    # Create DataFrames and export to Excel
    df_not_following = pd.DataFrame(not_following_back_details)
    df_followers = pd.DataFrame(followers_you_dont_follow_details)
    
    # Sort by username
    df_not_following = df_not_following.sort_values('username')
    df_followers = df_followers.sort_values('username')
    
    # Export to Excel
    df_not_following.to_excel('not_following_back.xlsx', index=False)
    df_followers.to_excel('followers_you_dont_follow.xlsx', index=False)
    
    print("\n=== Analysis Complete ===")
    print(f"Total followers: {len(followers)}")
    print(f"Total following: {len(following)}")
    print(f"Users who don't follow you back: {len(not_following_back_details)}")
    print(f"Users who follow you but you don't follow them: {len(followers_you_dont_follow_details)}")
    print(f"\nResults have been saved to:")
    print("- not_following_back.xlsx")
    print("- followers_you_dont_follow.xlsx")
    
    # Print samples of both cases
    if not_following_back_details:
        print("\nSample of users who don't follow you back:")
        for user in not_following_back_details[:5]:
            print(f"- {user['username']}")
            
    if followers_you_dont_follow_details:
        print("\nSample of users who follow you but you don't follow them:")
        for user in followers_you_dont_follow_details[:5]:
            print(f"- {user['username']}")

def main():
    """Main function to run the analysis."""
    print("Instagram Follower Analysis Tool")
    print("===============================")
    
    # Install requirements
    install_requirements()
    
    # Check for required files
    followers_file = "followers_1.html"
    following_file = "following.html"
    
    if not os.path.exists(followers_file):
        print(f"\nError: {followers_file} not found!")
        print("Please make sure you have exported your Instagram data and placed the files in the correct directory.")
        print("See README.md for instructions.")
        return
        
    if not os.path.exists(following_file):
        print(f"\nError: {following_file} not found!")
        print("Please make sure you have exported your Instagram data and placed the files in the correct directory.")
        print("See README.md for instructions.")
        return
    
    # Run analysis
    analyze_followers(followers_file, following_file)

if __name__ == "__main__":
    main() 
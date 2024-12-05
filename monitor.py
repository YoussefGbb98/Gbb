import requests
import smtplib
from email.mime.text import MIMEText
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime

# Website to monitor
url = 'https://www.islamweb.net/ar/fatwa/%D8%A7%D8%B3%D8%A3%D9%84-%D8%B9%D9%86-%D9%81%D8%AA%D9%88%D9%89'  # Replace with the actual URL

# Email details
sender_email = 'youssefguerboub@gmail.com'
recipient_email = 'youssefguerboub@gmail.com'
smtp_server = 'smtp.gmail.com'  # e.g., for Gmail: smtp.gmail.com
smtp_port = 587
smtp_user = 'youssefguerboub@gmail.com'
smtp_password = '0680231300'

# File to store previous content hash
hash_file = 'previous_hash.txt'

# Folder to save updated content
output_folder = 'saved_changes'  # Create this folder in your repository

# CSS selector for the part of the page you want to monitor
target_element_selector = 'div.right-nav.fatwalist #question'  # Adjust as needed

def send_email():
    msg = MIMEText('The monitored section of the webpage has changed, and the new content has been saved.')
    msg['Subject'] = 'Webpage Section Change Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def get_current_section():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element using the CSS selector
    target_element = soup.select_one(target_element_selector)
    if target_element:
        return target_element.get_text(), target_element.prettify()
    else:
        print(f"Error: Could not find element with selector {target_element_selector}")
        return None, None

def get_current_section_hash(text_content):
    return hashlib.sha256(text_content.encode()).hexdigest()

def load_previous_hash():
    try:
        with open(hash_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_current_hash(current_hash):
    with open(hash_file, 'w') as f:
        f.write(current_hash)

def save_change_to_file(content_html):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{output_folder}/change_{timestamp}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_html)
    print(f"Change saved to {filename}")

# Check for changes in the target section
text_content, html_content = get_current_section()
if text_content:
    current_hash = get_current_section_hash(text_content)
    previous_hash = load_previous_hash()

    if current_hash != previous_hash:
        send_email()
        save_change_to_file(html_content)
        save_current_hash(current_hash)
        print("Change detected and saved.")
    else:
        print("No changes detected in the monitored section.")
else:
    print("Failed to retrieve or hash the target section.")

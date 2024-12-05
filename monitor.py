import requests
import smtplib
from email.mime.text import MIMEText
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Website to monitor
url = 'https://www.islamweb.net/ar/fatwa/%D8%A7%D8%B3%D8%A3%D9%84-%D8%B9%D9%86-%D9%81%D8%AA%D9%88%D9%89'

# Email details
sender_email = 'youssefguerboub98@gmail.com'
recipient_email = 'youssefguerboub98@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'youssefguerboub98@gmail.com'
smtp_password = '0680231300'

# File to store previous content hash
hash_file = 'previous_hash.txt'

# Flag to track if a change has been saved
first_change_saved_flag = 'first_change_saved.txt'

# Folder to save updated content
output_folder = 'saved_changes'

# CSS selector for the part of the page you want to monitor
target_element_selector = 'div.right-nav.fatwalist #question'  # Adjust to your specific target element

# Function to send an email notification
def send_email():
    msg = MIMEText('The monitored section of the webpage has changed, and the new HTML content has been saved.')
    msg['Subject'] = 'Webpage Section Change Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

# Save the HTML content to a file
def save_change_to_file(content_html):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the filename with a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{output_folder}/change_{timestamp}.html'
    
    # Save the content to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_html)
    print(f"Change saved to {filename}")

# Get the current HTML section
def get_current_section():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Select the target element
    target_element = soup.select_one(target_element_selector)
    if target_element:
        return target_element.prettify()  # Return the HTML content
    else:
        print(f"Error: Could not find element with selector {target_element_selector}")
        return None

# Calculate the hash of the HTML content
def get_current_section_hash(html_content):
    return hashlib.sha256(html_content.encode()).hexdigest()

# Load the previously stored hash
def load_previous_hash():
    try:
        with open(hash_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Save the current hash to the file
def save_current_hash(current_hash):
    with open(hash_file, 'w') as f:
        f.write(current_hash)

# Check if the first change has been saved
def has_first_change_saved():
    return os.path.exists(first_change_saved_flag)

# Mark that the first change has been saved
def mark_first_change_saved():
    with open(first_change_saved_flag, 'w') as f:
        f.write('Change saved')

# Main monitoring logic
html_content = get_current_section()

if html_content:
    current_hash = get_current_section_hash(html_content)
    previous_hash = load_previous_hash()

    # If this is the first change, save it and mark it
    if previous_hash is None and not has_first_change_saved():
        save_change_to_file(html_content)
        save_current_hash(current_hash)
        mark_first_change_saved()
        send_email()
        print("First change detected and saved.")
    else:
        print("No further changes detected or the first change has already been saved.")
else:
    print("Failed to retrieve the target section.")

import requests
import smtplib
from email.mime.text import MIMEText
import hashlib
from bs4 import BeautifulSoup

# Website to monitor
url = 'https://www.example.com'  # Replace with the actual URL

# Email details
sender_email = 'your-email@example.com'
recipient_email = 'your-email@example.com'
smtp_server = 'smtp.example.com'  # e.g., for Gmail: smtp.gmail.com
smtp_port = 587
smtp_user = 'your-email@example.com'
smtp_password = 'your-email-password'

# Hash file to store previous content hash
hash_file = 'previous_hash.txt'

# CSS selector for the part of the page you want to monitor
target_element_selector = 'div.right-nav.fatwalist #question'  # Adjust to target specific element

def send_email():
    msg = MIMEText('The webpage has changed in the monitored section!')
    msg['Subject'] = 'Webpage Section Change Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def get_current_section_hash():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element using the CSS selector
    target_element = soup.select_one(target_element_selector)
    if target_element:
        return hashlib.sha256(target_element.get_text().encode()).hexdigest()
    else:
        print(f"Error: Could not find element with selector {target_element_selector}")
        return None

def load_previous_hash():
    try:
        with open(hash_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_current_hash(current_hash):
    with open(hash_file, 'w') as f:
        f.write(current_hash)

# Check for changes in the target section
current_hash = get_current_section_hash()
if current_hash:
    previous_hash = load_previous_hash()

    if current_hash != previous_hash:
        send_email()
        save_current_hash(current_hash)
    else:
        print("No changes detected in the monitored section.")
else:
    print("Failed to retrieve or hash the target section.")

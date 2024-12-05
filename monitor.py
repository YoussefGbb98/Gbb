import requests
import smtplib
from email.mime.text import MIMEText
import hashlib
from datetime import datetime
import os

# Website to monitor
url = 'https://www.islamweb.net/en/index.php?page=ask'

# Email details
sender_email = 'youssefguerboub98@gmail.com'
recipient_email = 'youssefguerboub98@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'youssefguerboub98@gmail.com'
smtp_password = 'vunm mfak ymcd igcd'

# Folder to save updated content
output_folder = 'saved_changes'

# Text snippet to search for
required_text = "Assalaamu Alaykum, the Fatwa centre in Islamweb apologizes for not being able to accept your question now. We have reached the maximum daily limit. Please try again later."

# Function to send an email notification
def send_email():
    msg = MIMEText('The monitored webpage has changed, and the new HTML content has been saved.')
    msg['Subject'] = 'Webpage Change Notification'
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

# Get the current HTML of the entire page
def get_current_page():
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # Return the full page HTML content
    else:
        print(f"Error: Failed to fetch the page. Status code: {response.status_code}")
        return None
        
# Main monitoring logic
html_content = get_current_page()

if html_content:
    # Check if the required text is absent
    if required_text not in html_content:
        print("Required text not found on the page.")
        save_change_to_file(html_content)
        send_email()
    else:
        print("No changes detected.")
else:
    print("Failed to retrieve the page.")

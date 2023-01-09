import requests

# URL of the webhook
WEBHOOK_URL_REVIEW = ""
WEBHOOK_URL_APPROVED = ""
# Function to send an embedded message with a hyperlink to the Discord channel
def send_embedded_message(title, description, url, color, fields):
    # Create the embed object
    embed = {
        "title": title,
        "description": "The following information was extracted from the Notion database:",
        "url": url,
        "color": color,
        "fields": fields,
    }

    # Create the request payload
    data = {"embeds": [embed]}

    # Send the POST request
    if "Approved" not in description:
        requests.post(WEBHOOK_URL_REVIEW, json=data)
        return
    else:
        requests.post(
            WEBHOOK_URL_APPROVED,
            json=data,
        )
        return

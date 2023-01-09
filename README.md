
# Notion Discord Webhook

This project allows you to send notifications to a Discord channel through webhooks when certain conditions are met in a Notion database.

## Prerequisites

Before you begin, make sure you have the following:

-   A Discord server and a Discord channel where you want to receive the notifications
-   A Discord webhook URL for the channel (you can create one by following the instructions [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))
-   A Notion account and a Notion database
-   The Notion API token, which you can get by following the instructions [here](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration)

## Installation

1.  Clone the repository:

Copy code

`git clone https://github.com/your-username/notion-discord-webhook.git` 

2.  Install the dependencies:

Copy code

`pip install -r requirements.txt` 

3.  Replace the placeholders in the `.env` file with your actual values:

-   `WEBHOOK_URL_REVIEW`: the Discord webhook URL for the channel where you want to receive notifications about tasks that are in review
-   `WEBHOOK_URL_APPROVED`: the Discord webhook URL for the channel where you want to receive notifications about approved tasks
-   `TOKEN`: your Notion API token
-   `DATABASE_ID`: the ID of your Notion database

## Usage

To start receiving notifications, run the script:

Copy code

`python main.py` 

The script will fetch the current version of the database, store a copy of it, and then check every minute if the database has changed. If a change is detected, it will send a notification to the Discord channel through a webhook. The type of notification depends on the status of the task and whether it has been submitted for review:

-   If a task is in review (its "Submit" checkbox is checked and its status is not "Approved" or "Rejected"), a notification will be sent to the `WEBHOOK_URL_REVIEW` webhook.
-   If a task is approved (its status is set to "Approved"), a notification will be sent to the `WEBHOOK_URL_APPROVED` webhook.
-   If a task is rejected (its status is set to "Rejected"), a notification will be sent to the `WEBHOOK_URL_REVIEW` webhook only if the task has been submitted for review (its "Submit" checkbox is checked).

## Customization

You can customize the behavior of the script by modifying the `check_db` function in the `main.py` file. This function compares two copies of the database and sends a notification if a change is detected. You can modify the conditions under which a notification is sent by editing the `if` statements in the function.

You can also customize the format of the notifications by modifying the `send_embedded_message` function in the `discord.py` file. This function creates an [embedded message](https://discord.com/developers/docs/resources/channel#embed-object) and sends it to the
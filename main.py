import requests
import json
import schedule
from discord import send_embedded_message

# Notion API token and database ID
TOKEN = ""
DATABASE_ID = ""

# Headers for API requests
HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13",
}

# File to store a copy of the database
DB_FILE = "./sample_db.json"

# Read the database with the given ID and headers
def read_database(database_id, headers):
    read_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.request("POST", read_url, headers=headers)
    data = res.json()
    return data


# Extract certain properties from the database
def get_data(data):
    ids = []

    # Extract data for each task in the database
    tasks = [i for i in data["results"]]
    sample_db = {}
    for task in tasks:
        sample_db[task["id"]] = {
            "checkbox": task["properties"]["Submit"]["checkbox"],
            "status": task["properties"]["Status"]["status"]["name"],
            "Task Reminder": task["properties"]["Task Reminder"]["formula"]["string"],
            "url": task["url"],
            "title": task["properties"][""]["title"][0]["plain_text"],
        }

    return sample_db


# Compare two copies of the database and check if the status of any tasks has changed
def check_db(data1, data2):
    for task_id in data1.keys():
        if task_id in data2.keys():
            # Check if the status of the task has changed
            if data1[task_id] == data2[task_id]:
                pass
            else:
                field = [
                    {"name": "Task", "value": data2[task_id]["title"]},
                    {"name": "Task Reminder", "value": data2[task_id]["Task Reminder"]},
                    {"name": "Status", "value": data2[task_id]["status"]},
                ]
                if (
                    "Approved" in data2[task_id]["status"]
                    and "Approved" not in data1[task_id]["status"]
                ):
                    # print("Approved")
                    # print(data2)
                    send_embedded_message(
                        "Approved",
                        "Approved Task",
                        data2[task_id]["url"],
                        "893080",
                        fields=field,
                    )
                elif "Rejected" in data2[task_id]["status"]:
                    if data2[task_id]["checkbox"] == True:
                        if data1[task_id]["checkbox"] == False:

                            send_embedded_message(
                                "Rejected Task in Review",
                                "Rejected Task in Review",
                                data2[task_id]["url"],
                                "893080",
                                fields=field,
                            )
                        else:
                            print("Rejected")
                else:
                    if (
                        data2[task_id]["checkbox"] == True
                        and data1[task_id]["checkbox"] == False
                    ):
                        send_embedded_message(
                            "Task in Review",
                            "Task in Review",
                            data2[task_id]["url"],
                            "893080",
                            fields=field,
                        )
        # Task not found in second copy of database
        else:
            print("Not found")


# Main function to check if the database has changed
def main():
    # Read the current version of the database
    current_db = get_data(read_database(DATABASE_ID, HEADERS))
    # Read the previous version of db
    old_db = json.load(open(DB_FILE, "r", encoding="utf8"))
    # Check if the database has changed
    check_db(old_db, current_db)
    # Update the database file
    with open(DB_FILE, "w", encoding="utf8") as f:
        json.dump(current_db, f, ensure_ascii=False, indent=4)

    return


if __name__ == "__main__":
    # Run the main function every 15 seconds
    schedule.every(0.25).minutes.do(main)

    while True:
        schedule.run_pending()

#

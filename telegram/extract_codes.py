from telethon import TelegramClient, events
import re

# Replace with your Telegram API credentials
api_id = '21485720'
api_hash = '5c812a333c60bc5c7b6a244c7969f21a'
channel_username = '@imcooladi4all'  # E.g., '@example_channel'

# File to save the filtered messages directly
output_file = "filtered_codes.txt"

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Set to store already saved codes
saved_codes = set()

# Load existing codes from the file (if it exists)
try:
    with open(output_file, "r") as f:
        saved_codes = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    pass  # File doesn't exist yet, no need to load anything

# This will be called when a new message is received
@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    try:
        # Get the message text
        msg_text = event.message.text

        # Use regex to find all text between backticks
        codes = re.findall(r'`(.*?)`', msg_text)

        # If codes are found, save them directly to the output file
        if codes:
            with open(output_file, "a") as f:
                for code in codes:
                    if code not in saved_codes:  # Check for duplicates
                        f.write(f"{code}\n")
                        saved_codes.add(code)  # Add the new code to the set
                        print(f"Saved code: {code}")
                    else:
                        print(f"Duplicate code skipped: {code}")
        else:
            print("No valid codes found in the message.")

    except Exception as e:
        print(f"Error while processing message: {e}")

# Run the Telegram client and listen for new messages
print("Listening for new messages... Press Ctrl+C to stop.")
with client:
    client.run_until_disconnected()

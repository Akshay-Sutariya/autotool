from telethon import TelegramClient, events
import re

# Replace with your Telegram API credentials
api_id = '21485720'
api_hash = '5c812a333c60bc5c7b6a244c7969f21a'
channel_username = '@imcooladi4all'  # E.g., '@example_channel'

# File to save the filtered unique messages directly
output_file = "filtered_codes.txt"

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Load existing codes into a set to avoid duplicates
existing_codes = set()
try:
    with open(output_file, "r") as f:
        existing_codes = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    # File doesn't exist yet; start with an empty set
    existing_codes = set()

# This will be called when a new message is received
@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    try:
        # Get the message text
        msg_text = event.message.text

        # Use regex to find all text between backticks
        codes = re.findall(r'`(.*?)`', msg_text)

        # Save only unique codes
        new_codes = [code for code in codes if code not in existing_codes]

        if new_codes:
            with open(output_file, "a") as f:
                for code in new_codes:
                    f.write(f"{code}\n")
                    existing_codes.add(code)  # Add to the set to prevent future duplicates

            print(f"Saved new codes: {', '.join(new_codes)}")
        else:
            print("No new unique codes found in the message.")

    except Exception as e:
        print(f"Error while processing message: {e}")

# Run the Telegram client and listen for new messages
print("Listening for new messages... Press Ctrl+C to stop.")
with client:
    client.run_until_disconnected()

# # test.py
# import sys

# import os
# os.environ['SLACK_API_TOKEN'] = 'TODO'

# # Enable debug logging
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # Verify it works
# from slack_sdk import WebClient
# client = WebClient()
# api_response = client.api_test()


# import os
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

# # Initialize a Web client
# slack_token = os.environ["SLACK_API_TOKEN"]
# client = WebClient(token=slack_token)

# # Channel ID
# channel_id = "C05N14ACVGE"

# try:
#     # Call the conversations.history method using the WebClient
#     result = client.channels_history(channel=channel_id)

#     for message in result['messages']:
#         # Check if message contains a file and is an image
#         if 'files' in message:
#             for file in message['files']:
#                 if file['mimetype'].startswith('image/'):
#                     image_url = file['url_private']
#                     # Code to download and save the image
#                     # ...

# except SlackApiError as e:
#     print(f"Error: {e}")

from constants import GDRIVE_FOLDER_LINK

import gdown

gdown.download_folder(
    GDRIVE_FOLDER_LINK,
    output="gdrive",
    remaining_ok=True,
)

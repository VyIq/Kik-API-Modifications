# Kik API Modifications
Modifications done to Tomer's Kik Bot API by me

## chatting.py Modifications
* **Added OutgoingSticker class**
* **Added OutgoingSponsoredGIFMessage class**
* **Added OutgoingFakeSystemMessage class**
* **Added OutgoingFakeStatusMessage class**
* **Added Tenor dev API key**
* **Added OutgoingChatIPLogger class**
* **Added OutgoingGroupIPLogger class**

## parsing_utilities.py Modifications
* **Added parse_sticker method** - Thanks to Kief for insights into parsing **<3**
* **Added icon_src.py** - Put a base64 encoded image string and it'll be the icon for the IP logger.

## client.py Modifications
* **Added send_sponsored_gif_image method**
* **Added send_sticker method**
* **Added send_fake_system_message method**
* **Added send_fake_status_message method**
* **Added send_ip_logger method**

## Miscellaneous files
* **example_bot.py** - This is a basic bot to demonstrate the new modifications.
* **sticker.png** - A PNG image that'll be used by the send_sticker method.

***
If you have any questions or concerns you can message me on Kik!
[@quacking](https://kik.me/quacking)

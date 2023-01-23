# Unfinished Files
Files I'll probably get done in the future but I've been slacking so might as well release just incase someone else could finish them (:

## chatting.py Modifications
* **Added OutgoingVideo class**

## parsing_utilities.py Modifications
* **Added parse_video method** - This is what is mainly broken ):

## client.py Modifications
* **Added send_video method**

## content.py Modifications
* **Added upload_gallery_video function**
* **Added misc. functions to differentiate images and videos**

***
## Notes
* The parse_video method doesn't work, it's because ffmpeg does't take a BytesIO object. I've tried getting the value of the BytesIO object into bytes but I'm probably doing it wrong.
* You'll need to install ffmpeg onto your computer and install **ffmpeg-python**, it's what actually interacts with ffmpeg in Python.
* If you want just a Youtube video searcher then you could probably get rid of ffmpeg and make this whole thing much easier with a Youtube downloader library.
* Finally, the other files might not completely work if you do fix parsing_video, they should but I didn't test them independently.

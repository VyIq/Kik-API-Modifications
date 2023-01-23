import hashlib
import logging
import requests
import time
from threading import Thread

from kik_unofficial.datatypes.exceptions import KikUploadError
from kik_unofficial.utilities.cryptographic_utilities import CryptographicUtils
from kik_unofficial.device_configuration import kik_version_info


log = logging.getLogger('kik_unofficial')
SALT = "YA=57aSA!ztajE5"

def upload_gallery_image(OutgoingChatImage, jid, username, password):
    url = "https://platform.kik.com/content/files/" + OutgoingChatImage.content_id
    username_passkey = CryptographicUtils.key_from_password(username, password)
    send_image(url, OutgoingChatImage, jid, username, password)

def upload_gallery_video(OutgoingVideo, jid, username, password):
    url = "https://platform.kik.com/content/files/" + OutgoingVideo.content_id
    username_passkey = CryptographicUtils.key_from_password(username, password)
    send_video(url, OutgoingVideo, jid, username, password)

def send_image(url, image, jid, username, password):
    app_id = "com.kik.ext.gallery"
    v = SALT + image.content_id + app_id

    verification = hashlib.sha1(v.encode('UTF-8')).hexdigest()
    headers = {
        'Host': 'platform.kik.com',
        'Connection': 'Keep-Alive',
        'Content-Length': str(image.parsed['size']),
        'User-Agent': f'Kik/{kik_version_info["kik_version"]} (Android 7.1.2) Content',
        'x-kik-jid': jid,
        'x-kik-password': username_passkey,
        'x-kik-verification': verification,
        'x-kik-app-id': app_id,
        'x-kik-content-chunks': '1',
        'x-kik-content-size': str(image.parsed['size']),
        'x-kik-content-md5': image.parsed['MD5'],
        'x-kik-chunk-number': '0',
        'x-kik-chunk-md5': image.parsed['MD5'],
        'x-kik-sha1-original': image.parsed['SHA1'].upper(),
        'x-kik-sha1-scaled': image.parsed['SHA1Scaled'].upper(),
        'x-kik-blockhash-scaled': image.parsed['blockhash'].upper(),
        'Content-Type': 'image/jpeg',
        'x-kik-content-extension': '.jpg'
    }
    # Sometimes Kik's servers throw 5xx when they're having issues, the new thread won't handle the exception
    Thread(
        target=image_upload_thread,
        args=(url, image.parsed['original'], headers),
        name='KikContent'
    ).start()

def send_video(url, video, jid, username, password):
    app_id = "com.kik.ext.gallery"
    v = SALT + video.content_id + app_id

    verification = hashlib.sha1(v.encode('UTF-8')).hexdigest()
    headers = {
        'Host': 'platform.kik.com',
        'Connection': 'Keep-Alive',
        'Content-Length': str(video.parsed['size']),
        'User-Agent': f'Kik/{kik_version_info["kik_version"]} (Android 7.1.2) Content',
        'x-kik-jid': jid,
        'x-kik-password': username_passkey,
        'x-kik-verification': verification,
        'x-kik-app-id': app_id,
        'x-kik-content-chunks': '1',
        'x-kik-content-size': str(video.parsed['size']),
        'x-kik-content-md5': video.parsed['MD5'],
        'x-kik-chunk-number': '0',
        'x-kik-chunk-md5': video.parsed['MD5'],
        'x-kik-sha1-original': video.parsed['SHA1'].upper(),
        'x-kik-sha1-scaled': video.parsed['SHA1Scaled'].upper(),
        'x-kik-blockhash-scaled': video.parsed['blockhash'].upper(),
        'Content-Type': 'video/mp4',
        'x-kik-content-extension': '.mp4'
    }
    # Sometimes Kik's servers throw 5xx when they're having issues, the new thread won't handle the exception
    Thread(
        target=video_upload_thread,
        args=(url, video.parsed['original'], headers),
        name='KikVideoContent'
    ).start()

def image_upload_thread(url, image, headers):
    log.debug('Uploading image')
    r = requests.put(url, data=image, headers=headers)
    if r.status_code != 200:
        raise KikUploadError(r.status_code, r.reason)

def video_upload_thread(url, video, headers):
    log.debug('Uploading video')
    r = requests.put(url, data=video, headers=headers)
    if r.status_code != 200:
        raise KikUploadError(r.status_code, r.reason)
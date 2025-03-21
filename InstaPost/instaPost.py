import os
import json
import time
import random
import requests
import logging
from uuid import uuid4
from PIL import Image, ExifTags
import hmac
import hashlib
import urllib.parse

# Configuration
API_DOMAIN = "i.instagram.com"
API_URL = f"https://{API_DOMAIN}/api/v1/"
USER_AGENT_BASE = (
    "Instagram 117.0.0.28.123 "
    "Android (28/9; 320dpi; 720x1280; Xiaomi; Redmi Note 4; mido; qcom; en_US; 166149665)"
)
SIG_KEY_VERSION = "4"
IG_SIG_KEY = "a86109795736d73c9a94172cd9b736917d7d94ca61c9101164894b3f0d43bef4"

# Request headers for Instagram API
REQUEST_HEADERS = {
    "X-IG-App-Locale": "en_US",
    "X-IG-Device-Locale": "en_US",
    "X-Pigeon-Session-Id": str(uuid4()),
    "X-Pigeon-Rawclienttime": str(round(time.time() * 1000)),
    "X-IG-Connection-Speed": "-1kbps",
    "X-IG-Bandwidth-Speed-KBPS": str(random.randint(7000, 10000)),
    "X-IG-Bandwidth-TotalBytes-B": str(random.randint(500000, 900000)),
    "X-IG-Bandwidth-TotalTime-MS": str(random.randint(50, 150)),
    "X-IG-Prefetch-Request": "foreground",
    "X-Bloks-Version-Id": "0a3ae4c88248863609c67e278f34af44673cff300bc76add965a9fb036bd3ca3",
    "X-IG-WWW-Claim": "0",
    "X-MID": "XkAyKQABAAHizpYQvHzNeBo4E9nm",
    "X-Bloks-Is-Layout-RTL": "false",
    "X-Bloks-Enable-RenderCore": "false",
    "X-IG-Connection-Type": "WIFI",
    "X-IG-Capabilities": "3brTvwE=",
    "X-IG-App-ID": "567067343352427",
    "X-IG-App-Startup-Country": "US",
    "Accept-Language": "en-US",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "Host": "i.instagram.com",
    "X-FB-HTTP-Engine": "Liger",
    "Connection": "close",
}

# Utility function to get image size
def get_image_size(fname):
    with Image.open(fname) as img:
        width, height = img.size
    return width, height

# Utility function to resize image to Instagram's requirements
def resize_image(fname):
    from math import ceil

    try:
        from PIL import Image, ExifTags
    except ImportError as e:
        print("ERROR: {err}".format(err=e))
        print(
            "Required module `PIL` not installed\n"
            "Install with `pip install Pillow` and retry"
        )
        return False
    print("Analizing `{fname}`".format(fname=fname))
    h_lim = {"w": 90.0, "h": 47.0}
    v_lim = {"w": 4.0, "h": 5.0}
    img = Image.open(fname)
    (w, h) = img.size
    deg = 0
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(img._getexif().items())
        o = exif[orientation]
        if o == 3:
            deg = 180
        if o == 6:
            deg = 270
        if o == 8:
            deg = 90
        if deg != 0:
            print("Rotating by {d} degrees".format(d=deg))
            img = img.rotate(deg, expand=True)
            (w, h) = img.size
    except (AttributeError, KeyError, IndexError) as e:
        print("No exif info found (ERR: {err})".format(err=e))
        pass
    img = img.convert("RGBA")
    ratio = w * 1.0 / h * 1.0
    print("FOUND w:{w}, h:{h}, ratio={r}".format(w=w, h=h, r=ratio))
    if w > h:
        print("Horizontal image")
        if ratio > (h_lim["w"] / h_lim["h"]):
            print("Cropping image")
            cut = int(ceil((w - h * h_lim["w"] / h_lim["h"]) / 2))
            left = cut
            right = w - cut
            top = 0
            bottom = h
            img = img.crop((left, top, right, bottom))
            (w, h) = img.size
        if w > 1080:
            print("Resizing image")
            nw = 1080
            nh = int(ceil(1080.0 * h / w))
            img = img.resize((nw, nh), Image.ANTIALIAS)
    elif w < h:
        print("Vertical image")
        if ratio < (v_lim["w"] / v_lim["h"]):
            print("Cropping image")
            cut = int(ceil((h - w * v_lim["h"] / v_lim["w"]) / 2))
            left = 0
            right = w
            top = cut
            bottom = h - cut
            img = img.crop((left, top, right, bottom))
            (w, h) = img.size
        if h > 1080:
            print("Resizing image")
            nw = int(ceil(1080.0 * w / h))
            nh = 1080
            img = img.resize((nw, nh), Image.ANTIALIAS)
    else:
        print("Square image")
        if w > 1080:
            print("Resizing image")
            img = img.resize((1080, 1080), Image.ANTIALIAS)
    (w, h) = img.size
    new_fname = "{fname}.CONVERTED.jpg".format(fname=fname)
    print("Saving new image w:{w} h:{h} to `{f}`".format(w=w, h=h, f=new_fname))
    new = Image.new("RGB", img.size, (255, 255, 255))
    new.paste(img, (0, 0, w, h), img)
    new.save(new_fname, quality=95)
    return new_fname

# Utility function to check if the image has a compatible aspect ratio for Instagram
def compatible_aspect_ratio(size):
    w, h = size
    return 0.8 <= w / h <= 1.91

# API class to interact with Instagram
class API:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.device_settings = {
            "manufacturer": "Xiaomi",
            "model": "Redmi Note 4",
            "android_version": 28,
            "android_release": "9",
            "dpi": "320dpi",
            "resolution": "720x1280",
            "cpu": "qcom",
            "version_code": "166149665",
        }
        self.device_id = "android-" + str(uuid4())
        self.user_agent = USER_AGENT_BASE.format(**self.device_settings)
        self.session = requests.Session()
        self.is_logged_in = False
        self.logger = logging.getLogger("instabot")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.total_requests = 0

    # Function to handle the challenge
    def handle_challenge(self, challenge_url):
        challenge_url = API_URL + challenge_url[1:]
        response = self.session.get(challenge_url)
        if response.status_code == 200:
            challenge_data = response.json()
            if challenge_data.get("step_name") == "select_verify_method":
                choice = input("Choose a verification method (0: SMS, 1: Email): ")
                self.session.post(challenge_url, data={"choice": choice})
            elif challenge_data.get("step_name") == "verify_code":
                code = input("Enter the verification code sent to you: ")
                self.session.post(challenge_url, data={"security_code": code})
            else:
                self.logger.error("Unknown challenge step: {}".format(challenge_data.get("step_name")))
        else:
            self.logger.error("Failed to load challenge page: {}".format(response.text))

    # Modify the login function to handle challenges
    def login(self):
        self.session.headers.update(REQUEST_HEADERS)
        self.session.headers.update({"User-Agent": self.user_agent})
        data = {
            "jazoest": "22264",
            "country_codes": '[{"country_code":"1","source":["default"]}]',
            "phone_id": str(uuid4()),
            "_csrftoken": "missing",
            "username": self.username,
            "adid": "",
            "guid": str(uuid4()),
            "device_id": self.device_id,
            "google_tokens": "[]",
            "password": self.password,
            "login_attempt_count": "0",
        }
        response = self.session.post(API_URL + "accounts/login/", data=data)
        if response.status_code == 200:
            self.is_logged_in = True
            self.logger.info("Logged in successfully")
        elif response.status_code == 400 and "challenge_required" in response.text:
            challenge_url = response.json()["challenge"]["api_path"]
            self.handle_challenge(challenge_url)
        else:
            self.logger.error("Failed to log in: {}".format(response.text))
            self.is_logged_in = False


    # Function to upload a photo to Instagram
    def upload_photo(self, photo, caption=None):
        if not self.is_logged_in:
            self.logger.error("You must log in first")
            return False

        upload_id = str(int(time.time() * 1000))
        if not compatible_aspect_ratio(get_image_size(photo)):
            self.logger.error("Photo does not have a compatible aspect ratio")
            photo = resize_image(photo)

        waterfall_id = str(uuid4())
        upload_name = f"{upload_id}_0_{random.randint(1000000000, 9999999999)}"
        rupload_params = {
            "retry_context": '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}',
            "media_type": "1",
            "xsharing_user_ids": "[]",
            "upload_id": upload_id,
            "image_compression": json.dumps(
                {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
            ),
        }
        photo_data = open(photo, "rb").read()
        photo_len = str(len(photo_data))
        self.session.headers.update(
            {
                "Accept-Encoding": "gzip",
                "X-Instagram-Rupload-Params": json.dumps(rupload_params),
                "X_FB_PHOTO_WATERFALL_ID": waterfall_id,
                "X-Entity-Type": "image/jpeg",
                "Offset": "0",
                "X-Entity-Name": upload_name,
                "X-Entity-Length": photo_len,
                "Content-Type": "application/octet-stream",
                "Content-Length": photo_len,
                "Accept-Encoding": "gzip",
            }
        )
        response = self.session.post(
            f"https://{API_DOMAIN}/rupload_igphoto/{upload_name}", data=photo_data
        )
        if response.status_code != 200:
            self.logger.error("Photo upload failed: {}".format(response.text))
            return False

        configure_timeout = 15
        for attempt in range(4):
            time.sleep(configure_timeout)
            if self.configure_photo(upload_id, photo, caption):
                self.logger.info("Photo uploaded successfully")
                return True
        self.logger.error("Failed to configure photo")
        return False

    # Function to configure the uploaded photo
    def configure_photo(self, upload_id, photo, caption=""):
        width, height = get_image_size(photo)
        data = {
            "media_folder": "Instagram",
            "source_type": 4,
            "caption": caption,
            "upload_id": upload_id,
            "device": self.device_settings,
            "edits": {
                "crop_original_size": [width * 1.0, height * 1.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.0,
            },
            "extra": {"source_width": width, "source_height": height},
        }
        return self.send_request("media/configure/?", data)

    # Function to send a request to the Instagram API
    def send_request(self, endpoint, post=None, login=False, with_signature=True, headers=None, extra_sig=None, timeout_minutes=None):
        self.session.headers.update(REQUEST_HEADERS)
        self.session.headers.update({"User-Agent": self.user_agent})
        if not self.is_logged_in and not login:
            msg = "Not logged in!"
            self.logger.critical(msg)
            raise Exception(msg)
        if headers:
            self.session.headers.update(headers)
        try:
            self.total_requests += 1
            if post is not None:
                if with_signature:
                    post = self.generate_signature(post)
                    if extra_sig is not None and extra_sig != []:
                        post += "&".join(extra_sig)
                response = self.session.post(API_URL + endpoint, data=post)
            else:
                response = self.session.get(API_URL + endpoint)
        except Exception as e:
            self.logger.warning(str(e))
            return False

        self.last_response = response
        if post is not None:
            self.logger.debug(
                "POST to endpoint: {} returned response: {}".format(endpoint, response)
            )
        else:
            self.logger.debug(
                "GET to endpoint: {} returned response: {}".format(endpoint, response)
            )
        if response.status_code == 200:
            try:
                self.last_json = json.loads(response.text)
                return True
            except json.JSONDecodeError:
                return False
        else:
            self.logger.debug(
                "Responsecode indicates error; response content: {}".format(
                    response.content
                )
            )
            if response.status_code != 404 and response.status_code != "404":
                self.logger.error(
                    "Request returns {} error!".format(response.status_code)
                )
            try:
                response_data = json.loads(response.text)
                if response_data.get(
                    "message"
                ) is not None and "feedback_required" in str(
                    response_data.get("message").encode("utf-8")
                ):
                    self.logger.error(
                        "ATTENTION!: `feedback_required`"
                        + str(response_data.get("feedback_message").encode("utf-8"))
                    )
                    try:
                        self.last_response = response
                        self.last_json = json.loads(response.text)
                    except Exception:
                        pass
                    return "feedback_required"
            except ValueError:
                self.logger.error(
                    "Error checking for `feedback_required`, "
                    "response text is not JSON"
                )
                self.logger.info("Full Response: {}".format(str(response)))
                try:
                    self.logger.info("Response Text: {}".format(str(response.text)))
                except Exception:
                    pass
            if response.status_code == 429:
                if timeout_minutes is None:
                    timeout_minutes = 0
                if timeout_minutes == 15:
                    time.sleep(1)
                    self.logger.error(
                        "Since we hit 15 minutes of time outs, we have to restart. Removing session and cookies. Please relogin."
                    )
                    delete_credentials()
                    sys.exit()
                timeout_minutes += 5
                self.logger.warning(
                    "That means 'too many requests'. I'll go to sleep "
                    "for {} minutes.".format(timeout_minutes)
                )
                time.sleep(timeout_minutes * 60)
                return self.send_request(
                    endpoint,
                    post,
                    login,
                    with_signature,
                    headers,
                    extra_sig,
                    timeout_minutes,
                )
            if response.status_code == 400:
                response_data = json.loads(response.text)
                if response_data.get("challenge_required"):
                    self.logger.error(
                        "Failed to login go to instagram and change your password"
                    )
                    delete_credentials()
                if response_data.get("two_factor_required"):
                    try:
                        self.last_response = response
                        self.last_json = json.loads(response.text)
                    except Exception:
                        self.logger.error("Error unknown send request 400 2FA")
                        pass
                    return self.two_factor_auth()
                else:
                    msg = "Instagram's error message: {}"
                    self.logger.info(msg.format(response_data.get("message")))
                    if "error_type" in response_data:
                        msg = "Error type: {}".format(response_data["error_type"])
                    self.logger.info(msg)

            try:
                self.last_response = response
                self.last_json = json.loads(response.text)
            except Exception:
                self.logger.error("Error unknown send request")
                pass
            return False

    # Function to generate a signature for the request
    @staticmethod
    def generate_signature(data):
        data = json.dumps(data)  # Ensure data is a JSON string
        body = (
            hmac.new(
                IG_SIG_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            + "."
            + urllib.parse.quote(data)
        )
        signature = "signed_body={body}&ig_sig_key_version={sig_key}"
        return signature.format(sig_key=SIG_KEY_VERSION, body=body)

    # Property to get the session cookies as a dictionary
    @property
    def cookie_dict(self):
        return self.session.cookies.get_dict()

    # Property to get the CSRF token from the cookies
    @property
    def token(self):
        return self.cookie_dict["csrftoken"]

    # Property to get the user ID from the cookies
    @property
    def user_id(self):
        return self.cookie_dict["ds_user_id"]

    # Property to get the rank token for the user
    @property
    def rank_token(self):
        return "{}_{}".format(self.user_id, self.uuid)

    # Property to get the default data for requests
    @property
    def default_data(self):
        return {"_uuid": self.uuid, "_uid": self.user_id, "_csrftoken": self.token}

    # Function to get the JSON data for a request
    def json_data(self, data=None):
        if data is None:
            data = {}
        data.update(self.default_data)
        return json.dumps(data)

# Main function to run the script
if __name__ == "__main__":
    username = input("Enter your Instagram email: ")
    password = input("Enter your Instagram password: ")
    photo_path = input("Enter the path to the photo: ")
    caption = input("Enter the caption for the photo: ")

    api = API(username, password)
    api.login()
    if api.is_logged_in:
        api.upload_photo(photo_path, caption)
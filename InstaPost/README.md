# InstaPost

This package allows you to generate Instagram captions using AI and schedule posts with images and captions to be uploaded at a specified date and time. It includes the following components:

- **`captionGen.py`**: Generates engaging Instagram captions using AI.
- **`instaPost.py`**: Handles Instagram login and photo uploads.
- **`schedulePost.py`**: Combines caption generation and photo upload to schedule posts.

This is a branch of the old python package instabot, specifically the api from this github repo: https://github.com/instagrambot/api.git. 
It used a bunch of other depricated packages and no longer worked on the latest versions of python. I went through condenced it by removing anything I didn't
need for this project, and updated all the dependancies. It now runs on python 3.13, and is focused on logging into instagram and posting.

> **NOTE:** The purpose of this was to get an MVP for a project until we can get the official Instagram API. The way this script works, Instagram will
> eventually detect that your are running a bot and will require a captia challange (which this script cannont handle). Currently I haven't tested much,
> but I have gotten roughly 20-40 logins before it was noticed.

---

This script logs into an Instagram account and uploads a photo with a caption. It uses the `requests` library to interact with the Instagram API and the `Pillow` library to handle image processing.

## Usage

### 1. **Generate Captions**
Run the `captionGen.py` script to generate a caption for your Instagram post:
```bash
python captionGen.py
```
Follow the prompts to input:
- Your industry
- Your target audience
- A description of the post

The script will output an AI-generated caption.

---

### 2. **Upload a Photo**
Run the `instaPost.py` script to upload a photo with a caption:
```bash
python instaPost.py
```
Follow the prompts to input:
- Your Instagram username and password
- The path to the photo
- The caption for the photo

The script will log in to your Instagram account and upload the photo.

---

### 3. **Schedule a Post**
Run the `schedulePost.py` script to schedule a post:
```bash
python schedulePost.py
```
Follow the prompts to input:
- Your Instagram username and password
- The path to the photo
- Your industry, audience, and post description (for caption generation)
- The date and time to post (in `YYYY-MM-DD HH:MM` format)

The script will:
1. Generate a caption using AI.
2. Ask for your approval of the caption.
3. Wait until the specified time and upload the photo with the caption.

---


## Example Workflow

1. **Generate a Caption**:
   ```bash
   python captionGen.py
   ```
   Input:
   ```
   Industry: flowers
   Audience: high schoolers
   Description: Don't forget to give your prom date some beautiful flowers.
   ```
   Output:
   ```
   "Make prom night unforgettable with a bouquet as beautiful as your date! 🌸💃 #PromFlowers"
   ```

2. **Schedule a Post**:
   ```bash
   python schedulePost.py
   ```
   Input:
   ```
   Instagram user email: your_email
   Instagram password: your_password
   Path to photo: /path/to/photo.png 
   Industry: flowers
   Audience: high schoolers
   Description: Don't forget to give your prom date some beautiful flowers.
   Date and time to post: 2025-03-21 18:00
   ```

   The script will:
   - Generate a caption.
   - Ask for your approval.
   - Wait until the specified time and upload the post.

---

## Notes

- Images work best in JPEG format, however other common forms like png shoud work just fine.
- Instagram *will* detect bot activity and require CAPTCHA challenges after repeated logins. This currently cannot bypass this.
- This package is intended for personal use and testing purposes only.

---

## Dependencies

Install the required dependencies using `pip`:
```bash
pip install requests Pillow google-genai
```

---


## Future Improvements

- Integrate with the official Instagram Graph API for more reliable and secure functionality.
- Add support for handling CAPTCHA challenges.
- Improve error handling and logging.

---

## Disclaimer

This package is not affiliated with or endorsed by Instagram. Use it at your own risk.
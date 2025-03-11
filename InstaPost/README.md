## instaPost

This script logs into an Instagram account and uploads a photo with a caption. It uses the `requests` library to interact with the Instagram API and the `Pillow` library to handle image processing.

### Configuration

The script includes several configuration constants:

- `API_DOMAIN`: The domain for the Instagram API.
- `API_URL`: The base URL for the Instagram API.
- `USER_AGENT_BASE`: The user agent string for the Instagram app.
- `SIG_KEY_VERSION`: The signature key version.
- `IG_SIG_KEY`: The Instagram signature key.
- `REQUEST_HEADERS`: The default request headers for the Instagram API.

### Utility Functions

#### `get_image_size(fname)`

Returns the width and height of the image specified by `fname`.

#### `resize_image(fname)`

Resizes the image specified by `fname` to meet Instagram's aspect ratio requirements. Returns the path to the resized image.

#### `compatible_aspect_ratio(size)`

Checks if the aspect ratio of the image size `size` is compatible with Instagram's requirements. Returns `True` if compatible, `False` otherwise.

### `API` Class

The `API` class handles interactions with the Instagram API.

#### `__init__(self, username, password)`

Initializes the `API` object with the specified `username` and `password`. Sets up device settings, user agent, and session.

#### `login(self)`

Logs into the Instagram account using the provided username and password. Updates the session headers and sends a login request to the Instagram API.

#### `upload_photo(self, photo, caption=None)`

Uploads the specified `photo` with the optional `caption` to the Instagram account. Resizes the photo if necessary and sends the upload request to the Instagram API.

#### `configure_photo(self, upload_id, photo, caption="")`

Configures the uploaded photo with the specified `upload_id`, `photo`, and `caption`. Sends a request to the `media/configure/` endpoint.

#### `send_request(self, endpoint, post=None, login=False, with_signature=True, headers=None, extra_sig=None, timeout_minutes=None)`

Sends a request to the specified `endpoint` with the optional `post` data. Handles request headers, signatures, and retries.

#### `generate_signature(data)`

Generates a signature for the specified `data` using the Instagram signature key.

#### Properties

- `cookie_dict`: Returns the session cookies as a dictionary.
- `token`: Returns the CSRF token from the session cookies.
- `user_id`: Returns the user ID from the session cookies.
- `rank_token`: Returns the rank token for the user.
- `default_data`: Returns the default data for requests, including UUID, user ID, and CSRF token.

#### `json_data(self, data=None)`

Returns the specified `data` as a JSON string, including the default data.

### Main Function

The main function prompts the user for their Instagram username, password, photo path, and caption. It then creates an `API` object, logs into the Instagram account, and uploads the photo with the specified caption.

### Example Usage

To use the script, run it from the command line:

```sh
python instagramBot.py
```

Follow the prompts to enter your Instagram username, password, photo path, and caption. The script will log into your Instagram account and upload the specified photo with the provided caption.

### Dependencies

- `requests`: For making HTTP requests to the Instagram API.
- `Pillow`: For image processing.
- `uuid`: For generating unique identifiers.
- `hmac`, `hashlib`, `urllib.parse`: For generating request signatures.
- `logging`: For logging messages.

Install the required dependencies using `pip`:

```sh
pip install requests Pillow
```

### Notes

- Ensure that the image file is in JPEG format and meets Instagram's aspect ratio requirements.
- The script handles login, photo upload, and photo configuration, including retries and error handling.
- The script uses a user agent string for the Instagram app and includes necessary request headers for interacting with the Instagram API.
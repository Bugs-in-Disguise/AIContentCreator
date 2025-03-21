from datetime import datetime, timedelta
import time
import threading
from captionGen import generate_instagram_post
from instaPost import API

def schedule_post(username, password, photo_path, industry, audience, description, post_time):
    api = API(username, password)
    api.login()
    
    if api.is_logged_in:
        post_text = generate_instagram_post(industry, audience, description)
        print("Generated Caption: ", post_text)
        
        approval = input("Do you approve this caption? (yes/no): ")
        if approval.lower() == 'yes':
            wait_time = (post_time - datetime.now()).total_seconds()
            if wait_time > 0:
                print(f"Post scheduled for {post_time}. Waiting...")
                time.sleep(wait_time)
                api.upload_photo(photo_path, post_text)
                print("Post uploaded successfully!")
            else:
                print("The specified time is in the past. Please choose a future time.")
        else:
            print("Caption not approved. Post will not be scheduled.")
    else:
        print("Login failed. Cannot schedule post.")

if __name__ == "__main__":
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    photo_path = input("Enter the path to the photo: ")
    industry = input("What industry are you a part of? ")
    audience = input("What is your target Audience? ")
    description = input("Describe the purpose behind your post: ")

    current_datetime = datetime.now()
    print("Current date and time:", current_datetime)
    
    post_time_input = input("Enter the date and time to post (YYYY-MM-DD HH:MM): ")
    post_time = datetime.strptime(post_time_input, "%Y-%m-%d %H:%M")
    
    schedule_post(username, password, photo_path, industry, audience, description, post_time)
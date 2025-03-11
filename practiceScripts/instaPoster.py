from instabot import Bot
from captionGen import generate_instagram_post

bot = Bot()

bot.login(username="USER_EMAIL", password="PASSWORD")

cap = generate_instagram_post("Content Creation", "Investors", "We are starting a buisness where we help automate social media marketing")

bot.upload_photo("BID", caption=cap)

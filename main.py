import praw
import pytesseract
import cv2
import urllib.request
import numpy as np

import creds


def get_image(img_url):
    req = urllib.request.urlopen(img_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv2.imdecode(arr, -1)


app_id = "text_from_pics"
version = '1.0.beta'
user_agent = f"python:{app_id}:{version} (by /u/lakmus85_real)"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

reddit = praw.Reddit(
    client_id=creds.client_id,
    client_secret=creds.secret,
    password=creds.password,
    user_agent=user_agent,
    username=creds.username,
)

for submission in reddit.subreddit("mildlyinfuriating").stream.submissions():
    url = submission.url
    if url.endswith('.png') or url.endswith('.jpg'):
        submission.comments.replace_more(limit=0)
        processed = False
        for top_level_comment in submission.comments:
            if top_level_comment.author == 'lakmus85_real' and top_level_comment.body.find("Bot version:") > -1:
                processed = True

        if processed:
            continue

        image = get_image(submission.url)
        text = pytesseract.image_to_string(image)

        if len(text) > 10:
            submission.reply(
                f"*This action is performed by a bot. Automatically recognized text from the picture:*  \n{text}  \n^({version})")

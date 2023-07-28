from google_speech import Speech
from threading import Thread
import requests
import uuid

def start():
    url = "https://api.vvhan.com/api/love"
    response = requests.get(url=url) 
    text = response.text.replace("<p>", "").replace("</p>", "").replace("\n", "")
    tts = Speech(text, "zh")

    file_name = str(uuid.uuid4())
    tts.save(f"./audios/{file_name}.mp3")
    with open(f"./audios/{file_name}.txt", "w", encoding="u8") as f:
        f.write(text)

if __name__ == "__main__":
    tasks = []
    for _ in range(10):
        tasks.append(Thread(target=start))
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
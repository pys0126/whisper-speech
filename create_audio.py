import requests, os
from uuid import uuid4

def fetch_mp3_url(message: str) -> str:
    url = f"https://zj.v.api.aa1.cn/api/baidu-01/?msg={message}"
    response = requests.get(url=url)
    download_url = response.json().get("download")
    return download_url

def download_mp3(url: str, save_dir: str) -> str:
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    response = requests.get(url=url)
    file_name = os.path.join(save_dir, str(uuid4()) + ".mp3")
    with open(file_name, "wb") as f:
        f.write(response.content)
    return file_name

def fetch_message() -> str:
    url = "https://v.api.aa1.cn/api/tiangou/index.php"
    response = requests.get(url=url)    
    return response.text

def save_message(message: str, mp3_file_name: str) -> str:
    file_name = mp3_file_name[:-3] + "txt"
    with open(file_name, "w", encoding="u8") as f:
        f.write(message)
    return file_name

if __name__ == "__main__":
    save_dir = "./audios"
    message = fetch_message()
    mp3_url = fetch_mp3_url(message=message)
    mp3_file_name = download_mp3(url=mp3_url, save_dir=save_dir)
    message_file_name = save_message(message=message, mp3_file_name=mp3_file_name)
    print(message.replace("\n", ""))
    print(mp3_file_name)
    print(message_file_name)



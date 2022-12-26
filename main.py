import requests
from pprint import pprint



class YandexDisk:
    files_url = "https://cloud-api.yandex.net/v1/disk/resources/files"
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def __init__(self, token):
        self.token = token

    @property
    def headers(self):
        return {
            "content-type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def get_upload_link(self, file_path):
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.headers)
        jsonify = response.json()
        pprint(jsonify)
        return jsonify

    def upload(self, file_path):
        href = self.get_upload_link(file_path).get("href")
        if not href:
            return

        with open(file_path, "rb") as file:
            response = requests.put(href, data=file)
            if response.status_code == 201:
                print("Файл загружен")
                return True
            print("Файл не загружен", response.status_code)
            return False

def get_token():
    with open("token.txt", "r") as file:
        return file.readline()

token = YandexDisk(get_token())
token.upload("image.jpg")
import requests
from io import BytesIO
from zipfile import ZipFile

url = 'http://mattmahoney.net/dc/text8.zip'

try:
    response = requests.get(url)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall()
        print("Files extracted successfully.")

except requests.exceptions.RequestException as e:
    print(f"Error downloading the file: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

url = "https://raw.githubusercontent.com/nicholas-leonard/word2vec/master/questions-words.txt"

try:
  response = requests.get(url)
  response.raise_for_status()

  file_content = response.text

  with open("files/questions-words.txt", "w") as src:
    src.write(file_content)

except requests.exceptions.RequestException as e:
  print(f"Error downloading the file: {e}")
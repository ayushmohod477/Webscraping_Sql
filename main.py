import requests
import selectorlib
import smtplib, ssl
import os
from dotenv import load_dotenv

URL = "http://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "justjigyasu@gmail.com"
    password = os.getenv('password')
    # password = "guky ksta hmzw pvzj"

    receiver = "justjigyasu@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent")


def read():
    with open("data.txt", "r") as file:
        return file.read()


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


if __name__ == "__main__":
    load_dotenv()
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read()
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message=f"Hey! New event {extracted} was announced")



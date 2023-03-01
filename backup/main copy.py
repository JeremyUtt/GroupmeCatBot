import requests
import json
from os import urandom
from time import sleep
import fs

def login(username, password, pinCB):
    deviceID = urandom(16).hex()

    session = requests.Session()

    res = session.request("POST", "https://v2.groupme.com/access_tokens", headers={
        'Content-Type': 'application/json'
    }, data=json.dumps({
        "username": username,
        "password": password,
        "grant_type": "password",
        "app_id": "groupme-web",
        "device_id": deviceID
    }))

    parsed = json.loads(res.text)
    code = parsed["response"]["verification"]["code"]

    res = session.request("POST", f"https://api.groupme.com/v3/verifications/{code}/initiate", headers={
        'Content-Type': 'application/json',
    }, data=json.dumps(
        {
            "verification": {
                "method": "sms"
            }
        }
    ))

    pin = pinCB()

    res = session.request("POST", f"https://api.groupme.com/v3/verifications/{code}/confirm", headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        "verification": {
            "pin": pin
        }
    }))

    res = session.request("POST", "https://v2.groupme.com/access_tokens", headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        "username": username,
        "password": password,
        "grant_type": "password",
        "app_id": "groupme-web",
        "device_id": deviceID,
        "verification": {
            "code": code
        }
    }))

    parsed = json.loads(res.text)
    token = parsed["response"]["access_token"]
    return token

def createPost(accessToken, groupID, text, imageURLs):
    res = requests.request("POST", f"https://api.groupme.com/v3/groups/{groupID}/messages", headers={
        'Content-Type': 'application/json',
        'X-Access-Token': accessToken
    }, data=json.dumps({
        "message": {
            "source_guid": urandom(16).hex(),
            "attachments": list(map(lambda imageURL: {
                "type": "image",
                "url": imageURL 
            }, imageURLs)),
            "text": text
        }
    }))
    
    parsed = json.loads(res.text)
    
    id = parsed["response"]["message"]["id"]
    
    return id

def uploadImage(accessToken, contentType, raw):
    res = requests.request("POST", "https://image.groupme.com/pictures", headers={
        'Content-Type': contentType,
        'X-Access-Token': accessToken
    }, data=raw)
    
    parsed = json.loads(res.text)
    
    picture_url = parsed["payload"]["picture_url"]
    
    return picture_url

def getCat():
    res = requests.get('https://some-random-api.ml/img/cat')
    response = json.loads(res.text)
    res = requests.request("GET", response["link"])

    contentType = res.headers.get("Content-Type")
    return (contentType, res.content)

accessTokenFile = open("key.txt","a+")
accessTokenFile.seek(0)
accessToken = accessTokenFile.read()
if(accessToken == ""):
    accessToken = login("jeremyu2022@gmail.com", "xkjDT1neDA#vX7", lambda: input("Enter confirmation PIN: "))
    accessTokenFile.write(accessToken)

accessTokenFile.close()

for i in range(0, 1):
    (contentType, raw) = getCat()

    image_url = uploadImage(accessToken, contentType, raw)

    createPost(accessToken, "88758093", "cat", [
        image_url
    ])
    
    sleep(2)
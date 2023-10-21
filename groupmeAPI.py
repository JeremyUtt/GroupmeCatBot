import requests
import json
from os import urandom

def login(email, password, pinCB):
    """Attempts to log into groupme using a email, password, and sms verification pin. 
    
    Args:
        email (str): email of user
        password (str): Password of User
        pinCB (str Callback): Callback function for the verification pin, which is not known at function runtime

    Returns:
        str: Access token
    """
    
    print("Starting Login Process...")

    
    # Generate random 16 bit device Id
    deviceID = urandom(16).hex()

    # Creates a web session the persists cookies across requests
    session = requests.Session()

    # Request 1: send email and password
    print("Sending Email and Password...")
    res = session.request("POST", "https://v2.groupme.com/access_tokens", 
        headers={
            'Content-Type': 'application/json'
        }, 
        data=json.dumps({
            "email": email,
            "password": password,
            "grant_type": "password",
            "app_id": "groupme-web",
            "device_id": deviceID
        })
    )

    # gets the verification code from the responce 
    code = json.loads(res.text)["response"]["verification"]["code"]


    # Request 2: ask to verify through sms
    print("Requesting SMS verification pin")
    res = session.request("POST", f"https://api.groupme.com/v3/verifications/{code}/initiate", 
        headers={
            'Content-Type': 'application/json',
        }, 
        data=json.dumps({
            "verification": {
                "method": "sms"
            }
        })
    )
    print("SMS verification pin sent to user. Check your phone")

    # TODO: understand callbacks more and add useful comment
    # Gets pin from Callback function passed in from login(...,pinCB) 
    pin = pinCB()

    # Request 3: send the verification PIN
    print(f"sending verification pin: {pin}...")
    res = session.request("POST", f"https://api.groupme.com/v3/verifications/{code}/confirm", 
        headers={
            'Content-Type': 'application/json',
        }, 
        data=json.dumps({
            "verification": {
                "pin": pin
            }
        })
    )
    
    
    # TODO: figure out why info must be sent a second time
    # Request 4: sends all information again?
    res = session.request("POST", "https://v2.groupme.com/access_tokens", 
        headers={
            'Content-Type': 'application/json',
        }, 
        data=json.dumps({
            "email": email,
            "password": password,
            "grant_type": "password",
            "app_id": "groupme-web",
            "device_id": deviceID,
            "verification": {
                "code": code
            }
        })
    )
    
    # Get the access token from the responce
    token = json.loads(res.text)["response"]["access_token"]
    return token

def createPost(accessToken, groupID, text, imageURLs):
    """Creates a post on groupme using text and/or pre-uploaded images

    Args:
        accessToken (str): Access token for authentication
        groupID (str): Id of group to post in
        text (str): message contents to post
        imageURLs (str): URl(s) of pre uploaded images

    Returns:
        str: Post ID
    """
    try:
        

        res = requests.request("POST", f"https://api.groupme.com/v3/groups/{groupID}/messages", 
            headers={
                'Content-Type': 'application/json',
                'X-Access-Token': accessToken
            }, 
            data=json.dumps({
                "message": {
                    # create random ID for the post
                    "source_guid": urandom(16).hex(),
                    # TODO: understand how list(map(foo, bar), foo2) works
                    "attachments": list(
                        map(lambda imageURL: {
                            "type": "image",
                            "url": imageURL
                        },
                        imageURLs
                        )
                    ),
                    "text": text
                }
            })
        )

        
        # gets the ID of the post from the server
        # (different than "source_guid"?)
        # TODO: is source_guid and id different?
        
        # try:
        return json.loads(res.text)["response"]["message"]["id"]
    except:
        print("Error creating post")
        return None

def uploadImage(accessToken, contentType, rawImage):
    """ Since GroupMe does not like outside images, 
        we must first upload the image to their server before
        we can post it to a chat
    
    Args:
        accessToken (str): access token for GroupMe login
        contentType (str): the type of content to post
        rawImage (bytes): raw bytes of the image to post

    Returns:
        str: Groupme Photo Url
    """
    try:
        
        
        # Uploads the photo to GroupMe
        res = requests.request("POST", "https://image.groupme.com/pictures", 
            headers={
                'Content-Type': contentType,
                'X-Access-Token': accessToken
            }, 
            data=rawImage
        )
        
        # Gets the new photo URL from the responce 
        picture_url = json.loads(res.text)["payload"]["picture_url"]
        return picture_url
    except:
        print("Error uploading image")
        return None
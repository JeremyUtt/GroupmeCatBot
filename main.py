# Python Modules
import requests
import json
from time import sleep

# Custom Librarys
from groupmeAPI import *
from accountManagement import *


def main():
    (accounts, groups) = readFileData()
    
    account = selectAccount(accounts)
    groupId = selectGroup(groups)
    
    accessToken = getAccessToken(account)

    count = int(input("How many photos?"))

    for i in range(0, count):
        print(f"fetching and sending cat {i+1} to group {groupId}")
        
        (contentType, rawImage) = getCat()

        image_url = uploadImage(accessToken, contentType, rawImage)

        createPost(accessToken, groupId, "cat", [image_url])

        sleep(2)
   
def getAccessToken(account):
    """Looks for a preexisting file containing a access token.
    if none is found, calls the login() function to get a new token

    Returns:
        string: Access Token
    """
    
    print("Checking for pre-existing access token...")
    
    token = account["token"]
    email = account["email"]
    password = account["password"]
    accountIndex = account["accountIndex"]
    
    
    if token == "":
        print("Token Not found, logging in w/ email, password")
        token = login(email, password, lambda: input("Enter confirmation PIN: "))
        writeAccountData(accountIndex, "token", token)
    else:
        print("Token Found!")

    return token
    
def getCat():
    """Get a random photo od a cat using an API

    Returns:
        str: contentType
        bytes: raw image bytes
    """
    
    
    # go to given Url, returns another Url of a cat picture
    res = requests.get('https://some-random-api.ml/img/cat')
    
    # gets the New URL from the responce
    parsed = json.loads(res.text)["link"]
    
    # Get the photo of the cat
    res = requests.request("GET", parsed)

    # get the type of content and return w/ it and photo data
    contentType = res.headers.get("Content-Type")
    return (contentType, res.content)

if __name__ == "__main__":
    main()
# Python Modules
import requests
import json
from time import sleep

# Custom Librarys
from groupmeAPI import *
from accountManagement import *


def main():
    setupAccounts()
    
    
    askQuestion = True
    while askQuestion:
        print("What would you like to do?")
        print("1: Run Cat Bot")
        print("2: Add Account to Database")
        print("3: Add Group to Database")
        option = input("Selection (1-3, default 1):")
        if option == "1" or option == "":
            askQuestion = False
        elif option == "2":
            addAccount()
        elif option == "3":
            addGroup()
        else:
            print("Invalad Option")
            continue
    

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
    """Get a random photo of a cat using an API

    Returns:
        str: contentType
        bytes: raw image bytes
    """
    
    
    # go to given Url, returns another Url of a cat picture
    res = requests.get('https://cataas.com/cat')
    
    # gets the New URL from the responce
    # parsed = json.loads(res.text)["link"]
    
    # Get the photo of the cat
    # res = requests.request("GET", parsed)

    # get the type of content and return w/ it and photo data
    contentType = res.headers.get("Content-Type")
    return (contentType, res.content)

if __name__ == "__main__":
    main()
import json
import glob

def readFileData():
    accountsFile = open("data/accounts.json", "r")
    accounts = json.loads(accountsFile.read())
    accountsFile.close()
 
    groupsFile = open("data/groups.json", "r")
    groups = json.loads(groupsFile.read())
    groupsFile.close()
    return (accounts, groups)
    
def writeAccountData(accountIndex, index, data):
    jsonFile = open("data/accounts.json", "r")
    accounts = json.loads(jsonFile.read())
    jsonFile.close()
    
    accounts[accountIndex][index] = data
    
    jsonFile = open("data/accounts.json", "w")
    jsonFile.write(json.dumps(accounts))
    jsonFile.close()
    
def selectAccount(accounts):
    for account in accounts:
        index = account["accountIndex"]
        name = account["username"]
        print(f"{index}: {name}")
    selection = 0
    selectionStr = input("Which Account world you like to Use? (default 0):")
    if selectionStr != "":
        selection = int(selectionStr)
    return accounts[selection]

def selectGroup(groups):
    
    index = 0
    for group in groups:
        name = group["name"]
        print(f"{index}: {name}")
        index += 1
    
    selection = 0
    selectionStr = input("Which Group do you want to post in? (default 0):")
    if selectionStr != "":
        selection = int(selectionStr)
    return groups[selection]["id"]

def setupAccounts():
    files = glob.glob("data/*")

    if "data/groups.json" not in files:
        # os.rename("data/groups.template.json", "data/groups.json")
        tempFile = open("data/groups.json", "w")
        tempFile.write(json.dumps([]))
        tempFile.close()

    
    if "data/accounts.json" not in files:
        # os.rename("data/accounts.template.json", "data/accounts.json")
        tempFile = open("data/accounts.json", "w")
        tempFile.write(json.dumps([]))
        tempFile.close()
   
def addAccount():
    username = input("Enter Username:")
    email = input("Enter Email:")
    password = input("Enter Password:")
    phone = input("Enter Phone number:")

    accountsFile = open("data/accounts.json", "r")
    accounts = json.loads(accountsFile.read())
    accountsFile.close()

    accounts.append({
		"accountIndex": len(accounts),
		"username": username,
		"email": email,
		"password": password,
		"phoneNum": phone,
		"token": ""
    })

    accountsFile = open("data/accounts.json", "w")
    accountsFile.write(json.dumps(accounts))
    accountsFile.close()

def addGroup():
    name = input("Enter Group Name:")
    id = input("Enter Group ID:")

    groupsFile = open("data/groups.json", "r")
    groups = json.loads(groupsFile.read())
    groupsFile.close()

    groups.append({
        "name": name,
        "id": id
    })

    groupsFile = open("data/groups.json", "w")
    groupsFile.write(json.dumps(groups))
    groupsFile.close()
    
import json


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

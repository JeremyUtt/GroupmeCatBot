# Groupme-Cat-Bot

A bot that can automatically generate images of cats and upload them to your group-me group. 

## Installation

Simply clone this repository and run main.py in python

## Configuration

To give the bot access to your groupme account, select the **Add Account** Option when prompted and follow in-program directions.

Repeat this same process to add a group ID to the bot.

To find the ID for your group, find an invite link to the group. it should be in the format:

     groupme.com/join_group/**{ID HERE}**/{UNRELATED}

the nunbers in the **ID HERE** section is the Groups ID number.


## Usage

After configuring, run the **main.py** file in python. select which account and group you want to use / post to. 
The first time you use a account, you will be sent a SMS verification code to your group-me account phone number. 
Enter that number into the program when prompted to authenticate the login. 
After the first login, a access token will be stored in your **accounts.json** file meaning future logins will not require a SMS pin. 


## Known Quirks

- If Groupme access token is already found, the program assumes it is valid without checking

- The program assumes the account you select has already joined the group you selected


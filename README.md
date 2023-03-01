# Groupme-Cat-Bot

A bot that can automatically generate images of cats and upload them to your group-me group. 

## Installation

Simply clone this repository and run main.py in python

## Configuration

Currently, there is no feature to configure groupme accounts within the program. To do so, copy the 
**accounts template.json** and **groups template.json**  to **accounts.json** and **groups.json** respectively.
Then, fill in your account and group information into their respective locations in the files. 
Leave the token field in **accounts.json** blank. 

> Note: I plan to add account integration into the program later on

## Usage

After configuring, run the **main.py** file in python. select which account and group you want to use / post to. 
The first time you use a account, you will be sent a SMS verification code to your group-me account phone number. 
Enter that number into the program when prompted to authenticate the login. 
After the first login, a access token will be stored in your **accounts.json** file meaning future logins will not require a SMS pin. 


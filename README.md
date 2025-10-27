# **Telegram Contact Transfer Script**

This Python script allows you to transfer your entire contact list from one Telegram account (a "source" account) to another ("destination" account).

It works by logging into both accounts, fetching the contacts with phone numbers from the source, and importing them into the destination.

## **Requirements**

* Python 3.7+  
* The telethon library

## **Installation**

1. Make sure you have Python installed.  
2. Install the required library using pip:  
   pip install telethon

## **How to Use**

This script is designed to be user-friendly and will prompt you for all necessary information. You do **not** need to edit the .py file.

### **Step 1: Get API Credentials**

You must have API credentials for **both** the source account and the destination account.

1. Log in to your Telegram account at [my.telegram.org](https://my.telegram.org).  
2. Go to "API development tools" and create a new application.  
3. You will be given an api\_id and api\_hash.  
4. **Repeat this process for your *other* account** so you have two sets of keys.

### **Step 2: Run the Script**

1. Open your terminal or command prompt.  
2. Navigate to the directory where contact\_transfer.py is saved.  
3. Run the script:  
   python contact\_transfer.py

4. The script will first ask for the api\_id and api\_hash for the **SOURCE** account (the one you are copying *from*).  
5. It will then ask for your phone number, 2FA password, or login code for that account.  
6. Next, it will ask for the api\_id and api\_hash for the **DESTINATION** account (the one you are copying *to*).  
7. It will ask for the login details for that account.  
8. Once both accounts are logged in, the script will automatically fetch and transfer the contacts.

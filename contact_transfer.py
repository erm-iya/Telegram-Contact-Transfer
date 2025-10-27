import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import GetContactsRequest, ImportContactsRequest
from telethon.tl.types import InputPhoneContact
from telethon.errors.rpcerrorlist import SessionPasswordNeededError

async def login_client(session_name, api_id, api_hash, account_name):
    """Logs in a Telegram client, handling 2FA."""
    client = TelegramClient(session_name, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        print(f"--- Logging in to {account_name} Account ---")
        phone = input(f"Enter the phone number for {account_name}: ")
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input("Enter the code you received: "))
        except SessionPasswordNeededError:
            await client.sign_in(password=input("Enter your 2FA password: "))
        print(f"Successfully logged in to {account_name}!")
    else:
        print(f"Already logged in to {account_name}.")
    
    return client

async def transfer_contacts():
    """
    Transfers contacts directly from one Telegram account to another
    by prompting the user for credentials.
    """
    print("--- Telegram Contact Transfer Utility ---")
    print("You will need API credentials for BOTH accounts (from my.telegram.org).\n")

    # Get Source Account credentials
    print("--- SOURCE Account (Copying FROM) ---")
    api_id_source = input("Enter SOURCE account API ID: ")
    api_hash_source = input("Enter SOURCE account API Hash: ")
    session_source = 'source_account_session'

    # Get Destination Account credentials
    print("\n--- DESTINATION Account (Copying TO) ---")
    api_id_dest = input("Enter DESTINATION account API ID: ")
    api_hash_dest = input("Enter DESTINATION account API Hash: ")
    session_dest = 'destination_account_session'

    client_source = None
    client_dest = None
    contacts_to_import = []

    try:
        # --- Step 1: Connect to the SOURCE account and get contacts ---
        client_source = await login_client(session_source, api_id_source, api_hash_source, "SOURCE")
        
        result = await client_source(GetContactsRequest(hash=0))
        print(f"\nFound {len(result.users)} total contacts in the source account.")

        for i, user in enumerate(result.users):
            if user.phone:
                contact = InputPhoneContact(
                    client_id=i,
                    phone=user.phone,
                    first_name=user.first_name or '',
                    last_name=user.last_name or ''
                )
                contacts_to_import.append(contact)
        
        if not contacts_to_import:
            print("\nNo contacts with phone numbers were found in the source account. Nothing to transfer.")
            return

        print(f"Found {len(contacts_to_import)} contacts with phone numbers to transfer.")
        print("-" * 30)

        # --- Step 2: Connect to the DESTINATION account and import contacts ---
        client_dest = await login_client(session_dest, api_id_dest, api_hash_dest, "DESTINATION")

        print("\nImporting contacts into DESTINATION account...")
        result = await client_dest(ImportContactsRequest(contacts_to_import))
        
        successful_imports = len(result.imported)
        print("\n--- Transfer Complete! ---")
        print(f"Successfully imported {successful_imports} out of {len(contacts_to_import)} contacts.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("This could be due to invalid credentials, rate limits, or other issues.")
    finally:
        # Ensure clients are disconnected
        if client_source and client_source.is_connected():
            await client_source.disconnect()
        if client_dest and client_dest.is_connected():
            await client_dest.disconnect()
        print("\nSessions disconnected. Script finished.")

if __name__ == "__main__":
    asyncio.run(transfer_contacts())

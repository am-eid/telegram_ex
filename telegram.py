import asyncio
import csv
from telethon import TelegramClient
import pyfiglet
from termcolor import colored
import colorama
colorama.init()
text = "Telegram_EX:"
ascii_art = pyfiglet.figlet_format(text)
colored_ascii_art = colored(ascii_art, color='red')
print(colored_ascii_art)

# Replace with API ID and API hash
api_id = 123456
api_hash = 'api hash' #api hash from https://my.telegram.org/auth

# Replace phone_number with your phone number with contry code
phone_number = '201234567'
client = TelegramClient(f'number {phone_number}', api_id, api_hash)

async def main():
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('\033[1;31m'+'Enter the code: '+'\033[0m'))

    dialogs = await client.get_dialogs(limit=None)

    entities = [dialog for dialog in dialogs if dialog.is_group]

    for i, entity in enumerate(entities):
        print('\033[1;31m'+f"{i + 1}. {entity.title}"+'\033[0m')
    group_index = int(input('\033[1;32m'+"Enter the number of the group to extract members : "+'\033[0m')) - 1

    selected_entity = entities[group_index]
    input_entity = selected_entity.input_entity
    participants = await client.get_participants(input_entity, aggressive=True)
    
    name=input('\033[1;31m'+"Enter Name to save : "+'\033[0m')
    count=0
    with open(name+'.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Full Name', 'Username', 'Phone'])
        
        for participant in participants:
            count+=1
            full_name = f"{participant.first_name} {participant.last_name}" if participant.first_name and participant.last_name else participant.first_name or participant.last_name or ""
            writer.writerow([participant.id, full_name, participant.username, participant.phone])
            
    print('\033[1;32m'+f'Done Extract {count} Member'+'\033[0m')
    a=input('\033[1;31m'+"Enter to exit.. : "+'\033[0m')
asyncio.run(main())

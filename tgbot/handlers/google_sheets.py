from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from gspread_asyncio import AsyncioGspreadClient

from tgbot.misc.database import get_users_data
from tgbot.services.google_sheets import create_spreadsheet, add_worksheet, share_spreadsheet, fill_in_data


async def create_spreadsheet_for_user(message: Message, state: FSMContext):
    google_client_manager = message.bot.get('google_client_manager')
    google_client = await google_client_manager.authorize()
    key = '1dZUPGOB4pl6gvf7FApXoCJlmkivCGm_aAS1Ew5UZoVk'

    # async_spreadsheet = await create_spreadsheet(google_client, 'New File')
    # await add_worksheet(async_spreadsheet, 'New List')
    # await share_spreadsheet(async_spreadsheet, email='kamoliddinibrohimov777@gmail.com', perm_type='anyone')
    # key = async_spreadsheet.ss.id
    await state.update_data(
        spreadsheet_id=key
    )
    await message.answer(f'Your file is here: https://docs.google.com/spreadsheets/d/{key}')


async def get_statistics(message: Message, state: FSMContext):
    data = await get_users_data()
    google_client_manager = message.bot.get('google_client_manager')
    google_client = await google_client_manager.authorize()

    data_fsm = await state.get_data()
    key = data_fsm.get('spreadsheet_id')
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.worksheet('Sheet1')
    await fill_in_data(worksheet, data, headers=['ID', 'Name', 'First Name', 'Phone', 'Address', 'Orders Amount'])
    await message.answer('Data has been completed!')


async def get_records(message: Message, state: FSMContext):
    data_fsm = await state.get_data()

    google_client_manager = message.bot.get('google_client_manager')
    google_client = await google_client_manager.authorize()
    key = data_fsm.get('spreadsheet_id')
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.worksheet('Sheet1')

    data = await worksheet.range(name='A31:E31')
    text = '31: ' + ', '.join([cell.value for cell in data])
    await message.answer(text)


def register_google_spreadsheets(dp):
    dp.register_message_handler(create_spreadsheet_for_user, Command('create'))
    dp.register_message_handler(get_statistics, Command('get_stats'))
    dp.register_message_handler(get_records, Command('get_records'))

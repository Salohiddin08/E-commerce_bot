from loader import dp,bot,db
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio
from utils.notify_admins import start,shutdown
from utils.set_botcommands import commands
import logging
import sys
import handlers


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands,scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        # Create Users Table
        try:
            db.create_table_users()
            db.create_table_products()
            db.create_table_categories()
            db.create_table_orders()
            db.add_to_cart()
            db.add_to_like()
        except:
            pass
        #############################
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

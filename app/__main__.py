from aiogram.utils import executor

from app.core import dp
from app import handlers


# Setup handlers
dp.register_message_handler(handlers.cmd_start, commands=["start"])
dp.register_message_handler(handlers.cmd_key, commands=["key"])
dp.register_message_handler(handlers.cmd_update, commands=["update"])
dp.register_message_handler(handlers.cmd_revoke, commands=["revoke"])
dp.register_message_handler(handlers.cmd_delete, commands=["delete"])
dp.register_message_handler(handlers.cmd_add, commands=["add"])
dp.register_inline_handler(handlers.inline_quotes)

# Start
executor.start_polling(dp)

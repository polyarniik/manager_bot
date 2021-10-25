import aiogram
from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import (
    MessageCantBeEdited,
    MessageToEditNotFound,
    MessageIdInvalid,
    MessageNotModified,
)


async def message_sender(bot: Bot, edit=False, **kwargs):
    if edit:
        try:
            return await bot.edit_message_text(**kwargs)
        except (
            MessageCantBeEdited,
            MessageToEditNotFound,
            MessageIdInvalid,
        ) as e:
            print(e)
            del kwargs["message_id"]
            return await bot.send_message(**kwargs)
        except MessageNotModified:
            pass
    else:
        return await bot.send_message(**kwargs)


async def delete_previous_messages(bot: Bot, chat_id: int, state: FSMContext):
    async with state.proxy() as data:
        try:
            if "mess_to_del" in data:
                for mess_id in data["mess_to_del"]:
                    await bot.delete_message(
                        chat_id=chat_id,
                        message_id=mess_id,
                    )
                del data["mess_to_del"]
        except KeyError:
            pass
        except aiogram.exceptions.MessageToDeleteNotFound as e:
            print(e)
        except aiogram.exceptions.MessageCantBeDeleted as e:
            print(e)

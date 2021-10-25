from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboards.inline as ik
from config.loader import bot
from data import callback_data_attrs as ca
from data.database import Manager
from states.AdminState import AdminState
from utils.message_worker import message_sender, delete_previous_messages
from utils.state_worker import add_mess_id_to_state


async def get_admin_panel(message: Message, state: FSMContext):
    await add_mess_id_to_state(state, message.message_id)
    await delete_previous_messages(
        bot=bot,
        chat_id=message.chat.id,
        state=state,
    )
    await state.reset_state()
    mess = await message_sender(
        bot=bot,
        edit=False,
        chat_id=message.chat.id,
        text="Админ-меню",
        reply_markup=await ik.show_admin_menu(),
    )
    await add_mess_id_to_state(state, mess.message_id)


async def get_admin_panel_callback(callback: CallbackQuery, state: FSMContext):
    await state.reset_state()
    mess = await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Админ-меню",
        reply_markup=await ik.show_admin_menu(),
    )
    await delete_previous_messages(
        bot=bot,
        chat_id=callback.message.chat.id,
        state=state,
    )
    await add_mess_id_to_state(state, mess.message_id)


async def get_managers_list(callback: CallbackQuery, state: FSMContext):
    await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Список менеджеров",
        reply_markup=await ik.show_manager_list(),
    )


async def add_manager_handler(callback: CallbackQuery, state: FSMContext):
    await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Перешли сообщение от менеджера или отправьте его Telegram ID",
    )
    await AdminState.enter_manager_id.set()


async def get_manager_id(message: Message, state: FSMContext):
    if message.forward_from:
        mess = await message_sender(
            bot=bot,
            chat_id=message.chat.id,
            text=f"Введи ФИО {message.forward_from.username}.\n"
            f"Если это не менеджер, введи /admin",
        )
        await state.update_data(manager_id=message.forward_from.id)
        await AdminState.enter_manager_full_name.set()
        await add_mess_id_to_state(state, mess.message_id, message.message_id)
    else:
        try:
            manager_id = int(message.text)
        except ValueError:
            mess = await message_sender(
                bot=bot, chat_id=message.chat.id, text=f"Это не ID, попробуй ещё раз"
            )
            await add_mess_id_to_state(state, mess.message_id, message.message_id)
            return

        mess = await message_sender(
            bot=bot,
            chat_id=message.chat.id,
            text=f"Введи ФИО {manager_id}.\n" f"Если это не менеджер, введи /admin",
        )
        await add_mess_id_to_state(state, mess.message_id, message.message_id)
        await state.update_data(manager_id=message.forward_from.id)
        await AdminState.enter_manager_full_name.set()


async def get_manager_full_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    try:
        manager = await Manager.create(
            telegram_id=state_data["manager_id"],
            full_name=message.text.strip(),
        )
    except:
        mess = await message_sender(
            bot=bot,
            chat_id=message.chat.id,
            text=f"Менеджер с таким id уже есть.",
        )
        await add_mess_id_to_state(state, mess.message_id)
        return
    await add_mess_id_to_state(state, message.message_id)
    await delete_previous_messages(
        bot=bot,
        chat_id=message.chat.id,
        state=state,
    )
    mess = await message_sender(
        bot=bot,
        chat_id=message.chat.id,
        text=f"Менеджер {manager.full_name} - {manager.telegram_id} добавлен",
    )
    await add_mess_id_to_state(state, mess.message_id)


async def show_manager(callback: CallbackQuery, callback_data: dict):
    print(callback_data)
    manager = await Manager.get(int(callback_data[ca.MANAGER_ID]))
    await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=f"Имя: {manager.full_name}\n" f"Telegram ID: {manager.telegram_id}",
        reply_markup=await ik.show_manager_info(manager.telegram_id),
    )


async def delete_manager(callback: CallbackQuery, callback_data: dict):
    print(callback_data)
    manager = await Manager.delete.where(
        Manager.telegram_id == int(callback_data[ca.MANAGER_ID])
    ).gino.status()
    print(manager)
    await callback.answer("Менеджер удалён")
    await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Список менеджеров",
        reply_markup=await ik.show_manager_list(),
    )

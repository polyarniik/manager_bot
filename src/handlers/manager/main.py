from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from config.config import COORDINATOR_ID
from config.loader import bot
from data import callback_data_attrs as ca
from data.database import Subject, Tariff, SaleType, Month, Student, Manager
from keyboards import inline as ik
from keyboards.inline import show_student_is_correct
from services.main import add_update_student, is_student_exist
from states.ManagerState import ManagerState
from utils.message_worker import message_sender, delete_previous_messages
from utils.state_worker import add_mess_id_to_state


async def start(message: Message, state: FSMContext):
    await delete_previous_messages(
        bot=bot,
        chat_id=message.chat.id,
        state=state,
    )
    await state.reset_state()
    mess = await message_sender(
        bot=bot,
        chat_id=message.chat.id,
        text="Выберите предмет, по которому сделана продажа:",
        reply_markup=await ik.show_subjects(),
    )
    await add_mess_id_to_state(state, mess.message_id, message.message_id)


async def get_subject_handler(callback: CallbackQuery, callback_data: dict):
    await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери тип продажи:",
        reply_markup=await ik.show_sale_types(callback_data),
    )


async def get_sale_type_handler(
        callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    if (await SaleType.get(int(callback_data[ca.SALE_TYPE]))).name == "Новая продажа":
        await state.update_data(is_exist=False)
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выберите тариф:",
            reply_markup=await ik.show_tariffs(callback_data),
        )
    else:
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Введите email ученика для продления: ",
        )
        await ManagerState.enter_existing_email.set()
        await state.update_data(is_exist=True, callback_data=callback_data)
        await state.update_data(callback_data)


async def check_email_existing(message: Message, state: FSMContext):
    state_data = await state.get_data()
    student = await is_student_exist(message.text, int(state_data[ca.SUBJECT]))
    if student:
        await message_sender(
            bot=bot,
            chat_id=message.chat.id,
            text=f"{student} {message.text} это он?",
            reply_markup=await show_student_is_correct(),
        )
        await state.update_data(email=message.text)
        await state.reset_state(with_data=False)
    else:
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=message.chat.id,
            message_id=message.message_id,
            text="Такого ученика нет, введите другой email ученика для продления: ",
        )


async def is_founded_user_correct(callback: CallbackQuery, state: FSMContext):
    if callback.data == "student_correct":
        state_data = await state.get_data()
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Выберите тариф:",
            reply_markup=await ik.show_tariffs(state_data["callback_data"]),
        )
    else:
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Снова введите email ученика для продления: ",
        )
        await ManagerState.enter_existing_email.set()


async def get_tariff_handler(callback: CallbackQuery, callback_data: dict):
    await message_sender(
        bot=bot,
        edit=True,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выберите месяц: ",
        reply_markup=await ik.show_months(callback_data),
    )


async def get_month_handler(
        callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    callback_data.pop("@")
    await state.update_data(callback_data)
    state_data = await state.get_data()
    if state_data["is_exist"]:
        await get_email_handler(callback.message, state)
    else:
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Напиши фамилию и имя ученика (как ВКонтакте):",
        )
        await ManagerState.enter_vk_name.set()


async def get_vk_name_handler(message: Message, state: FSMContext):
    await state.update_data(vk_name=message.text)
    mess = await message_sender(
        bot=bot,
        chat_id=message.chat.id,
        text="Напиши ссылку на страницу ВКонтакте ученика:",
    )
    await add_mess_id_to_state(
        state,
        message.message_id,
        mess.message_id,
    )
    await ManagerState.enter_vk_url.set()


async def get_vk_url_handler(message: Message, state: FSMContext):
    await state.update_data(vk_url=message.text)
    mess = await message_sender(
        bot=bot,
        chat_id=message.chat.id,
        text="Напиши почту (email) ученика:",
    )
    await add_mess_id_to_state(
        state,
        message.message_id,
        mess.message_id,
    )
    await ManagerState.enter_email.set()


async def get_email_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if "email" not in state_data:
        await state.update_data(email=message.text)
    state_data = await state.get_data()
    subject = await Subject.get(int(state_data[ca.SUBJECT]))
    sale_type = await SaleType.get(int(state_data[ca.SALE_TYPE]))
    if state_data[ca.MONTH] == "all_year":
        month = "Весь год"
    else:
        month = (await Month.get(int(state_data[ca.MONTH]))).name
    tariff = await Tariff.get(int(state_data[ca.TARIFF]))
    student = await Student.query.where(
        Student.email == state_data["email"]
    ).gino.first()
    if student:
        message_text = (
            f"<b>Перепроверь, все ли верно введено:</b>\n"
            f"<b><u>{sale_type.name}</u></b>\n"
            f"<b><u>ФИ:</u></b> {student.full_name}\n"
            f"<b><u>ВКонтакте:</u></b> {student.vk_url}\n"
            f"<b><u>Email:</u></b> {student.email}\n"
            f"<b><u>Предмет:</u></b> {subject.name}\n"
            f"<b><u>Тариф:</u></b> {tariff.name}\n"
            f"<b><u>Месяц:</u></b> {month}"
        )
    else:
        message_text = (
            f"<b>Перепроверь, все ли верно введено:</b>\n"
            f"<b><u>{sale_type.name}</u></b>\n"
            f"<b><u>ФИ:</u></b> {state_data['vk_name']}\n"
            f"<b><u>ВКонтакте:</u></b> {state_data['vk_url']}\n"
            f"<b><u>Email:</u></b> {state_data['email']}\n"
            f"<b><u>Предмет:</u></b> {subject.name}\n"
            f"<b><u>Тариф:</u></b> {tariff.name}\n"
            f"<b><u>Месяц:</u></b> {month}"
        )
    await message_sender(
        bot=bot,
        chat_id=message.chat.id,
        text=message_text,
        reply_markup=await ik.show_confirm(),
    )

    await add_mess_id_to_state(
        state,
        message.message_id,
    )
    await state.reset_state(with_data=False)


async def confirm_subscribe(callback: CallbackQuery, state: FSMContext):
    if callback.data.split(":")[1] == "no":
        await start(callback.message, state)
    else:
        await callback.answer("Заполняем данные, ожидайте")
        state_data = await state.get_data()
        await add_update_student(callback.from_user.id, state_data)
        await message_sender(
            bot=bot,
            edit=True,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=callback.message.text.split(":", 1)[1],
        )
        await delete_previous_messages(
            bot,
            callback.from_user.id,
            state,
        )
        state_data = await state.get_data()
        subject = await Subject.get(int(state_data[ca.SUBJECT]))
        sale_type = await SaleType.get(int(state_data[ca.SALE_TYPE]))
        if state_data[ca.MONTH] == "all_year":
            month = "Весь год"
        else:
            month = (await Month.get(int(state_data[ca.MONTH]))).name
        tariff = await Tariff.get(int(state_data[ca.TARIFF]))
        manager = await Manager.get(callback.from_user.id)
        await message_sender(
            bot=bot,
            chat_id=COORDINATOR_ID,
            text=f"<b><u>{sale_type.name}</u></b>\n"
                 f"<b><u>Менеджер:</u></b> {manager.full_name}"
                 f"<b><u>ФИ:</u></b> {state_data['vk_name']}\n"
                 f"<b><u>ВКонтакте:</u></b> {state_data['vk_url']}\n"
                 f"<b><u>Email:</u></b> {state_data['email']}\n"
                 f"<b><u>Предмет:</u></b> {subject.name}\n"
                 f"<b><u>Тариф:</u></b> {tariff.name}\n"
                 f"<b><u>Месяц:</u></b> {month}",
        )
        await state.reset_state()

from aiogram.dispatcher import FSMContext


async def add_mess_id_to_state(state: FSMContext, *args):
    async with state.proxy() as data:
        if "mess_to_del" not in data:
            data["mess_to_del"] = list(args)
        else:
            data["mess_to_del"].extend(args)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
import asyncio

import os
from getting_colors import make_contours, colors_into_code
from bank import make_instruction

TOKEN = ""

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


user_data = {}
def new_user(id):
    if id in user_data.keys():
        return
    user_data[id] = {
        'kubedata': [],
    }


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    new_user(message.from_user.id)

    await message.answer("Привет! Отправь мне фото кубика с жёлтой стороны,"
                         " так что зелёная была сверху от неё и начну решать его!")


@dp.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
    phases = {1: ['красную', 'жёлтая'],
              2: ['синюю', 'жёлтая'],
              3: ['белую', 'синяя'],
              4: ['оранжевую', 'жёлтая'],
              5: ['зелёную', 'жёлтая']}
    new_user(message.from_user.id)
    try:
        user_id = message.from_user.id
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)

        # Формируем имя файла
        filename = f"photo_{user_id}.jpg"
        save_path = os.path.join("buffer", filename)

        await bot.download_file(file.file_path, save_path)

        user_data[message.from_user.id]['kubedata'].append(make_contours(f'buffer/photo_{user_id}.jpg', f"1photo_{user_id}.jpg"))
        if len(user_data[message.from_user.id]['kubedata']) < 6:
            say = phases[len(user_data[message.from_user.id]['kubedata'])]
            await message.answer_photo(
                photo=FSInputFile(f'buffer/1photo_{user_id}.jpg'),
                caption=f"Так, хорошо, теперь сфотографируй {say[0]}"
                        f" сторону, так чтобы {say[1]} была сверху он неё."
            )
        else:
            await message.answer_photo(
                photo=FSInputFile(f'buffer/1photo_{user_id}.jpg'),
                caption=""
            )
            a = colors_into_code(user_data[message.from_user.id]['kubedata'])
            n = make_instruction(a)
            await message.answer_photo(
                photo=FSInputFile(f'shema.png'),
                caption=f'Решение : {n}\nЖду тебя снова! '
                        f'(чтобы решить ещё один куб просто начни присылать мне фото, в той же последовательности как ты делал это ранее)'
            )

            user_data[message.from_user.id]['kubedata'] = []

    except Exception as e:
        await message.answer(f"Ошибка {str(e)}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
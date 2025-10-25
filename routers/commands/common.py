from aiogram import Router, types

router = Router(name=__name__)

@router.message()
async def echo_message(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text= "Wait a second... ",
    # )
    # await message.reply(text=message.text) #отвечает на сообщение
    # await message.answer(text= message.text) #без ответа на сообщение
    if message.text:
        await message.answer(
            text=message.text,
            entities=message.entities,
        )
        print(message.from_user.id)
    elif message.sticker:
        await message.reply_sticker(sticker=message.sticker.file_id)
    else:
        await message.reply(text="This is wrong data")
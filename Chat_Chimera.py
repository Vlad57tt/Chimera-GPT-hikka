# ---------------------------------------------------------------------------------
# Name: Chat_Chimera
# Author: vladdrazz
# Commands:
# .chat 
# ---------------------------------------------------------------------------------

"""
    Copyleft 2023 t.me/vladdrazz                                                            
    This program is free software; you can redistribute it and/or modify 
"""
# meta developer: @vladdrazz


import asyncio

import openai
from telethon import functions
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class ChatGPTfreeMod(loader.Module):
    """
    Бесплатный ChatGPT, основанный на Chimera GPT
    """
    time_prem = "<emoji document_id=5017179932451668652>🕖</emoji>"
    bl_prem = "<emoji document_id=5017122105011995219>⛔</emoji>"
        
    strings = {
        "name": "Chat_Chimera",
        "loading": f"{time_prem} Ваш запрос обрабатывается",
        "no_args": f"{bl_prem} Не указан текст для обработки!",
        "conf_err": f"{bl_prem} Нет рабочего ключа в ",
        "guide": (
            'Как получить Chimera токен:\n1. <a href="https://discord.gg/nYrwM7HHdA">'
            f"Зайдите в официальный дискорд канал</a>.\n2. В ветке #🤖bot напишите <code><b>/key get</b></code> slash командой.\n3. Установите ваш ключ в "
        ),
    }


    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                lambda: "Ключ вашего Chimera API",
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "Model",
                "gpt-3.5-turbo",
                lambda: "Модель, которая будет обрабатывать ваши запросы, доступна по следующему адресу: https://chimeragpt.adventblocks.cc/api/v1/models .",
            ),
        )
        
    async def on_dlmod(self):
        self.prefix = self.get_prefix()
        await self.inline.bot.send_message(
            self._tg_id,
            self.strings["guide"] + f"<code>{self.prefix}config Chat_Chimera</code>",
        )
        
    async def chatcmd(self, message: Message):
        """
        [Текст или ответ]: Получить ответ на ваш вопрос от Chimera GPT.
        """
        txt = utils.get_args_raw(message)
        #self.prefix = self.get_prefix()        
        reply = await message.get_reply_message()
        if not txt and (not reply or not reply.raw_text):
            await utils.answer(message, self.strings["no_args"])
            return
        if self.config["api_key"] is None:
            await utils.answer(message, self.strings["conf_err"] + f"<code>{self.prefix}config Chat_Chimera</code>")
            return

        await utils.answer(message, self.strings["loading"])
        args = txt or reply.raw_text
        
        openai.api_key = self.config["api_key"]
        model = self.config["Model"]
        openai.api_base = "https://chimeragpt.adventblocks.cc/api/v1"
        await utils.answer(message, self.strings["loading"] + '.')
        try:
            conversation = [{"role": "user", "content": args}]
            await utils.answer(message, self.strings["loading"] + '..')
            response = openai.ChatCompletion.create(model=model, messages=conversation)
            ai_response = response.choices[0].message["content"]
            await utils.answer(message, self.strings["loading"] + '...')
            await utils.answer(message, f"<b>🤖 {model} :</b>\n" + ai_response)
        except Exception as ex:
            await utils.answer(message, f"Возникла ошибка, лог: <code><b>{ex}</b></code>")
            

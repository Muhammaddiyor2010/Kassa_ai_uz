from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from loader import db, bot
import io
from google import genai
from google.genai import types
import mimetypes
from aiogram.types import InputFile
import io
import tempfile
import os
from config import load_config
from states.auth import AuthStates

config = load_config()
client = genai.Client(api_key=config.gemini.api_key)

from utils.gemini import Geminiutils

chiqim_router: Router = Router()

gemini = Geminiutils()


@chiqim_router.message(F.voice)
async def audio_msg(message: Message):
    file_id = message.voice.file_id
    
    file = await bot.get_file(file_id)

    file_obj = io.BytesIO()
 

    file_obj.seek(0)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
        await bot.download_file(file.file_path, destination=temp_file)
        temp_file_path = temp_file.name

    try:
        chiqimtext = gemini.get_text(temp_file_path)
        await message.reply(f" {chiqimtext}")
        await gemini.add_chiqimlar(chiqimtext, message.from_user.id)
        # # Gemini'ga yuklash
        # myfile = client.files.upload(file=temp_file_path)
        # # myfile = client.files.upload(file=file_obj, config={ mime_type: "audio/ogg" })

        # prompt = "Ushbu o'zbek tilidagi audioni matnga aylantir"

        # response = client.models.generate_content(
        # model='gemini-2.5-flash',
        # contents=[prompt, myfile]
        # )
        # print(response.text)
        # await message.reply(f" {response.text}")

    except Exception as e:
  # Temporary file'ni o'chiramiz
        print(f"errors: {e}")
        await message.reply(f"error: {e}")
    finally:
      
        os.unlink(temp_file_path)

    
    
        
      
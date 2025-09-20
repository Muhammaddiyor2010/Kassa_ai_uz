from google import genai
from google.genai import types
from loader import db, bot
from config import load_config
from datetime import datetime
from keyboards.keyboards import report_keyboard

class Geminiutils():

    def __init__(self) -> None:
        config = load_config()
        self.client = genai.Client(api_key=config.gemini.api_key)

    async def send_report(self, user_id: int, transaction_type: str, summa: str, kategoriya: str, izoh: str):
        """Foydalanuvchiga hisobot yuborish"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report_text = f"""Hisobotga qo'shildi ✅

{transaction_type}:
Sana: {current_time}

Summa: {summa} so'm
Kategoriya: {kategoriya}
Izoh: {izoh}"""
        
        try:
            await bot.send_message(chat_id=user_id, text=report_text)
            # Hisobot ko'rish uchun inline keyboard yuboramiz
            await bot.send_message(
                chat_id=user_id, 
                text="📊 Hisobotlarni ko'rasizmi?", 
                reply_markup=report_keyboard
            )
        except Exception as e:
            print(f"Hisobot yuborishda xatolik: {e}")

   

    async def add_chiqim_f(self, summa: int, kategoriya: str, izoh: str, user_id: int) -> dict[str, int | str]:
        add = db.add_chiqim(str(summa), izoh, kategoriya, user_id)
        print(f"chiqim qo'shildi - user_id: {user_id}")
        await self.send_report(user_id, "Chiqim", str(summa), kategoriya, izoh)
        return add

    async def add_kirim_f(self, summa: int, kategoriya: str, izoh: str, user_id: int) -> dict[str, int | str]:
        add = db.add_kirim(str(summa), izoh, kategoriya, user_id)
        print(f"kirim qo'shildi - user_id: {user_id}")
        await self.send_report(user_id, "Kirim", str(summa), kategoriya, izoh)
        return add


    def get_text(self,audio):


        myfile = self.client.files.upload(path=audio)
        prompt = "Ushbu o'zbek tilidagi audioni matnga aylantir"

        response = self.client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt, myfile]
        )

        return response.text


    async def add_chiqimlar(self, text, user_id: int):
        add_chiqim = {
                "name": "add_chiqim_f",
                "description": "chiqimlarni saqlash uchun",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summa": {
                            "type": "integer",
                            "description": "chiqimning summasi, qancha ekani, masalan: 90000 so'm, 180000 so'm",
                        },
                        "kategoriya": {
                            "type": "string",
                            "enum": ["ovqat", "kiyim", "mashina", "ta'lim"],
                            "description": "chiqimning kategoriyasi, nima maqsadda sarf qilingani ",
                        },
                        "izoh": {
                            "type": "string",
                            "description": "bu qo'shimcha, bu shunchaki harajat uchun qandaydir izoh",
                        },
                    },
                    "required": ["summa", "kategoriya", "izoh"],
                },
            }
        
        add_kirim = {
                "name": "add_kirim_f",
                "description": "kirimlarni saqlash uchun",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summa": {
                            "type": "integer",
                            "description": "kirimning summasi, qancha ekani, masalan: 500000 so'm, 1000000 so'm",
                        },
                        "kategoriya": {
                            "type": "string",
                            "enum": ["ish", "savdo", "investitsiya", "boshqa"],
                            "description": "kirimning kategoriyasi, qayerdan kelgani",
                        },
                        "izoh": {
                            "type": "string",
                            "description": "bu qo'shimcha, bu shunchaki daromad uchun qandaydir izoh",
                        },
                    },
                    "required": ["summa", "kategoriya", "izoh"],
                },
            }
        tools = types.Tool(function_declarations=[add_chiqim, add_kirim]) # type: ignore
        
        print("salom")


        contents = [
            types.Content(
                role="user", parts=[types.Part(text=text)]
            )
        ]
        config = types.GenerateContentConfig(tools=[tools])


        # Send request with function declarations
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
        try:
            tool_call = response.candidates[0].content.parts[0].function_call # type: ignore
        except (AttributeError, IndexError):
            tool_call = None

        if tool_call is not None:
            if tool_call.name == "add_chiqim_f": # type: ignore
                # user_id ni qo'shamiz
                args = tool_call.args.copy() # type: ignore
                args['user_id'] = user_id
                result = await self.add_chiqim_f(**args) # type: ignore
                print(f"Chiqim qo'shildi: {result}")
            elif tool_call.name == "add_kirim_f": # type: ignore
                # user_id ni qo'shamiz
                args = tool_call.args.copy() # type: ignore
                args['user_id'] = user_id
                result = await self.add_kirim_f(**args) # type: ignore
                print(f"Kirim qo'shildi: {result}")
        else:
            print("AI ma'lumotni tushunmadi yoki funksiya chaqiruvini qaytarmadi")

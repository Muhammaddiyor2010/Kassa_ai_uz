import google.generativeai as genai
from loader import db, bot
from config import load_config
from datetime import datetime
from keyboards.keyboards import report_keyboard

class Geminiutils():

    def __init__(self) -> None:
        config = load_config()
        genai.configure(api_key=config.gemini.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

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
        # Upload audio file using upload_file
        try:
            audio_file = genai.upload_file(path=audio)
            prompt = "Ushbu o'zbek tilidagi audioni matnga aylantir"
            response = self.model.generate_content([prompt, audio_file])
            # Clean up uploaded file
            genai.delete_file(audio_file.name)
            return response.text
        except Exception as e:
            print(f"Upload error: {e}")
            # Fallback: simple text response
            return "Audio fayl yuklanmadi, lekin matn qayta ishlash mumkin"


    async def add_chiqimlar(self, text, user_id: int):
        # Create function declarations for tools
        add_chiqim_tool = genai.types.FunctionDeclaration(
            name="add_chiqim_f",
            description="chiqimlarni saqlash uchun",
            parameters={
                "type": "object",
                "properties": {
                    "summa": {
                        "type": "integer",
                        "description": "chiqimning summasi, qancha ekani, masalan: 90000 so'm, 180000 so'm"
                    },
                    "kategoriya": {
                        "type": "string",
                        "enum": ["ovqat", "kiyim", "mashina", "ta'lim"],
                        "description": "chiqimning kategoriyasi, nima maqsadda sarf qilingani"
                    },
                    "izoh": {
                        "type": "string",
                        "description": "bu qo'shimcha, bu shunchaki harajat uchun qandaydir izoh"
                    },
                },
                "required": ["summa", "kategoriya", "izoh"]
            }
        )
        
        add_kirim_tool = genai.types.FunctionDeclaration(
            name="add_kirim_f",
            description="kirimlarni saqlash uchun",
            parameters={
                "type": "object",
                "properties": {
                    "summa": {
                        "type": "integer",
                        "description": "kirimning summasi, qancha ekani, masalan: 500000 so'm, 1000000 so'm"
                    },
                    "kategoriya": {
                        "type": "string",
                        "enum": ["ish", "savdo", "investitsiya", "boshqa"],
                        "description": "kirimning kategoriyasi, qayerdan kelgani"
                    },
                    "izoh": {
                        "type": "string",
                        "description": "bu qo'shimcha, bu shunchaki daromad uchun qandaydir izoh"
                    },
                },
                "required": ["summa", "kategoriya", "izoh"]
            }
        )
        
        # Create tools list
        tools = [add_chiqim_tool, add_kirim_tool]
        
        print("salom")

        # Generate content with function calling
        response = self.model.generate_content(
            text,
            tools=tools
        )
        
        try:
            # Check if response has function calls
            if response.candidates and response.candidates[0].content.parts:
                part = response.candidates[0].content.parts[0]
                if hasattr(part, 'function_call') and part.function_call:
                    tool_call = part.function_call
                    
                    if tool_call.name == "add_chiqim_f":
                        # user_id ni qo'shamiz
                        args = dict(tool_call.args)
                        args['user_id'] = user_id
                        result = await self.add_chiqim_f(**args)
                        print(f"Chiqim qo'shildi: {result}")
                    elif tool_call.name == "add_kirim_f":
                        # user_id ni qo'shamiz
                        args = dict(tool_call.args)
                        args['user_id'] = user_id
                        result = await self.add_kirim_f(**args)
                        print(f"Kirim qo'shildi: {result}")
                else:
                    print("AI ma'lumotni tushunmadi yoki funksiya chaqiruvini qaytarmadi")
            else:
                print("AI ma'lumotni tushunmadi yoki funksiya chaqiruvini qaytarmadi")
        except Exception as e:
            print(f"Xatolik: {e}")
            print("AI ma'lumotni tushunmadi yoki funksiya chaqiruvini qaytarmadi")

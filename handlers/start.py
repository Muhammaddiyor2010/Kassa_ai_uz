from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import phone
from aiogram.filters.command import Command

from loader import db
from states.auth import AuthStates


start_router: Router = Router()



@start_router.message(Command("start"))
async def start_msg(message: Message, state: FSMContext):
    # Foydalanuvchi mavjudligini tekshiramiz
    existing_user = db.select_user(id=message.from_user.id)
    
    if existing_user is None:
        # Yangi foydalanuvchi - ma'lumotlar bazasiga qo'shamiz
        try:
            db.add_user(id=message.from_user.id, name=message.from_user.full_name, language=message.from_user.language_code)
            print("Yangi foydalanuvchi qo'shildi")
        except Exception as e:
            print(f"Foydalanuvchi qo'shishda xatolik: {e}")
    
    # Barcha foydalanuvchilar uchun darhol botdan foydalanish mumkin
    await state.set_state(AuthStates.phone_entered)
    await message.reply("✅ Xush kelibsiz! Kassa AI - sizning harajat va daromadlaringizni qayd qilib borishga yordam beradi. Ovozli xabar yuboring yoki matn yozing.")

@start_router.message(Command("help"))
async def help_msg(message: Message):
    """Help komandasi - botdan qanday foydalanishni ko'rsatadi"""
    help_text = """🤖 **Kassa AI Bot - Yordam**

**📋 Mavjud komandalar:**
• `/start` - Botni ishga tushirish
• `/help` - Bu yordam xabari

**🎯 Botdan qanday foydalanish:**

**1. Ovozli xabar yuborish** 🎤
• Mikrofon tugmasini bosing
• Ovozli xabar yuboring
• Masalan: "Bugun ovqat uchun 50000 so'm sarf qildim"

**2. Matn yozish** ✍️
• Oddiy matn yozing
• Masalan: "Ishdan 500000 so'm oldim"

**📊 Hisobot ko'rish:**
• Har bir kirim/chiqim kiritilgandan keyin "Hisobotlarni ko'rasizmi?" xabari chiqadi
• "📊 Ha, ko'raman" tugmasini bosing
• To'liq hisobot ko'rsatiladi

**💰 Kategoriyalar:**
• **Chiqim:** ovqat, kiyim, mashina, ta'lim
• **Kirim:** ish, savdo, investitsiya, boshqa

**💡 Maslahatlar:**
• Aniq summa va kategoriya ayting
• Qisqa va tushunarli gapiring
• Bot avtomatik ravishda tahlil qiladi

**❓ Savollar bo'lsa:** @Kassa_aiuz_bot ga yozing"""
    
    await message.reply(help_text, parse_mode="Markdown")

@start_router.message()
async def text_message(message: Message):
    """Matn xabarlarini qabul qilish"""
    from utils.gemini import Geminiutils
    gemini = Geminiutils()
    
    try:
        # Matnni AI ga yuboramiz
        await gemini.add_chiqimlar(message.text, message.from_user.id)
    except Exception as e:
        print(f"Matn qayta ishlashda xatolik: {e}")
        await message.reply("Xatolik yuz berdi. Iltimos qayta urinib ko'ring.")

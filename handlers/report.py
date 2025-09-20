from aiogram import Router, F
from aiogram.types import CallbackQuery
from loader import db
from states.auth import AuthStates

report_router: Router = Router()


@report_router.callback_query(F.data == "show_report")
async def show_report_callback(callback: CallbackQuery):
    """Hisobotlarni ko'rsatish"""
    user_id = callback.from_user.id
    
    # Foydalanuvchining ma'lumotlarini olamiz
    chiqimlar = db.get_user_chiqimlar(user_id)
    kirimlar = db.get_user_kirimlar(user_id)
    total_chiqim = db.get_user_total_chiqim(user_id)
    total_kirim = db.get_user_total_kirim(user_id)
    
    # Hisobot matnini tayyorlaymiz
    report_text = f"""📊 Sizning hisobotlaringiz:

💰 Jami kirim: {total_kirim:,} so'm
💸 Jami chiqim: {total_chiqim:,} so'm
📈 Qoldiq: {total_kirim - total_chiqim:,} so'm

📋 So'nggi chiqimlar:"""
    
    if chiqimlar:
        for chiqim in chiqimlar[:5]:  # So'nggi 5 ta chiqim
            report_text += f"\n• {chiqim[1]} so'm - {chiqim[3]} ({chiqim[2]})"
    else:
        report_text += "\n• Chiqimlar yo'q"
    
    report_text += "\n\n📋 So'nggi kirimlar:"
    
    if kirimlar:
        for kirim in kirimlar[:5]:  # So'nggi 5 ta kirim
            report_text += f"\n• {kirim[1]} so'm - {kirim[3]} ({kirim[2]})"
    else:
        report_text += "\n• Kirimlar yo'q"
    
    try:
        await callback.message.edit_text(report_text)
        await callback.answer("Hisobot yuborildi!")
    except Exception as e:
        print(f"Hisobot yuborishda xatolik: {e}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)

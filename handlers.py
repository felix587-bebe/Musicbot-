import os
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import (
    kb_effects, kb_back, kb_custom_speed, kb_custom_pitch,
    kb_custom_bass, kb_custom_echo, kb_custom_done,
)
from audio import process_audio
from storage import user_states, audio_cache

router = Router()


# ============================================================
# СТАРТ
# ============================================================
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "🎵 <b>Hotoci MuzBot</b>\n\n"
        "Скинь мне <b>аудио</b> или <b>голосовое</b>, "
        "и я обработаю его:\n\n"
        "🐌 Slowed + Reverb\n"
        "⚡ Sped Up\n"
        "🌙 Nightcore\n"
        "🔊 Bass Boost\n"
        "⚙️ Своя настройка",
        parse_mode="HTML"
    )


# ============================================================
# ПРИЁМ АУДИО
# ============================================================
@router.message(F.audio | F.document)
async def handle_audio(message: Message, bot: Bot):
    file_id = None
    if message.audio:
        file_id = message.audio.file_id
    elif message.document:
        file_id = message.document.file_id
    
    if not file_id:
        return
    
    audio_cache[message.from_user.id] = file_id
    user_states.pop(message.from_user.id, None)
    
    await message.answer(
        "🎵 <b>Выбери эффект:</b>",
        reply_markup=kb_effects()
    )


# ============================================================
# ГОТОВЫЕ ЭФФЕКТЫ
# ============================================================
@router.callback_query(F.data.startswith("fx_"))
async def apply_effect(callback: CallbackQuery, bot: Bot):
    effect = callback.data.replace("fx_", "")
    
    if effect == "custom":
        user_states[callback.from_user.id] = {
            "speed": 1.0, "pitch": 1.0, "bass": 0, "echo": 0,
        }
        await callback.message.edit_text(
            "⚙️ <b>Своя настройка</b>\n\nШаг 1/4: Выбери <b>скорость</b>:",
            reply_markup=kb_custom_speed()
        )
        await callback.answer()
        return
    
    file_id = audio_cache.get(callback.from_user.id)
    if not file_id:
        await callback.answer("❌ Сначала отправь аудио!", show_alert=True)
        return
    
    await callback.message.edit_text(f"⏳ Обрабатываю ({effect})...")
    
    file = await bot.get_file(file_id)
    input_path = f"/tmp/{file_id}.mp3"
    await bot.download_file(file.file_path, input_path)
    
    output_path = process_audio(input_path, effect)
    
    if not output_path:
        await callback.message.edit_text("❌ Ошибка обработки")
        await callback.answer()
        return
    
    await callback.message.answer_audio(
        FSInputFile(output_path),
        caption=f"✅ Готово: <b>{effect}</b>",
        parse_mode="HTML"
    )
    
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        pass
    
    await callback.message.delete()
    await callback.answer()


# ============================================================
# СВОЯ НАСТРОЙКА
# ============================================================
@router.callback_query(F.data.startswith("sp_"))
async def set_speed(callback: CallbackQuery):
    speed = float(callback.data.replace("sp_", ""))
    st = user_states.get(callback.from_user.id, {})
    st["speed"] = speed
    user_states[callback.from_user.id] = st
    await callback.message.edit_text(
        f"⚙️ <b>Своя настройка</b>\n\nСкорость: <b>{speed}x</b>\n\nШаг 2/4: Выбери <b>тон</b>:",
        reply_markup=kb_custom_pitch()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pt_"))
async def set_pitch(callback: CallbackQuery):
    pitch = float(callback.data.replace("pt_", ""))
    st = user_states.get(callback.from_user.id, {})
    st["pitch"] = pitch
    user_states[callback.from_user.id] = st
    await callback.message.edit_text(
        f"⚙️ <b>Своя настройка</b>\n\nСкорость: <b>{st['speed']}x</b>\nТон: <b>{pitch}x</b>\n\nШаг 3/4: Выбери <b>бас</b>:",
        reply_markup=kb_custom_bass()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("bs_"))
async def set_bass(callback: CallbackQuery):
    bass = int(callback.data.replace("bs_", ""))
    st = user_states.get(callback.from_user.id, {})
    st["bass"] = bass
    user_states[callback.from_user.id] = st
    await callback.message.edit_text(
        f"⚙️ <b>Своя настройка</b>\n\nСкорость: <b>{st['speed']}x</b>\nТон: <b>{st['pitch']}x</b>\nБас: <b>+{bass} dB</b>\n\nШаг 4/4: Выбери <b>эхо</b>:",
        reply_markup=kb_custom_echo()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ec_"))
async def set_echo(callback: CallbackQuery):
    echo = int(callback.data.replace("ec_", ""))
    st = user_states.get(callback.from_user.id, {})
    st["echo"] = echo
    user_states[callback.from_user.id] = st
    await callback.message.edit_text(
        f"⚙️ <b>Своя настройка</b>\n\nСкорость: <b>{st['speed']}x</b>\nТон: <b>{st['pitch']}x</b>\nБас: <b>+{st['bass']} dB</b>\nЭхо: <b>{echo}%</b>\n\nНажми «Обработать»:",
        reply_markup=kb_custom_done()
    )
    await callback.answer()


@router.callback_query(F.data == "custom_process")
async def custom_process(callback: CallbackQuery, bot: Bot):
    st = user_states.get(callback.from_user.id)
    file_id = audio_cache.get(callback.from_user.id)
    
    if not st or not file_id:
        await callback.answer("❌ Сначала отправь аудио!", show_alert=True)
        return
    
    await callback.message.edit_text("⏳ Обрабатываю...")
    
    file = await bot.get_file(file_id)
    input_path = f"/tmp/{file_id}.mp3"
    await bot.download_file(file.file_path, input_path)
    
    output_path = process_audio(input_path, "custom", st)
    
    if not output_path:
        await callback.message.edit_text("❌ Ошибка обработки")
        await callback.answer()
        return
    
    params_text = f"Скорость: {st['speed']}x, Тон: {st['pitch']}x, Бас: +{st['bass']} dB, Эхо: {st['echo']}%"
    await callback.message.answer_audio(
        FSInputFile(output_path),
        caption=f"✅ Готово: <b>Своя настройка</b>\n{params_text}",
        parse_mode="HTML"
    )
    
    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        pass
    
    await callback.message.delete()
    user_states.pop(callback.from_user.id, None)
    await callback.answer()


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text("🎵 <b>Выбери эффект:</b>", reply_markup=kb_effects())
    await callback.answer() 

def kb_effects():
    """Главное меню эффектов"""
    return {
        "inline_keyboard": [
            [{"text": "🐌 Slowed + Reverb", "callback_data": "fx_slowed"}],
            [{"text": "⚡ Sped Up", "callback_data": "fx_spedup"}],
            [{"text": "🌙 Nightcore", "callback_data": "fx_nightcore"}],
            [{"text": "🔊 Bass Boost", "callback_data": "fx_bassboost"}],
            [{"text": "⚙️ Своя настройка", "callback_data": "fx_custom"}],
        ]
    }


def kb_back():
    """Кнопка назад"""
    return {
        "inline_keyboard": [
            [{"text": "◀️ Назад", "callback_data": "back_main"}],
        ]
    }


def kb_custom_speed():
    """Выбор скорости"""
    return {
        "inline_keyboard": [
            [{"text": "0.7x", "callback_data": "sp_0.7"}],
            [{"text": "0.8x", "callback_data": "sp_0.8"}],
            [{"text": "0.9x", "callback_data": "sp_0.9"}],
            [{"text": "1.0x", "callback_data": "sp_1.0"}],
            [{"text": "1.1x", "callback_data": "sp_1.1"}],
            [{"text": "1.2x", "callback_data": "sp_1.2"}],
            [{"text": "◀️ Назад", "callback_data": "back_main"}],
        ]
    }


def kb_custom_pitch():
    """Выбор тона"""
    return {
        "inline_keyboard": [
            [{"text": "0.8x", "callback_data": "pt_0.8"}],
            [{"text": "0.9x", "callback_data": "pt_0.9"}],
            [{"text": "1.0x", "callback_data": "pt_1.0"}],
            [{"text": "1.1x", "callback_data": "pt_1.1"}],
            [{"text": "1.2x", "callback_data": "pt_1.2"}],
            [{"text": "◀️ Назад", "callback_data": "back_main"}],
        ]
    }


def kb_custom_bass():
    """Выбор баса"""
    return {
        "inline_keyboard": [
            [{"text": "0 dB", "callback_data": "bs_0"}],
            [{"text": "+5 dB", "callback_data": "bs_5"}],
            [{"text": "+10 dB", "callback_data": "bs_10"}],
            [{"text": "+15 dB", "callback_data": "bs_15"}],
            [{"text": "◀️ Назад", "callback_data": "back_main"}],
        ]
    }


def kb_custom_echo():
    """Выбор эха"""
    return {
        "inline_keyboard": [
            [{"text": "0%", "callback_data": "ec_0"}],
            [{"text": "20%", "callback_data": "ec_20"}],
            [{"text": "50%", "callback_data": "ec_50"}],
            [{"text": "80%", "callback_data": "ec_80"}],
            [{"text": "◀️ Назад", "callback_data": "back_main"}],
        ]
    }


def kb_custom_done():
    """Кнопка "Обработать" """
    return {
        "inline_keyboard": [
            [{"text": "✅ Обработать", "callback_data": "custom_process"}],
            [{"text": "◀️ Назад", "callback_data": "back_main"}],
        ]
  } 

import os
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def process_audio(input_path: str, effect: str, params: dict = None) -> str:
    """
    Обрабатывает аудио и возвращает путь к результату.
    
    effect: slowed, spedup, nightcore, bassboost, custom
    params: {"speed": 1.0, "pitch": 1.0, "bass": 0, "echo": 0}
    """
    params = params or {}
    output_path = input_path.replace(".mp3", f"_{effect}.mp3")
    
    effects = {
        "slowed": "atempo=0.85,aecho=0.8:0.9:1000:0.3",
        "spedup": "atempo=1.15",
        "nightcore": "atempo=1.25,asetrate=44100*1.25",
        "bassboost": "bass=g=10",
    }
    
    if effect == "custom":
        # Собираем цепочку из параметров
        filters = []
        
        speed = params.get("speed", 1.0)
        if speed != 1.0:
            filters.append(f"atempo={speed}")
        
        pitch = params.get("pitch", 1.0)
        if pitch != 1.0:
            filters.append(f"asetrate=44100*{pitch}")
        
        bass = params.get("bass", 0)
        if bass > 0:
            filters.append(f"bass=g={bass}")
        
        echo = params.get("echo", 0)
        if echo > 0:
            filters.append(f"aecho=0.8:0.9:{int(echo*10)}:0.3")
        
        af = ",".join(filters) if filters else "anull"
    else:
        af = effects.get(effect)
    
    if not af:
        return None
    
    cmd = [
        FFMPEG,
        "-i", input_path,
        "-af", af,
        "-y",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ FFmpeg error: {result.stderr}")
        return None
    
    return output_path if os.path.exists(output_path) else None 

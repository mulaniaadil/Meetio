# backend/app.py
import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from deepgram_client import transcribe_audio
from murf_client import synthesize_speech
from emotion import detect_emotion
from convo_state import ConversationState

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

conv = ConversationState()

@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...), user_id: str = "anon"):
    # 1) save incoming audio to temp file
    tmp_name = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(tmp_name, "wb") as f:
        f.write(await file.read())

    # 2) ASR: transcribe using Deepgram
    try:
        transcript, asr_conf = transcribe_audio(tmp_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR error: {e}")

    # 3) Emotion detection (simple text-based)
    emotion, score = detect_emotion(transcript)

    # 4) Build reply (simple policy for prototype)
    # Use conversation memory to personalize
    history = conv.get_history(user_id)
    if "stressed" in emotion or score < 0:
        reply_text = (
            "I hear you. It sounds like you are stressed. "
            "Take three deep breaths with me. Inhale... Exhale... "
            "Would you like a short grounding exercise or a calming story?"
        )
    elif "happy" in emotion:
        reply_text = "That's wonderful to hear! Tell me what's going well — I'm listening."
    else:
        reply_text = "Thanks for sharing. Can you tell me one thing that's on your mind right now?"

    conv.append(user_id, {"transcript": transcript, "emotion": emotion, "reply": reply_text})

    # 5) Choose Murf voice based on emotion
    voice_profile = "calm"  # mapping example; murf_client will map to a model voice
    if "sad" in emotion or "stressed" in emotion:
        voice_profile = "soft"
    elif "happy" in emotion:
        voice_profile = "energetic"

    # 6) TTS (Murf Falcon)
    try:
        audio_url = synthesize_speech(reply_text, voice_profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {e}")

    return {
        "transcript": transcript,
        "asr_confidence": asr_conf,
        "detected_emotion": emotion,
        "emotion_score": score,
        "reply_text": reply_text,
        "audio_url": audio_url,
        "history_len": len(history)+1
    }

# --- START of myagent.py ---
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv() 

from livekit.agents import JobContext, WorkerOptions, cli, JobProcess, get_job_context
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import murf, groq, silero, deepgram

class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a voice agent build using Murf TTS",
            stt=deepgram.STT(model="nova-3"),
            llm=groq.LLM(model="llama-3.1-8b-instant"),
            tts=murf.TTS(voice="en-IN-Anisha", style="Conversation"),
            vad=get_job_context().proc.userdata["vad"],
        )

    async def on_enter(self):
        await self.session.say("Hi, I am a voice agent powered by Murf, how can I help you?")



async def entrypoint(ctx: JobContext):
    await ctx.connect()
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session = AgentSession()

    await session.start(
        agent=MyAgent(),
        room=ctx.room
    )


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
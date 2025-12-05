import asyncio
from typing import Any, Callable, Dict, List, Tuple, Type

# --- MOCKED LIVEKIT.AGENTS COMPONENTS ---
# These classes simulate the necessary parts of the livekit.agents ecosystem 
# and your Murf AI implementation for demonstration purposes.

class MockAPIConnectOptions:
    """Mock for APIConnectOptions."""
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

class MockTTS:
    """Mock base class for TTS systems."""
    def __init__(self, sample_rate: int = 24000):
        self.sample_rate = sample_rate
        self.provider = "Murf"

class MockAudioEmitter:
    """Mock for tts.AudioEmitter to simulate audio output."""
    def initialize(self, **kwargs):
        print(f"  [TTS Emitter] Initialized for audio stream (SR: {kwargs.get('sample_rate')})")
    def push(self, data: bytes):
        pass # In a real system, this pushes audio data
    def flush(self):
        print("  [TTS Emitter] Finished pushing audio chunks.")
    def end_input(self):
        print("  [TTS Emitter] Stream closed.")

class MockChunkedStream:
    """Mock for your Murf TTS ChunkedStream."""
    def __init__(self, tts: 'MurfTTS', input_text: str, conn_options: MockAPIConnectOptions):
        self._tts = tts
        self._input_text = input_text
        self._conn_options = conn_options
        self._FlushSentinel = object
    
    async def _run(self, output_emitter: MockAudioEmitter) -> None:
        """Simulates the async work of sending text and receiving audio."""
        print(f"  [Murf TTS] API Call: Synthesizing text via HTTP chunking...")
        print(f"  [Murf TTS] Input: '{self._input_text}'")
        output_emitter.initialize(request_id="mock-id", sample_rate=self._tts.sample_rate, num_channels=1, mime_type="audio/pcm")
        # Simulate pushing data
        await asyncio.sleep(0.01) # Simulate network latency
        output_emitter.push(b'mock_audio_data_1')
        await asyncio.sleep(0.01)
        output_emitter.push(b'mock_audio_data_2')
        output_emitter.flush()

    def __await__(self):
        # Allow the stream to be awaited, as in the livekit framework
        return self._run(MockAudioEmitter()).__await__()


# Use the structure of your original TTS class, but with mocks
class MurfTTS(MockTTS):
    def __init__(self, **kwargs):
        super().__init__(sample_rate=kwargs.get('sample_rate', 24000))
        # Store options as in your original code
        self._opts = type('_TTSOptions', (object,), kwargs)
        self.provider = "Murf AI"

    def synthesize(self, text: str, *, conn_options: MockAPIConnectOptions = MockAPIConnectOptions()) -> MockChunkedStream:
        """Returns a chunked stream object that can be awaited."""
        return MockChunkedStream(tts=self, input_text=text, conn_options=conn_options)


# --- SCHEDULING AND ALARM TOOLS (The 'Action' Components) ---

class CalendarManager:
    """Manages scheduling actions using a mock external API."""
    def schedule_meeting(self, time: str, subject: str, attendees: str) -> str:
        """
        Schedules a meeting in the user's calendar.
        
        Args:
            time (str): The time/date of the meeting (e.g., "tomorrow at 10 AM").
            subject (str): The subject or topic of the meeting.
            attendees (str): Who is invited (e.g., "John and Jane").
        
        Returns:
            str: A confirmation message.
        """
        print(f"\n[CALENDAR TOOL] Executing: Schedule Meeting")
        print(f"    TIME: {time}, SUBJECT: {subject}, INVITES: {attendees}")
        # In a real app, this is where you call the Google/Outlook API
        return f"Got it. I have successfully scheduled a meeting on '{subject}' with {attendees} for {time}."

class AlarmManager:
    """Manages alarm and reminder actions."""
    def set_alarm(self, time: str, message: str = "wake up") -> str:
        """
        Sets a persistent alarm or reminder.

        Args:
            time (str): The time/date to set the alarm (e.g., "7 AM").
            message (str): The purpose of the alarm.
        
        Returns:
            str: A confirmation message.
        """
        print(f"\n[ALARM TOOL] Executing: Set Alarm")
        print(f"    TIME: {time}, MESSAGE: {message}")
        # In a real app, this would use a dedicated reminder service
        return f"Alarm confirmed for {time}. The reminder message is: '{message}'."


# --- AGENT / MCP (The Orchestrator) ---

class AgentMCP:
    """
    Main Agent component that handles user requests, decides the intent,
    executes tools, and uses TTS to deliver the final spoken response.
    """
    def __init__(self, tts: MurfTTS):
        self.tts = tts
        self.calendar = CalendarManager()
        self.alarm = AlarmManager()

    def _mock_llm_decide_action(self, user_text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Mocks the core function-calling logic of a Large Language Model (LLM).
        
        It determines the intent and extracts arguments for the required tool.
        In a real application, this would be an API call to Gemini, OpenAI, etc.
        """
        user_text_lower = user_text.lower()
        
        # NOTE: This mock logic is very basic (keyword matching).
        # A real LLM/NLU system would be far more robust at argument extraction.
        
        if "schedule" in user_text_lower and ("meeting" in user_text_lower or "call" in user_text_lower):
            # Mock extraction for scheduling
            return "schedule_meeting", {
                "time": "Tomorrow at 10:00 AM", 
                "subject": "Project Alpha Status", 
                "attendees": "Alice and Bob"
            }
        
        if "set" in user_text_lower and ("alarm" in user_text_lower or "reminder" in user_text_lower):
            # Mock extraction for setting an alarm
            return "set_alarm", {
                "time": "7:00 AM", 
                "message": "Start the coffee maker"
            }
        
        # Default intent: simple text synthesis (No tool needed)
        return "synthesize_text", {"text": user_text}

    async def handle_request(self, user_text: str) -> None:
        """
        Processes a user's request through the full workflow.
        """
        if not user_text.strip():
            return

        print(f"\n========================================================")
        print(f"Agent received: '{user_text}'")
        print(f"--------------------------------------------------------")
        
        # 1. Intent Recognition (LLM/NLU Step)
        intent, args = self._mock_llm_decide_action(user_text)
        
        print(f"Determined Intent: {intent}")
        print(f"Extracted Arguments: {args}")
        
        final_response_text = ""
        
        # 2. Tool/Action Execution
        if intent == "schedule_meeting":
            # Run the Calendar Tool
            final_response_text = self.calendar.schedule_meeting(**args)
            
        elif intent == "set_alarm":
            # Run the Alarm Tool
            final_response_text = self.alarm.set_alarm(**args)
            
        elif intent == "synthesize_text":
            # Just repeat the input text for a simple chat response
            # In a real LLM-powered agent, this is where the LLM generates a thoughtful response
            final_response_text = f"You said: '{args['text']}'. (This is a generic response as no tool was triggered.)"
        
        # 3. TTS Synthesis (Vocalization)
        print(f"\n[Agent] Final text to vocalize: '{final_response_text}'")
        
        # Call the Murf TTS synthesize method and await the stream result
        await self.tts.synthesize(final_response_text)
        
        print("--------------------------------------------------------")
        print("Workflow complete. Audio sent to user.")
        print("========================================================")

# --- EXECUTION ---

# Function to read user input asynchronously, simulating STT input
async def async_input(prompt: str) -> str:
    """Runs input() in a separate thread to prevent blocking the asyncio loop."""
    return await asyncio.to_thread(input, prompt)

async def main():
    # Initialize the Murf TTS Client
    murf_tts_client = MurfTTS(
        api_key="MOCK_KEY",
        model="FALCON",
        voice="en-US-matthew",
        sample_rate=24000
    )

    # Initialize the Agent/MCP with the TTS client
    agent = AgentMCP(tts=murf_tts_client)
    
    print("Agent is running. Type 'exit' or 'quit' to stop.")
    
    # The continuous conversational loop
    while True:
        try:
            # Simulate receiving STT transcript from a user
            user_input = await async_input("User > ")
            
            if user_input.lower() in ("exit", "quit"):
                print("Agent shutting down.")
                break
            
            # Handle the request and generate the response audio
            await agent.handle_request(user_input)
            
        except EOFError:
            # Handle case where input stream closes (e.g., Ctrl+D)
            print("\nAgent shutting down.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
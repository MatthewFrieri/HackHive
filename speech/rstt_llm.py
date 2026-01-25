import json
import threading
import time
from RealtimeSTT import AudioToTextRecorder
from openai import OpenAI

MODEL = "gpt-4o-mini"
CONFIDENCE_THRESHOLD = 0.7

SYSTEM_PROMPT = """
You are interpreting speech commands in a poker game.

Valid actions:
- CHECK
- CALL
- FOLD
- RAISE(amount)

Speech-to-text output may contain errors, misheard words, or phonetic confusion. For example, the word "fold" may get
interpeted as "hold". Some common examples include: "raise" gets interpreted as "grays", "fold" gets interpreted as "forward", etc.
You must use your best judgement to correct these errors, using the confidence score to reflect the uncertainty of any corrections.

Here are some other common examples to look out for:
{
    "raise": ['raise', 'grays', 'graze', 'gaze', 'greys', 'ray is'],
    "fold": ["fold", "forward", "hold", "fall"],
    "check": ['check'],
    "call": ['call']
}

Note that the presence of a keyword does not necessarily mean that there is intent to act. Look at the context of the phrase and reflect in the confidence level.

Do not use the presence of a number as the only indication of a raise. Look for the word raise or take further context, since players can say "call X" where X is an integer.

Rules:
- Only output valid actions
- If action is RAISE, amount must be an integer
- If unsure, return action = NONE
- Return confidence between 0 and 1
- Respond ONLY with valid JSON

Example outputs:
{"action":"RAISE","amount":25,"confidence":0.92}
{"action":"CALL","amount":null,"confidence":0.85}
{"action":"NONE","amount":null,"confidence":0.3}
"""


client = OpenAI()


def llm_parse_action(text: str) -> dict:
    """
    Send raw ASR text to LLM and get structured poker intent.
    """
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            temperature=0.0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f'Raw speech text: "{text}"'}
            ]
        )

        return json.loads(resp.choices[0].message.content)

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return {"action": "NONE", "amount": None, "confidence": 0.0}

class STT:
    def __init__(self):
        self.recorder = AudioToTextRecorder()
        self.listening = False
        self.lock = threading.Lock()

        self.current_action = None
        self.current_action_time = time.time()

        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
    
    def get_state(self):
        return (self.current_action_time, self.current_action)

    def start_listening(self):
        with self.lock:
            if not self.listening:
                self.listening = True
                print("Listening ON")

    def stop_listening(self):
        with self.lock:
            self.listening = False
            print("Listening OFF")


    def _listen_loop(self):
        while True:
            self.recorder.text(self._maybe_parse)

    def _maybe_parse(self, text: str):
        with self.lock:
            if not self.listening:
                return
        self.parse(text)


    def parse(self, text: str):
        if not text.strip():
            return

        print(f"RAW ASR: {text}")

        result = llm_parse_action(text)
        print(f"LLM RESULT: {result}")

        confidence = result.get("confidence", 0.0)
        action = result.get("action", "NONE")
        amount = result.get("amount", None)

        if confidence < CONFIDENCE_THRESHOLD:
            print("Low confidence, ignoring")
            return

        if action == "NONE":
            print("No action detected")
            return

        if action == "RAISE":
            if amount is None:
                print("Raise without amount, ignoring")
                return
            action_emb = f"R{amount}"
        else:
            action_emb = {
                "CALL": "C",
                "CHECK": "X",
                "FOLD": "F"
            }.get(action)

        if not action_emb:
            return

        with self.lock:
            self.current_action = action_emb
            self.current_action_time = time.time()

        print(f"ACTION_EMB: {action_emb}")


    def run(self):
        print("Recorder ready. Call start_listening() / stop_listening().")
        self._thread.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    stt = STT()
    stt.run()

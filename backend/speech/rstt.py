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

        self.current_action = None
        self.current_action_time = None

        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def start(self):
        """Start STT in background thread."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )
        self.thread.start()
        print("STT thread started")

    def stop(self):
        """Stop STT cleanly."""
        self.running = False

    def get_state(self):
        """Safe access from anywhere."""
        with self.lock:
            return self.current_action_time, self.current_action


    def _listen_loop(self):
        print("Wait until it says 'speak now'")
        while self.running:
            self.recorder.text(self.parse)


    def parse(self, text: str):
        if not text.strip():
            return

        print(f"RAW ASR: {text}")
        result = llm_parse_action(text)
        print(f"\nLLM RESULT: {result}")

        confidence = result.get("confidence", 0.0)
        action = result.get("action", "NONE")
        amount = result.get("amount", None)

        if confidence < CONFIDENCE_THRESHOLD:
            return

        if action == "NONE":
            return

        if action == "RAISE":
            if amount is None:
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


if __name__ == "__main__":
    stt = STT()
    stt.start()

    old_state = stt.get_state()
    new_state = old_state
    while new_state == old_state:
        new_state = stt.get_state()
        time.sleep(0.5)
    print(f"GOT NEW STATE: {new_state[1]}")

    old_state = stt.get_state()
    new_state = old_state
    while new_state == old_state:
        new_state = stt.get_state()
        time.sleep(0.5)
    print(f"GOT NEW STATE: {new_state[1]}")



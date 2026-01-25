import threading
import time
from RealtimeSTT import AudioToTextRecorder

VOCAB = {
    "raise": ['raise', 'grays', 'graze', 'gaze', 'greys'],
    "fold": ["fold", "forward", "hold"],
    "check": ['check'],
    "call": ['call']
}

ACTION_MAP = {
    "raise": 'R',
    "fold": "F",
    "check": "X",
    "call": "C"
}

class STT:
    def __init__(self):
        self.recorder = AudioToTextRecorder()
        self.current_action = None
        self.current_action_time = time.time()
        self.lock = threading.lock()

    def get_state(self):
        return (self.current_action_time, self.current_action)

    def parse(self, text):
        print(f"CURRENT ACTION: {self.current_action}")
        print(f"RAW: {text}")
        text = text.lower().replace(".", "").replace("'", "").replace("!", "")
        print(f"PROCESSED: {text}")
        action_emb = None
        for action, near in VOCAB.items():
            for tok in text.split():
                if tok in near:
                    action_emb = ACTION_MAP[action]
                    if action == 'raise':
                        tokens = text.split()
                        numbers = [int(t) for t in tokens if t.isdigit()]
                        amount = numbers[0] if numbers else None 
                        action_emb += str(amount)
        print(f"ACTION_EMB: {action_emb}")
        with self.lock:
            self.current_action_time = time.time()
            self.current_action = action_emb
    
    def run(self):
        try: 
            while True:
                self.recorder.text(self.parse)
        except KeyboardInterrupt:
            print("\nStopped")

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()


if __name__ == "__main__":
    S = STT()
    S.run()
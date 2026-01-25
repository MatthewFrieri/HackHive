import cv2
from ultralytics import YOLO

class CardRecognizer:
    def __init__(
        self,
        number_model_path: str,
        suit_model_path: str,
        number_crop: tuple,
        suit_crop: tuple,
        confidence_threshold: float = 0.5
    ):
        """
        number_crop & suit_crop: (x1, y1, x2, y2)
        confidence_threshold: float between 0 and 1
        """

        self.number_model = YOLO(number_model_path)
        self.suit_model = YOLO(suit_model_path)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")

        self.number_crop = number_crop
        self.suit_crop = suit_crop
        self.conf_thresh = confidence_threshold

        # store last prediction in case confidence is too low
        self.last_card = "??"

    def get_card(self) -> str:
        """
        Captures one frame, runs both classifiers,
        returns card string like 'Ah', '9d', 'Ks'
        Only updates prediction if confidence >= threshold
        """

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")

        # Crop for number and suit separately
        x1, y1, x2, y2 = self.number_crop
        num_frame = frame[y1:y2, x1:x2]

        x1, y1, x2, y2 = self.suit_crop
        suit_frame = frame[y1:y2, x1:x2]

        # Run number classifier
        num_result = self.number_model(num_frame, verbose=False)[0]
        num_conf = float(num_result.probs.top1conf)
        num_idx = int(num_result.probs.top1)
        num_label = self.number_model.names[num_idx]

        # Run suit classifier
        suit_result = self.suit_model(suit_frame, verbose=False)[0]
        suit_conf = float(suit_result.probs.top1conf)
        suit_idx = int(suit_result.probs.top1)
        suit_label = self.suit_model.names[suit_idx]

        # Check confidence
        if num_conf >= self.conf_thresh and suit_conf >= self.conf_thresh:
            number_char = self._normalize_number(num_label)
            suit_char = self._normalize_suit(suit_label)
            self.last_card = f"{number_char}{suit_char}"

        return self.last_card

    def release(self):
        self.cap.release()

    @staticmethod
    def _normalize_number(label: str) -> str:
        label = label.upper()
        if label in ["J", "Q", "K", "A"]:
            return label
        return label  # assumes "2"–"10" already correct

    @staticmethod
    def _normalize_suit(label: str) -> str:
        label = label.lower()
        suit_map = {
            "hearts": "h", "heart": "h", "h": "h",
            "spades": "s", "spade": "s", "s": "s",
            "clubs": "c", "club": "c", "c": "c",
            "diamonds": "d", "diamond": "d", "d": "d",
        }
        return suit_map.get(label, "?")

# -----------------------
# CONFIG
# -----------------------
number_model_path = "/Users/davfrieri/Documents/Poker_Robot/runs/classify/train3/weights/number_model.pt"
suit_model_path = "/Users/davfrieri/Documents/Poker_Robot/runs/classify/train/weights/suit_model.pt"

number_crop = (888, 488, 1278, 757)
suit_crop = (587, 457, 1319, 999)
confidence_threshold = 0.5  # 50%

recognizer = CardRecognizer(
    number_model_path=number_model_path,
    suit_model_path=suit_model_path,
    number_crop=number_crop,
    suit_crop=suit_crop,
    confidence_threshold=confidence_threshold
)

# -----------------------
# USAGE EXAMPLE
# -----------------------
print("Capturing card...")
card = recognizer.get_card()
print("Detected card:", card)

recognizer.release()

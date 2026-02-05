from input_type import Type
import time

class Input:
    def __init__(self, id: int, type: Type, value: float, start_time):
        self.id = id
        self.type = type
        self.value = value
        self.timestamp = time.time() - start_time

        if value == Type.BUTTON:
            value = int(value)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'type': self.type.value,  # Get the integer value of the enum
            'value': self.value,
            'timestamp': self.timestamp
        }
        
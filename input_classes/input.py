from input_classes.input_type import Type

class Input():
    def __init__(self, *args, **kwargs):
        """Constructor of the Input class. This constructor can be used two different ways (this because of a poor implemenation of overloading in Python)

        **Args**:
            id (int): ID of the button or axis
            type (Type): Type of button, either Type.AXIS or Type.BUTTON
            value (float): the value of the input, 0 or 1 if it is a button, [-1, 1] if it
            is a axis value
            start_time (float): the relative time when this value was set, got from time.perf_counter()

        **Args**:
            json (object): the value of the input in a dictionary, can be got from Input.to_dict()
        """

        if len(args) == 4:
            self.id, self.type, self.value, self.timestamp = args

            if self.type == Type.BUTTON:
                self.value = int(self.value)

        if len(args) == 1:
            json = args[0]

            self.id = json["id"]
            self.type = Type(json["type"])
            self.value = json["value"]
            self.timestamp = json["timestamp"]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'type': self.type.value,  # Get the integer value of the enum
            'value': self.value,
            'timestamp': self.timestamp
        }
        
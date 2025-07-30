import mido
import datetime
from typing import Callable
from dataclasses import dataclass


@dataclass
class ButtonPress:
    button: str
    timestamp: datetime.datetime


class USBGoBox:
    BUTTONS = {
        1: "green",
        2: "blue",
        5: "yellow",
        8: "red",
        19: "right",
        20: "left",
    }

    def __init__(self):
        """
        Initialize the USB Go Box.

        Raises:
            RuntimeError: If no USB Go Box is found.
        """
        try:
            self.midi_in = mido.open_input('USB GO BOX', callback=self.callback)
        except OSError:
            raise RuntimeError("USB Go Box not found. Make sure it is connected.")
        self.on_press = None
        self.history = []
        self.history_capacity = 16
        self.macros = {}

    def add_macro(self, sequence: list[str], callback: Callable):
        self.macros[tuple(sequence)] = callback

    def callback(self, msg):
        if msg.type == "sysex":
            assert len(msg.data) == 5
            index = msg.data[4]
            if index in USBGoBox.BUTTONS:
                name = USBGoBox.BUTTONS[index]
                press = ButtonPress(name, datetime.datetime.now())
                self.history.append(press)
                if len(self.history) > self.history_capacity:
                    self.history.pop(0)
                currently_pressed = self.currently_pressed
                for presses, callback in self.macros.items():
                    if presses == currently_pressed:
                        callback()
                if self.on_press:
                    self.on_press(name)
            else:
                raise ValueError("Invalid sysex index: %d" % index)

    @property
    def currently_pressed(self) -> tuple:
        """
        Returns a list of the currently-pressed button names.

        Returns:
            tuple[str]: A list of the button names.
        """
        rv = []
        for press in reversed(self.history):
            if (datetime.datetime.now() - press.timestamp).total_seconds() < 1.5:
                rv.insert(0, press.button)
            else:
                break
        return tuple(rv)

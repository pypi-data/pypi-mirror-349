import time
from .gobox import USBGoBox

def main():
    box = USBGoBox()
    def on_press(button_name):
        print("Button pressed: %s" % button_name)
    box.on_press = on_press
    box.add_macro(["blue", "red"], lambda: print("stop!"))
    box.add_macro(["blue", "green"], lambda: print("start!"))
    box.add_macro(["blue", "yellow"], lambda: print("test!"))
    print("Awaiting button presses...")
    while True:
        time.sleep(1)

main()
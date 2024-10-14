from gpiozero import Button

pins = [2, 3, 4, 14, 15, 17, 18, 27, 22, 23, 24, 10, 9, 25, 11, 8, 7, 5, 6, 12, 13, 19, 16, 26, 20, 21]

def button_pressed(pin):
    print(f"PIN: {pin}")

buttons = []
for pin in pins:
    button = Button(pin)
    button.when_pressed = lambda p=pin: button_pressed(p)
    buttons.append(button)

while True:
    pass
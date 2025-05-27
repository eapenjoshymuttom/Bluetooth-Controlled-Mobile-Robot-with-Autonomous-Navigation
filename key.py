import serial  # Import the serial library for Bluetooth communication
import keyboard  # For detecting key presses
import guester as n2

# Setup Bluetooth communication with HC-05 via the serial port

bluetooth_serial = serial.Serial('COM5', 9600)  # COM port and baud rate (9600 is typical for HC-05)

print("Use W, A, S, D for movement and E to stop. Press 'q' to quit.")

while True:
    # Check for keyboard inputs
    if keyboard.is_pressed('O'):  # 'O' for Obstacle
        bluetooth_serial.write(b'O')
    elif keyboard.is_pressed('B'):  # 'B' for Bluetooth
        bluetooth_serial.write(b'P')
    elif keyboard.is_pressed('G'):  # 'G' for Followgesture
        n2.new()
    elif keyboard.is_pressed('w'):  # 'w' for forward
        bluetooth_serial.write(b'F')
        print("Sent 'F' to Arduino (Forward)")
    elif keyboard.is_pressed('s'):  # 's' for backward
        bluetooth_serial.write(b'B')
        print("Sent 'B' to Arduino (Backward)")
    elif keyboard.is_pressed('a'):  # 'a' for left
        bluetooth_serial.write(b'L')
        print("Sent 'L' to Arduino (Left)")
    elif keyboard.is_pressed('d'):  # 'd' for right
        bluetooth_serial.write(b'R')
        print("Sent 'R' to Arduino (Right)")
    elif keyboard.is_pressed('e'):  # 'e' for stop
        bluetooth_serial.write(b'S')
        print("Sent 'S' to Arduino (Stop)")

    # Press 'q' to quit the program
    if keyboard.is_pressed('q'):
        print("Exiting...")
        break   # Break the loop if 'q' is pressed

# Close the Bluetooth serial connection
bluetooth_serial.close()
import serial  # For Bluetooth communication
import speech_recognition as sr  # For voice recognition

# Setup Bluetooth communication with HC-05 via the serial port
bluetooth_serial = serial.Serial('COM5', 9600)  # Update 'COM5' to your Bluetooth serial port

# Initialize the speech recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("Say 'go' for forward, 'back' for backward, 'left' for left, 'right' for right, and 'stop' to stop. Say 'quit' to exit.")

while True:
    try:
        # Capture voice input
        with microphone as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)  # Listen for the audio input

        # Recognize speech using Google Speech Recognition
        command = recognizer.recognize_google(audio).lower()  # Convert to lowercase for consistency
        print(f"Command received: {command}")

        # Send corresponding signal based on the voice command
        if "go" in command:
            bluetooth_serial.write(b'F')
            print("Sent 'F' to Arduino (Forward)")
        elif "back" in command:
            bluetooth_serial.write(b'B')
            print("Sent 'B' to Arduino (Backward)")
        elif "left" in command:
            bluetooth_serial.write(b'L')
            print("Sent 'L' to Arduino (Left)")
        elif "right" in command:
            bluetooth_serial.write(b'R')
            print("Sent 'R' to Arduino (Right)")
        elif "stop" in command:
            bluetooth_serial.write(b'S')
            print("Sent 'S' to Arduino (Stop)")
        elif "quit" in command:
            print("Exiting...")
            break  # Exit the loop if "quit" is spoken

    except sr.UnknownValueError:
        # If the recognizer couldn't understand the audio
        print("Could not understand the command. Please speak again.")
    except sr.RequestError as e:
        # If there's an error with the recognizer service
        print(f"Could not request results from the speech recognition service; {e}")

# Close the Bluetooth serial connection
bluetooth_serial.close()

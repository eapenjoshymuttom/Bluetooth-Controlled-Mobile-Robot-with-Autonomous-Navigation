import cv2
import serial  # Import the serial library for Bluetooth communication
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture (Webcam)
def new():
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
      print("Error: Could not open camera")
      exit()

  # Initialize HandDetector
  detector = HandDetector(detectionCon=0.8, maxHands=1)

  # Setup Bluetooth communication with HC-05 via the serial port
  # Change 'COM5' to your actual Bluetooth port (check Device Manager)
  bluetooth_serial = serial.Serial('COM5', 9600)  # COM port and baud rate (9600 is typical for HC-05)


  def detect_hand_action(fingers):

      # Check for different gestures
      if fingers == [0, 0, 0, 0, 0]:
          return "Back"
      elif fingers == [1, 0, 0, 0, 0]:
          return "Forward"
      elif fingers == [0, 1, 1, 0, 0]:
          return "Left"
      elif fingers == [0, 0, 1, 1, 1]:
          return "Right"
      elif fingers == [1, 1, 1, 1, 1]:
          return "Stop"
      else:
          return "No Recognized Gesture"


  while True:
      success, img = cap.read()
      if not success:
          print("Failed to capture image")
          break

      # Detect hands and landmarks
      hands, img = detector.findHands(img)  # With Draw

      if hands:
          # Hand 1
          hand = hands[0]
          fingers = detector.fingersUp(hand)

          # Detect hand action based on fingers up
          action = detect_hand_action(fingers)
          print(f"Detected Action: {action}")

          # Send corresponding signals to Arduino via Bluetooth
          if action == "Back":
              bluetooth_serial.write(b'B')  # Send 'B' for Closed Fist
              print("Sent 'B' to Arduino")
          elif action == "Forward":
              bluetooth_serial.write(b'F')  # Send 'F' for Forward Gesture
              print("Sent 'F' to Arduino")
          elif action == "Left":
              bluetooth_serial.write(b'L')  # Send 'L' for Left Gesture
              print("Sent 'L' to Arduino")
          elif action == "Right":
              bluetooth_serial.write(b'R')  # Send 'R' for Right Gesture
              print("Sent 'R' to Arduino")
          elif action == "Stop" or action == "No Recognized Gesture":
              bluetooth_serial.write(b'S')  # Send 'S' for Open Hand (Stop)
              print("Sent 'S' to Arduino")

      # Display the image
      cv2.imshow("Image", img)

      # Press 'q' to quit
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break   # Break the loop

  # Release the capture and close windows
  cap.release()
  cv2.destroyAllWindows()

  # Close the Bluetooth serial connection
  bluetooth_serial.close()

new()
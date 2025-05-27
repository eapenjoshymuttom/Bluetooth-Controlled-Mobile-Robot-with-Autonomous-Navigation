#include <AFMotor.h> // Import library to control motor shield
#include <Servo.h>   // Import library to control the servo

// Create motor objects
AF_DCMotor rightBack(2);
AF_DCMotor rightFront(3);
AF_DCMotor leftFront(4);
AF_DCMotor leftBack(1);

Servo servoLook; // Create servo object

// Assign pins for the ultrasonic sensor
byte trig = A1;
byte echo = A0;

// Declare variables
byte maxDist = 150;
byte stopDist = 50;
float timeOut = 2 * (maxDist + 10) / 100 / 340 * 1000000;

byte motorSpeed = 155;
int motorOffset = 10;
int turnSpeed = 60;
int turnCount = 0;
const int maxTurnsBeforeFullTurn = 2;

char command;
#define MODE_MANUAL 0
#define MODE_AUTONOMOUS 1
int currentMode = MODE_AUTONOMOUS;

void setup() {
  // Initialize motors
  rightBack.setSpeed(motorSpeed);
  rightFront.setSpeed(motorSpeed);
  leftFront.setSpeed(motorSpeed + motorOffset);
  leftBack.setSpeed(motorSpeed + motorOffset);

  // Initialize servo
  servoLook.attach(10);

  // Initialize ultrasonic sensor pins
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Check for serial input for manual commands
  if (Serial.available() > 0) {
    command = Serial.read();
    processCommand(command);
  }

  if (currentMode == MODE_AUTONOMOUS) {
    servoLook.write(90);
    delay(750);
    int distance = getDistance();
    if (distance >= stopDist) {
      moveForward();
      delay(20);
      turnCount = 0;
    } else {
      stopMove();
      int turnDir = checkDirection();
      turnCount++;

      if (turnCount >= maxTurnsBeforeFullTurn) {
        fullTurn();
        turnCount = 0;
      } else {
        switch (turnDir) {
          case 0: turnLeft(1200); break;
          case 1: turnLeft(1200); break;
          case 2: turnRight(1200); break;
        }
      }
    }
  }
}

// Function to process manual commands
void processCommand(char cmd) {
  switch (cmd) {
    case 'F': moveForward(); break;
    case 'B': moveBackward(); break;
    case 'L': turnLeft(800); break;
    case 'R': turnRight(800); break;
    case 'S': stopMove(); break;
    case 'O':
      currentMode = MODE_AUTONOMOUS;
      Serial.println("Switched to Autonomous Mode");
      break;
    case 'P':
      currentMode = MODE_MANUAL;
      Serial.println("Switched to Manual Mode");
      stopMove();
      break;
  }
}

// Movement functions
void moveForward() {
  rightBack.run(FORWARD);
  rightFront.run(FORWARD);
  leftFront.run(FORWARD);
  leftBack.run(FORWARD);
}

void moveBackward() {
  rightBack.run(BACKWARD);
  rightFront.run(BACKWARD);
  leftFront.run(BACKWARD);
  leftBack.run(BACKWARD);
}

void stopMove() {
  rightBack.run(RELEASE);
  rightFront.run(RELEASE);
  leftFront.run(RELEASE);
  leftBack.run(RELEASE);
}

void turnLeft(int duration) {
  rightBack.setSpeed(motorSpeed + turnSpeed);
  rightFront.setSpeed(motorSpeed + turnSpeed);
  leftFront.setSpeed(motorSpeed + motorOffset + turnSpeed);
  leftBack.setSpeed(motorSpeed + motorOffset + turnSpeed);

  rightBack.run(FORWARD);
  rightFront.run(FORWARD);
  leftFront.run(BACKWARD);
  leftBack.run(BACKWARD);
  delay(duration);
  stopMove();
}

void turnRight(int duration) {
  rightBack.setSpeed(motorSpeed + turnSpeed);
  rightFront.setSpeed(motorSpeed + turnSpeed);
  leftFront.setSpeed(motorSpeed + motorOffset + turnSpeed);
  leftBack.setSpeed(motorSpeed + motorOffset + turnSpeed);

  rightBack.run(BACKWARD);
  rightFront.run(BACKWARD);
  leftFront.run(FORWARD);
  leftBack.run(FORWARD);
  delay(duration);
  stopMove();
}

void fullTurn() {
  rightBack.setSpeed(motorSpeed + turnSpeed);
  rightFront.setSpeed(motorSpeed + turnSpeed);
  leftFront.setSpeed(motorSpeed + motorOffset + turnSpeed);
  leftBack.setSpeed(motorSpeed + motorOffset + turnSpeed);

  rightBack.run(FORWARD);
  rightFront.run(FORWARD);
  leftFront.run(BACKWARD);
  leftBack.run(BACKWARD);
  delay(2000);
  stopMove();
}

int getDistance() {
  unsigned long pulseTime;
  int distance;
  digitalWrite(trig, HIGH);
  delayMicroseconds(4);
  digitalWrite(trig, LOW);
  pulseTime = pulseIn(echo, HIGH, timeOut);
  distance = (float)pulseTime * 340 / 2 / 10000;
  return distance;
}

int checkDirection() {
  int distances[2] = {0, 0};
  int turnDir = 1;
  servoLook.write(180);
  delay(500);
  distances[0] = getDistance();
  servoLook.write(0);
  delay(1000);
  distances[1] = getDistance();
  if (distances[0] >= 200 && distances[1] >= 200) turnDir = 0;
  else if (distances[0] <= stopDist && distances[1] <= stopDist) turnDir = 1;
  else if (distances[0] >= distances[1]) turnDir = 0;
  else turnDir = 2;
  return turnDir;
}

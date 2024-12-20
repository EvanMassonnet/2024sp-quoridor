#include <Servo.h>
#include <AccelStepper.h>
#include <MultiStepper.h>
#include "boardMovement.h"
#include "boardUtils.cpp"

AccelStepper X(
  AccelStepper::DRIVER, 
  StepperXPin1, 
  StepperXPin2
);
AccelStepper Y1(
  AccelStepper::DRIVER, 
  StepperY1Pin1, 
  StepperY1Pin2 
);

AccelStepper Y2(
  AccelStepper::DRIVER, 
  StepperY2Pin1, 
  StepperY2Pin2 
);

MultiStepper XY;
long pos_xy[3] = {0,0,0};

bool isClawHigh = true;
bool isClawClose = false;
WallOrientation clawOrientation = HORIZONTAL;

//range servo black : 270°
//range command : 0-180°
// 0°   = 0°
// 90°  = 65°
// 180° = 125°


Servo linearServo;
Servo rotationServo;
Servo gripperServo;

int linearPos = 0;
int rotationPos = 0;
int gripperPos = 0;

//Speed
int linearSpeed = 10;
int rotationSpeed = 10;
int gripperSpeed = 10;

//Starting position
int linearStart = 130;
int rotationStart = 0;


//End position
int linearEnd = 10;
int linearMid = 75;
int rotationEnd = 125;

//gripper position
int gripperFullOpen = 100;
int gripperMidOpen = 130;
int gripperClose = 180;
int gripperWall = 160;
int gripperPawn = 165;

void downMid(){
  for (linearPos; linearPos >= linearMid; linearPos -= 1) {
    linearServo.write(linearPos);
    delay(linearSpeed);
  }
  delay(100);
}

void downFull(){
  for (linearPos; linearPos >= linearEnd; linearPos -= 1) {
    linearServo.write(linearPos);
    delay(linearSpeed);
  }
  delay(100);
}

void upFull(){
    for (linearPos; linearPos <= linearStart; linearPos += 1) {
    linearServo.write(linearPos);
    delay(linearSpeed);
  }
  delay(100);
}

void upMid(){
    for (linearPos; linearPos <= linearMid; linearPos += 1) {
    linearServo.write(linearPos);
    delay(linearSpeed);
  }
  delay(100);
}

void rotate(int angle){
  if(angle > rotationPos){
    for (rotationPos; rotationPos <= angle; rotationPos += 1) {
      rotationServo.write(rotationPos);
      delay(rotationSpeed);
    }
  }else{
    for (rotationPos; rotationPos >= angle; rotationPos -= 1) {
      rotationServo.write(rotationPos);
      delay(rotationSpeed);
    }
  }
  delay(100);
}

void grabWall(){
    for (gripperPos; gripperPos <= gripperWall; gripperPos += 1) {
    gripperServo.write(gripperPos);
    delay(gripperSpeed);
  }
  delay(500);
}

void grabPawn(){
    for (gripperPos; gripperPos <= gripperPawn; gripperPos += 1) {
    gripperServo.write(gripperPos);
    delay(gripperSpeed);
  }
  delay(100);
}

void openMid(){
  for (gripperPos; gripperPos >= gripperMidOpen; gripperPos -= 1) {
    gripperServo.write(gripperPos);
    delay(gripperSpeed);
  }
  delay(100);
}


void closeMid(){
  for (gripperPos; gripperPos <= gripperMidOpen; gripperPos += 1) {
    gripperServo.write(gripperPos);
    delay(gripperSpeed);
  }
  delay(100);
}

void openFull(){
  for (gripperPos; gripperPos >= gripperFullOpen; gripperPos -= 1) {
    gripperServo.write(gripperPos);
    delay(gripperSpeed);
  }
  delay(100);
}

void setupGrabber() {
  gripperServo.write(gripperClose);
  delay(100);
  gripperPos = gripperClose;

  linearServo.write(linearStart);
  linearPos = linearStart;
  delay(100);
  rotationServo.write(0);
  rotationPos = 0;
  delay(100);

  linearServo.attach(11);
  gripperServo.attach(6);
  rotationServo.attach(5);

  //Set the gripper to the right starting position
  //openMid();
  upFull();
  rotate(0);

  delay(1000);
}

void setupMotors() {

  X.setMaxSpeed(CALIBRATION_SPEED);
  X.setAcceleration(Acceleration);
  X.setEnablePin(StepperXPin3);
  X.setPinsInverted(false, false, true);
  X.enableOutputs();

  Y1.setMaxSpeed(CALIBRATION_SPEED);
  Y1.setAcceleration(Acceleration);
  Y1.setEnablePin(StepperY1Pin3);
  Y1.setPinsInverted(false, false, true);
  Y1.enableOutputs();

  Y2.setMaxSpeed(CALIBRATION_SPEED);
  Y2.setAcceleration(Acceleration);
  Y2.setEnablePin(StepperY2Pin3);
  Y2.setPinsInverted(true, false, true);
  Y2.enableOutputs();

  XY.addStepper(X);
  XY.addStepper(Y1);
  XY.addStepper(Y2);

  setupGrabber();

  Serial.begin(9600);
  delay(1000);
  Serial.println("START");
}

void forceStopMotors(){
  X.stop();
  Y1.stop();
  Y2.stop();
  X.disableOutputs();
  Y1.disableOutputs();
  Y2.disableOutputs();
}

void moveToXY(long x, long y){
  pos_xy[0] = x;
  pos_xy[1] = y;
  pos_xy[2] = y;
  XY.moveTo(pos_xy);
  XY.runSpeedToPosition();
}

void goToOrigin(){
  moveToXY(0, 0);
}

bool validPlayer(BoardPosition pos){
  return 0 <= pos && pos / 10 <= 8 && pos % 10 <= 8;
}

bool validWall(BoardPosition pos){
  return 0 <= pos && (pos / 10 <= 7 && pos % 10 <= 7 || pos % 10 == 8);
}

void playMove(MoveData move_data){

  //Check for invalid positions
  if((move_data.piece_type == PLAYER && !validPlayer(move_data.old_position)) ||
     (move_data.piece_type == PLAYER && !validPlayer(move_data.new_position)) ||
     (move_data.piece_type == WALL && !validWall(move_data.old_position)) ||
     (move_data.piece_type == WALL && !validWall(move_data.new_position))
     ){
      Serial.println("NOT VALID POSITION");
      return;
    }

  X.enableOutputs();
  Y1.enableOutputs();
  Y2.enableOutputs();

  moveToBoardPosition(move_data.old_position, move_data.piece_type);
  rotateTo(move_data.old_orientation);
  downMid();
  openFull();
  downFull();

  closeClaw(move_data.piece_type);
  upFull();

  rotateTo(move_data.new_orientation);
  moveToBoardPosition(move_data.new_position, move_data.piece_type);

  downFull();
  openFull();
  upMid();
  closeMid();
  upFull();

  rotateTo(HORIZONTAL);
  goToOrigin();

  X.disableOutputs();
  Y1.disableOutputs();
  Y2.disableOutputs();
}

void moveToBoardPosition(BoardPosition pos, PieceType type){
  
  long x, y;
  //Translate pos into a x and y coordinate for the motors depending on the piece type
  long posX = pos % 10;
  long posY = pos / 10;
  if(type == PLAYER){
    x = getStepXPlayer(posX);
    y = getStepYPlayer(posY);
  }else{
    x = getStepXWall(posX, posY);
    y = getStepYWall(posX, posY);
  }
  moveToXY(x, y);
}

void openClaw(){
  if(isClawClose){
    //release();
    isClawClose = false; 
  }
}

void closeClaw(PieceType type){
  //if(!isClawClose){
    if(type == PLAYER){
      grabPawn();
    }else{
      grabWall();
    } 
  //isClawClose = true; 
  //}
}

void rotateTo(WallOrientation orientation){
  if(clawOrientation != orientation){
    if(orientation == HORIZONTAL){
      rotate(0);
    }else{
      rotate(65);
    }
    clawOrientation = orientation; 
  }
}

void lowerClaw(PieceType type){
  if(isClawHigh){
    //down();
    isClawHigh = false;
  }
}

void raiseClaw(PieceType type){
  if(!isClawHigh){
    //up();
    isClawHigh = true;
  }
}

void debugStartMotors(){
  X.enableOutputs();
  Y1.enableOutputs();
  Y2.enableOutputs();
}

//For debug only
void motorControlLoop(){
  if (X.distanceToGo() == 0 && Y1.distanceToGo() == 0 && Y2.distanceToGo() == 0) {
    while (Serial.available() == 0) {}
    String s;
    pos_xy[0] = Serial.parseInt(); 
    pos_xy[1] = Serial.parseInt();
    pos_xy[2] = pos_xy[1];
    s = Serial.readString();
    Serial.print("x = ");
    Serial.print(pos_xy[0]);
    Serial.print(" y1 = ");
    Serial.print(pos_xy[1]);
    Serial.print(" y2 = ");
    Serial.print(pos_xy[2]);
    Serial.println(s);
    XY.moveTo(pos_xy);
  }
  XY.runSpeedToPosition();
}

void calibrateMotors() {

  X.enableOutputs();
  Y1.enableOutputs();
  Y2.enableOutputs();

  while (!digitalRead(XMinStopPin)) {
    X.move(CALIBRATION_STEP);
    X.run();
  }
  Serial.println("0 for X");

  while (!digitalRead(YMinStopPin)) {
    Y1.move(-CALIBRATION_STEP);
    Y2.move(-CALIBRATION_STEP);
    Y1.run();
    Y2.run();
  }
  Serial.println("0 for Y");

  X.setSpeed(Speed);
  Y1.setSpeed(Speed);
  Y2.setSpeed(Speed);

  X.setCurrentPosition(0);
  Y1.setCurrentPosition(0);
  Y2.setCurrentPosition(0);

  forceStopMotors();
}
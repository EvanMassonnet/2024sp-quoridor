#include <stdint.h>

//https://reprap.org/forum/read.php?219,168722 as stated here
//TODO PUT CORRECT PINS FOR STEPPER AND SERVOS
#define StepperXPin1 54
#define StepperXPin2 55
#define StepperXPin3 38

#define StepperY1Pin1 60
#define StepperY1Pin2 61
#define StepperY1Pin3 56

#define StepperY2Pin1 26
#define StepperY2Pin2 28
#define StepperY2Pin3 24

#define Speed 20 //1400
#define Acceleration 20 //9000

#define XMinStopPin 3
#define YMinStopPin 14
#define CALIBRATION_SPEED 1000
#define CALIBRATION_STEP 500

#define ServoClawPin 1
#define ServoRotationPin 1
#define ServoZPin 1

enum PieceType {WALL, PLAYER};
enum WallOrientation{VERTICAL, HORIZONTAL};
typedef uint8_t BoardPosition;
typedef struct{
  BoardPosition old_position;
  BoardPosition new_position;
  PieceType piece_type;
  WallOrientation old_orientation;
  WallOrientation new_orientation;
}MoveData; 

void setupMotors();
void forceStopMotors();

void playMove(MoveData move_data);
void moveToBoardPosition(BoardPosition pos, PieceType type);
void openClaw();
void closeClaw(PieceType type);
void rotateTo(WallOrientation orientation);
void lowerClaw(PieceType type);
void raiseClaw(PieceType type);

void debugStartMotors();
void motorControlLoop();
void calibrateMotors();
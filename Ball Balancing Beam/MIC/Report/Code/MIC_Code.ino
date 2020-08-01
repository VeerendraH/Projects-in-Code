
// note: for my beam to be horizontal, Servo Motor angle should be 18 degrees.


#include<Servo.h>
#include<PID_v1.h>

#define LEFT 0
#define RIGHT 1
#define TRIG 0
#define ECHO 1


const int maxAngle = 40;
float prevus[2];
int tolerance = 4;
const int servoPin = 9;                                              
int pingPin[2][2];
const int eqbAngle = 18;
float currentAngle = eqbAngle;

float Kp = 0.357;                                                      //Initial Proportional Gain
float Ki = 0.007  ;                                                      //Initial Integral Gain
float Kd = 0.046;                                                    //Intitial Derivative Gain

double Setpoint, Input, Output, ServoOutput;                                       
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);           //Initialize PID object, which is in the class PID.
                                                                                                                                                                                                                                                                              
Servo myServo;                                                       //Initialize Servo.

void setup() {

  prevus[LEFT]=prevus[RIGHT]=0.0;
  pingPin[LEFT][TRIG]=12;
  pingPin[LEFT][ECHO]=13;
  pingPin[RIGHT][TRIG]=7;
  pingPin[RIGHT][ECHO]=3;
  
  Serial.begin(9600);                                                //Begin Serial 
  pinMode(pingPin[LEFT][TRIG], OUTPUT);
  pinMode(pingPin[RIGHT][TRIG], OUTPUT);
  pinMode(pingPin[LEFT][ECHO], INPUT);
  pinMode(pingPin[RIGHT][ECHO],INPUT);

  myServo.attach(servoPin);                                       
                                                                                                        //  position as the input to the PID algorithm
  long Angle_old = myServo.read();
  
  myPID.SetMode(AUTOMATIC);                                          //Set PID object myPID to AUTOMATIC 
  myPID.SetOutputLimits(-80,80);  //Set Output limits to -80 and 80 degrees. 
  float pos = 0;
}

void loop()
{
   Setpoint = 21.5;
  float leftDistance = readPosition(LEFT);
  float rightDistance = readPosition(RIGHT);
  prevus[LEFT] = leftDistance;
  prevus[RIGHT] = rightDistance;
//Serial.print("Left");
//Serial.println(leftDistance);
//Serial.print(",");
//Serial.println("Right");
Serial.println(rightDistance);  
  float minDistance = (leftDistance<rightDistance)?leftDistance:rightDistance;
//
  float error= fabs(minDistance);
  Input = error; 
  myPID.Compute();                                                   

  Output = (fabs(Output)<maxAngle)?fabs(Output):maxAngle;
  ServoOutput = (leftDistance<rightDistance)?eqbAngle-Output:eqbAngle+Output;  
  
//  if(currentAngle+4<ServoOutput){
//    myServo.write(++currentAngle);
//  }
//  else if(currentAngle>ServoOutput+4){
//    myServo.write(--currentAngle);
//  }
   
 // Serial.println(ServoOutput);
  myServo.write(ServoOutput );
}     
      

float readPosition(int PIN) 
{
  float duration; 
  float cm;
  digitalWrite(pingPin[PIN][TRIG], LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin[PIN][TRIG], HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin[PIN][TRIG], LOW);
  
  duration = pulseIn(pingPin[PIN][ECHO], HIGH);
  cm = duration/(29*2);

  if (cm>25){
    cm = 25;
    prevus[PIN]=cm;
  }
//  else if(cm>4){
//    prevus[PIN]=cm;
//  }
//  else{
//    cm = prevus[PIN];
//  }
//  Serial.println(cm);
  return cm; //Returns distance value.
}


 

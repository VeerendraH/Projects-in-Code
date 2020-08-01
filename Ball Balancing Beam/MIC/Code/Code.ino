
// note: for my beam to be horizontal, Servo Motor angle should be 102 degrees.

int last_reading;
#include<Servo.h>
#include<PID_v1.h>


const int servoPin = 9;                                               //Servo Pin

const int TrigPin = 4;

const int EchoPin = 3;

const float eq = -25;
 
 
float Kp = 1;                                                      //Initial Proportional Gain
float Ki = 2;                                                      //Initial Integral Gain
float Kd = 2;                                                    //Intitial Derivative Gain
double Setpoint, Input, Output, ServoOutput;                                       
                                  

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);           //Initialize PID object, which is in the class PID.
                                                                      
                                                                     
                                                                     
                                                                     
Servo myServo;                                                       //Initialize Servo.


void setup() {
  last_reading=5;
  Serial.begin(9600);                                                //Begin Serial 
  pinMode(TrigPin, OUTPUT);
  pinMode(EchoPin, INPUT);
  
  myServo.attach(servoPin);                                          //Attach Servo

  Input = readPosition();                                            //Calls function readPosition() and sets the balls
                                                                     //  position as the input to the PID algorithm

  
 
  myPID.SetMode(AUTOMATIC);                                          //Set PID object myPID to AUTOMATIC 
  myPID.SetOutputLimits(-30,30);                                     //Set Output limits to -80 and 80 degrees. 
}

void loop()
{
  Setpoint = 22.5;
  Input = readPosition();                                            

 
  myPID.Compute();                                                   //computes Output in range of -80 to 80 degrees
 last_reading= Input; 
  ServoOutput= -60 - Output;                                            // 102 degrees is my horizontal 
  myServo.write(ServoOutput); 
}
      
      
      

float readPosition() {
  delay(60);                                                            //Don't set too low or echos will run into eachother.      
  
  long duration, cm;
  unsigned long now = millis();
  //pinMode(TrigPin, OUTPUT);
  digitalWrite(TrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(TrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(TrigPin, LOW);


  //pinMode(EchoPin, INPUT);
  duration = pulseIn(EchoPin, HIGH);

  cm = duration/(29*2);
  
  
// if(cm > 40)     // 30 cm is the maximum position for the ball
//  {cm=40;}
  
  //cm=40-cm;
 /* if (cm <7 ) {cm=6; Serial.println("Mazen");}*/
  Serial.println("Angle");
  Serial.println(ServoOutput);
  Serial.println(cm);
  
  return cm;                                          //Returns distance value.
}

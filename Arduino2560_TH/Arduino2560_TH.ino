
/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: wifi-robot
* File identification:
* Abstract: WiFi robot smart car control
* Description: Program main function file
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/
#include <Servo.h>
#include <EEPROM.h>
#include <LCD12864RSPI.h>
#define SIZE( a ) sizeof( a ) / sizeof( a[0] )

int ledpin1 = A6;                   //Set the system startup indicator 1
int ledpin2 = A7;                   //Set the system startup indicator 2
int ENA = 5;                        //L298 enable A
int ENB = 6;                        //L298 enable B
int INPUT2 = 7;                     //Motor interface 1
int INPUT1 = 8;                     //Motor interface 2
int INPUT3 = 12;                    //Motor interface 3
int INPUT4 = 13;                    //Motor interface 4         
int Key1_times;                     //Button 1 pinning time or Button 1 debounce time
int Key2_times;                     //Button 2 pinning time or Button 2 debounce time
boolean MoterStatusLED = true;      //Motor indicator status indicator 
boolean ServoStatusLED = true;      //Steering gear indicator status indication/indicator
/*
LCD  Arduino2560 PIN
PIN1 = GND
PIN2 = 5V
RS(CS) = A12;                        //LCD RS pin
RW(SID)= A11;                        //LCD RW pin
E(CLK) = A13;                        //LCD E pin
PIN15 PSB = GND;
*/

#define INIT         0               // LCD initial display mode
#define NORMAL       0               // LCD display normal mode
#define FOLLOW       1               // LCD display shows follow mode
#define AVOID        2               // LCD display shows infrared obstacle avoidance mode
#define WAVEAVOID    3               // LCD display shows ultrasonic obstacle avoidance mode
static int Level = 0;                // Define menu level
static int Mode = 0;                 // Define menu mode
int Refresh = 0;                     // LCD refresh mark

int adjust = 1;                      // Define motor flag
int Echo = A5;                       // Define the ultrasonic signal receiving pin
int Trig = A4;                       // Define the ultrasonic signal emission pin
int Input_Detect_LEFT = A13;         // Define the car to track the left side of the infrared
int Input_Detect_RIGHT = A14;        // Define the car to track the right side of the infrared
int Input_Detect = A1;               // Define the front of the car
int Input_Detect_TrackLeft = A2;     // Define the car to follow the left side of the infrared
int Input_Detect_TrackRight = A3;    // Define the car to follow the right side of the infrared
int Carled = A0;                     // Define the car light interface
int Cruising_Flag = 0;               // Mode switching flag
int Pre_Cruising_Flag = 0 ;          // Record last mode
int Left_Speed_Hold = 255;           // Define the left speed variable
int Right_Speed_Hold = 255;          // Define the right speed variable

Servo servo1;                       // Create steering gear #1
Servo servo2;                       // Create steering gear #2
Servo servo3;                       // Create steering gear #3
Servo servo4;                       // Create steering gear #4
Servo servo5;                       // Create steering gear #5
Servo servo6;                       // Create steering gear #6
Servo servo7;                       // Create steering gear #7
Servo servo8;                       // Create steering gear #8

byte angle1 = 70;                    // Steering gear #1 initial value
byte angle2 = 60;                    // Steering gear #2 initial value
byte angle3 = 60;                    // Steering gear #3 initial value
byte angle4 = 60;                    // Steering gear #4 initial value
byte angle5 = 60;                    // Steering gear #5 initial value
byte angle6 = 60;                    // Steering gear #6 initial value
byte angle7 = 60;                    // Steering gear #7 initial value
byte angle8 = 60;                    // Steering gear #8 initial value

int buffer[3];                       // Serial port receive data buffer
int rec_flag;                        // Serial port receiving flag
int serial_data;                     // Serial data zero time storage
unsigned long Costtime;              // Serial port timeout count
int IR_R;                            // Follow the right infrared status flag
int IR_L;                            // Follow the left infrared status flag
int IR;                              // Intermediate infrared status flag
int IR_TL;                           // Infrared status flag on the left side of the line                       
int IR_TR;                           // Infrared status flag on the right side of the line

int RevStatus = 0;
int TurnAngle = 0;
int Golength = 0;

#define MOTOR_GO_FORWARD  {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,HIGH);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,HIGH);}      // Car body forward                            
#define MOTOR_GO_BACK     {digitalWrite(INPUT1,HIGH);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,HIGH);digitalWrite(INPUT4,LOW);}      // Car body back
#define MOTOR_GO_RIGHT    {digitalWrite(INPUT1,HIGH);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,HIGH);}      // Turn the car right
#define MOTOR_GO_LEFT     {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,HIGH);digitalWrite(INPUT3,HIGH);digitalWrite(INPUT4,LOW);}      // Turn the car left
#define MOTOR_GO_STOP     {digitalWrite(INPUT1,LOW);digitalWrite(INPUT2,LOW);digitalWrite(INPUT3,LOW);digitalWrite(INPUT4,LOW);}        // Car body stop

/*
*********************************************************************************************************
** Function name :setup()
** Function: Set function
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void setup()
{
  pinMode(ledpin1, OUTPUT);
  pinMode(ledpin2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(INPUT1, OUTPUT);
  pinMode(INPUT2, OUTPUT);
  pinMode(INPUT3, OUTPUT);
  pinMode(INPUT4, OUTPUT);
  pinMode(Input_Detect_LEFT, INPUT);
  pinMode(Input_Detect_RIGHT, INPUT);
  pinMode(Input_Detect_TrackLeft,INPUT);
  pinMode(Input_Detect_TrackRight,INPUT);
  pinMode(Carled, OUTPUT);
  pinMode(Input_Detect, INPUT);
  pinMode(Echo, INPUT);
  pinMode(Trig, OUTPUT);
  pinMode(20, INPUT);
  pinMode(21, INPUT);
  digitalWrite(20, HIGH);
  digitalWrite(21, HIGH);
  LCDA.Initialise();                      // Screen initialization
  LCDA.CLEAR();                           // Clear screen
  MENU(INIT,INIT);                        // Display 12864 menu
  Delayed();                              // Delay 50 seconds and other WiFi modules are started
  attachInterrupt(2, Key1, FALLING);      // Button 1 is interrupted the interrupt function is Key1 and the falling edge triggers
  attachInterrupt(3, Key2, FALLING);      // Button 2 is interrupted the interrupt function is Key2 and the falling edge triggers
  servo1.attach(11);                      // Define the servo 1 control port
  servo2.attach(2);                       // Define the servo 2 control port
  servo3.attach(4);                       // Define the servo 3 control port
  servo4.attach(3);                       // Define the servo 4 control port
  servo5.attach(A8);                      // Define the servo 5 control port
  servo6.attach(A9);                      // Define the servo 6 control port
  servo7.attach(9);                       // Define the servo 7 control port
  servo8.attach(10);                      // Define the servo 8 control port
  USART_init();                           // Serial port initialization baud rate is set to 9600 bps
  Init_Steer();                           // Steering gear angle motor speed initialization
}

/*
*********************************************************************************************************
** Function name : Cruising_Mod()
** Function: Main function
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Cruising_Mod()//模式功能切换函数
{
  if (Pre_Cruising_Flag != Cruising_Flag)
  {
    if (Pre_Cruising_Flag != 0)
    {
      MOTOR_GO_STOP;
    }
    Pre_Cruising_Flag =  Cruising_Flag;
  }
  switch (Cruising_Flag)
  {
    case 1: Follow(); return;               //Follow mode
    case 2: TrackLine(); return;            //Patrol mode
    case 3: Avoiding(); return;             //Obstacle avoidance mode
    case 4: AvoidByRadar(15); return;       //Ultrasonic obstacle avoidance mode
    case 5: Send_Distance(); return;        //Ultrasonic distance PC display
    case 7: Route(); return;                //Route plan
    default: return;
  }
}

/*
*********************************************************************************************************
** Function name :loop()
** Function: Main function
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void loop()
{  
  MENU(Level,Mode);                       //Show Menu
  while (1)
  {
    UartTimeoutCheck();                   //Serial port timeout detection
    Cruising_Mod();                       //Mode switching
    if(Key1_times>0){Key1_times--;}       //Button 1 debounce
    if(Key2_times>0){Key2_times--;}       //Button 1 debounce
  }
}

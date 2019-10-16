/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: Init
* File identification:
* Abstract: WiFi robot smart car control
* Description: Initialization file
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/

/*

*********************************************************************************************************
** Function name : Delayed()
** Function function : Delay program
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void  Delayed()    //After 40 seconds delay, the wifi module is started
{
  int i;
  for (i = 0; i < 25; i++)
  {
    digitalWrite(ledpin1, HIGH);
    digitalWrite(ledpin2, LOW);
    delay(1000);
    digitalWrite(ledpin1, LOW);
    digitalWrite(ledpin2, HIGH);
    delay(1000);
  }
  
  for (i = 0; i < 10; i++)
  {
    digitalWrite(ledpin1, HIGH);
    digitalWrite(ledpin2, HIGH);
    delay(500);
    digitalWrite(ledpin1, LOW);
    digitalWrite(ledpin2, LOW);
    delay(500);
  }
  MOTOR_GO_STOP;
  digitalWrite(ledpin1, LOW);
  digitalWrite(ledpin2, LOW);
  digitalWrite(Input_Detect,HIGH);
  digitalWrite(Input_Detect_LEFT,HIGH);
  digitalWrite(Input_Detect_RIGHT,HIGH);
  digitalWrite(Input_Detect_TrackLeft,HIGH);
  digitalWrite(Input_Detect_TrackRight,HIGH);
}

/*
*********************************************************************************************************
** Function name :setup().Init_Steer()
** Function: System initialization (serial port, motor, servo, indicator initialization).
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Init_Steer()   //Steering gear initialization(angle is the last saved value)
{
  angle1 = EEPROM.read(0x01);//Read the value in register 0x01
  angle2 = EEPROM.read(0x02);//Read the value in register 0x02
  angle3 = EEPROM.read(0x03);//Read the value in register 0x03
  angle4 = EEPROM.read(0x04);//Read the value in register 0x04
  angle5 = EEPROM.read(0x05);//Read the value in register 0x05
  angle6 = EEPROM.read(0x06);//Read the value in register 0x06
  angle7 = EEPROM.read(0x07);//Read the value in register 0x07
  angle8 = EEPROM.read(0x08);//Read the value in register 0x08
  if ((angle1 == 255)|| (angle2 == 255)||( angle2 == 255)|| (angle2 == 255)||( angle2 == 255)|| (angle2 == 255)|| (angle2 == 255)|| (angle2 == 255)|| (angle2 == 255))
  {
    EEPROM.write(0x01, 60); //Store the initial angle in address 0x01
    EEPROM.write(0x02, 60); //Store the initial angle in address 0x02
    EEPROM.write(0x03, 60); //Store the initial angle in address 0x03
    EEPROM.write(0x04, 60); //Store the initial angle in address 0x04
    EEPROM.write(0x05, 60); //Store the initial angle in address 0x05
    EEPROM.write(0x06, 60); //Store the initial angle in address 0x06
    EEPROM.write(0x07, 60); //Store the initial angle in address 0x07
    EEPROM.write(0x08, 60); //Store the initial angle in address 0x08
    return;
  }
  servo1.write(angle1);
  servo2.write(angle2);
  servo3.write(angle3);
  servo4.write(angle4);
  servo5.write(angle5);
  servo6.write(angle6);
  servo7.write(angle7);
  servo8.write(angle8);
  adjust = EEPROM.read(0x10);//Read the value in register 0x10
  if (adjust == 0xff)EEPROM.write(0x10, 1);
  
    Left_Speed_Hold = EEPROM.read(0x09);//Read the value in register 0x03
    Right_Speed_Hold = EEPROM.read(0x0A);//Read the value in register 0x04
    if((Left_Speed_Hold<55)||(Right_Speed_Hold<55))
    {
       Left_Speed_Hold=255;
       Right_Speed_Hold=255;
     }
    analogWrite(ENB,Left_Speed_Hold);//Assign L298 enable B
    analogWrite(ENA,Right_Speed_Hold);//Assign L298 enable A
    MOTOR_GO_STOP;
}

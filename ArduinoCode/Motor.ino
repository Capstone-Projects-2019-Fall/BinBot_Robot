/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: Motor
* File identification:
* Abstract: WiFi robot smart car control
* Description: Motor Control related documents
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/
/*
Calibrate the car direction with the calibration value
*/ 
void forward(int adjust)
{
  switch (adjust)
  {
    case 1: MOTOR_GO_FORWARD; return;
    case 2: MOTOR_GO_FORWARD; return;
    case 3: MOTOR_GO_BACK; return;
    case 4: MOTOR_GO_BACK; return;
    case 5: MOTOR_GO_LEFT; return;
    case 6: MOTOR_GO_LEFT; return;
    case 7: MOTOR_GO_RIGHT; return;
    case 8: MOTOR_GO_RIGHT; return;
    default: return;
  }
}
/*
Calibrate the car direction with the calibration value
*/ 
void back(int adjust)
{
  switch (adjust)
  {
    case 1: MOTOR_GO_BACK; return;
    case 2: MOTOR_GO_BACK; return;
    case 3: MOTOR_GO_FORWARD; return;
    case 4: MOTOR_GO_FORWARD; return;
    case 5: MOTOR_GO_RIGHT; return;
    case 6: MOTOR_GO_RIGHT; return;
    case 7: MOTOR_GO_LEFT; return;
    case 8: MOTOR_GO_LEFT; return;
    default: return;
  }
}
/*
Calibrate the car direction with the calibration value
*/ 
void left(int adjust)
{
  switch (adjust)
  {
    case 1: MOTOR_GO_LEFT; return;
    case 2: MOTOR_GO_RIGHT; return;
    case 3: MOTOR_GO_LEFT; return;
    case 4: MOTOR_GO_RIGHT; return;
    case 5: MOTOR_GO_FORWARD; return;
    case 6: MOTOR_GO_BACK; return;
    case 7: MOTOR_GO_FORWARD; return;
    case 8: MOTOR_GO_BACK; return;
    default: return;
  }
}
/*
Calibrate the car direction with the calibration value
*/ 
void right(int adjust)
{
  switch (adjust)
  {
    case 1: MOTOR_GO_RIGHT; return;
    case 2: MOTOR_GO_LEFT; return;
    case 3: MOTOR_GO_RIGHT; return;
    case 4: MOTOR_GO_LEFT; return;
    case 5: MOTOR_GO_BACK; return;
    case 6: MOTOR_GO_FORWARD; return;
    case 7: MOTOR_GO_BACK; return;
    case 8: MOTOR_GO_FORWARD; return;
    default: return;
  }
}


/*
*********************************************************************************************************
** Function name :Avoiding
** Function: Detecting that there is no obstacle before the infrared in front of the front of the car body, and if any, the car stops.
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/  
void  Avoiding()//Infrared obstacle avoidance function
{
  IR = digitalRead(Input_Detect);
  if ((IR == LOW))
  {
    MOTOR_GO_STOP;// Stop
  }
}

/*
*********************************************************************************************************
** Function name : Follow
** Function: Detect the position of the black line between the two infrared rays, and make the direction change of the car through logical judgment.
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/ 
void Follow() //Follow mode
{  
    IR = digitalRead(Input_Detect);
    IR_TL = digitalRead(Input_Detect_TrackLeft);
    IR_TR = digitalRead(Input_Detect_TrackRight);
    if(IR == HIGH) //The intermediate sensor did not detect the object
    {
        if((IR_TL == LOW)&& (IR_TR == LOW)) //Both sides detect objects at the same time
        {
          MOTOR_GO_STOP;// Stop 
        } 
         
        if((IR_TL == LOW)&& (IR_TR == HIGH))// Object detected on the left
        {
          left(adjust); //Turn left
        }
        if((IR_TL == HIGH)&& (IR_TR == LOW))//Object detected on the right
        {
          right(adjust); //Turn right
        }
        if((IR_TL == HIGH)&& (IR_TR == HIGH))// No object detected
        {
           forward(adjust);//Straight
        }
    }
    else
    {
       MOTOR_GO_STOP;
    }
} 

/*
*********************************************************************************************************
** Function Name : TrackLine
** Function: Detect the position of the black line between the two infrared rays, and make the direction change of the car through logical judgment.
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/ 
void TrackLine()   // Patrol mode
{
  IR = digitalRead(Input_Detect);
  IR_L = digitalRead(Input_Detect_LEFT);//Read the left sensor value
  IR_R = digitalRead(Input_Detect_RIGHT);//Read the right sensor value
  if(IR == HIGH) //The intermediate sensor did not detect the object 
    {
        if ((IR_L == HIGH) && (IR_R == HIGH))//Detected on both sides, just like a video in the video encountered a horizontal tape
        {
          MOTOR_GO_STOP;//Stop
        }
        
        if ((IR_L == HIGH) && (IR_R == LOW)) //Black line on the left
        {
          left(adjust);//turn left
        }
        
        if ((IR_L == LOW) && ( IR_R == HIGH)) //Black line on the right
        {
          right(adjust);//turn right
        }
        
        if ((IR_L == LOW) && (IR_R == LOW))//No black lines were detected on both sides indicating that they are in the track
        {
          forward(adjust);//Straight
        }
    }
    else
    {
        MOTOR_GO_STOP;
    }
}

/*
*********************************************************************************************************
** Function name :AvoidByRadar
** Function: When the distance detected by the ultrasonic wave is less than distance (in cm), the car stops.
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void AvoidByRadar(int distance)//Ultrasonic obstacle avoidance function
{
  int leng = Get_Distance();
  if(distance<10)distance=10;    //Limit the minimum obstacle avoidance distance to 10cm
  if((leng>1)&&(leng < distance))//Obstacle distance value(in cm), greater than 1 is to avoid the blind spot of ultrasound
  {
    while((Get_Distance()>1)&&(Get_Distance() < distance))
     {
      back(adjust);
     }
     MOTOR_GO_STOP;
  }
}

/*
*********************************************************************************************************
** Function name : Route()
** Function function: path planning
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Route()
{
  if (RevStatus == 0)
  {
    Sendbyte(0xff);
    Sendbyte(0xA8);
    Sendbyte(0x00);
    Sendbyte(0x00);
    Sendbyte(0xff);
    delay(500);
  }

  while (RevStatus)
  {
    if (RevStatus == 1)
    {
      RevStatus = 0;
      left(adjust);
      delay(TurnAngle * 6);
      MOTOR_GO_STOP;
      forward(adjust);
      delay(Golength * 10);
      MOTOR_GO_STOP;
      break;
    }
    if (RevStatus == 2)
    {
      RevStatus = 0;
      right(adjust);
      delay(TurnAngle * 6);
      MOTOR_GO_STOP;
      forward(adjust);
      delay(Golength * 10);
      MOTOR_GO_STOP;
      break;
    }
  }
}

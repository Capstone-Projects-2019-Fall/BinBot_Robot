
/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: Display_12864
* File identification:
* Abstract: WiFi robot smart car control
* Description: 12864 display driver file
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/

/***********************************************************************************************************************************************************************************************/
                                                                
/*12864 LCD display related function*/                                              


unsigned char show0[] = { 0xD0, 0xA1, 0xB6, 0xFE, 0xBF, 0xC6, 0xBC, 0xBC}; // Small technology
unsigned char show1[] = "wifi-robots";
unsigned char Normal_S[] = {
  0xA1, 0xF1,
  0xD5, 0xFD,
  0xB3, 0xA3,
  0xC4, 0xA3,
  0xCA, 0xBD
};                    //●Normal Mode
unsigned char Normal[]={
  0xD5, 0xFD,
  0xB3, 0xA3,
  0xC4, 0xA3,
  0xCA, 0xBD
     };                    //Normal Mode
unsigned char Follow_S[] = {
  0xA1, 0xF1,
  0xBA, 0xEC,
  0xCD, 0xE2,
  0xD1, 0xAD,
  0xBC, 0xA3
};                    //●Infrared tracking
unsigned char follow[] = {
  0xBA, 0xEC,
  0xCD, 0xE2,
  0xD1, 0xAD,
  0xBC, 0xA3
};                    //Infrared tracking
unsigned char Avoid_S[]={
  0xA1, 0xF1,
  0xBA, 0xEC,
  0xCD, 0xE2,
  0xB1, 0xDC,
  0xD5, 0xCF
};                    //●Infrared obstacle avoidance
unsigned char Avoid[]={
  0xBA, 0xEC,
  0xCD, 0xE2,
  0xB1, 0xDC,
  0xD5, 0xCF
};                    //Infrared obstacle avoidance
unsigned char WaveAvoid_S[] = {
  0xA1, 0xF1,
  0xB3, 0xAC,
  0xC9, 0xF9,
  0xB2, 0xA8,
  0xB1, 0xDA,
  0xD5, 0xCF
};                    //●Ultrasonic Barrier / Ultrasonic obstacle avoidance
unsigned char WaveAvoid[] = {
  0xB3, 0xAC,
  0xC9, 0xF9,
  0xB2, 0xA8,
  0xB1, 0xDA,
  0xD5, 0xCF
};                    //Ultrasonic barrier / Ultrasonic obstacle avoidance

/*

/*************************************************************
              External interrupt 2 function Key1()
*************************************************************/
void Key1()
{
 if(Key1_times==0)
{
  Key1_times=7000;
  MENU(Level,Mode);MENU(Level,Mode);
  Refresh = 1;
  switch(Level)
  {
    case 0:Level = 1; Mode = 0;  MENU(Level,Mode);MENU(Level,Mode);return;
    case 1:Level = 2;
           switch(Mode)
           {
             case NORMAL:Cruising_Flag = 0; MENU(Level,Mode);MENU(Level,Mode);return;
             case FOLLOW:Cruising_Flag = 2; MENU(Level,Mode);MENU(Level,Mode);return;
             case AVOID: Cruising_Flag = 3; MENU(Level,Mode);MENU(Level,Mode);return;
             case WAVEAVOID:Cruising_Flag =4; MENU(Level,Mode);MENU(Level,Mode);return;
             default:Cruising_Flag = 0; MENU(Level,Mode);MENU(Level,Mode);return;
           }
             MENU(Level,Mode);MENU(Level,Mode);return;
    default:Level = 2;  MENU(Level,Mode);MENU(Level,Mode);return;
  }
 MENU(Level,Mode);MENU(Level,Mode);
 }
}
/*************************************************************
               External interrupt 3 function Key2()
*************************************************************/
void Key2()
{ 
if(Key2_times==0)
{
  Key2_times=7000;
  MENU(Level,Mode);MENU(Level,Mode);
  Refresh = 1;
  switch(Level)
  {
    case 0:  MENU(Level,Mode);MENU(Level,Mode);return;
    case 1:Mode++;if (Mode > 3)Mode = 0;  MENU(Level,Mode);MENU(Level,Mode);return;
    default:Level = 1;Cruising_Flag = 0;  MENU(Level,Mode);MENU(Level,Mode);return;
  }  
 MENU(Level,Mode);MENU(Level,Mode);
}
}
/*************************************************************
                 Menu option display
*************************************************************/

void MENU(int Level,int Mode)
{
  if(Refresh)    // Refresh screen
  {
    Refresh = 0;
    LCDA.CLEAR();   
  }
  delay(10);// This delay must be /
  switch(Level)
  {
    case 0:
         if(!Mode)
         {
           LCDA.DisplayString(0, 2, show0, SIZE(show0)); //The first line starts with the third grid and displays the text Xiao Er technology
           LCDA.DisplayString(2, 1, show1, SIZE(show1)); //The third line starts with the second grid and displays the text wifi-robots
         }
         return;
    case 1:
          switch(Mode)
          {
            case NORMAL:   LCDA.DisplayString(0, 0, Normal_S, SIZE(Normal_S));
                           LCDA.DisplayString(1, 1, follow, SIZE(follow));
                           LCDA.DisplayString(2, 1, Avoid, SIZE(Avoid));
                           LCDA.DisplayString(3, 1, WaveAvoid, SIZE(WaveAvoid));
                           return;                                                   //Choice is normal mode
            case FOLLOW:   LCDA.DisplayString(0, 1, Normal, SIZE(Normal));
                           LCDA.DisplayString(1, 0, Follow_S, SIZE(Follow_S));
                           LCDA.DisplayString(2, 1, Avoid, SIZE(Avoid));
                           LCDA.DisplayString(3, 1, WaveAvoid, SIZE(WaveAvoid)); 
                           return;                                                   //The selection is infrared tracking mode
            case AVOID:    LCDA.DisplayString(0, 1, Normal, SIZE(Normal));
                           LCDA.DisplayString(1, 1, follow, SIZE(follow));
                           LCDA.DisplayString(2, 0, Avoid_S, SIZE(Avoid_S));
                           LCDA.DisplayString(3, 1, WaveAvoid, SIZE(WaveAvoid));
                           return;                                                   //The option is infrared barrier or obstacle avoidance mode
            case WAVEAVOID:LCDA.DisplayString(0, 1, Normal, SIZE(Normal));
                           LCDA.DisplayString(1, 1, follow, SIZE(follow));
                           LCDA.DisplayString(2, 1, Avoid, SIZE(Avoid));
                           LCDA.DisplayString(3, 0, WaveAvoid_S, SIZE(WaveAvoid_S));
                           return;                                                   //The option is ultrasonic barrier or obstacle avoidance mode
          }
          return;
    case 2:
          switch(Mode)
          {
            case NORMAL:LCDA.DisplayString(1, 2, Normal, SIZE(Normal));return;               //Normal mode
            case FOLLOW:LCDA.DisplayString(1, 2, follow, SIZE(follow));return;               //Infrared tracking mode
            case AVOID: LCDA.DisplayString(1, 2, Avoid, SIZE(Avoid));return;                 //Infrared (barrier or obstacle avoidance) mode
            case WAVEAVOID:LCDA.DisplayString(1, 1, WaveAvoid, SIZE(WaveAvoid));return;      //Ultrasonic (barrier or obstacle avoidance) mode
          }
          return;
    default:return;
  }
}
                               
                      /*12864 LCD display related function */                                          
/***********************************************************************************************************************************************************************************************/

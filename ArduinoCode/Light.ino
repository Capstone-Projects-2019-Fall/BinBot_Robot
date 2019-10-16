/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: Light
* File identification:
* Abstract: WiFi robot smart car control
* Description: Headlight control file
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/
/*
*********************************************************************************************************
** Function name : Open_Light
** Function: Turn on the lights
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/ 
void Open_Light()//Headlight
{
  digitalWrite(Carled, HIGH);  // Pull low, the positive pole is connected to the power supply, and the negative pole is connected to the Io port.
  delay(1000);
}

 /*
*********************************************************************************************************
** Function name : Close_Light
** Function: Turn off the lights
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Close_Light()//Off headlights
{
  digitalWrite(Carled, LOW);   // Pull low, the positive pole is connected to the power supply, and the negative pole is connected to the Io port.
  delay(1000);
}

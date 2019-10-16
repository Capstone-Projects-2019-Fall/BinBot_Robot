/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: Ultrasonic
* File identification:
* Abstract: WiFi robot smart car control
* Description: Ultrasound module file
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/

/*
*********************************************************************************************************
** Function name : Get_Distence
** Function: Detects the measured distance value of the ultrasonic wave and returns (in cm)
** Entry parameters: none
** Export parameters: Ldistance
*********************************************************************************************************
*/ 
char Get_Distance()//Measure distance
{
  digitalWrite(Trig, LOW);   // Let the ultrasonic wave emit low voltage 2μs
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);  // Let the ultrasonic wave emit a high voltage of 10μs，here at leat 10μs
  delayMicroseconds(10);
  digitalWrite(Trig, LOW);    // Maintain ultrasonic emission low voltage
  float Ldistance = pulseIn(Echo, HIGH,5000);  // Read difference time
  Ldistance = Ldistance / 5.8 / 10; // Turn time into distance (unit:cm)
  //Serial.println(Ldistance);      //Display distance
  return Ldistance;
}

/*
*********************************************************************************************************
** Function name : Send_Distance
** Function: Send ultrasonic data to the host computer (data format: 0XFF, 0X03, angle (default 0X00), distance (dis), 0XFF)
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Send_Distance()//Ultrasonic distance PC display
{
  int dis = Get_Distance();
  Sendbyte(0xff);
  Sendbyte(0x03);
  Sendbyte(0x00);
  Sendbyte(dis);
  Sendbyte(0xff);
  delay(1000);
}

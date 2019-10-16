
/*
Copyright Notice:
Shenzhen Xiao Erji Technology (Small R Technology): WIFI Robot Network·Robot Creative Studio Copyright www.wifi-robots.com
You can modify this program arbitrarily and apply it to your own smart car robots and other electronic products, but it is forbidden for commercial profit.
Little R Technology reserves the right to file a lawsuit against infringement!
* File name: Uart
* File identification:
* Abstract: WiFi robot smart car control
* Description: Serial port parsing file
* Current version: 2560TH v2.5
* Author: BY WIFI robot network · robot creative studio
* Completion date: June 2017
*/


#define BAUD 9600

/*
*********************************************************************************************************
** Function name : USART_init()
** Function: Serial port initialization function
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void USART_init()
{
  SREG = 0x80;                              //Turn on total interruption
  //bitSet(UCSR0A,U2X0);
  bitSet(UCSR0B,RXCIE0);                    //Allow receive completion interrupt// 
  bitSet(UCSR0B,RXEN0);                     //Turn on reception// 
  bitSet(UCSR0B,TXEN0);                     //Turn on sending// 
  bitSet(UCSR0C,UCSZ01);
  bitSet(UCSR0C,UCSZ00);                    //Set asynchronous communication, no parity, 1 stop bit, 8 bits of data
  UBRR0=(F_CPU/16/BAUD-1);                  //Baud rate 9600
}
/*
*********************************************************************************************************
** Function name :put_char()
** Function: Send data frame
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/ 
static void put_char(unsigned int data)  
{  
    if (data == '/r')  
        put_char(0x09);  
    while ( !(UCSR0A & (1<<UDRE0)) )    //Not empty, wait for
        ;  
    UDR0 = data;  
}  

/*
*********************************************************************************************************
** Function name : myprintf()
** Function: Custom serial print function
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/ 
static void myprintf(const char* fmt,...)  
{  
    const char* s;  
    int d;  
    char buf[16];  
    va_list ap;  
    va_start(ap,fmt);   // Point ap to fmt (that is, the first one to change the parameter? Next?)
    while (*fmt)  
    {  
        if (*fmt != '%')  
        {  
            put_char(*fmt++);   // Normal transmission 
            continue;     
        }  
        switch (*++fmt) // next %  
        {  
        case 's':  
            s = va_arg(ap,const char*); // Convert the app pointer to char* and return it 
            for (; *s; s++)  
                put_char(*s);  
            break;  
        case 'x':  
            d = va_arg(ap,int);     // Convert ap directional to int and return 
            itoa(d,buf,16);         // Transfer integer d to hexadecimal to buf
            for (s = buf; *s; s++)  
                put_char(*s);  
            break;  
        case 'd':  
            d = va_arg(ap,int);  
            itoa(d,buf,10);         // Transfer integer d to the buf in decimal  
            for (s = buf; *s; s++)  
                put_char(*s);  
            break;  
        default:  
            put_char(*fmt);  
            break;  
        }  
        fmt++;  
    }  
    va_end(ap);  
}

/*
*********************************************************************************************************
** Function name : Sendbyte()
** Function: Serial port sends a byte
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/  
void Sendbyte(char c)
{
  loop_until_bit_is_set(UCSR0A,UDRE0);
  UDR0=c;
}

/*
*********************************************************************************************************
** Function name : ISR()
** Function: Serial port interrupt
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
//ISR(USART_RX_vect)                    //Suitable for UNO
ISR(USART0_RX_vect)                     //Suitable for MEGA 2560
{
  UCSR0B &= ~(1 << RXCIE0);         //Turn off the serial port interrupt 
  Get_uartdata(); 
  UCSR0B |=  (1 << RXCIE0);         //Open serial port interrupt
}

/*
*********************************************************************************************************
** Function name : ISR()
** Function: Send a string via uart0 and add a carriage return at the end
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void SendString(char *str)
{
  while(*str)
  {
    Sendbyte(*str);
    str++;
  }
  Sendbyte(0x0d);
  Sendbyte(0x0a);  
}
/*
*********************************************************************************************************
** Function name : Get_uartdata()
** Function: Read serial command
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Get_uartdata(void)
{
  ServoStatusLED=!ServoStatusLED;
   static int i;
    serial_data = UDR0;//Read serial port
    if (rec_flag == 0)
    {
      if (serial_data == 0xff)//Get 0xff for the first time (ie header)
      {
        rec_flag = 1;
        i = 0;
        Costtime = 0;
      }
    }
    else
    {
      if (serial_data == 0xff)//The second time to get 0xff(that is, the end of the package)
      {
        rec_flag = 0;
        if (i == 3)//The intermediate data is 3 bytes, indicating that the command is in the correct format
        {
          Communication_Decode();//Execute command parsing function
        }
        i = 0;
      }
      else
      {
        buffer[i] = serial_data;//Temporary data
        i++;
      }
    }
}
/*
*********************************************************************************************************
** Function name : UartTimeoutCheck()
** Function: Serial port timeout detection
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void UartTimeoutCheck(void)
{
  if (rec_flag == 1)
  {
    Costtime++;
    if (Costtime == 100000)
    {
      rec_flag = 0;
    }
  }
}

/*
*********************************************************************************************************
** Function name : Communication_Decode()
** Function: Serial command decoding
** Entry parameters: none
** Export parameters: none
*********************************************************************************************************
*/
void Communication_Decode()
{
  if (buffer[0] == 0x00)
  {
    MoterStatusLED=!MoterStatusLED;    //Motor status light flip
    digitalWrite(ledpin1,MoterStatusLED);
    switch (buffer[1])  //Motor command
    {
      case 0x01: MOTOR_GO_FORWARD;  return;
      case 0x02: MOTOR_GO_BACK;     return;
      case 0x03: MOTOR_GO_LEFT;     return;
      case 0x04: MOTOR_GO_RIGHT;    return;
      case 0x00: MOTOR_GO_STOP;     return;
    }
  }
  else if (buffer[0] == 0x01) //Rudder Command
  {
    ServoStatusLED=!ServoStatusLED;   //Steering gear status light flip
    digitalWrite(ledpin2,ServoStatusLED);
    if (buffer[2] > 170)return;
    switch (buffer[1])
    {
      case 0x01: angle1 = buffer[2]; servo1.write(angle1);  return;
      case 0x02: angle2 = buffer[2]; servo2.write(angle2);  return;
      case 0x03: angle3 = buffer[2]; servo3.write(angle3);  return;
      case 0x04: angle4 = buffer[2]; servo4.write(angle4);  return;
      case 0x05: angle5 = buffer[2]; servo5.write(angle5);  return;
      case 0x06: angle6 = buffer[2]; servo6.write(angle6);  return;
      case 0x07: angle7 = buffer[2]; servo7.write(angle7);  return;
      case 0x08: angle8 = buffer[2]; servo8.write(angle8);  return;
      default: return;
    }
  }

  else if (buffer[0] == 0x02) //Speed regulation
  {
    if (buffer[2] > 100)return;

    if (buffer[1] == 0x01) //Left shift
    {
      Left_Speed_Hold=buffer[2]*2+55;//The speed gear is 0~100, converted to pwm, the speed pwm is lower than 55, the motor does not turn
      analogWrite(ENB, Left_Speed_Hold);
      EEPROM.write(0x09,Left_Speed_Hold);//Storage speed
    }
    if (buffer[1] == 0x02) //Right shift
    {
      Right_Speed_Hold=buffer[2]*2+55;//The speed gear is 0~100, converted to pwm, the speed pwm is lower than 55, the motor does not turn
      analogWrite(ENA,Right_Speed_Hold);
      EEPROM.write(0x0A,Right_Speed_Hold);//Storage speed
    } else return;
  }
  else if (buffer[0] == 0x33) //Read the steering angle and assign
  {
    Init_Steer(); return;
  }
  else if (buffer[0] == 0x32) //Save command
  {
    EEPROM.write(0x01, angle1);
    EEPROM.write(0x02, angle2);
    EEPROM.write(0x03, angle3);
    EEPROM.write(0x04, angle4);
    EEPROM.write(0x05, angle5);
    EEPROM.write(0x06, angle6);
    EEPROM.write(0x07, angle7);
    EEPROM.write(0x08, angle8);
    return;
  }
  else if (buffer[0] == 0x13) //Mode switch
  {
    switch (buffer[1])
    {
      case 0x01: Cruising_Flag = 1; 
      return;   //Follow mode
      case 0x02: Cruising_Flag = 2;
      LCDA.CLEAR();delay(10);LCDA.DisplayString(1, 2, follow, SIZE(follow));
      return;  //Patrol mode
      case 0x03: Cruising_Flag = 3;
      LCDA.CLEAR();delay(10);LCDA.DisplayString(1, 2, Avoid, SIZE(Avoid));
      return;  //Obstacle avoidance mode
      case 0x04: Cruising_Flag = 4;
      LCDA.CLEAR();delay(10);LCDA.DisplayString(1, 1, WaveAvoid, SIZE(WaveAvoid));
      return;  //Radar avoidance mode
      case 0x05: Cruising_Flag = 5;
      return;  //Ultrasonic distance PC display
      case 0x07: Cruising_Flag = 7;               //Route plan 
          analogWrite(ENA,140);
          analogWrite(ENB,140);
          return;
      case 0x00: Cruising_Flag = 0;
          LCDA.CLEAR();delay(10);LCDA.DisplayString(1, 2, Normal, SIZE(Normal));
          analogWrite(ENA,Left_Speed_Hold);
          analogWrite(ENB,Right_Speed_Hold);
      return;  //Normal mode
      default: Cruising_Flag = 0;
      LCDA.CLEAR();delay(10);LCDA.DisplayString(1, 2, Normal, SIZE(Normal));
      return;  //Normal mode
    }
  }
  else if (buffer[0] == 0x04)//The driving light command is FF040000FF,and the closing light command is FF040100FF
  {
    switch (buffer[1])  
    {
      case 0x00: Close_Light(); return;  //Turn off the lights
      case 0x01: Open_Light(); return;   //Driving light
      default: return;
    }
  }
  else if (buffer[0] == 0x40) //Storage motor sign
  {
    adjust = buffer[1];
    EEPROM.write(0x10, adjust);
  }
        else if(buffer[0]==0xA0)//Received a right turn
      {
         RevStatus = 2;
         TurnAngle=buffer[1];
         Golength=buffer[2];
      }
      else if(buffer[0]==0xA1)//Received a left turn
      {
         RevStatus = 1;
         TurnAngle=buffer[1];
         Golength=buffer[2];
      }
}

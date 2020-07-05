int trigPin = 3;
int echoPin = 2;

char receivedChar;
int Data = 0;
boolean newData = false;

float maxDistance = 200;          // define the range(cm) for ultrasonic ranging module, Maximum sensor distance is rated at 400-500cm.
float rangingTimeOut = 2 * maxDistance / 100 / 340 * 1000000; // define the timeout(ms) for ultrasonic ranging module

void setup() 
{
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);

}

void loop() 
{
  getInfo();
  //Serial.println(getDistance());
  if(newData)
  {
    Data = (receivedChar - '0');
    //Serial.print("NEW DATA = ");
    //Serial.println(Data);
    if(Data == 1)
    {
      int distance = getDistance();
      //Serial.print(distance);
      Serial.write(distance);
    }
    else if(Date == 2)
    {
      
    }
    //Serial.println(Distance);
    newData = false;
  }

}

void getInfo() 
{
  if (Serial.available() > 0) 
  {
    receivedChar = Serial.read();
    newData = true;    
  } 
}

float getDistance() {
  unsigned long pingTime; // save the high level time returned by ultrasonic ranging module
  float distance;         // save the distance away from obstacle

  // set the trigPin output 10us high level to make the ultrasonic ranging module start to measure
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // get the high level time returned by ultrasonic ranging module
  pingTime = pulseIn(echoPin, HIGH, rangingTimeOut);

  if (pingTime != 0) {  // if the measure is not overtime
    distance = pingTime * 340 / 2 / 10000;  // calculate the obstacle distance(cm) according to the time of high level returned
    return distance;    // return distance(cm)
  }
  else                  // if the measure is overtime
    return maxDistance; // returns the maximum distance(cm)
}

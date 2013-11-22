

int key = 7;
int led  = 8;

uint8_t lastKey = LOW;

void setup()
{
  Serial.begin(9600);
  
  pinMode(key, INPUT);
  digitalWrite(key, HIGH);
  
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
}


void loop()
{
  if(Serial.available())
  {
    char buffer[3];
    int len = Serial.readBytesUntil('\n', buffer, 3);
    
    if(buffer[0] == '+')
    {
      if(buffer[1] == 'C')
      {
        if(buffer[2] == '4')
        {
          digitalWrite(led, HIGH);
        }
      }
    }
    if(buffer[0] == '-')
    {
      if(buffer[1] == 'C')
      {
        if(buffer[2] == '4')
        {
          digitalWrite(led, LOW);
        }
      }
    }
  }
  
  if(digitalRead(key) == LOW)
  {
    if(lastKey == LOW)
      return;
    
    lastKey = LOW;
    char buffer[4] = "C4\n";
    Serial.write((const unsigned char*)buffer, 3);
    delay(100);
  }
  else
  {
    lastKey = HIGH;
  }
}



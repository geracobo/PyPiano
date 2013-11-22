

int key = 7;

uint8_t lastKey = LOW;

void setup()
{
  Serial.begin(9600);
  
  pinMode(key, INPUT);
  digitalWrite(key, HIGH);
}


void loop()
{
//  if(Serial.available())
//  {
//    char buffer[64];
//    int len = Serial.readBytesUntil('\n', buffer, 64);
//    
//    buffer[len] = '\n';
//    buffer[len+1] = '\0';
//    
//    Serial.write(">");
//    Serial.write((const unsigned char*)buffer, len+1);
//  }
  
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



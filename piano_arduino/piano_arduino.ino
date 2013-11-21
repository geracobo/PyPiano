

void setup()
{
  Serial.begin(9600);
}


void loop()
{
  if(Serial.available())
  {
    char buffer[64];
    int len = Serial.readBytesUntil('\n', buffer, 64);
    
    buffer[len] = '\n';
    buffer[len+1] = '\0';
    
    Serial.write(">");
    Serial.write((const unsigned char*)buffer, len+1);
  }
}



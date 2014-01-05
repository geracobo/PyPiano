/*
For PyPiano
Using Arduino Mega


Gerardo Cobo
*/


typedef struct Key
{
  char name[3];
  int key;
  int light;
  
  uint8_t last_key;
} Key;

// Key name, Key input pin, Key output light pin, Last key state
Key keys[] = {
  {"C4", 22, 38, LOW},
  {"D4", 23, 39, LOW},
  {"E4", 24, 40, LOW},
  {"F4", 25, 41, LOW},
  {"G4", 26, 42, LOW},
  {"A4", 27, 43, LOW},
  {"B4", 28, 44, LOW},
  {"C5", 29, 45, LOW},
  {"D5", 30, 46, LOW},
  {"E5", 31, 47, LOW},
  {"F5", 32, 48, LOW},
  {"G5", 33, 49, LOW},
  {"A5", 34, 50, LOW},
  {"B5", 35, 51, LOW}
};


void setup()
{
  Serial.begin(9600);
  
  // For each key...
  for (int i = 0; i < (sizeof(keys)/sizeof(Key)); i++)
  {
    pinMode(keys[i].key, INPUT);
    digitalWrite(keys[i].key, HIGH);
    pinMode(keys[i].light, OUTPUT);
    digitalWrite(keys[i].light, LOW);
  }
}


int match_key(char name[3])
{
  for(int i = 0; i < (sizeof(keys)/sizeof(Key)); i++)
  {
    if(strcmp(keys[i].name, name) == 0)
    {
      return i;
    }
  }
}


void loop()
{
  // Check if they are sending us something...
  if(Serial.available())
  {
    // We will only receive turning lights ON and OFF
    // commands...
    char buffer[3];
    int len = Serial.readBytesUntil('\n', buffer, 3);

    char name[3] = {buffer[1], buffer[2], '\0'};
    Key* k = &keys[match_key(name)];

    if(k != NULL)
    {
      if(buffer[0] == '+')
      {
        digitalWrite(k->light, HIGH);
      }
      else if(buffer[0] == '-')
      {
        digitalWrite(k->light, LOW);
      }
    }
  }

  // Check every key.
  for(int i = 0; i < (sizeof(keys)/sizeof(Key)); i++)
  {
    Key k = keys[i];
    if(digitalRead(k.key) == HIGH)
    {
      if(k.last_key == HIGH)
        continue;

      keys[i].last_key = HIGH;
      char buffer[4] = {k.name[0], k.name[1], '\n', '\0'};
      Serial.write((const unsigned char*)buffer, 4);

      // The delay may be necessary, depending on the switch noise.
      //delay(300);
    }
    else
    {
      if(k.last_key == LOW)
        continue;

      keys[i].last_key = LOW;

      // The delay may be necessary, depending on the switch noise.
      //delay(300);
    }
  }
  //Serial.println("--------");
}



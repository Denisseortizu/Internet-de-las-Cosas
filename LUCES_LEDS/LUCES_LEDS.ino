void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);// LED 1
  pinMode(12, OUTPUT);// LED 2
  pinMode(11, OUTPUT);// LED 3
  pinMode(10, OUTPUT);// LED 4
  pinMode(9, OUTPUT);// LED 5
  pinMode(8, OUTPUT);// LED 6
  pinMode(7, OUTPUT);// LED 7
  pinMode(6, OUTPUT);// LED 8

  //Configuramos para recibir por puerto serial

  

}

void loop() {
  int i = 0;
  for(i=6;i<14;i++){
    digitalWrite( i , HIGH);
    delay(500);
    digitalWrite( i , LOW);
    delay(500);
  }
}

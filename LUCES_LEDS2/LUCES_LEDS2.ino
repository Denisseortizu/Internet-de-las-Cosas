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

  Serial.begin(9600);

}

void loop() {
  //Preguntar por el nombre (en minus)
  //if (Serial.available())
  //{
  String nombre = Serial.readStringUntil('\n');
  nombre.trim();
  //}
  for(int le=0; le>8;le++){
    digitalWrite( le , HIGH);
    }
  //Convertir los caracteres a accii
  int i = 0 ; //Iniciar la variable


  do {
    int let = nombre.charAt(i); //Vslor ASCII

    //Convertir
    int bits[8] = {};

    for (int j = 8; j > 0; j--) {
      bits[j] = let % 2;
      let = let / 2;
      digitalWrite( j , HIGH);
    }


    delay(1500);
    digitalWrite( i , LOW);
    delay(1500);
  } while (i >= nombre.length());
}

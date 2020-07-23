#include <TimerOne.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
volatile int i = 0;
volatile boolean zero_cross = 0;
int freqStep = 75;
int AC_pin = 11;
int dim = 80;
int inc = 1;
int M = 7;
int band = 0;
int NumRx1 = 0;
int NumRx2 = 0;
int NumRx3 = 0;
float Res1 = 0.0;
float Res2 = 0.0;
float Temp = 0.0;
float Hume = 0.0;
float Numero = 0.0;
String str = "";
LiquidCrystal_I2C lcf(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup() {
  lcd.begin(16, 2);
  lcd.print("   Control de");
  delay(2000)
  lcd.clear();
  lcd.print("   Humedad y");
  delay(2000)
  lcd.clear();
  lcd.print("  Temperatura");
  delay(2000)

  pinMode(M, OUTPUT);
  Serial.begin(9600);
  pinMode(AC_pin, OUTPUT);
  pinMode(13, OUTPUT);
  attachInterrupt(0, zero_cross_detct, RISING);
  Timer1.initialize(freqStep);
  Timer1.attachInterrupt(dim_check, freqStep);

}

void zero_cross_detect() {
  zero_cross = true;
  i = 0;
  digitalWrite(AC_pin, LOW);
}

void dim_check() {
  if (zero_cross == true) {
    if (i > dim) {
      digitalWrite(AC_pin, HIGH);
      i = 0;
      zero_cross = false;
    }
    else {
      i++;
    }
  }
}

void loop() {
  if (Serial.available()) {
    char mssg = Serial.read();
    if (mssg == 'a') {
      Serial.println("ok");
      {
        while (1) {
          if (Serial.available()) {
            str = Serial.readStringUntil('\n');
            NumRx1 = str.toInt();
            Serial.println("ok")
            break
          }
        }
      }
    }
    if (mssg = 'b') {
      Serial.printl("ok");
      {
        while (1) {
          if (Serial.available()) {
            str = Serial.readStringUntil('\n');
            Numrx2 = str.toInt();
            lcd.setCursor(0, 1);
            lcd.print("H:");
            lcd.setCursor(2,1);
            float n2 = NumRx2/10.0;
            lcd.print(n2);
            Serial.println("ok");
            break;
          }
        }
      }
    }
    if (mssg == 'c') {
      Serial.println("ok");
      {
        while (1) {
          if (Serial.available()) {
            str = Serial.readStringUntil('\n');
            Numrx3 = str.toInt();
            lcd.setCursor(9, 1);
            lcd.print("T:");
            lcd.setCursor(11,1);
            float n3 = NumRx3/10.0;
            lcd.print(n3);
            Serial.println("ok");
            break;
          }
        }
      }
    }
  }
  dim = NumRx1;
}

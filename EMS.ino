const int ACS712_PIN = A0; // Analog pin connected to ACS712 sensor
const float ACS712_SENSITIVITY = 0.185; // Sensitivity of the ACS712 sensor for 30A version

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read analog value from ACS712 sensor
  int sensorValue = analogRead(ACS712_PIN);

  // Convert analog value to voltage
  float voltage = sensorValue * (5.0 / 1023.0);

  // Convert voltage to current using ACS712 sensitivity
  float current = (voltage - 2.5) / ACS712_SENSITIVITY;

  // Display voltage, current, and power readings
  Serial.print("Voltage (V): ");
  Serial.print(voltage);
  Serial.print("\t Current (A): ");
  Serial.print(current);
  Serial.print("\t Power (W): ");
  Serial.println(voltage * current);

  delay(1000); // Delay for stability
}

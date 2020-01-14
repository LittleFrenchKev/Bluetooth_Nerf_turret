/*
    Name:          NERF Turret.ino
    Created:	   12/01/2020 17:55:17
    Author:        shurillu@tiscalinet.it
    Description:   Blynk platform porting of the awesome work of Kevin. Check here
	           https://www.littlefrenchkev.com/bluetooth-nerf-turret
	
    PAY ATTENTION: SOME PINS/ANGLES OF YOUR TURRET COULD BE DIFFERENT FORM WHAT IS USED HERE
                   CHECK ALL SECTIONS MARKED BY "CHECK THESE/THIS"
*/

 /* Comment this out to disable prints and save space */
//#define BLYNK_PRINT Serial

#define BLYNK_USE_DIRECT_CONNECT

#include <BlynkSimpleSerialBLE.h>
#include <Servo.h>

// CHECK THESE <-------------------------------------------
// Servos and rollers pins
#define ROLLERS_PIN      12
#define RECOIL_SERVO_PIN 11
#define TILT_SERVO_PIN   10
#define PAN_SERVO_PIN     9

// CHECK THESE <-------------------------------------------
// Servos max and min angle
#define PAN_ANGLE_MIN         0
#define PAN_ANGLE_CENTER     90
#define PAN_ANGLE_MAX       180
#define TILT_ANGLE_MIN       50
#define TILT_ANGLE_CENTER    90
#define TILT_ANGLE_MAX      140
#define RECOIL_ANGLE_PUSHED  30
#define RECOIL_ANGLE_REST   100

#define FIRE_TIME 200

#define JOYSTICK_VIRTUAL_PIN V0
#define ARMED_VIRTUAL_PIN    V1
#define FIRE_VIRTUAL_PIN     V2

// CHECK THIS  <-------------------------------------------
// Blynk app token
#define BLYNK_TOKEN "YourBlynkAppToken" 

Servo panServo;
Servo tiltServo;
Servo recoilServo;

int armed;


BLYNK_WRITE(JOYSTICK_VIRTUAL_PIN) {
	int pan  = param[0].asInt();
	int tilt = param[1].asInt();

	int panAngle  = map(pan, 0,  255, PAN_ANGLE_MIN,  PAN_ANGLE_MAX);
	int tiltAngle = map(tilt, 0, 255, TILT_ANGLE_MIN, TILT_ANGLE_MAX);

	panServo.write(panAngle);
	tiltServo.write(tiltAngle);
}

BLYNK_WRITE(ARMED_VIRTUAL_PIN) {
	armed = param.asInt();

	if (1 == armed) 
		digitalWrite(ROLLERS_PIN, HIGH);
	else 
		digitalWrite(ROLLERS_PIN, LOW);
}

BLYNK_WRITE(FIRE_VIRTUAL_PIN) {
	int fire = param.asInt();
	if ((1 == fire) && (1 == armed)) {
		recoilServo.write(RECOIL_ANGLE_PUSHED);
		delay(FIRE_TIME);
		recoilServo.write(RECOIL_ANGLE_REST);
		delay(FIRE_TIME);
	}
}

void setup()
{
	Serial.begin(9600);
	while (!Serial)
		delay(500);

	panServo.attach(PAN_SERVO_PIN);
	panServo.write(PAN_ANGLE_CENTER);

	tiltServo.attach(TILT_SERVO_PIN);
	tiltServo.write(TILT_ANGLE_CENTER);

	recoilServo.attach(RECOIL_SERVO_PIN);
	recoilServo.write(RECOIL_ANGLE_REST);

	pinMode(ROLLERS_PIN, OUTPUT);
	digitalWrite(ROLLERS_PIN, LOW);
	armed = 0;
	Blynk.begin(Serial, BLYNK_TOKEN);
}

void loop()
{
	Blynk.run();
}

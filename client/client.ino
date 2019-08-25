#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <FastLED.h>


#define LED_OUTPUT_PIN        4
#define LED_TYPE              WS2812B
#define LED_PIXELS            60
#define LED_ORDER             GRB

#define UDP_LISTEN_PORT       10001
#define UDP_BUFFER_LENGTH     10000

#define WIFI_SSID             "*****" // Update this value
#define WIFI_PASSWORD         "*****" // Update this value

WiFiUDP udp;
CRGBArray<LED_PIXELS> leds;


/*
 * These variables are automatically updated by sketch
 * so there is no need to modify this manually.
*/
static uint8_t CURRENT_HUE = 0;
static uint8_t WORKING_DISPLAY_MODE = 0;
static uint8_t WORKING_INTENSITY = 0;
CRGB WORKING_RGB_VALUES;
static char WORKING_PACKET_BUFFER[UDP_BUFFER_LENGTH];

void setup() {
  Serial.begin(115200);

  delay(1000);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.println("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.println(WiFi.localIP());

  udp.begin(UDP_LISTEN_PORT);
  FastLED.addLeds<LED_TYPE, LED_OUTPUT_PIN, LED_ORDER>(leds, LED_PIXELS);
}

CHSV getRainbowPixel(uint8_t hue) {
    CHSV hsv;
    hsv.hue = hue;
    hsv.val = 255;
    hsv.sat = 240;

    return hsv;
}

void rainbow(uint8_t fill) {
  uint8_t hueAdder = -10;

  for(int i = 0; i < LED_PIXELS/2; i++) {
    int leftPixel = LED_PIXELS/2-1-i;
    int rightPixel = LED_PIXELS/2+i;

    if(leftPixel < fill) {
      leds[LED_PIXELS/2-leftPixel] = getRainbowPixel(CURRENT_HUE + (hueAdder+=10));
    } else {
      leds[LED_PIXELS/2-leftPixel].fadeToBlackBy(40);
    }

    if(rightPixel < fill+LED_PIXELS/2) {
      leds[rightPixel] = getRainbowPixel(CURRENT_HUE + (hueAdder-=10));
    } else {
      leds[rightPixel].fadeToBlackBy(40);
    }
  }
}

void parsePacket() {
  int packetLength = udp.parsePacket();

  if(packetLength >= 1) {
    udp.read(WORKING_PACKET_BUFFER, UDP_BUFFER_LENGTH);

    WORKING_DISPLAY_MODE      = (uint8_t) WORKING_PACKET_BUFFER[0];
    WORKING_INTENSITY         = (uint8_t) WORKING_PACKET_BUFFER[1];
    WORKING_RGB_VALUES.r      = (uint8_t) WORKING_PACKET_BUFFER[2];
    WORKING_RGB_VALUES.g      = (uint8_t) WORKING_PACKET_BUFFER[3];
    WORKING_RGB_VALUES.b      = (uint8_t) WORKING_PACKET_BUFFER[4];
  }
}

void loop() {
  parsePacket();


  if(WORKING_INTENSITY == 0) {
    leds.fadeToBlackBy(40);
  }

  if(WORKING_INTENSITY > 0 && WORKING_DISPLAY_MODE > 100) {
    switch(WORKING_DISPLAY_MODE) {
 
      // STATIC
      case 101:
        // Fill strip with a static rainbow
        leds.fill_rainbow(0, 10);
        break;
      case 102:
        // Fill strip with wave rainbow
        leds.fill_rainbow(CURRENT_HUE, 10);
        break;
      case 103:
        // Fill strip with solid color
        leds.fill_solid(WORKING_RGB_VALUES);
        break;
 
      // DYNAMIC
      case 201:
        // Fill n leds with static rainbow
        rainbow(WORKING_INTENSITY);
    }
  }
  FastLED.show();
  FastLED.delay(1000/60);

  EVERY_N_MILLISECONDS(2) {
    CURRENT_HUE++;
  }
}

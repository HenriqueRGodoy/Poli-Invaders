#include <WiFi.h>
#include <PubSubClient.h>

const char *ssid = "Tadaki_Lan";
const char *password = "12345678";
const char *mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char *mqtt_user = "";
const char *mqtt_password = "";
const char *mqtt_serial_publish_ch = "FPGA/input";
const char *mqtt_serial_receiver_ch = "FPGA/input";

const int pontos_pins[] = {36, 39, 34, 35};
int pontos[4];

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
    Serial.println("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void mqtt_callback(char *topic, byte *payload, unsigned int length) {
    Serial.println("-------new message from broker-----");
    Serial.print("channel:");
    Serial.println(topic);
    Serial.print("data:");
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        String clientId = "ESP32Client-";
        clientId += String(random(0xffff), HEX);
        if (client.connect(clientId.c_str(), mqtt_user, mqtt_password)) {
            Serial.println("connected");
            client.publish("FPGA/output", "connected");
            client.subscribe(mqtt_serial_receiver_ch);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(mqtt_callback);

    for (int i = 0; i < 4; i++) {
        pinMode(pontos_pins[i], INPUT);
    }

    reconnect();
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    String data = "";
    for (int i = 0; i < 4; i++) {
        pontos[i] = digitalRead(pontos_pins[i]);
        data += String(pontos[i]);
    }

    Serial.println(data);
    client.publish(mqtt_serial_publish_ch, data.c_str());
    delay(100);
}

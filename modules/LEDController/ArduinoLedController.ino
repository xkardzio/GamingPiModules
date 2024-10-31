#define BAUDRATE 115200 ///< UART baud rate for serial communication.

/// Macro to calculate the size of an array.
#define ARRAY_SIZE(x) (sizeof(x) / sizeof(x[0]))

/**
 * @brief Structure representing a data packet.
 */
typedef struct {
  uint8_t header; ///< Packet header identifying the type of data.
  uint8_t value;  ///< Packet value representing either a command or a pin state.
} Packet;

/**
 * @brief Enumeration for available commands.
 */
enum Command {
  INIT = 0x32, ///< Command for initializing pins.
};

/**
 * @brief Enumeration for return types to indicate success or error statuses.
 */
enum ReturnType {
  COMMAND_ERROR = 0x64, ///< Indicates an unknown command error.
  COMMAND_SUCCESS = 0x65, ///< Indicates successful command execution.
  INIT_ERROR = 0x6e, ///< Indicates initialization error.
  INIT_SUCCESS = 0x6f, ///< Indicates successful initialization.
  PIN_ERROR = 0xc8, ///< Indicates invalid pin error.
  PIN_OK = 0xc9 ///< Indicates successful pin operation.
};

/**
 * @brief Enumeration for packet types.
 */
enum PacketType {
  PIN = 0, ///< Packet is a pin operation.
  COMMAND = 1 ///< Packet is a command operation.
};

const uint8_t PWM_LED[] = {3, 5, 6, 9, 10, 11}; ///< Array of pins supporting PWM.
const uint8_t NORMAL_LED[] = {0, 1, 2, 4, 7, 8, 12, 13}; ///< Array of pins for normal digital output.

/**
 * @brief Initializes the LED pins.
 */
void initPins(void) {
  for (uint8_t i = 0; i < ARRAY_SIZE(PWM_LED); i++) {
    pinMode(PWM_LED[i], OUTPUT);
    analogWrite(PWM_LED[i], 0);
  }

  for (uint8_t i = 0; i < ARRAY_SIZE(NORMAL_LED); i++) {
    pinMode(NORMAL_LED[i], OUTPUT);
    digitalWrite(NORMAL_LED[i], 0);
  }

  Serial.write(INIT_SUCCESS);
}

/**
 * @brief Configures the serial communication and initializes pins.
 */
void setup() {
  Serial.begin(BAUDRATE);
  initPins();
}

/**
 * @brief Determines the type of a packet based on its header.
 * 
 * @param header Header of the packet.
 * @return PacketType The determined type of the packet (PIN or COMMAND).
 */
PacketType getPacketType(const uint8_t header) {
  if (contains(PWM_LED, sizeof(PWM_LED) / sizeof(PWM_LED[0]), header))
    return PIN;
  if (contains(NORMAL_LED, sizeof(NORMAL_LED) / sizeof(NORMAL_LED[0]), header))
    return PIN;
  else
    return COMMAND;
}

/**
 * @brief Checks if a value exists in an array.
 * 
 * @param array The array to search.
 * @param arraySize Size of the array.
 * @param value Value to search for in the array.
 * @return true if value is found, otherwise false.
 */
bool contains(const uint8_t* array, size_t arraySize, const uint8_t value) {
    for (size_t i = 0; i < arraySize; i++) {
        if (array[i] == value)
            return true;
    }
    return false;
}

/**
 * @brief Processes and handles command packets.
 * 
 * @param packet Packet to process.
 * @return true on successful command handling, false otherwise.
 */
bool handleCommand(const Packet packet) {
  switch (packet.header) {
    case Command::INIT:
      initPins();
      break;
    default:
      Serial.write(COMMAND_ERROR);
      break;
  }
}

/**
 * @brief Writes a value to a specified LED pin.
 * 
 * @param pin The pin number to operate on.
 * @param value The value to write to the pin (PWM value or digital HIGH/LOW).
 */
void writeLed(const uint8_t pin, const uint8_t value) {
    bool isPwmPin = contains(PWM_LED, sizeof(PWM_LED) / sizeof(PWM_LED[0]), pin);
    bool isNormalPin = contains(NORMAL_LED, sizeof(NORMAL_LED) / sizeof(NORMAL_LED[0]), pin);
    if (isPwmPin)
      analogWrite(pin, value);
    else if (isNormalPin)
      digitalWrite(pin, value > 0 ? HIGH : LOW);

    if (isPwmPin || isNormalPin)
      Serial.write(PIN_OK);
    else
      Serial.write(PIN_ERROR);
}

/**
 * @brief Main loop that processes incoming packets.
 */
void loop() {
  Packet packet = {};

  if (Serial.available() >= sizeof(Packet)) {
    Serial.readBytes((char *)&packet, sizeof(Packet));

    PacketType packetType = getPacketType(packet.header);

    if (packetType == PIN) {
      writeLed(packet.header, packet.value);
    } 
    else if (packetType == COMMAND) {
      handleCommand(packet);
    } 
  }
}

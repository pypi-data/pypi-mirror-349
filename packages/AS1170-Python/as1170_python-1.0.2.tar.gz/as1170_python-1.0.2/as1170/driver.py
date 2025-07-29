import time
import smbus2
import RPi.GPIO as GPIO
import threading

class AS1170LED:
    """Complete AS1170 LED controller with all methods exposed."""

    def __init__(self):
        # Default I2C bus and AS1170 address
        self.I2C_BUS = 3  # Default Raspberry Pi I2C bus
        self.I2C_ADDR = 0x30  # Default AS1170 I2C address

        # AS1170 Registers
        self.REG_STROBE_SIGNAL = 0x07
        self.REG_FLASH_TIMER = 0x05
        self.REG_CURRENT_LED1 = 0x01
        self.REG_CURRENT_LED2 = 0x02
        self.REG_CONTROL = 0x06

        # STROBE pin configuration
        self.STROBE_PIN = 19
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.STROBE_PIN, GPIO.OUT, initial=GPIO.LOW)

        # Initialize I2C bus
        self.bus = smbus2.SMBus(self.I2C_BUS)

        # LED states
        self.led1_current = self.convert_mA_to_register(450)  # Default current for LED1 (~450mA)
        self.led2_current = self.convert_mA_to_register(450)  # Default current for LED2 (~450mA)
        self.strobe_active = False
        self.strobe_thread = None
        self.initialized = False

        # Run initialization sequence on startup
        self._initialize_device()

    def _initialize_device(self):
        """Run the initialization sequence for AS1170 on module startup."""
        try:
            print("Running AS1170 initialization sequence...")
            # i2cset -y 4 0x30 0x07 0xC0
            self.write_register(self.REG_STROBE_SIGNAL, 0xC0)
            # i2cset -y 4 0x30 0x05 0x80
            self.write_register(self.REG_FLASH_TIMER, 0x80)
            # i2cset -y 4 0x30 0x06 0x1B
            self.write_register(self.REG_CONTROL, 0x1B)
            print("AS1170 initialization sequence completed")
        except Exception as e:
            print(f"Warning: AS1170 initialization sequence failed: {e}")

    def init(self, i2c_bus=None, strobe_pin=None):
        """Initialize the AS1170 with custom I2C bus and strobe pin."""
        if i2c_bus is not None:
            self.set_i2c_bus(i2c_bus)
        if strobe_pin is not None:
            self.set_strobe_pin(strobe_pin)

        # Run initialization sequence again with new bus if changed
        if i2c_bus is not None:
            self._initialize_device()

        self.initialized = True
        print(f"AS1170 initialized - I2C bus: {self.I2C_BUS}, STROBE pin: {self.STROBE_PIN}")

    def set_i2c_bus(self, bus_id):
        """Sets the I2C bus dynamically."""
        self.I2C_BUS = bus_id
        self.bus.close()  # Close the old bus before reassigning
        self.bus = smbus2.SMBus(self.I2C_BUS)
        print(f"I2C bus set to {self.I2C_BUS}")

    def set_id(self, new_id):
        """Sets the AS1170 I2C address dynamically."""
        self.I2C_ADDR = new_id
        print(f"AS1170 I2C address set to {hex(self.I2C_ADDR)}")

    def set_strobe_pin(self, pin):
        """Sets the STROBE pin dynamically."""
        GPIO.cleanup(self.STROBE_PIN)
        self.STROBE_PIN = pin
        GPIO.setup(self.STROBE_PIN, GPIO.OUT, initial=GPIO.LOW)
        print(f"STROBE pin set to {self.STROBE_PIN}")

    def write_register(self, register, value):
        """Writes a value to an AS1170 register."""
        self.bus.write_byte_data(self.I2C_ADDR, register, value)
        time.sleep(0.01)  # Small delay for stability

    def convert_mA_to_register(self, current_mA):
        """Converts current in mA (0-450) to register value (0x00-0x7F)."""
        return max(0, min(0x7F, int((current_mA / 450) * 0x7F)))

    def set_intensity(self, led1, led2):
        """Sets intensity for LED1 and LED2 using mA values (0-450mA)."""
        # Update internal state
        self.led1_current = self.convert_mA_to_register(led1)
        self.led2_current = self.convert_mA_to_register(led2)

        # Write to registers
        self.write_register(self.REG_CURRENT_LED1, self.led1_current)
        self.write_register(self.REG_CURRENT_LED2, self.led2_current)
        print(f"LED1 intensity: {led1}mA, LED2 intensity: {led2}mA")

    def on(self):
        """Turns on both LEDs with their current intensity."""
        self.strobe_active = False
        self.write_register(self.REG_CURRENT_LED1, self.led1_current)
        self.write_register(self.REG_CURRENT_LED2, self.led2_current)
        self.write_register(self.REG_CONTROL, 0x1B)  # Enable flash mode
        GPIO.output(self.STROBE_PIN, GPIO.HIGH)
        print("Both LEDs ON")

    def off(self):
        """Turns off both LEDs and stops any active strobe mode."""
        self.strobe_active = False
        self.write_register(self.REG_CONTROL, 0x00)  # Disable LEDs
        GPIO.output(self.STROBE_PIN, GPIO.LOW)
        print("Both LEDs OFF")

    def _strobe_loop(self, frequency):
        """Internal method for strobe effect."""
        period = 1.0 / frequency
        print("Strobe mode activated")
        while self.strobe_active:
            self.write_register(self.REG_CURRENT_LED1, self.led1_current)
            self.write_register(self.REG_CURRENT_LED2, self.led2_current)
            self.write_register(self.REG_CONTROL, 0x1B)  # Enable flash mode
            GPIO.output(self.STROBE_PIN, GPIO.HIGH)
            time.sleep(period / 2)
            self.write_register(self.REG_CONTROL, 0x00)  # Disable LEDs
            GPIO.output(self.STROBE_PIN, GPIO.LOW)
            time.sleep(period / 2)
        print("Strobe mode stopped")

    def strobe(self, frequency=10):
        """Flashes both LEDs on and off at a given frequency until manually stopped."""
        if self.strobe_active:
            print("Strobe is already running")
            return
        self.strobe_active = True
        self.strobe_thread = threading.Thread(target=self._strobe_loop, args=(frequency,), daemon=True)
        self.strobe_thread.start()

    def cleanup(self):
        """Clean up GPIO and close I2C bus."""
        self.off()
        GPIO.cleanup()
        self.bus.close()

# Create the global led object that has all methods
led = AS1170LED()

# Expose module-level functions that delegate to the led object for backward compatibility
def init(i2c_bus=None, strobe_pin=None):
    return led.init(i2c_bus, strobe_pin)

def set_i2c_bus(bus_id):
    return led.set_i2c_bus(bus_id)

def set_id(new_id):
    return led.set_id(new_id)

def set_intensity(led1, led2):
    return led.set_intensity(led1, led2)

def on():
    return led.on()

def off():
    return led.off()

def strobe(frequency=10):
    return led.strobe(frequency)

# If used as a standalone script, run a basic test
if __name__ == "__main__":
    try:
        led.init(i2c_bus=3, strobe_pin=19)
        led.set_id(0x30)  # Example: Set I2C address

        led.set_intensity(300, 200)  # Example intensity settings in mA
        led.strobe(frequency=5)  # Strobe effect at 5 Hz until manually stopped
        time.sleep(10)  # Let it strobe for 10 seconds
        led.off()
    except KeyboardInterrupt:
        led.off()
        print("Exiting program...")
    finally:
        led.cleanup()

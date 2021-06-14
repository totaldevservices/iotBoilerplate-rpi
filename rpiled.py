# importing required libraries
from bluetooth import *
import RPi.GPIO as GPIO
import threading

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

# Set pin 8 to be an output pin and set initial value to low (off)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

server_sock = BluetoothSocket(RFCOMM)  # declaring server socket
server_sock.bind(("", PORT_ANY))  # declaring port binding
server_sock.listen(1)

# Retrieving socket name
port = server_sock.getsockname()[1]

# BT UUID
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# Declaring Bluetooth Advertising Service in order for other Bluetooth device to find the SBC's Bluetooth
advertise_service(server_sock, "RPI_BT_Server",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


# Receiving data function
def recv_data():
    while True:
        recv_data = client_sock.recv(1024)

        if not recv_data:
            sys.exit(0)

        if recv_data == "on":
            print("received [%s]" % recv_data)
            GPIO.output(8, GPIO.HIGH)  # Turn LED on at GPIO 8

        elif recv_data == "off":
            print("received [%s]" % recv_data)
            GPIO.output(8, GPIO.LOW)  # Turn LED off at GPIO 8

        print("received [%s]" % recv_data)

# Sending data thread


def send_data():
    while True:
        send_data = raw_input("Enter message: ")
        client_sock.send(send_data)

# Since we're both receiving and sending data simultaneously, we'll need a thread for each functionality:
# a thread for receiving data and a thread for sending data


# Start multithreading
t = threading.Thread(target=recv_data)
t.start()
send_data()

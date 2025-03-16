from pyModbusTCP.client import ModbusClient
import time

# List of reference numbers to read from the Modbus server
reference_numbers = [] # CHANGE THIS

modbus_server_ip = "" # CHANGE THIS
modbus_server_port = "" # CHANGE THIS

# Initialize Modbus client
modbus_client = ModbusClient(host=modbus_server_ip, port=modbus_server_port, unit_id=52)

# Check if the client is connected
if not modbus_client.open():
    print("Unable to connect to Modbus server")
else:
    print("Connected to Modbus server")

# Initialize an empty string to concatenate the values
concat_values = ""

# Iterate over each reference number to read target holding register address
for reference_number in reference_numbers:
    # Read holding register
    val = modbus_client.read_holding_registers(reference_number, 1)
    
    # Check if the read was successful
    if val:
        # Convert the register value to a string
        val_set = "".join(map(chr, val))
        concat_values += val_set
        print(f"Reference Number: {reference_number}, Value: {val_set}")
    else:
        print(f"Failed to read reference number: {reference_number}")

# Output the entire concatenated string at the end
print("Concatenated Values:", concat_values)

# Close the Modbus client connection
modbus_client.close()
print("Connection closed")
#!/usr/bin/env python3
import sys
import subprocess

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <client_ip> <pcap_file>")
        sys.exit(1)

    client_ip = sys.argv[1]
    pcap_file = sys.argv[2]

    # Build the tshark filter expression including all modbus function codes for writing registers:
    #   6  -> Write Single Register
    #   16 -> Write Multiple Registers
    #   22 -> Mask Write Register
    #   23 -> Read/Write Multiple Registers
    filter_expr = (
        f"ip.src == {client_ip} and "
        f"(modbus.func_code == 6 or modbus.func_code == 16 or modbus.func_code == 22 or modbus.func_code == 23)"
    )

    # Build the tshark command:
    # - -r: read the pcap file.
    # - -Tfields: output only fields.
    # - -Y: display filter.
    # - -e: extract the field 'modbus.reference_num'.
    tshark_cmd = [
        "tshark", "-r", pcap_file,
        "-Tfields",
        "-Y", filter_expr,
        "-e", "modbus.reference_num" # Extract the field 'modbus.reference_num'. or Reference Number
    ]

    try:
        # Run the tshark command and capture its output.
        result = subprocess.run(tshark_cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running tshark:", e.stderr)
        sys.exit(1)

    # The output should be a series of numbers (one per field) possibly across multiple lines.
    nums = result.stdout.split()
    if not nums:
        print("No matching packets found.")
        sys.exit(0)

    try:
        # Convert each extracted number into an integer.
        byte_list = [int(num) for num in nums]
    except ValueError as e:
        print("Error converting bytes:", e)
        sys.exit(1)

    # Print the kind of data found
    print(f"Write Register Reference Numbers: {len(byte_list)}")
    print(byte_list)

    # Convert the list of integers into a bytes object.
    data_bytes = bytes(byte_list)
    print("Bytes:")
    print(data_bytes)

if __name__ == "__main__":
    main()
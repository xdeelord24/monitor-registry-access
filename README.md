# Registry Monitoring Script

This Python script monitors the Windows registry for network interface changes and retrieves the current MAC and IP addresses of the machine. It provides a summary of the IP addresses found in the registry and identifies any discrepancies between the current IP address and those found in the registry.

## Requirements

- Python 3.x
- `winreg` (comes with Python's standard library)
- `socket` (comes with Python's standard library)
- `uuid` (comes with Python's standard library)
- `ifaddr` (can be installed via pip)

## Installation

1. Install the required Python packages using pip:

   ```sh
   pip install ifaddr
   ```

2. Save the script as `monitor_registry.py`.

## Usage

Run the script using Python:

```sh
python monitor_registry.py
```

## Script Overview

### Functions

#### `get_mac_address()`

This function retrieves the MAC address of the current machine.

- **Returns:** A string representing the MAC address in the format `XX:XX:XX:XX:XX:XX`.

#### `get_ip_address()`

This function retrieves the current IPv4 address of the machine.

- **Returns:** A string representing the IP address if found, otherwise `None`.

### Main Function

#### `monitor_registry_access()`

This is the main function that performs the following tasks:

1. Retrieves and prints the current MAC and IP addresses.
2. Opens the registry key `SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces` to monitor network interfaces.
3. Iterates through each subkey to find IP addresses (`DhcpIPAddress` and `IPAddress`).
4. Compares the found IP addresses with the current IP address and prints any discrepancies.

### Example Output

```sh
Current MAC Address: XX:XX:XX:XX:XX:XX
Current IP Address: 192.168.1.100
Number of subkeys: 5
Accessing subkey: {GUID-1}
Found IP Address in subkey {GUID-1}: 192.168.1.101
Note: Different IP address found!
IP Address:  192.168.1.101

Accessing subkey: {GUID-2}
Found IP Address in subkey {GUID-2}: 192.168.1.102
Note: Different IP address found!
IP Address:  192.168.1.102

...

Summary of found IP addresses:
{GUID-1}: 192.168.1.101 (Different from current IP)
{GUID-2}: 192.168.1.102 (Different from current IP)
```

## Notes

- Ensure you have the necessary permissions to access the registry.
- The script currently only compares IPv4 addresses and assumes the first IP address found in a list (if any) is the relevant one.

## License

This script is released under the MIT License. See `LICENSE` file for details.

## Contribution

Feel free to contribute by submitting issues or pull requests to the repository.

---

This README provides a comprehensive overview of the script, its functions, usage instructions, and example output. It also includes installation steps and notes on permissions and IP address handling.

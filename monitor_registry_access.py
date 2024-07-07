import winreg
import socket
import uuid
import ifaddr

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
    return mac.upper()

def get_ip_address():
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        for ip in adapter.ips:
            if isinstance(ip.ip, str) and ip.is_IPv4:
                return ip.ip
    return None

def monitor_registry_access():
    mac_address = get_mac_address()
    ip_address = get_ip_address()

    print(f"Current MAC Address: {mac_address}")
    print(f"Current IP Address: {ip_address}")

    # Whitelist of known valid IP addresses
    known_valid_ips = {
    }

    # List to store found IP addresses
    found_ips = []

    # Open the registry key for monitoring
    reg_key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key_path)

    # Get the number of subkeys under the registry key
    num_subkeys = winreg.QueryInfoKey(reg_key)[0]

    print(f"Number of subkeys: {num_subkeys}")

    # Iterate through each subkey
    for i in range(num_subkeys):
        try:
            # Open the subkey
            subkey_name = winreg.EnumKey(reg_key, i)
            print(f"Accessing subkey: {subkey_name}")
            subkey = winreg.OpenKey(reg_key, subkey_name)

            # Try to get the IP address value
            ip = None
            try:
                ip = winreg.QueryValueEx(subkey, "DhcpIPAddress")[0]
            except FileNotFoundError:
                pass

            # Try to get the IP address value if not found
            if not ip:
                try:
                    ip = winreg.QueryValueEx(subkey, "IPAddress")[0]
                except FileNotFoundError:
                    pass

            # Handle cases where IP address is a list
            if isinstance(ip, list) and ip:
                ip = ip[0]

            if ip:
                found_ips.append((subkey_name, ip))
                print(f"Found IP Address in subkey {subkey_name}: {ip}")
                if ip != ip_address:
                    print("Note: Different IP address found!")
                    print("IP Address: ", ip)
                    print("")

            # Close the subkey
            winreg.CloseKey(subkey)
        except Exception as e:
            print("Error accessing registry subkey:", e)

    # Close the registry key
    winreg.CloseKey(reg_key)

    print("\nSummary of found IP addresses:")
    for subkey, ip in found_ips:
        discrepancy = " (Different from current IP)" if ip != ip_address else ""
        print(f"{subkey}: {ip}{discrepancy}")

# Run the intrusion detection
monitor_registry_access()

# Prevent terminal from closing immediately
input("Press Enter to exit...")

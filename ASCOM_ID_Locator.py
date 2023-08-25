import win32com.client

def get_ascom_device_id(device_type):
    """
    Retrieve ASCOM device ID of the given type using the Choose method.

    :param device_type: Type of the ASCOM device (e.g., 'Telescope', 'Camera', etc.)
    :return: Device ID or None if not selected
    """
    chooser = win32com.client.Dispatch("ASCOM.Utilities.Chooser")
    chooser.DeviceType = device_type
    return chooser.Choose(None)

if __name__ == '__main__':
    device_types = [
        'Telescope', 'Camera', 'Switch', 'Focuser',
        'Rotator', 'Dome', 'FilterWheel', 'SafetyMonitor',
        'ObservingConditions'
    ]

    for device_type in device_types:
        print(f"Select a device for type {device_type}:")
        device_id = get_ascom_device_id(device_type)
        
        if device_id:
            print(f"Selected Device ID for {device_type}: {device_id}")
        else:
            print(f"No device selected for {device_type}.")
        
        print('-' * 50)

from typing import Optional, Union, List

# z3scn.pyi - Type stubs for z3scn extension

# initialization
def init(com: int,
    device_id: Union[int, List[int]] = 0,
    stroke: int = 100,
    accel: int = 200,
    gain: int = 7,
    normal_speed: int = 7800,
    home_speed: int = 2000,
    move_mode: int = 0,
    go_home: int = 0,
    go_center: int = 0,
    diag: int = 0) -> bool:
    """
    Initialize the SCN device.

    Parameters:
        com (int): Required. COM port number (e.g., 4 for COM4)
        id (int or list[int]): Optional. Device ID Range [0-15]
        stroke (int): Optional. Stroke length (e.g., 100)
        accel (int): Optional. Acceleration value
        gain (int): Optional. Control gain
        normal_speed (int): Optional. Normal movement speed
        home_speed (int): Optional. Speed for homing
        move_mode (int): Optional. Movement mode
        go_home (int): Optional. If non-zero, go home on init
        go_center (int): Optional. If non-zero, go center after home
        diag (int): Optional. Dump actuator BANK settings
    Returns:
        bool: True if initialization succeeded, False otherwise
    """
    ...

# mandatory ending   
def terminate() -> None: 
    """Cleanly shuts down the SCN device and releases resources."""
    ...  

# device information
def get_device_info(selector: str, id: int = 0) -> Union[str, int]:
    """
    Retrieve information from the SCN device.

    Parameters:
        selector (str): The info field to query (e.g., 'version', 'name', 'ticks', 'type', 'vendor id', 'product id', 'serial number').
        id (int): Optional. Device ID (default is 0).

    Returns:
        Union[str, int]:: A string or int containing the requested information, -4 in case of wrong selector.
    """

# device motion control
def go_home(id: int = 0) -> bool:
    """
    Move the actuator to its home position.

    Parameters:
        id (int): Optional. Device ID (default is 0).

    Returns:
        bool: True if the command was successfully issued, False otherwise.
    """

def go_center(id: int = 0) -> bool:
    """
    Move the actuator to the center of its stroke range.

    Parameters:
        id (int): Optional. Device ID (default is 0).

    Returns:
        bool: True if the command was successfully issued, False otherwise.
    """

def go_position(pos: float, id: int = 0) -> bool:
    """
    Move the actuator to an absolute position (in mm). Submit command is optional.

    Parameters:
        pos (float): Target position in millimeters.
        id (int): Optional. Device ID (default is 0).

    Returns:
        bool: True if the command was successfully issued, False otherwise.
    """

def load_position(pos: float, id: int = 0) -> bool:
    """
    Load a target position without immediate execution.

    Parameters:
        pos (float): Target position in millimeters.
        id (int): Optional. Device ID (default is 0).

    Returns:
        bool: True if the position was successfully loaded, False otherwise.
    """

def clear_position(id: int = 0) -> None:
    """
    Clear the currently loaded position.

    Parameters:
        id (int): Optional. Device ID (default is 0).
    """

def check_scn(id: int = 0) -> bool:
    """
    Check if the alarm is set.

    Parameters:
        id (int): Optional. Device ID (default is 0).

    Returns:
        bool: True if the actuator is okay, False if the alarm is set.
    """

def submit_check(id: int = 0) -> None:
    """
    Submit the current pending commands including homing and check the actuator status.

    Parameters:
        id (int): Optional. Device ID (default is 0).
    """

def submit(id: int = 0) -> None:
    """
    Submit the pending motion command and return immediately.

    Parameters:
        id (int): Optional. Device ID (default is 0).
    """

"""
A silly little program that illustrates (literally!) the basic outline of a
computer memory.

This is not reliable, fast, or really much of anything other than a fun
little project. Enjoy!

author: isaac1000000
"""

import os
import turtle as t
from dotenv import load_dotenv
from utils import normalize, detection

load_dotenv('.env', override=True)

SHOW_TURTLE = False

# HIGHLY experimental. Don't change unless you've got some big ideas...
BLOCK_SIZE = (32, 16) # (width, height) in bytes
BLOCK_GAP = 4 # number of pen size units to leave between blocks in the grid
CELL_GAP = 1 # number of pen size units between cells in a block
BYTE_ORDER = 'little'

try:
    TURTLE_PEN_SIZE = int(os.getenv('TURTLE_PEN_SIZE'))
    TURTLE_SPEED = int(os.getenv('TURTLE_SPEED'))
    TURTLE_SCREENSIZE_X = int(os.getenv('TURTLE_SCREENSIZE_X'))
    TURTLE_SCREENSIZE_Y = int(os.getenv('TURTLE_SCREENSIZE_Y'))
    TURTLE_WINDOW_BUFFER = int(os.getenv('TURTLE_WINDOW_BUFFER'))

    turtle_origin = ((-TURTLE_SCREENSIZE_X+TURTLE_PEN_SIZE)//2+TURTLE_WINDOW_BUFFER, (TURTLE_SCREENSIZE_Y-TURTLE_PEN_SIZE)//2-TURTLE_WINDOW_BUFFER)

    GRID_WIDTH = int(os.getenv('GRID_WIDTH'))
    GRID_HEIGHT = int(os.getenv('GRID_HEIGHT'))
except Exception:
    print("Error loading environment variables. Ensure your .env file is properly configured")
    exit()

normalizer = normalize.Normalizer(turtle_origin, TURTLE_PEN_SIZE, BLOCK_SIZE, GRID_WIDTH, GRID_HEIGHT, BLOCK_GAP, CELL_GAP, BYTE_ORDER)
detector = detection.Detector(t)

def read_bytes(address:bytes, num_bytes: int) -> bytes:
    """
    Reads a specific number of bytes at a given address

    Args:
        address (bytes): the address to begin reading
        num_bytes (int): the number of bytes to read
    Returns:
        bytes: the bytes found at the given address
    """

    normalized_address = normalizer.address_to_pos(address)
    t.setpos(normalized_address)
    t.seth(0)

    result = b''
    for cell in range(num_bytes):
        if (int.from_bytes(address, BYTE_ORDER) + cell) % BLOCK_SIZE[0] == 0:
            normalized_address = normalizer.address_to_pos(address)
            t.setpos(normalized_address)
            t.seth(0)
        result += read_byte()
        _l()
        _f(2)
        t.seth(0)

    return result



def read_byte() -> bytes:
    """
    Reads a byte at the current address in memory

    Returns:
        bytes: the byte found at the current address.
    """

    byte = _read_nibble()
    byte = byte << 4
    _r()
    _f()
    _r()
    byte += _read_nibble()

    return byte.to_bytes(1, BYTE_ORDER)


def _read_nibble() -> int:
    """
    An internal function that returns an int from the current nibble

    Returns:
        int: the int found at the current nibble
    """

    result = 0
    for i in range(3):
        result = result << 1
        if detector.marked():
            result += 1
        _f()
    result = result << 1
    if detector.marked():
        result += 1
    return result

def write_bytes(address: bytes, data: bytes) -> bool:
    """
    Writes bytes at a specific address in the memory.

    WARNING: This is not secure! It can very easily overwrite
    old memory.
    
    Args:
        address (bytes): the address to write the bytes at
        data (bytes): the byte-format data to be written

    Returns:
        bool: True if write is successful
    """

    normalized_address = normalizer.address_to_pos(address)
    t.setpos(normalized_address)
    t.seth(0)
    
    for cell, byte in enumerate(data):
        if (int.from_bytes(address, BYTE_ORDER) + cell) % BLOCK_SIZE[0] == 0:
            normalized_address = normalizer.address_to_pos(address)
            t.setpos(normalized_address)
            t.seth(0)
        write_byte(byte.to_bytes(1, BYTE_ORDER))
        _l()
        _f(2)
        _l()

def write_byte(data: bytes) -> bool:
    """
    Writes a byte at the current address in memory

    Args:
        data (bytes): the byte to write at address.

    Returns:
        bool: True if write is successful, otherwise False.
    """
    assert isinstance(data, bytes), "Invalid operation: attempt to write non-bytes object"
    assert len(data) == 1, "Invalid operation: attempt to write more or less than one byte"

    bit_array = [int.from_bytes(data, BYTE_ORDER) & 2**i != 0 for i in range(7, -1, -1)] # endian-ness does not matter here b/c one byte

    try:
        _write_nibble_at_current(bit_array[:4])
    except Exception:
        return False
    
    # Move down a row to continue writing the byte
    _r()
    _f()
    _r()

    try:
        _write_nibble_at_current(bit_array[4:])
    except Exception:
        return False

    return True


def _write_nibble_at_current(nib: list[bool]) -> None:
    """
    An internal function for writing 4 bits' worth of information

    Args:
        nib (list[bool]): A length-4 list of boolean values
    """

    assert len(nib) == 4, "Invalid operation: attempt to write nibble of improper length"

    # Only first 3 need moves after them, so split the nibble to save a step
    for bit_value in nib[:3]:
        assert isinstance(bit_value, bool), "Invalid operation: attempt to write non-bool elememt to nibble"
        if bit_value:
            _m()
        else:
            _u()
        _f()
    if nib[3]:
        _m()

def _r(degrees: float=90) -> None:
    """
    An internal shorthand function that turns turtle to the right, defaults to 90 degrees

    Args:
        degrees(float)=90: The degrees to turn turtle
    """
    t.rt(degrees)

def _l(degrees: float=90) -> None:
    """
    An internal shorthand function that turns turtle to the left, defaults to 90 degrees

    Args:
        degrees(float)=90: The degrees to turn turtle
    """
    t.lt(degrees)

def _f(distance: float=1) -> None:
    """
    An internal shorthand function that moves turtle forward, defaults to 1 square

    Args:
        distance(float): The distance to move turtle, defaults to TURTLE_PEN_SIZE
    """
    t.fd(distance * TURTLE_PEN_SIZE)

def _b(distance: float=1) -> None:
    """
    An internal shorthand function that moves turtle backwards, defaults to 1 square

    Args:
        distance(float): The distance to move turtle, defaults to TURTLE_PEN_SIZE
    """
    t.bk(distance * TURTLE_PEN_SIZE)

def _m() -> None:
    """
    An internal shorthand function to mark the current space with turtle
    """
    t.dot(TURTLE_PEN_SIZE)

def _u() -> None:
    """
    An internal shorthand function to unmark the current space with turtle
    """
    t.dot(TURTLE_PEN_SIZE, 'white')

def _reset_turtle() -> None:
    """
    An internal function that resets turtle to the origin
    """
    t.setpos(turtle_origin)
    t.seth(0)

def initialize():

    screen = t.Screen()
    screen.setup(width=TURTLE_SCREENSIZE_X, height=TURTLE_SCREENSIZE_Y)
    if not SHOW_TURTLE:
        screen.tracer(0)

    t.pensize(TURTLE_PEN_SIZE)
    t.speed(TURTLE_SPEED)
    t.pu()
    t.setposition(turtle_origin)

if __name__ == "__main__":
    initialize()

    write_bytes(b'\x00', b'\x3f\xaa')
    print(read_bytes(b'\x00', 2))

    input()

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

load_dotenv('.env', override=True)

try:
    TURTLE_PEN_SIZE = int(os.getenv('TURTLE_PEN_SIZE'))
    TURTLE_SPEED = int(os.getenv('TURTLE_SPEED'))
    TURTLE_SCREENSIZE_X = int(os.getenv('TURTLE_SCREENSIZE_X'))
    TURTLE_SCREENSIZE_Y = int(os.getenv('TURTLE_SCREENSIZE_Y'))
    TURTLE_WINDOW_BUFFER = int(os.getenv('TURTLE_WINDOW_BUFFER'))
    turtle_origin = ((-TURTLE_SCREENSIZE_X+TURTLE_PEN_SIZE)//2+TURTLE_WINDOW_BUFFER, (TURTLE_SCREENSIZE_Y-TURTLE_PEN_SIZE)//2-TURTLE_WINDOW_BUFFER)
except Exception:
    print("Error loading environment variables. Ensure your .env file is properly configured")
    exit()


def initialize():

    screen = t.Screen()
    screen.setup(width=TURTLE_SCREENSIZE_X, height=TURTLE_SCREENSIZE_Y)

    t.pensize(TURTLE_PEN_SIZE)
    t.speed(TURTLE_SPEED)
    t.pu()
    t.setposition(*turtle_origin)

def write_byte(address: int, data: bytes) -> bool:
    """
    Writes a byte to a specific address in memory.

    Args:
        address (int): the address to write the byte to.
        data (bytes): the byte to write at address.

    Returns:
        bool: True if write is successful, otherwise False.
    """
    assert isinstance(data, bytes), "Invalid operation: attempt to write non-bytes object"
    assert len(data) == 1, "Invalid operation: attempt to write more or less than one byte"

    #TODO: move to memory address

    bit_array = [int.from_bytes(data, 'little') & 2**i != 0 for i in range(7, -1, -1)] # endian-ness does not matter here b/c one byte
    print(bit_array)

    _write_nibble_at_current(bit_array[:4])
    
    # Move down a row to continue writing the byte
    _r()
    _f()
    _r()

    _write_nibble_at_current(bit_array[4:])


def _write_nibble_at_current(nib: list[bool]) -> None:
    """
    An internal function for writing 4 bits' worth of information

    Args:
        nib(list[bool]): A length-4 list of boolean values
    """

    assert len(nib) == 4, "Invalid operation: attempt to write nibble of improper length"

    # Only first 3 need moves after them, so split the nibble to save a step
    for bit_value in nib[:3]:
        assert isinstance(bit_value, bool), "Invalid operation: attempt to write non-bool elememt to nibble"
        if bit_value:
            _m()
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

def _f(distance: float=TURTLE_PEN_SIZE) -> None:
    """
    An internal shorthand function that moves turtle forward, defaults to 1 square

    Args:
        distance(float): The distance to move turtle, defaults to TURTLE_PEN_SIZE
    """
    t.fd(distance)

def _b(distance: float=TURTLE_PEN_SIZE) -> None:
    """
    An internal shorthand function that moves turtle backwards, defaults to 1 square

    Args:
        distance(float): The distance to move turtle, defaults to TURTLE_PEN_SIZE
    """
    t.bk(distance)

def _m() -> None:
    """
    An internal shorthand function to mark the current space with turtle
    """
    t.dot(TURTLE_PEN_SIZE)


if __name__ == "__main__":
    initialize()
    write_byte(0, b'\xAA')
    t.hideturtle()


    input()

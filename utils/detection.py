class Detector:
    """
    A class with functions to help with certain things that
    turtle is not able to do alone, like color detection at
    a certain pixel
    """

    def __init__(self, turtle):
        self.turtle = turtle

    def marked(self) -> bool:
        """
        A function to see if a certain pixel is marked

        Args:
            x (int): the x coordinate of the pixel
            y (int): the y coordinate of the pixel
        Returns:
            bool: True if the pixel is marked
        """
        # tkinter canvas idiosyncracy
        x, y = self.turtle.pos()

        y = -y

        canvas = self.turtle.getcanvas()
        ids = canvas.find_overlapping(x, y, x, y)

        # Returns true if an object was found at this pixel - turtle is counted as an object
        if len(ids) > 1:
            return True
        return False



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
        x, y = self.turtle.pos()

        # tkinter canvas idiosyncracy
        y = -y

        canvas = self.turtle.getcanvas()
        ids = canvas.find_overlapping(x, y, x, y)

        # Returns true if an object was found at this pixel - turtle is counted as an object
        if self.turtle.Screen().tracer() and len(ids) > 1:
            index = ids[-2]
        elif not self.turtle.Screen().tracer() and len(ids) > 0: 
            index = ids[-1]
        else:
            return False
        
        color = canvas.itemcget(index, "fill")

        if color == 'black':
            return True
        
        return False


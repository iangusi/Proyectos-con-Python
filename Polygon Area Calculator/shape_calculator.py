class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return f'Rectangle(width={self.width}, height={self.height})'

    def set_width(self,width):
        self.width = width

    def set_height(self,height):
        self.height = height

    def get_area(self):
        return self.width*self.height

    def get_perimeter(self):
        return (self.width*2) + (self.height*2)

    def get_diagonal(self):
        return ((self.width**2) + (self.height**2))**.5

    def get_picture(self):
        figure = ''
        if self.width and self.height<= 50:
            for row in range(self.height):
                figure += '*'*self.width+'\n'
        return figure

    def get_amount_inside(self, square):
        num_width = self.width//square.width
        num_height = self.height//square.width
        return num_width*num_height

class Square(Rectangle):
    def __init__(self,side):
        self.width = side
        self.height = side

    def __str__(self):
        return f'Square(side={self.width})'

    def set_side(self,side):
        self.width = side
        self.height = side

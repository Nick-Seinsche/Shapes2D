'''
    Title: polyon.py
    Description: Creates Coordinates for Polygons
    Author: Nick Seinsche
    Libaries:
        Standard Library
        Math
'''

# imports
import math

# CONSTANTS
PI = math.pi
sin = lambda x: math.sin(x)
cos = lambda x: math.cos(x)


def dist(p1: list, p2: list) -> float:
    '''
    Description:
        Returns the distance of two points
    Args:
        p1 (list) - n-dimensional coordinate
        p2 (list) - n-dimensional coordinate
    Returns:
        distance as a float
    Examples:
        >>> dist([1, 2], [3, 4])
        2.8284271247461903
        >>> dist([1, 2, 3, 8], [3, 4, 16, -3])
        17.26267650163207
    '''
    dtsq = [(p2[i] - p1[i])**2 for i in range(0, min(len(p1), len(p2)))]
    return math.sqrt(sum(dtsq))


def circle(x: float, y: float, radius: float):
    '''
    Description:
        calculates the coordinates of the outer points a circle bases on
        the angle (radiant)
    Args:
        x - the X-coordinate of the circle center
        y - the Y-coordinate of the circle center
        radius - the radius of the circle
    Returns:
        a lambda function that takes in the angle in radiants and returns
        a (x,y) tuple containing the coordinates of the circles outer point
        at the given angle
    Examples:
        >>> (circle(0,0,1))(0)
        (1.0, 0.0)
        >>> (circle(0,0,1))(pi)
        (-1.0, 1.2246467991473532e-16)
    '''
    return lambda a: (x + math.cos(a) * radius, y + math.sin(a) * radius)


def sphere(x: float, y: float, z: float, radius: float):
    '''
    Description:
        calculates the coordinates of the outer points a circle bases on
        the angle (radiant)
    Args:
        x - the X-coordinate of the spheres center
        y - the Y-coordinate of the spheres center
        z - the Z-coordinate of the spheres center
        radius - the radius of the sphere
    Returns:
        a lambda function that takes in the angle in radiants and returns
        a (a,b,c) tuple containing the coordinates of the circles outer point
        at the given angle
    Examples:
        >>> x(PI/4,PI/4)
        (0.5000000000000001, 0.5000000000000001, 0.7071067811865476)
        >>> x(PI/4,PI/3)
        (0.6123724356957946, 0.6123724356957946, 0.5000000000000001)
    '''
    return lambda s,t: (x + radius * cos(s) * sin(t),
                        y + radius * sin(s) * sin(t),
                        z + radius * cos(t))


def translate(origin: list, p3: list, p2: list) -> None:
    pass


class Shape:
    '''
    Description:
        Generic Class for Polygons
    Args:
        x - x-coordinate of shape
        y - y-coordinate of shape
        points - list of coordinate of points of the shape
        cirlce - instance of the circle function
    Methods:
        get() - returns the list of points
        __next__
    '''
    def __init__(self, x: float, y: float, size: float) -> None:
        self.x = x
        self.y = y
        self.points = []
        self.circle = circle(x, y, size)

    def update(self):
        print('no update funtion implemented')

    def rotate(self, angle: float, update=True) -> None:
        if not angle:
            if update:
                self.update()
            return
        self.rotAngle -= angle
        if update:
            self.update()

    def move(self, dx: float, dy: float, update=True) -> None:
        if not dx and not dy:
            if update:
                self.update()
            return
        for i in range(0, len(self.points)):
            self.points[i] = (self.points[i][0] + dx, self.points[i][1] + dy)
        self.x += dx
        self.y += dy
        if update:
            self.update()

    def get(self) -> list:
        return self.points

    def __iter__(self):
        return self

    def __next__(self) -> float:
        if self.next is None:
            self.next = 0
        self.next += 1
        return self.points[self.next-1]


class isoTriangle(Shape):
    '''
    Description:
        Class for an isosceles triangle. Calculates the three points of the
        triangle based on location, angle, size and rotation
    Args:
        x - x-coordinate of the top point of the triangle
        y - y-coordinate of the top point of the triangle
        innerAngle - the angle at the top point of the triangle (radiants)
        rotAngle - the angle the triangle is rotated (radiants)
    Methods:
        get() - inherited from Polygon
    Examples:
        >>> isoTriangle(0,0,1,3,0).get()
        (0, 0),
        (-1.4382766158126088, -2.6327476856711183),
        (1.4382766158126092, -2.632747685671118)
    '''
    def __init__(self, x: float, y: float, innerAngle: float,
                 side_length: float, rotAngle: float) -> None:
        super().__init__(x, y, side_length)
        self.points.append((x, y))
        self.innerAngle = innerAngle
        self.side_length = side_length
        self.rotAngle = rotAngle
        self.points.append(self.circle(rotAngle + PI/2 - innerAngle/2))
        self.points.append(self.circle(rotAngle + PI/2 + innerAngle/2))

    def update(self) -> None:
        self.circle = circle(self.x, self.y, self.side_length)
        self.points[0] = (self.x, self.y)
        self.points[1] = self.circle(
            self.rotAngle + PI/2 - self.innerAngle/2)
        self.points[2] = self.circle(
            self.rotAngle + PI/2 + self.innerAngle/2)


class regPolygon(Shape):
    '''
    Description:
        Class for a regular polyon (a polygon where all sides have the same
        length and all inner angles are the same). Calculates the n points
        of the polygon based on location and rotation angle
    Args:
        x - x-coordinate of the center of the polygon
        y - y-coordinate of the center of the polygon
        n - number of sides the polyon should have
        rotAngle - the angle the polygon should be rotated by
    Methods:
        get() returns a list of 2-tuples of coordinates of the points
        update() updates the points
        rotate(float) rotates the polygon clockwiese for positive values
        move(float, float) adds the point to the position
    Examples:
        >>> regPolygon(0,0,3,1,0).get()
        [(-0.4999999999999992, 0.8660254037844392),
        (-0.5000000000000013, -0.8660254037844378),
        (1.0, -4.898587196589413e-16)]
    '''
    def __init__(self, x: float, y: float, size: float, rotAngle: float,
                 n: int) -> None:
        super().__init__(x, y, size)
        self.n = n
        self.size = size
        self.rotAngle = rotAngle
        for i in range(0, n):
            self.points.append(self.circle(
                rotAngle - PI/2 + (i / n) * 2 * PI)
            )

    def update(self) -> None:
        self.circle = circle(self.x, self.y, self.size)
        for i in range(0, self.n):
            self.points[i] = self.circle(
                self.rotAngle - PI/2 + (i / self.n) * 2 * PI
            )


class regStar(Shape):
    '''
    Description:
        Calculates the points for a star with equal side length
    Args:
        x - x-coordinate of the stars center
        y - y-coordinate of the stars center
        size - the size of the body of the star
        rotAngle - the rotational angle (radiants)
        n - number of sides the star should have
        ratio - the ratio between the body and the legs
    Methods:
        get() returns a list of 2-tuples of coordinates of the points
        update() updates the points
        rotate(float) rotates the polygon clockwiese for positive values
        move(float, float) adds the point to the position
    Examples:
        >>> regStar(0, 0, 25, PI, 3, 1.8).get()
        [(2.7554552980815448e-15, 45.0), (2.7554552980815448e-15, 45.0),
        (-38.97114317029975, -22.499999999999986), (-38.97114317029975,
        -22.499999999999986), (38.971143170299726, -22.50000000000002),
        (38.971143170299726, -22.50000000000002)]
    '''
    def __init__(self, x: float, y: float, size: float, rotAngle: float,
                 n: int, ratio: float) -> None:
        super().__init__(x, y, size)
        self.x_new = self.x
        self.y_new = self.y
        self.size = size
        self.rotAngle = rotAngle
        self.n = n
        self.ratio = ratio
        self.poly = regPolygon(x, y, size, rotAngle, n)
        self.big_poly = regPolygon(x, y, size * ratio, rotAngle - PI / n, n)
        for i in range(0, 2 * len(self.poly.points)):
            if i % 2 == 0:
                self.points.append(self.big_poly.points[int(i / 2)])
            elif i % 2 == 1:
                self.points.append(self.big_poly.points[int((i - 1) / 2)])

    def update(self) -> None:
        self.points = []
        self.poly = regPolygon(self.x, self.y, self.size,
                               self.rotAngle - PI/self.n, self.n)
        self.big_poly = regPolygon(self.x, self.y, self.size*self.ratio,
                                   self.rotAngle, self.n)
        for i in range(0, 2 * len(self.poly.points)):
            if i % 2 == 0:
                self.points.append(self.poly.points[int(i / 2)])
            elif i % 2 == 1:
                self.points.append(self.big_poly.points[int((i - 1) / 2)])


if __name__ == "__main__":
    # print(regStar(0, 0, 25, PI, 3, 1.8).get())
    # print(dist([1, 2, 3, 8], [3, 4, 16, -3]))
    sp = sphere(0,0,0,1)
    print(sp(PI/2,0))
    pass

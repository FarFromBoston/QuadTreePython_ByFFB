
"""
# THIS PROGRAM COMPARES A QUADTREE SEARCH ALGORITHM AGAINST A LINEAR SEARCH ALGORITHM
# Please read the section READ ME below to get started

READ ME:
    1) Make sure that you have the prequiste packages installed into your current
       python version. Including:
           time
           tkinter   - MAY need to install
           random
           collections.defaultdict

Return to Main python file MAIN_and_TESTER
"""


from collections import defaultdict
import random
import tkinter
import time




# Setup Tkinter
root = tkinter.Tk()
root.title("QUADTREE VISUALIZER")
root.geometry("400x400")
canvas = tkinter.Canvas()

# List of all point objects
list_of_points = []
# List of those points that have the same directory
list_of_points_nearby = []


"""
Point objects that hold their directory to be quickly queried for.
Each point is added to the global list above

Params:
    (point_ID)             int                        - rectangle perimter object
    (point)                tuple(x int, y int)        - Max num of points per a quadrant
    (Point_directory)      List(Str)                  - Str list of directions to point as an index
                                                         i.e. for some point it may have an index of
                                                        NE,SE,NE
                                                        Other points with the same index are in the
                                                        same quadrant
"""
class Point(object):
    
    def __init__(self, point_ID, point, Point_directory=[]):
        self._point_ID = point_ID
        self._point = point
        self._Point_directory = Point_directory

        list_of_points.append(self)
        
    def getID(self):
        return self._point_ID
    def getPoint(self):
        return self._point
    def getDirectory(self):
        return self._Point_directory
    def updateDirectory(self, new_directory):
        self._Point_directory.append(new_directory)
    def __str__(self):
        pointID = self._point_ID
        return f"point=('{pointID}')"
    def __repr__(self):
        pointID = self._point_ID
        return f"point=('{pointID}')"




"""
Create a bounding box for to check if points are within it

Params:
    Self-Explanatory
"""
class Rectangle(object):
    def __init__(self, xTopLeft,yTopLeft,xBotRight,yBotRight):
        self._x1 = xTopLeft
        self._y1 = yTopLeft
        self._x2 = xBotRight
        self._y2 = yBotRight
        
    def getX1(self):
        return self._x1
    def getY1(self):
        return self._y1
    def getX2(self):
        return self._x2
    def getY2(self):
        return self._y2

    def contains(self, point):
        # See if point is within this rectangle, return True if it is
        if (self._x1 <= point[0] <= self._x2 and \
            self._y1 <= point[1] <= self._y2):
            return True
        else:
            return False

    """
    Compare rectangle search window with a quadtree quadrant rectangle
    as an index to find intersection

    Params:
        searchWindow (rectangle) obj: rectangle to compare against
        current rectangle
    """
    def Notintersects(self, searchWindow):
        return (searchWindow.getX1() > self.getX2() or \
                searchWindow.getY1() > self.getY2() or \
                searchWindow.getX2() < self.getX1() or \
                searchWindow.getY2() < self.getY1())
        
"""
Create Quadtree with children quadrants to each hold points

Params:
    (Rectangle)   obj        - rectangle perimter object
    (bucket_size) int        - Max num of points per a quadrant
    (Points)      List(Obj)  - List of point objects
    (divided)     Bool       - Recorder if a quadrant has been divided
"""
class QuadTree(object):
    def __init__(self, Rectangle, bucket_size, directory):
        self._Rectangle = Rectangle
        self._bucket_size = bucket_size
        self._Points = []
        self._divided = False
        self._directory = directory

    def getListOfPoints(self):
        return self._Points

    # Split quadtree into 4 smaller quadtrees   NW,NE,SW,SE
    # Each new rectangle partition of the quadtree will have its own new top left and bottom right
    def breakRoot(self):
        x1 = self._Rectangle.getX1()
        y1 = self._Rectangle.getY1()
        x2 = self._Rectangle.getX2()
        y2 = self._Rectangle.getY2()

        # sub quadrant dimensions
        NW = Rectangle(x1,            y1,             (x1 + x2)/2,           (y1 + y2)/2)
        NE = Rectangle((x1 + x2)/2,   y1,             x2,             (y1 + y2)/2)
        SW = Rectangle(x1,            (y1 + y2)/2,    (x1 + x2)/2,           y2)
        SE = Rectangle((x1 + x2)/2,   (y1 + y2)/2,    x2,              y2)

        # update boundary with the new location
        self._northeast = QuadTree(NE,self._bucket_size, f"{self._directory} NE");
        self._northwest = QuadTree(NW,self._bucket_size, f"{self._directory} NW");
        self._southeast = QuadTree(SE,self._bucket_size, f"{self._directory} SE");
        self._southwest = QuadTree(SW,self._bucket_size, f"{self._directory} SW");

        self._divided = True
        

    # insert point into proper quadrant recursively
    def insert(self, point, pointObj,updatedDirectory):
        # Check if point is inside the boundary, if not stop
        if (self._Rectangle.contains(point) == False):
            return False

        # check if bucket size not overflowing
        if len(self._Points) < self._bucket_size and self._divided == False:
            self._Points.append(pointObj)
        else:
            # split current quadrant into smaller quandrants
            if (self._divided == False):
                for points in self._Points:
                    points.updateDirectory(updatedDirectory)
                list_of_points_nearby.append(self._Points)
                self.breakRoot()
                
            # recursively add point if in quadrant/create new quadrant if overflowing
            self._northeast.insert(point, pointObj,"NE")
            self._northwest.insert(point, pointObj,"NW")
            self._southeast.insert(point, pointObj,"SE")
            self._southwest.insert(point, pointObj,"SW")

            # remove all current points and put into children
            for a_point in self._Points:
                self._northeast.insert(a_point.getPoint(), a_point,"NE")
                self._northwest.insert(a_point.getPoint(), a_point,"NW")
                self._southeast.insert(a_point.getPoint(), a_point,"SE")
                self._southwest.insert(a_point.getPoint(), a_point,"SW")
            self._Points = []

    # add rectangles and points to canvas
    def show(self):
        canvas.create_rectangle(self._Rectangle.getX1(), self._Rectangle.getY1(), \
                                self._Rectangle.getX2(), self._Rectangle.getY2())
        if(self._divided == True):
            self._northeast.show()
            self._northwest.show()
            self._southeast.show()
            self._southwest.show()
        for points in self._Points:
            point = points.getPoint()
            canvas.create_oval(point[0], point[1], \
                                 (point[0] + 3), (point[1] + 3))

    # Query Window to search points from a rectangle search window, using the quadtree indices
    def query_Quadtree_search_box(self, SrchWindRect, pts_found):
        if pts_found == 0:
            pts_found = []
        print(self)
            
        # Here we use the rectangle/quadrant of the quadtree as the index to check against
        # the search window (SrchWindRect)
        if (self._Rectangle.Notintersects(SrchWindRect)):
            return
        else:
            for p in self._Points:
                print(p)
                if SrchWindRect.contains(p.getPoint()):
                    pts_found.append(p)
            if self._divided == True:
                self._northwest.query_Quadtree_search_box(SrchWindRect,pts_found)
                self._northeast.query_Quadtree_search_box(SrchWindRect,pts_found)
                self._southeast.query_Quadtree_search_box(SrchWindRect,pts_found)
                self._southwest.query_Quadtree_search_box(SrchWindRect,pts_found)
        return pts_found

    
    # Query Window to search points from a rectangle search window, not using the quadtree indices
    def query_Linear_search_box(self, SrchWindRect):
        points_found = []

        for p in list_of_points:
            print(p)
            if SrchWindRect.contains(p.getPoint()):
                points_found.append(p)
        return points_found

    def __str__(self):
        direct = self._directory
        divided = self._divided
        return f"direct and divided=('{direct} | {divided}')"
    def __repr__(self):
        divided = self._divided
        return f"direct and divided=('{direct} | {divided}')"


    
"""
Creates Randomly distributed data points
"""
def CreateRandomData(num_points, pts_minXY, pts_maxXY):
    counter = 1
    while counter != num_points:
        x = random.randint(pts_minXY, pts_maxXY)
        y = random.randint(pts_minXY, pts_maxXY)
        # points added to global list within Point class
        a_point = Point(counter, (x,y))
        counter += 1

"""
Creates Normally distributed data points
"""
def CreateNormalData(num_points, pts_minXY, pts_maxXY, mean, stdev):
    counter = 1
    while counter != num_points:
        # get X
        X = random.gauss(mean, stdev)
        # get Y
        Y = random.gauss(mean, stdev)
        if X >= pts_minXY and X < pts_maxXY \
           and Y >= pts_minXY and Y < pts_maxXY:
            # points added to global list within Point class
            a_point = Point(counter, (X,Y))
            counter += 1


"""
Create a rectangle search window that will find all points within it'
Uses the rectangle quadrants to determine intersection
rather than a manual point by point comparison

Params:
    (QuadTree_Root)   obj        - The entire quadtree
"""
def searchWindow(QuadTree_Root, search_type, srchWin_pts_minXY, srchWin_pts_maxXY):
    # Query window
    canvas.create_rectangle(srchWin_pts_minXY, srchWin_pts_minXY, srchWin_pts_maxXY, srchWin_pts_maxXY, outline='red')
    search_window_rect = Rectangle(srchWin_pts_minXY, srchWin_pts_minXY, srchWin_pts_maxXY, srchWin_pts_maxXY)

    # Search with method linear or quadtree
    if search_type == "Linear" or search_type == "L":
        points_found = QuadTree_Root.query_Linear_search_box(search_window_rect)
        print("LINEAR SEARCH POINTS ", points_found)
    else:
        points_found = QuadTree_Root.query_Quadtree_search_box(search_window_rect, 0)
        print("QUADTREE SEARCH POINTS ", points_found)

    return points_found
    
"""
Turns all search window points found to red in visual window
"""
def MakePointsFoundRed(points_found):
    for points in points_found:
        point = points.getPoint()
        canvas.create_oval(point[0], point[1], (point[0] + 3), (point[1] + 3), outline='red')

"""
Show the quadtree visually WITH the search window if function above was used
"""
def showCanvas():
    # SHOW THE QUADTREE CANVAS
    canvas['bg'] = 'green'
    canvas.pack()
    root.mainloop()







"""
-------------------------------------------------------------------------------------------------------
"""
def main(dataT, num_points, bucket_size, pts_minXY, pts_maxXY, srchWin_pts_minXY, srchWin_pts_maxXY):
    # CREATE ROOT QUADRANT
    rectangle = Rectangle(pts_minXY,pts_minXY,pts_maxXY,pts_maxXY)
    QuadTree_Root = QuadTree(rectangle, bucket_size, "Root")

    # ---------------DATA----------------
    
    if dataT == "R":
        # Use *ONE* of the data distribution methods on the lines below,
        # comment out the other
        
        # RANDOMLY DISTRIBUTED DATA POINTS
        CreateRandomData(num_points, pts_minXY, pts_maxXY)
    else:
        # NORMALLY DISTRIBUTED DATA POINTS
        # change mean and stdv accordingly
        mean = 100 #100
        stdev = 75/3  #75/3

        CreateNormalData(num_points, pts_minXY, pts_maxXY, mean, stdev)
    # ----------------DATA---------------
    

    # ADD POINTS TO QUADTREE AND START DIVIDING
    for points in list_of_points:
        QuadTree_Root.insert(points.getPoint(), points, "Root")


    # ADD ELEMENTS (rectangle quadrants and points) TO CANVAS
    QuadTree_Root.show()

    # START QUERY TIMER
    start_time = time.time()
    
    # ---------------Quadtree Search vs Linear Search----------------
    # START QUERY TIMER
    start_time = time.time()
    search_type = "Q"
    points_found = searchWindow(QuadTree_Root, search_type, srchWin_pts_minXY, srchWin_pts_maxXY)
    Quad_search_Time = time.time() - start_time
    # SHOW QUERY CALCULATION TIME
    print("--- %s seconds ---" % (time.time() - start_time))


    # START QUERY TIMER
    start_time = time.time()
    search_type = "L"
    points_found = searchWindow(QuadTree_Root, search_type, srchWin_pts_minXY, srchWin_pts_maxXY)
    Linear_Search_Time = time.time() - start_time
    # SHOW QUERY CALCULATION TIME
    print("--- %s seconds ---" % (time.time() - start_time))

    # All times
    print()
    print("QUADTREE search time =")
    print(f"--- {Quad_search_Time} seconds ---")
    print("LINEAR search time =")
    print(f"--- {Linear_Search_Time} seconds ---")

    # ---------------------------------------------------------------
    # show tkinter quadtree
    MakePointsFoundRed(points_found)
    showCanvas()
    

def MainInputs():
    defaults = input("Would you like to set the program paramters or run as default? "  \
                     "default uses pre-built values (enter either     D or S    for Default and SetNew): ")
    if defaults == "S" or defaults == "s":
        dataT = input("would you like random or normal data? pleasure enter either: R or N ")
        num_points = input("Please input your prescribed number of data points as a single number (i.e. 30): ")
        bucket_size = input("Please input quadtree bucket size as a single number (i.e. 5): ")
        pts_minXY = input("Quadtree root top left X and Y as a single number (i.e. 0   for 0,0): ")
        pts_maxXY = input("Quadtree root bottom right X and Y as a single number (i.e. 200   for 200,200): ")

        print("\n")
        print("We must now determine the area of points to search for intersection, or the search query window")
        print()
        srchWin_pts_minXY = input("Search window top left X and Y as a single number (i.e. 0   for 0,0): ")
        srchWin_pts_maxXY = input("Search window bottom right X and Y as a single number (i.e. 200   for 200,200): ")
        

        num_points = int(num_points)
        bucket_size = int(bucket_size)
        pts_minXY = int(pts_minXY)
        pts_maxXY = int(pts_maxXY)
        srchWin_pts_minXY = int(srchWin_pts_minXY)
        srchWin_pts_maxXY = int(srchWin_pts_maxXY)
        
    else:
        dataT = "N"
        num_points = 30
        bucket_size = 5
        pts_minXY = 0
        pts_maxXY = 200
        srchWin_pts_minXY = 60
        srchWin_pts_maxXY = 95
    
    main(dataT, num_points, bucket_size, pts_minXY, pts_maxXY, srchWin_pts_minXY, srchWin_pts_maxXY)


#MainInputs()







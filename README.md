# QuadTree_Python38


- To run the program

-- Run Main_and_Tester file only.

-- No packages/libraries must be installed.

-- Program created in python3.8, but any version 3.8+ should work.



--------------------------------------------------------------------------------------------------
- What the program does

-- This is a Quadtree algorithm (see wikipedia) in which spatial data points (x,y) are created (as many as you want) and then grouped into buckets and visualized. So imagine a bunch of data points. A sqaure is drawn around them. As new data points are entered the square holding all the points will eventually reach capacity. When capacity of the square is reached the square will be divided into 4 sub squares with the same capacity as the parent. Now each child square will be checked until its capcity is full then it will subdivide and so on. 

-- Then we perform a query window (just a square which covers an area and any points within this square are MARKED and returned) search and return all those points. This program COMPARES a linear search and the quadtree search. A linear search must compare the search window's area against EVERY single point. Whilst our QUADTREE search checks the buckets/quadrants as indices; so essentially the job is 1/4 as long to compute (assuming even distribution of points and the search widnow doesn't cover every damn square).

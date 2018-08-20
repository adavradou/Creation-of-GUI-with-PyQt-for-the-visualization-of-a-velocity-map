# Vectormap
Creation of GUI with PyQt for the visualization of a velocity map

-----------------------------------------------------------------------------------------------------------
This GUI was created in the contexts of a course for the visualization of a fluid’s flow velocity.

A graphical interface using PyQt is created in order to edit the resulted vectormap (zoom in, change color, etc) using matplotlib.

The code needs a .txt file of 5 columns: x y vx vy v.
The x and y are the coordinates and and vx, vy are the components of velocity v. 
You have first to select the .txt file and the click on “Plot” in order for the vectormap to be visualized.

The .txt file I use contains experimental results I obtained during my diploma thesis in collaboration with the company Fasmatech Science and Technology SA.

This was my first experience with Python, Qt and Object-Oriented Programming.
I was trying to experiment with as many features as possible and that is the reason I 
implemented a video splashscreen, the “help” tab, etc. 

	# Annabelle Strong
	# 10/25/2017
	# Upon my honor, I have neither given nor recieved unauthirized aid.

################################### SETUP
# import the libraries you'll need
import tkinter
from tkinter import *
from tkinter import StringVar

import random

# create a new Tkinter window
window = Tk()

# variables we will use throughout the program
WIDTH = 800 # width and height of our picture in pixels
HEIGHT = 800

# create a canvas, and place it in the window
canvas = Canvas(window, width = WIDTH, height = HEIGHT, bg = "#FFFFFF")

# set up the canvas so it can hold a picture
img = PhotoImage(width = WIDTH, height = HEIGHT)
canvas.create_image((0, 0), image = img, state = "normal", anchor = tkinter.NW)

# zoom defaults
xmin = -2
xmax = 2
ymin = -2
ymax = 2

# zoom variables
xmin_var = StringVar()
xmax_var = StringVar()
ymin_var = StringVar()
ymax_var = StringVar()

# set up text-box-entry for zoom variables
xmin_in = Entry(window, text="X-Min", textvariable=xmin_var)
xmax_in = Entry(window, text="X-Max", textvariable=xmax_var)
ymin_in = Entry(window, text="Y-Min", textvariable=ymin_var)
ymax_in = Entry(window, text="Y-Max", textvariable=ymax_var)

# initialize sliders for each rgb color
rs = Scale(window, from_=0, to=255, length=600, tickinterval=25, orient=HORIZONTAL)
gs = Scale(window, from_=0, to=255, length=600, tickinterval=25, orient=HORIZONTAL)
bs = Scale(window, from_=0, to=255, length=600, tickinterval=25, orient=HORIZONTAL)

# set default slider values
rs.set(255)
gs.set(255)
bs.set(255)

# set up booleans for whether or not a color is dependant on the number of escapes
rmv = BooleanVar()
gmv = BooleanVar()
bmv = BooleanVar()

# set default bool values
rmv.set(True)
gmv.set(True)
bmv.set(True)

# initialize checkboxes to control the booleans
m1 = Checkbutton(window, text="Make red value M-dependent?", variable=rmv)
m2 = Checkbutton(window, text="Make green value M-dependent?", variable=gmv)
m3 = Checkbutton(window, text="Make blue value M-dependent?", variable=bmv)

# "points of interest" arrays; will be used save a and d values of points that have an escape value of 100+ (aka arent's boring background sections)
a_list = []
d_list = []

maxIt = 255 # max iterations of mandelbrot function; corresponds to color

# recursive mandelbrot function gives us the number of iterations to escape
def mandelbrot(z, c, count):

	z = (z*z) + c
	count = count + 1

	# if we escape or we hit the max number of iterations
	# stop executing and return the number of iterations
	if count >= maxIt or abs(z) >= 2:
		return count

	# otherwise, since we didn't escape or hit the max iterations,
	# calculate a new z again (call mandelbrot function again)
	else:
		return mandelbrot(z, c, count)

def print_fractal(r, g, b):
	# "make color m-dependant?" bools
	global rmv 
	global gmv
	global bmv

	# read bool settings
	rm = rmv.get()
	gm = gmv.get()
	bm = bmv.get()

	for row in range(HEIGHT):
		for col in range(WIDTH):
	    	# calculate C for each pixel
			a = (((xmax-xmin)/WIDTH) * col) + xmin
			d = (((ymax-ymin)/HEIGHT) * row) + ymin
			c = complex(a, d)

	        # set z to 0
			z = complex(0, 0)

	        # execute the mandelbrot calculation
			m = mandelbrot(z, c, 0)

			# add points to "points of interest" lists
			if m >= 100:
				a_list.append(a)
				d_list.append(d)

			# calculate colors based on m-value and slider, or just slider
			if rm == True:
				rv = int((m/255)*r)
			else:
				rv = r

			if gm == True:
				gv = int((m/255)*g)
			else:
				gv = g

			if bm == True:
				bv = int((m/255)*b)
			else:
				bv = b

	        # use the mandelbrot result to create a color
			red = hex(rv)[2:].zfill(2) 
			green = hex(gv)[2:].zfill(2)
			blue = hex(bv)[2:].zfill(2) 

	        # update the pixel at the current position to hold
	        # the color we created with the mandelbrot result
			img.put("#" + red + green + blue, (col, row))

# refreshes mandelbrot to reflect new settings
def update_window():
	# color sliders
	global rs
	global gs
	global bs

	# get slider values
	r = rs.get()
	g = gs.get()
	b = bs.get()

	# prints newly colored fractal
	print_fractal(r, g, b)

# prints min and max values to entry boxes
def print_view():
	# current min and max values
	global xmin
	global xmax
	global ymin
	global ymax

	# min and max text box values
	global xmin_var
	global xmax_var
	global ymin_var
	global ymax_var

	# update text boxes to reflect current min and max values
	xmin_var.set(str(xmin))
	xmax_var.set(str(xmax))
	ymin_var.set(str(ymin))
	ymax_var.set(str(ymax))

# reads input values and sets new view before refreshing canvas
def set_view():
	# current min and max values
	global xmin
	global xmax
	global ymin
	global ymax

	# min and max text box values
	global xmin_var
	global xmax_var
	global ymin_var
	global ymax_var

	# read text box values and set current min and max to those values
	xmin = float(xmin_var.get())
	xmax = float(xmax_var.get())
	ymin = float(ymin_var.get())
	ymax = float(ymax_var.get())

	# refresh to reflect changes
	update_window()

	# randomizes view based on "points of interest" lists; technically works but tends to pick a lot of very similar views
def random_view():
	# current min and max values
	global xmin
	global xmax
	global ymin
	global ymax

	# "points of interest" lists
	global a_list
	global d_list

	# generate random entry from those lists
	v = random.randint(0, len(a_list)-1)

	# access point values at that entry
	a = a_list[v]
	b = d_list[v]

	# generate random window radius; .5 is a semi-randomly chosen max value 
	x = random.uniform(0, .5)

	# set bounds of window with point at center and edges at ends of radius
	xmin = a - x
	xmax = a + x
	ymax = b + x
	ymin = b - x

	# update both fractal and displayed min and max values
	update_window()
	print_view()

# first chosen fractal
def preset_1():
	# current min and max values
	global xmin
	global xmax
	global ymin
	global ymax

	# color sliders
	global rs
	global gs
	global bs

	# "make color m-dependant?" bools
	global rmv 
	global gmv
	global bmv

	# set view
	xmin = -1.7573702534039815 
	xmax = -1.758038236035241
	ymin = 0.017416973908742268
	ymax = 0.016748991277482774

	# set colors
	rs.set(80)
	gs.set(255)
	bs.set(200)

	# set m-bools
	rmv.set(False)
	gmv.set(True)
	bmv.set(False)

	# update both fractal and displayed min and max values
	update_window()
	print_view()

# second chosen fractal
def preset_2():
	# current min and max values
	global xmin
	global xmax
	global ymin
	global ymax

	# color sliders
	global rs
	global gs
	global bs

	# "make color m-dependant?" bools
	global rmv 
	global gmv
	global bmv

	# set view
	xmin = -0.051869710286458336
	xmax = -0.044708251953125
	ymin = 0.669464111328125
	ymax = 0.6766255696614584

	# set colors
	rs.set(154)
	gs.set(255)
	bs.set(107)

	# set m-bools
	rmv.set(True)
	gmv.set(True)
	bmv.set(False)

	# update both fractal and displayed min and max values
	update_window()
	print_view()

# third chosen fractal
def preset_3():
	# current min and max values
	global xmin
	global xmax
	global ymin
	global ymax

	# color sliders
	global rs
	global gs
	global bs

	# "make color m-dependant?" bools
	global rmv 
	global gmv
	global bmv

	# set view
	xmin = -0.04731920030381945
	xmax = -0.04690890842013889
	ymin = 0.6739493476019965
	ymax = 0.6743596394856771

	# set colors
	rs.set(200)
	gs.set(200)
	bs.set(255)

	# set m-bools
	rmv.set(True)
	gmv.set(True)
	bmv.set(True)

	# update both fractal and displayed min and max values
	update_window()
	print_view()


######################### EXCECUTION

# load canvas on left
canvas.pack(side = LEFT)

# load min and max text boxes as well as 'set' and 'random' buttons
Label(window, text="X-Min:").pack()
xmin_in.pack()
Label(window, text="X-Max:").pack()
xmax_in.pack()
Label(window, text="Y-Min:").pack()
ymin_in.pack()
Label(window, text="Y-Max:").pack()
ymax_in.pack()
Button(window, text='Set View', command=set_view).pack()
Button(window, text='Random View', command=random_view).pack()

# spacing
Label(window, text="	").pack()

# load color sliders
rs.pack()
Label(window, text="Red Slider").pack()
gs.pack()
Label(window, text="Green Slider").pack()
bs.pack()
Label(window, text="Blue Slider").pack()

# spacing
Label(window, text="	").pack()

# load chceckboxes
m1.pack()
m2.pack()
m3.pack()

# spacing
Label(window, text="	").pack()

# load 'update window' button
Button(window, text='Update Window', command=update_window).pack()

# spacing
Label(window, text="	").pack()
Label(window, text="	").pack()

# load preset buttons
Button(window, text='Preset 1', command=preset_1).pack()
Button(window, text='Preset 2', command=preset_2).pack()
Button(window, text='Preset 3', command=preset_3).pack()

# print fractal for first time and display default min and max values
update_window()
print_view()

window.mainloop()



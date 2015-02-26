try:
    from Tkinter import * # Python 2
    import tkMessageBox as msg
    import tkSimpleDialog as dlg
    import ttk
except ImportError:
    from tkinter import * # Python 3
    from tkinter.ttk import *
    from tkinter import messagebox as msg
    from tkinter import simpledialog as dlg

import sys
import numpy
#import tkMessageBox as msg
#import tkSimpleDialog as dlg
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title("Ellipse Plotter")

def exit_everything():
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", exit_everything)

CHOICE1 = "Ellipse with one focus at origin"
CHOICE2 = "Ellipse with center at origin"

plotChoice = StringVar(root)
plotChoice.set(CHOICE1)
'''plotChoiceMenu = OptionMenu(root, plotChoice, CHOICE1, CHOICE2)
plotChoiceMenu.grid(row=0, column=1, sticky=EW)
plotChoiceLabel = Label(root, text="Ellipse plot type:")
plotChoiceLabel.grid(row=0, column=0)'''


def choice1Action():
    choice = 1
    type_lbl.configure(text=CHOICE1)
    c2_plot_btn.grid_remove()
    c1_plot_btn.grid(row=15, columnspan=3)

def choice2Action():
    choice = 2
    type_lbl.configure(text=CHOICE2)
    c1_plot_btn.grid_remove()
    c2_plot_btn.grid(row=15, columnspan=3)



def horiz_axis_action():
    rot_lbl.grid_remove()
    angle_ent.grid_remove()
    deg_btn.grid_remove()
    rad_btn.grid_remove()
    line_lbl.grid_remove()
    line_ent.grid_remove()

def vert_axis_action():
       
    rot_lbl.grid_remove()
    angle_ent.grid_remove()
    deg_btn.grid_remove()
    rad_btn.grid_remove()
    line_lbl.grid_remove()
    line_ent.grid_remove()

def line_axis_action():
    rot_lbl.grid_remove()
    angle_ent.grid_remove()
    deg_btn.grid_remove()
    rad_btn.grid_remove()
    line_lbl.grid_remove()
    line_ent.grid_remove()
    line_lbl.grid(row=8, column=0, columnspan=2, sticky=W)
    line_ent.grid(row=8, column=2, sticky=EW)

def rot_axis_action():
    line_lbl.grid_remove()
    line_ent.grid_remove()
    rot_lbl.grid(row=8, column=0, rowspan=2, sticky=W)
    angle_ent.grid(row=8, column=1, rowspan=2)
    deg_btn.grid(row=8, column=2, sticky=W)
    rad_btn.grid(row=9, column=2, sticky=W)

def deg_action():
    global oldDegRadChoice
    if oldDegRadChoice == 1:
        return
    radAngle = angle.get()
    degAngle = radAngle * (180 / numpy.pi)
    if degAngle.is_integer():
        degAngle = int(degAngle)
    elif int(degAngle) < int(degAngle + 1e-8):  #if it's something like x.999999999
        degAngle = int(degAngle + 0.5)
    elif int(degAngle) > int(degAngle - 1e-8) and not degAngle.is_integer():  #if it's something like x.0000001
        degAngle = int(degAngle)
    angle.set(degAngle)
    oldDegRadChoice = 1

def rad_action():
    global oldDegRadChoice
    if oldDegRadChoice == 2: 
        return
    degAngle = angle.get()
    radAngle = degAngle * (numpy.pi / 180)
    if radAngle.is_integer():
        radAngle = int(radAngle)
    elif int(radAngle) < int(radAngle + 1e-8):  #if it's something like x.999999999
        radAngle = int(radAngle + 0.5)
    elif int(radAngle) > int(radAngle - 1e-8) and not radAngle.is_integer():  #if it's something like x.0000001
        radAngle = int(radAngle)
    angle.set(radAngle)
    oldDegRadChoice = 2



class AboutDialog(dlg.Dialog):  #for the about page
    def body(self, master):
        abttxt = Label(master, text="Ellipse Plotter v2\n\n"+
                                    "A program that plots ellipses, given certain parameters.\n"+
                                    "Functionality for variable center locations, axis lengths,\n" +
                                    "and axis orientations.\n\n" +
                                    "Brian Slininger\nSeptember 9-13, 2013")
        abttxt.grid(row=0, column=0)
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
#        w = Button(box, text="Cancel", width=10, command=self.cancel)
#       w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
#       self.bind("<Escape>", self.cancel)
        box.pack()
#    def apply(self):
#        print "We did it!"

def aboutButtonAction():
    AboutDialog(root, title="About Ellipse Plotter")

def c1_plot_ellipse():
    try:
        aval = a.get()
        bval = b.get()
    except ValueError:
        msg.showerror("Input error", "Please enter a valid number.")
        return
    if not (numpy.isfinite(aval) and numpy.isfinite(bval)):
        msg.showerror("Input error", "Please do not use infinity or NaN as input values.")
        return
    if aval <= 0:
        msg.showerror("Input error", "The length of the semimajor axis must be positive.")
        return
    if bval <= 0:
        msg.showerror("Input error", "The length of the semiminor axis must be positive.")
        return
    if aval < bval:
        msg.showerror("Input error", "The length of the semimajor axis must not be less than " +
                                     "the length of the semiminor axis.")
        return
    e = numpy.sqrt((aval*aval - bval*bval)/(aval*aval))  #eccentricity
    if numpy.isnan(e) or e > 1 - 1e-8:
        msg.showerror("Input error","The ellipse's eccentricity is too close to 1.  The " +
                                    "lengths of the semimajor and semiminor axes are too " +
                                    "far apart.")
        return
    thetas = numpy.linspace(0, 2*numpy.pi, 501)
    rs = (aval * (1 - e*e)) / (1 - e * numpy.cos(thetas))
    xs = numpy.multiply(rs, numpy.cos(thetas))
    ys = numpy.multiply(rs, numpy.sin(thetas)) 
    focusxs = [0.0, 2*aval*e]
    focusys = [0.0, 0.0]
    plt.clf()
    # ax1=fig.add_subplot(1,1,1)
    plt.axis('equal')
    plt.plot(xs, ys)
    plt.plot(focusxs, focusys, 'ro')
    plt.gcf().canvas.draw()
    # plt.show()
    fociLabel.configure(text="Locations of foci:  ({0}, {1}) and ({2}, {3})".format(
                             int(focusxs[0]) if focusxs[0].is_integer() else focusxs[0],
                             int(focusys[0]) if focusys[0].is_integer() else focusys[0],
                             int(focusxs[1]) if focusxs[1].is_integer() else focusxs[1],
                             int(focusys[1]) if focusys[1].is_integer() else focusys[1]))

def c2_plot_ellipse():
    try:
        aval = a.get()
        bval = b.get()
        hval = h.get()
        kval = k.get()
    except ValueError:
        msg.showerror("Input error", "At least one entry box has had an invalid (non-numeric) " +
                                     "value entered into it.  Please enter valid numeric " +
                                     "values only.")
        return
    if orientationChoice.get() == 3:
        try:
            slopeval = slope.get()
        except ValueError:
            msg.showerror("Input error", "At least one entry box has had an invalid (non-numeric) " +
                                         "value entered into it.  Please enter valid numeric " +
                                         "values only.")
            return
        if numpy.isnan(slopeval):
            msg.showerror("Input error", "Please do not use NaN as an input value.")
            return
    if orientationChoice.get() == 4:
        try:
            angleval = angle.get()
        except ValueError:
            msg.showerror("Input error", "At least one entry box has had an invalid (non-numeric) " +
                                         "value entered into it.  Please enter valid numeric " +
                                         "values only.")
            return
        if numpy.isnan(angleval):
            msg.showerror("Input error", "Please do not use NaN as an input value.")
            return
        if not numpy.isfinite(angleval):
            msg.showerror("Input error", "The angle of rotation must be a finite value.")
            return
    if (numpy.isnan(aval) or numpy.isnan(bval) or numpy.isnan(hval) or numpy.isnan(kval)):
        msg.showerror("Input error", "Please do not use NaN as an input value.")
        return
    if aval <= 0:
        msg.showerror("Input error", "The length of the semimajor axis must be positive.")
        return
    if bval <= 0:
        msg.showerror("Input error", "The length of the semiminor axis must be positive.")
        return
    if not numpy.isfinite(aval):
        msg.showerror("Input error", "The length of the semimajor axis must be finite.")
        return
    if not numpy.isfinite(bval):
        msg.showerror("Input error", "The length of the semiminor axis must be finite.")
        return
    if not numpy.isfinite(hval):
        msg.showerror("Input error", "The x-coordinate of the center of the ellipse must be a finite value.")
        return
    if not numpy.isfinite(kval):
        msg.showerror("Input error", "The y-coordinate of the center of the ellipse must be a finite value.")
        return
    if aval < bval:
        msg.showerror("Input error", "The length of the semimajor axis must not be less than " +
                                     "the length of the semiminor axis.")
        return
    if aval / bval > 1000:
        msg.showerror("Input error", "Please keep the length of the semimajor axis to no more than " +
                                     "a factor of 1000 times larger than the length of the " +
                                     "semiminor axis.")
        return
    e = numpy.sqrt((aval*aval - bval*bval)/(aval*aval))  #eccentricity
    if numpy.isnan(e) or e > 1 - 1e-8:
        msg.showerror("Input error","The ellipse's eccentricity is too close to 1.  The " +
                                    "lengths of the semimajor and semiminor axes are too " +
                                    "far apart.  This is generally caused by using values " +
                                    "that are extremely large.")
        return
    thetas = numpy.linspace (0, 2*numpy.pi, 501)
    if orientationChoice.get() == 2:
        temp = aval
        aval = bval
        bval = temp
        phi = 0
    elif orientationChoice.get() == 3:
        phi = numpy.arctan(slopeval)
    elif orientationChoice.get() == 4:
        phi = angleval
        if degRadChoice.get() == 1:
            phi = phi * (numpy.pi / 180)
    else:
        phi = 0
    xs = aval * numpy.cos(thetas) * numpy.cos(phi) - bval * numpy.sin(thetas) * numpy.sin(phi)
    ys = aval * numpy.cos(thetas) * numpy.sin(phi) + bval * numpy.sin(thetas) * numpy.cos(phi)
    if numpy.cos(phi) < 1e-6 and numpy.cos(phi) > -1e-6:  #close enough to zero
        temp = aval
        aval = bval  #swapping a and b in the formula, to make a vertical ellipse
        bval = temp
        phi = 0  #it's pretty much vertical so let's consider it to be vertical
    if numpy.sin(phi) < 1e-6 and numpy.sin(phi) > -1e-6:
        phi = 0  #pretty much horizontal
    if orientationChoice.get() == 2 or aval < bval:
        focal_y_loc = numpy.sqrt(bval*bval - aval*aval)
        focusxs = [0.0, 0.0]
        focusys = [-focal_y_loc, focal_y_loc]
    else:
        focal_x_loc = numpy.sqrt(aval*aval - bval*bval)
        focusxs = [-focal_x_loc, focal_x_loc]
        focusys = [0.0, 0.0]
    for i in range(2):
        newx = focusxs[i] * numpy.cos(phi) - focusys[i] * numpy.sin(phi)
        newy = focusxs[i] * numpy.sin(phi) + focusys[i] * numpy.cos(phi)
        focusxs[i] = newx + hval
        focusys[i] = newy + kval
    xs = xs + hval
    ys = ys + kval
    plt.clf()
    # ax1=fig.add_subplot(1,1,1)
    plt.axis('equal')
    plt.plot(xs, ys)
    plt.plot(focusxs, focusys, 'ro')
    plt.gcf().canvas.draw()
    # plt.show()
    fociLabel.configure(text="Locations of foci:  ({0}, {1}) and ({2}, {3})".format(
                             int(focusxs[0]) if focusxs[0].is_integer() else focusxs[0],
                             int(focusys[0]) if focusys[0].is_integer() else focusys[0],
                             int(focusxs[1]) if focusxs[1].is_integer() else focusxs[1],
                             int(focusys[1]) if focusys[1].is_integer() else focusys[1]))


'''
plotChoiceMenu = Menu(root, tearoff=False)
plotChoiceMenuButton = ttk.Menubutton(root, text="Ellipse type to plot", underline=0, direction='below', menu=plotChoiceMenu)
plotChoiceMenu.add_command(label=CHOICE1, command=choice1Action)
plotChoiceMenu.add_command(label=CHOICE2, command=choice2Action)
plotChoiceMenuButton.grid(row=0, column=0, columnspan=3, sticky=N)

# Everything starts with Choice 1 as the default

choice = 1


type_lbl = Label(root, text=CHOICE1)
type_lbl.grid(row=1, column=0, columnspan=3)
'''

h = DoubleVar()
k = DoubleVar()
center_x_lbl = Label(root, text="Ellipse center x-coordinate")
center_y_lbl = Label(root, text="Ellipse center y-coordinate")
center_x_ent = Entry(root, textvariable=h, width=9)
center_y_ent = Entry(root, textvariable=k, width=9)
h.set(0)
k.set(0)
center_x_lbl.grid(row=0, column=0, columnspan=2, sticky=W)
center_y_lbl.grid(row=1, column=0, columnspan=2, sticky=W)
center_x_ent.grid(row=0, column=2, sticky=EW)
center_y_ent.grid(row=1, column=2, sticky=EW)

semimaj_lbl = Label(root, text="Length of semimajor axis:")
semimin_lbl = Label(root, text="Length of semiminor axis:")
a = DoubleVar()  #semimajor axis length
b = DoubleVar()  #semiminor axis length
a.set(13)
b.set(12)
semimaj_ent = Entry(root, textvariable=a, width=9)
semimin_ent = Entry(root, textvariable=b, width=9)
semimaj_lbl.grid(row=2, column=0, columnspan=2, sticky=W)
semimin_lbl.grid(row=3, column=0, columnspan=2,sticky=W)
semimaj_ent.grid(row=2, column=2, sticky=EW)
semimin_ent.grid(row=3, column=2, sticky=EW)

orientationChoice = IntVar()
orientationChoice.set(1)
horiz_btn = Radiobutton(root, text="Horizontal major axis", variable=orientationChoice, value=1, command=horiz_axis_action)
vert_btn = Radiobutton(root, text="Vertical major axis", variable=orientationChoice, value=2, command=vert_axis_action)
line_btn = Radiobutton(root, text="Major axis along line", variable=orientationChoice, value=3, command=line_axis_action)
rot_btn = Radiobutton(root, text="Major axis rotated by angle", variable=orientationChoice, value=4, command=rot_axis_action)
line_lbl = Label(root, text="Slope of major axis:")
slope = DoubleVar()
slope.set(1)
line_ent = Entry(root, textvariable=slope, width=4)
rot_lbl = Label(root, text="Angle of rotation:")
angle = DoubleVar() #angle of rotation of ellipse
angle.set(45)
angle_ent = Entry(root, textvariable=angle, width=4)
degRadChoice = IntVar()
degRadChoice.set(1)
oldDegRadChoice = 1
deg_btn = Radiobutton(root, text="degrees", variable=degRadChoice, value=1, command=deg_action)
rad_btn = Radiobutton(root, text="radians", variable=degRadChoice, value=2, command=rad_action)
horiz_btn.grid(row=4, column=0, columnspan=3, sticky=W)
vert_btn.grid(row=5, column=0, columnspan=3, sticky=W)
line_btn.grid(row=6, column=0, columnspan=3, sticky=W)
rot_btn.grid(row=7, column=0, columnspan=3, sticky=W)


fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
#ax1.axis('equal')
canvas = FigureCanvasTkAgg(fig, master=root)
plt.axis('equal')
plt.axis([0, 7, 0, 5])
plt.gcf().canvas.draw()
exit_btn = Button(root, text="Exit", command=exit_everything)
exit_btn.grid(row=17, columnspan=3)
fociLabel = Label(root)
fociLabel.grid(row=17, column=3)
canvas.get_tk_widget().grid(row=0, column=3, rowspan=17)

about_btn = Button(root, text="About", command=aboutButtonAction)
c1_plot_btn = Button(root, text="Plot the ellipse", command=c1_plot_ellipse)
c2_plot_btn = Button(root, text="Plot the ellipse ", command=c2_plot_ellipse)
about_btn.grid(row=16, columnspan=3)
c2_plot_btn.grid(row=15, columnspan=3)











root.mainloop()

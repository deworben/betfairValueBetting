import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.pyplot import subplot, figure, subplots
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
# style.use("ggplot")

import tkinter as tk
from tkinter import ttk
from tkinter import DoubleVar, StringVar

import time

import sys
sys.path.insert(0, r'C:\Users\User\Documents\Betting\Tennis\oddsPatterns\betfairTennisAnalysis')
from singleVariableSimulation import SingleVariableSimulation
from multiVariableSimulation import MultivariableSimulation
from defaultTestVars import defaultOdds


strat = "earlyLiveOdds"
newVars = defaultOdds[strat]



LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 0)

#make new matplotlib figure for manual slider page
manualFig = Figure(figsize=(5, 5), dpi=100)
manualPlot = manualFig.add_subplot(111)

#new matplotlib figure for sensitivity analysis
sensitivityFig = Figure(figsize=(5, 5), dpi=100)
sensitivityPlot = sensitivityFig.add_subplot(111)



def animate(i):
    try:
        for i, var in enumerate(list(newVars)[0:-1]):
            newVars[var] = [app.sliderVars[i].get()]
       
    except:
        pass
    manualPlot.clear()
    # sensitivityPlot.clear()

    SingleVariableSimulation(fig=manualPlot, unchangedVars=newVars)
    # SensitivityAnalysis()    





class BLM(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        

        tk.Tk.wm_title(self, "Lets test some variables")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.sliderVars = []
        self.sliderRanges = newVars["ranges"]

        for var in enumerate(list(newVars)[0:-1]):
            self.sliderVars.append(DoubleVar())


        self.frames = {}

        for F in (StartPage, ManualTest, SensitivityAnalysis, Liveapi):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Are you ready to make some money", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

       
        button1 = ttk.Button(self, text="Go to manual simulator!", 
                            command = lambda:controller.show_frame(ManualTest))
        button1.pack()

        button2 = ttk.Button(self, text="Go to sensitivity analysis",
                            command=lambda:controller.show_frame(SensitivityAnalysis))
        button2.pack()

        button3 = ttk.Button(self, text="Go to Live api betting",
                            command=lambda:controller.show_frame(Liveapi))
        button3.pack()


class Liveapi(tk.Frame):

    def __init__(self, parent, controller):
        #buttons and page setup
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Live API", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Go to Home", command = lambda:controller.show_frame(StartPage))
        button1.pack()

class SensitivityAnalysis(tk.Frame):

    def __init__(self, parent, controller):
        #buttons and page setup
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Sensitivity analysis", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Go to Home", command = lambda:controller.show_frame(StartPage))
        button1.pack()


        # #create a canvas on tk background and draw figure from canvas
        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # #create little bottom toolbar for zoom, home, etc
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
        # slide1 = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        # slide1.pack()
        
class ManualTest(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Adjusting simulation Page!", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        label.grid(row=1, column=12, sticky="E", pady=10, padx=10)
        button1 = ttk.Button(self, text="Go to Home", command = lambda:controller.show_frame(StartPage))
        # button1.pack()
        button1.grid(row=1, column=22, sticky="E")

        button2 = ttk.Button(self, text="Go to SensitivityAnalysis", command = lambda:controller.show_frame(SensitivityAnalysis))
        # button2.pack()
        button2.grid(row=1, column=23, sticky="E")


        
        # self.var1 = tk.Scale( self, variable = controller.sliderVars[0] )
        # self.var1.set(25)
        # self.var1.pack(side=tk.LEFT)
        for i, var in enumerate(list(newVars)[0:-1]):
            # self.i = tk.Scale( self, controller,
            #                     variable = controller.sliderVars[i], 
            #                     from_=newVars["ranges"][i][0], 
            #                     to=newVars["ranges"][i][1], 
            #                     resolution=newVars["ranges"][i][2] 
            #                     )
            # self.i.set(25)
            # self.i.pack(side=tk.LEFT)
            self.i = Slider( self, controller, i, 
                                childText=var, 
                                variable = controller.sliderVars[i], 
                                from_=newVars["ranges"][i][0], 
                                to=newVars["ranges"][i][1], 
                                resolution=newVars["ranges"][i][2] 
                                )


        #create a canvas on tk background and draw figure from canvas
        canvas = FigureCanvasTkAgg(manualFig, self)
        canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().grid(row=5, column=0, rowspan=5, columnspan=15)

        #create little bottom toolbar for zoom, home, etc
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas._tkcanvas.grid(row=1)



class Slider:

    def __init__(self, parent, controller, i, childText, variable, from_, to, resolution):

        direction = tk.LEFT

        self.slide = tk.Scale( parent, 
                                variable = controller.sliderVars[i], 
                                from_=newVars["ranges"][i][0], 
                                to=newVars["ranges"][i][1], 
                                resolution=newVars["ranges"][i][2],
                                orient=tk.HORIZONTAL                             
                                )
        label = ttk.Label(parent, text=childText, font=LARGE_FONT)
        # label.pack(side=direction)
        self.slide.set(5)
        # self.slide.pack(side=direction)
        self.slide.grid(row=30, column=2*i)

        label.grid(row=29, column=2*i)

    def get(self):
        return self.slide.get()



        

        


app = BLM()
app.geometry("1280x720")
ani = animation.FuncAnimation(manualFig, animate, interval=4000)
app.mainloop()
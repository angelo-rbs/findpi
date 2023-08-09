import sys
import random
import timeit
import numpy as np

if sys.version_info[0] == 3:
    import tkinter.ttk as ttk
    import tkinter as tk
else:
    import Tkinter as tk

root = tk.Tk()

RADIUS = 300
DIAMETER = 2*RADIUS + 1
SQUARE_SIDE = DIAMETER

def truncateFloat(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier

def generatePoint(radius):
    limit = 2 * radius
    x = random.randint(0, limit)
    y = random.randint(0, limit)
    return (x, y)

def drawPoint(x, y, canvas):
    canvas.create_line((x, y), (x+1, y), fill='green')

def calcPi(dotsAll, dotsInside):
    return 4*(dotsInside/dotsAll)

def generate(dotsInput, radius, canvas, piLabel):

    canvas.delete('all')
    canvas.create_arc(*points, style=tk.ARC, width=1, outline='red', extent=359)

    start = timeit.default_timer()

    try:
        dotCount = int(dotsInput.get('0.0', 'end'))

        if dotCount > 1000000:
            logLabel.configure(text='input too large')
            return

        dotsInside = 0
        randomLimit = 2*radius + 1
        r2 = radius**2

        rng = np.random.default_rng()
        

        for i in range(dotCount):

            x = rng.integers(low=0, high=randomLimit)
            y = rng.integers(low=0, high=randomLimit)

            dotsInside += (x-radius)*(x-radius) + (y-radius)*(y-radius) <= r2

            drawPoint(x, y, canvas)

        calcTime = truncateFloat(timeit.default_timer() - start, 3)

        
        pi = 4*(dotsInside/(dotCount*1.0))
        error = truncateFloat(np.abs(np.pi - pi)*100.0/np.pi, 2)

        print(f'pi estimated value: {pi}')
        print(f'error: {error}%')
        print(f'time elapsed: {calcTime} seconds')
        

        piLabel.configure(text=str(pi))
        logLabel.configure(text='calculated')
        
    except:
        logLabel.configure(text='invalid dot input')

    


# create your widgets here

root.title('findpi')
root.configure(background='skyblue')
root.minsize(900, 600)
root.maxsize(900, 600)
root.geometry('900x600')


# painel visual

visual_panel = tk.Frame(root, width=SQUARE_SIDE, height=SQUARE_SIDE, background='blue')
visual_panel.pack(side='left')

canvas = tk.Canvas(visual_panel, bg='black', width=SQUARE_SIDE, height=SQUARE_SIDE)

points = (
    (0, 0),
    (DIAMETER, DIAMETER)
)

canvas.pack(anchor=tk.CENTER, expand=True)
canvas.create_arc(*points, style=tk.ARC, width=1, outline='red', extent=359)



# painel de configuração

options_panel = tk.Frame(root, width=RADIUS, height=SQUARE_SIDE, background='lightgrey')
options_panel.pack(side='left', expand=True, fill='both')


dotsLabel = tk.Label(options_panel, text='dots to generate:')
dotsLabel.pack(anchor='center')

dotsInput = tk.Text(options_panel, height=1, width=10, )
dotsInput.pack(anchor='center')
dotsInput.insert('0.0', '100000')

calculateButton = tk.Button(options_panel, text='Calculate', background='darkgrey', command=lambda: generate(dotsInput, RADIUS, canvas, piValue))
calculateButton.pack(anchor='center', expand=False)

piValueLabel = tk.Label(options_panel, text='pi ≃ ')
piValueLabel.pack(side='left')

piValue = tk.Label(options_panel)
piValue.pack(side='left')

logLabel = tk.Label(options_panel, text='')
logLabel.pack(side='bottom')

root.mainloop()
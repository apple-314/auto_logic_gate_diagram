import tkinter as tk
from logic import *

def and_gate(canvas, x, y, width=40, height=40): # width and height must be the same
    canvas.create_line(x - width / 2, y - height / 2, x - width / 2, y + height / 2, width=2)
    canvas.create_line(x - width / 2, y - height / 2, x, y - height / 2, width=2)
    canvas.create_line(x - width / 2, y + height / 2, x, y + height / 2, width=2)
    canvas.create_arc(x-width/2, y-width/2, x + width/2, y + height/2, start=-90, extent=180, style="arc", width=2)

def or_gate(canvas, x, y, width=40, height=40):
    canvas.create_arc(x-(width*2/3), y-width/2, x-width/3, y + height/2, start=-90, extent=180, style="arc", width=2)
    canvas.create_arc(x-(width*3/2), y-width/2, x+width/2, y + height/2, start=-90, extent=180, style="arc", width=2)

def hori_jump(canvas, x, y, width=5, height=5):
    canvas.create_arc(x-width/2, y-height/2, x+width/2, y+height/2, start=0, extent=180, style="arc", width=2)

def not_gate(canvas, x, y, width=4, height=4):
    canvas.create_oval(x-width/2, y-height/2, x+width/2, y+height/2, width=2)

def vert_jump(canvas, x, y, width=5, height=5):
    canvas.create_arc(x-width/2, y-height/2, x+width/2, y + height/2, start=80, extent=200, style="arc", width=2)

def line(canvas, x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2, width=2)

def draw(values):
    n = len(values)

    w = 425
    h = 100 + max((n - 1) * 50, (inputs - 1) * 30)
    root = tk.Tk()
    canvas = tk.Canvas(root, width=w, height=h+50)
    canvas.pack()

    # gates setup
    and_pos = [(h - 50 * (n - 1)) / 2 + i * 50 for i in range(n)]
    for i in range(n):
        and_gate(canvas, 250, and_pos[i])
    or_gate(canvas, 375, h/2)

    or_heights = [h / 2 - 17.5 + 35 / (n - 1) * i for i in range(n)]
    for i in range(n):
        offset = abs((n - 1) / 2 - i) * 5
        line(canvas, 270, and_pos[i], 280 + (offset), and_pos[i])
        line(canvas, 280 + (offset), and_pos[i], 280 + (offset), or_heights[i])
        line(canvas, 280 + (offset), or_heights[i], 375 - 20, or_heights[i])
    line(canvas, 395, h/2, w, h/2)
        
    # inputs
    in_offset = [(-35/2) + 35 / (inputs - 1) * i for i in range(inputs)]
    # in_y = [(h - 30 * (inputs - 1)) / 2 + i * 30 + in_offset[i] for i in range(inputs)]
    in_x = [75 + (175 - 75) / (inputs - 1) * i for i in range(inputs)]

    in_min = [h for i in range(inputs)]
    for i in range(n):
        for x in values[i][0] + values[i][1]:
            in_min[x] = min(in_min[x], and_pos[i] + in_offset[x])

    barriers = []
    for i in range(inputs):
        line(canvas, in_x[i], in_min[i], in_x[i], h+20)
        canvas.create_text(in_x[i], h+25, text=str(2**i), font=('bold', 10))
        barriers.append([in_x[i], in_min[i]])

    barriers.sort()
    for i in range(n):
        for x in values[i][0] + values[i][1]:
            cur = in_x[x]
            for barrier in barriers:
                if barrier[0] <= cur or barrier[1] > and_pos[i] + in_offset[x]:
                    continue
                line(canvas, cur, and_pos[i] + in_offset[x], barrier[0] - 2.5, and_pos[i] + in_offset[x])
                hori_jump(canvas, barrier[0], and_pos[i] + in_offset[x])
                cur = barrier[0] + 2.5

            line(canvas, cur, and_pos[i] + in_offset[x], 250 - 20 - (4 * (x in values[i][0])), and_pos[i] + in_offset[x])
            
            if x in values[i][0]:
                not_gate(canvas, 250 - 22, and_pos[i] + in_offset[x])

    root.mainloop()



# valid = ["0001", "0010", "0011", "0101", "0111", "1011", "1101"] # 4 primes
# valid = ["0000", "0011", "1000", "1111"] # squares
# valid = ["00001", "00010", "00011", "00101", "00111", "01011", "01101", "10001", "10011", "10111", "11101", "11111"] # 5 primes
valid = ["000001", "000010", "000011", "000101", "000111", "001011", "001101", "010001", "010011", "010111", "011101", "011111", "100101", "101001", "101011", "101111", "110101", "111011", "111101"] # 6 primes
print(len(valid))
inputs, init_values = convert(valid)
values = find_circuit(inputs, init_values)

draw(values)
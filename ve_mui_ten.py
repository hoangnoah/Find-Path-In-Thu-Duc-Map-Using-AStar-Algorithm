import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def ve_mui_ten(b, a, tx, ty):
    p_mui_ten = [(0,0,1), (-20,10,1), (-15,0,1), (-20,-10,1)]
    p_mui_ten_ma_tran = [np.array([[0],[0],[1]],np.float32),
                            np.array([[-20],[10],[1]],np.float32),
                            np.array([[-15],[0],[1]],np.float32),
                            np.array([[-20],[-10],[1]],np.float32)]

    # Tạo ma trận dời (tịnh tiến) - translate
    M1 = np.array([[1, 0, tx], 
                    [0, 1, ty], 
                    [0, 0, 1]], np.float32)

    # Tạo ma trận quay - rotation
    theta = np.arctan2(b, a)
    M2 = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta),  np.cos(theta), 0],
                    [     0,             0,        1]], np.float32)

    M = np.matmul(M1, M2)

    q_mui_ten = []

    for p in p_mui_ten_ma_tran:
        q = np.matmul(M, p)
        q_mui_ten.append([q[0,0], q[1,0]])
    return q_mui_ten 

xmin = 91
xmax = 562
ymin = 270
ymax = 570


fig, ax = plt.subplots()

px = [100, 500, 100]
py = [300, 450, 550]

lines, = ax.plot(px, py)
L = len(px)
N = 21
d = 100

lst_vi_tri = []

for i in range(0,L-1):
    x1 = px[i]
    y1 = py[i]
    x2 = px[i+1]
    y2 = py[i+1]

    b = y2-y1
    a = x2-x1

    d0 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    N0 = int(N*d0/d)
    dt = 1/(N0-1)
    for j in range(0, N0):
        t = j*dt
        x = x1 + (x2-x1)*t
        y = y1 + (y2-y1)*t

        q = ve_mui_ten(b,a,x,y)
        lst_vi_tri.append(q)


red_polygon, = ax.fill([],[], color = 'red')

FRAME = len(lst_vi_tri)

def init():
    ax.axis([xmin-70, xmax+70, ymin-70, ymax+70])
    # Trả về nhiều đoạn thẳng và đoạn thẳng tìm được
    return lines, red_polygon
 
def animate(i):
    temp = lst_vi_tri[i]
    red_polygon.set_xy(lst_vi_tri[i])
    return lines, red_polygon 

anim = FuncAnimation(fig, animate, frames=FRAME, interval=50, init_func=init, repeat=False)

plt.show()

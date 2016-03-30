#!/usr/bin/env python3

import math
import os
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import tkinter as Tk

def add(x,y):
    return x + y

def minus(x,y):
    return x - y

def mul(x,y):
    return x * y

def div(x,y):
    return x / y

def trapeze_discr(left, numl, numr, right, n):
    kl = 1/(numl - left)
    bl = -left/(numl - left)
    kr = 1/(numr - right)
    br = -right/(numr - right)
    xl = np.array([])
    xr = np.array([])
    for lmb in np.arange(0.0, 1.0 + 1/n, 1/n):
        xl = np.append(xl, (lmb - bl)/ kl)
        xr = np.append(xr, (lmb - br)/ kr)
    return xl, xr, np.arange(0.0, 1.0 + 1/n, 1/n)

def normal_discr(mean, variance, n):
    xl = np.array([mean - math.sqrt(-2*(variance**2)*math.log(1/(n)))])
    xr = np.array([mean + math.sqrt(-2*(variance**2)*math.log(1/(n)))])
    for lmb in np.arange(1/n, 1.0 + 1/n, 1/n):
        xl = np.append(xl, mean - math.sqrt(-2*(variance**2)*math.log(lmb)))
        xr = np.append(xr, mean + math.sqrt(-2*(variance**2)*math.log(lmb)))
    return xl, xr, np.arange(0, 1.0 + 1/n, 1/n)

def points_discr(xes,mus,n):
    i, j = 0, -1
    if max(mus) != 1 or mus[-1] == 1 or mus[0] == 1:
        raise ValueError
    xl = np.array([xes[0]])
    xr = np.array([xes[-1]])
    for lmb in np.arange(1/n, 1.0 + 1/n, 1/n):
        if lmb <= mus[i]:
            if i == 0 or xes[i+1] == xes[i]:
                xl = np.append(xl, xes[i])
            else:
                k = (mus[i]-mus[i-1])/(xes[i]-xes[i-1])
                b = mus[i-1] - k*xes[i-1]
                xl = np.append(xl, (lmb - b)/k)
        else:
            while lmb > mus[i]:
                i += 1
            if xes[i] == xes[i-1]:
                xl = np.append(xl, xes[i])
            else:
                k = (mus[i]-mus[i-1])/(xes[i]-xes[i-1])
                b = mus[i-1] - k*xes[i-1]
                xl = np.append(xl, (lmb - b)/k)
            
        if lmb <= mus[j]:
            if j == -1 or xes[j+1] == xes[j]:
                xr = np.append(xr, xes[j])
            else:
                k = (mus[j]-mus[j+1])/(xes[j]-xes[j+1])
                b = mus[j+1] - k*xes[j+1]
                xr = np.append(xr, (lmb - b)/k)
        else:
            while lmb > mus[j]:
                j -= 1
            if xes[j+1] == xes[j]:
                xr = np.append(xr, xes[j])
            else:
                k = (mus[j]-mus[j+1])/(xes[j]-xes[j+1])
                b = mus[j+1] - k*xes[j+1]
                xr = np.append(xr, (lmb - b)/k)
    return xl, xr, np.arange(0, 1.0 + 1/n, 1/n)


def vertex_fuzzy_bifunc(xl, xr, yl, yr, mus, f):
    resl = np.array([])
    resr = np.array([])
    for i in range(len(mus)):
        minres = min(f(xl[i],yl[i]),f(xl[i],yr[i]),
                             f(xr[i],yl[i]),f(xr[i],yr[i]))
        maxres = max(f(xl[i],yl[i]),f(xl[i],yr[i]),
                             f(xr[i],yl[i]),f(xr[i],yr[i]))
        resl = np.append(resl, minres)
        resr = np.append(resr, maxres)
    return resl, resr

def add_interval(a,b,c,d):
    return a+c, b+d

def minus_interval(a,b,c,d):
    return a-d, b-c

def mul_interval(a,b,c,d):
    return min(a*c, a*d, b*c, b*d), max(a*c, a*d, b*c, b*d)

def div_interval(a,b,c,d):
    return mul_interval(a,b,1/d, 1/c)

def o_interval(a,b,c,d,f):
    if f == add:
        return add_interval(a,b,c,d) 
    if f == minus:
        return minus_interval(a,b,c,d) 
    if f == mul:
        return mul_interval(a,b,c,d) 
    if f == div:
        return div_interval(a,b,c,d) 

def dsw_fuzzy_bifunc(xl, xr, yl, yr, mus, f):
    lmb_l = np.array([])
    lmb_r = np.array([])
    for i in range(len(mus)):
        z1, z2 = o_interval(xl[i], xr[i], yl[i], yr[i], f)
        lmb_l, lmb_r = np.append(lmb_l,z1), np.append(lmb_r,z2)
    return lmb_l, lmb_r

def plot(x,y,z,mu,mu_z):
    plt = Tk.Toplevel(master=root)
    plt.wm_title("Fuzzy Plots")

    f = Figure(figsize=(5, 4), dpi=100)
    a1 = f.add_subplot(111)
    a2 = f.add_subplot(111)
    ares = f.add_subplot(111)

    ares.plot(z,mu_z)
    a1.plot(x,mu)
    a2.plot(y,mu)

    canvas = FigureCanvasTkAgg(f, master=plt)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, plt)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


    def on_key_event(event):
        print('you pressed %s' % event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)


    def _quit():
        plt.destroy()

    button = Tk.Button(master=plt, text='Quit', command=_quit)
    button.pack(side=Tk.BOTTOM)
    
def error():
    error = Tk.Toplevel(master=root)
    error.title("Error")
    err_lbl = Tk.Label(error, text="Invalid input", font='Arial 20', fg='red')
    err_lbl.pack()
    def _quit():
        error.destroy()

    button = Tk.Button(master=error, text='Quit', command=_quit)
    button.pack(side=Tk.BOTTOM)

    
def calculate():
    try:
        val_memb1 = varmemb1.get()
        val_memb2 = varmemb2.get()
        value2 = var2.get()
        n = 100
        if val_memb1 == 1:
            n1 = ent1.get().split()
            num1 = list(map(lambda x: float(x), n1))
            num1.sort()
            if len(num1) == 3:
                x_left, x, x_right = num1
                x_numl = x_numr = x
            else:
                x_left, x_numl, x_numr, x_right = num1

            xl, xr, mux = trapeze_discr(x_left, x_numl, x_numr, x_right, n)
        elif val_memb1 == 2:
            n1 = ent1.get().split()
            mean1, variance1 = list(map(lambda x: float(x), n1))
            xl, xr, mux = normal_discr(mean1, variance1, n)
        else:
            filex = open(fl1_x.get(), 'r')
            x_str = filex.readlines()
            xes = list(map(lambda ch: float(ch), x_str))
            filem = open(fl1_mu.get(), 'r')
            mu_str = filem.readlines()
            mus = list(map(lambda ch: float(ch), mu_str))
            xl, xr, mux = points_discr(xes, mus, n)
            filex.close()
            filem.close()
        if val_memb2 == 1:
            n2 = ent2.get().split()
            num2 = list(map(lambda x: float(x), n2))
            num2.sort()
            if len(num2) == 3:
                y_left, y, y_right = num2
                y_numl = y_numr = y
            else:
                y_left, y_numl, y_numr, y_right = num2
            yl, yr, muy = trapeze_discr(y_left, y_numl, y_numr, y_right, n)
        elif val_memb2 == 2:
            n2 = ent2.get().split()
            mean2, variance2 = list(map(lambda x: float(x), n2))
            yl, yr, muy = normal_discr(mean2, variance2, n)
        else:
            filex = open(fl2_x.get(), 'r')
            x_str = filex.readlines()
            xes = list(map(lambda ch: float(ch), x_str))
            filem = open(fl1_mu.get(), 'r')
            mu_str = filem.readlines()
            mus = list(map(lambda ch: float(ch), mu_str))
            yl, yr, muy = points_discr(xes, mus, n)
            filex.close()
            filem.close()

        mus = mux
                
        value = var.get()
        if value == 1:
            f = add
        elif value == 2:
            f = minus
        elif value == 3:
            f = mul
        else:
            f = div
            
        x = np.append(xl, xr[::-1])
        y = np.append(yl, yr[::-1])
        mu = np.append(mus, mus[::-1])
        if value2 == 1:
            lmb_l, lmb_r = vertex_fuzzy_bifunc(xl, xr, yl, yr, mus, f)
            z = np.append(lmb_l, lmb_r[::-1])
            mu_z = mu
        else:
            lmb_l, lmb_r = dsw_fuzzy_bifunc(xl, xr, yl, yr, mus, f)
            z = np.append(lmb_l, lmb_r[::-1])
            mu_z = mu
        filename1 = ent3.get()
        if filename1 == "":
            filename1 = "x_out"
        filename2 = ent4.get()
        if filename2 == "":
            filename2 = "mu_out"
        file1 = open(os.path.join(dr.get(),filename1), "w")
        file2 = open(os.path.join(dr.get(),filename2), "w")
        for i in range(len(z)):
            file1.write("".join([str(z[i]),"\n"]))
            file2.write("".join([str(mu_z[i]),"\n"]))
        file1.close()
        file2.close()
        plot(x,y,z,mu,mu_z)
    except:
        error = Tk.Toplevel(master=root)
        error.title("Error")
        err_lbl = Tk.Label(error, text="Invalid input", font='Arial 20', fg='red')
        err_lbl.pack()
        def _quit():
          error.destroy()

        button = Tk.Button(master=error, text='Quit', command=_quit)
        button.pack(side=Tk.BOTTOM)

def select_dir():
    directory = Tk.filedialog.askdirectory()
    if directory == "" or directory == ():
        directory = os.getcwd()
    dr.set(directory)

def clear1():
    for widget in frame_inp1.winfo_children():
        widget.pack_forget()

def clear2():
    for widget in frame_inp2.winfo_children():
        widget.pack_forget()

def trap1_pack():
    clear1()
    label1_tr.pack()
    ent1.pack()
    
def norm1_pack():
    clear1()
    label1_n.pack()
    ent1.pack()

def file1_pack():
    clear1()
    label1_f_x.pack()
    file1_x_but.pack()
    label1_file_x.pack()
    label1_f_mu.pack()
    file1_mu_but.pack()
    label1_file_mu.pack()
    
def trap2_pack():
    clear2()
    label2_tr.pack()
    ent2.pack()
    
def norm2_pack():
    clear2()
    label2_n.pack()
    ent2.pack()

def file2_pack():
    clear2()
    label2_f_x.pack()
    file2_x_but.pack()
    label2_file_x.pack()
    label2_f_mu.pack()
    file2_mu_but.pack()
    label2_file_mu.pack()

def select_file1_x ():
    file = Tk.filedialog.askopenfile(mode='r')
    if file:
        fl1_x.set(file.name)

def select_file1_mu ():
    file = Tk.filedialog.askopenfile(mode='r')
    if file:
        fl1_mu.set(file.name)

def select_file2_x ():
    file = Tk.filedialog.askopenfile(mode='r')
    if file:
        fl2_x.set(file.name)

def select_file2_mu ():
    file = Tk.filedialog.askopenfile(mode='r')
    if file:
        fl2_mu.set(file.name)    
    
root = Tk.Tk()
root.title("1FC")

frame_memb1 = Tk.Frame(root)
varmemb1 = Tk.IntVar()
rmemb1_tr = Tk.Radiobutton(frame_memb1,text = 'Triangle/trapeze',variable=varmemb1,value=1,command = trap1_pack)
rmemb1_n =Tk.Radiobutton(frame_memb1,text = 'Normal distribution',variable=varmemb1,value=2,command = norm1_pack)
rmemb1_f =Tk.Radiobutton(frame_memb1,text = 'From file',variable=varmemb1,value=3,command = file1_pack)
varmemb1.set(1)
frame_memb1.pack(side = 'top')
rmemb1_tr.pack(side = 'left')
rmemb1_n.pack(side = 'left')
rmemb1_f.pack(side = 'left')
frame_inp1 = Tk.Frame(root)
frame_inp1.pack()
label1_tr = Tk.Label(frame_inp1,text = "Number(format:'left num(+num_right for trapeze) right)")
label1_n = Tk.Label(frame_inp1,text = "Number(format:'mean variance')")
label1_tr.pack(side = 'top')
ent1 = Tk.Entry(frame_inp1)
ent1.pack(side='top')
label1_f_x = Tk.Label(frame_inp1,text = "Xes from file:")
fl1_x = Tk.StringVar()
file1_x_but = Tk.Button(frame_inp1, text="Select file", command=select_file1_x)
label1_file_x = Tk.Label(frame_inp1, textvariable = fl1_x)
label1_f_mu = Tk.Label(frame_inp1,text = "MUs from file:")
fl1_mu = Tk.StringVar()
file1_mu_but = Tk.Button(frame_inp1, text="Select file", command=select_file1_mu)
label1_file_mu = Tk.Label(frame_inp1, textvariable = fl1_mu)

frame_memb2 = Tk.Frame(root)
varmemb2 = Tk.IntVar()
rmemb2_tr = Tk.Radiobutton(frame_memb2,text='Triangle/trapeze',variable=varmemb2,value=1,command = trap2_pack)
rmemb2_n = Tk.Radiobutton(frame_memb2,text='Normal distribution',variable=varmemb2,value=2,command = norm2_pack)
rmemb2_f =Tk.Radiobutton(frame_memb2,text = 'From file',variable=varmemb2,value=3,command = file2_pack)
varmemb2.set(1)
frame_memb2.pack(side='top')
rmemb2_tr.pack(side='left')
rmemb2_n.pack(side='left')
rmemb2_f.pack(side = 'left')
frame_inp2 = Tk.Frame(root)
frame_inp2.pack()
label2_tr = Tk.Label(frame_inp2,text="Number(format:'left num(+num_right for trapeze) right)")
label2_n = Tk.Label(frame_inp2,text = "Number(format:'mean variance')")
label2_tr.pack(side='top')
ent2 = Tk.Entry(frame_inp2)
ent2.pack(side='top')
label2_f_x = Tk.Label(frame_inp2,text = "Xes from file:")
fl2_x = Tk.StringVar()
file2_x_but = Tk.Button(frame_inp2, text="Select file", command=select_file2_x)
label2_file_x = Tk.Label(frame_inp2, textvariable = fl2_x)
label2_f_mu = Tk.Label(frame_inp2, text = "MUs from file:")
fl2_mu = Tk.StringVar()
file2_mu_but = Tk.Button(frame_inp2, text="Select file", command=select_file2_mu)
label2_file_mu = Tk.Label(frame_inp2, textvariable = fl1_mu)

var=Tk.IntVar()
frame1 = Tk.Frame(root)
rbutton1=Tk.Radiobutton(frame1,text='+',variable=var,value=1)
rbutton2=Tk.Radiobutton(frame1,text='-',variable=var,value=2)
rbutton3=Tk.Radiobutton(frame1,text='*',variable=var,value=3)
rbutton4=Tk.Radiobutton(frame1,text='/',variable=var,value=4)
var.set(1)
rbutton1.pack(side='left')
rbutton2.pack(side='left')
rbutton3.pack(side='left')
rbutton4.pack(side='left')
frame1.pack(side='top')
label_method = Tk.Label(text="Method:")
label_method.pack(side='top')
var2=Tk.IntVar()
frame2 = Tk.Frame(root)
rbutton_m1=Tk.Radiobutton(frame2,text='Vertex method',variable=var2,value=1)
rbutton_m2=Tk.Radiobutton(frame2,text='DSW method',variable=var2,value=2)
var2.set(1)
rbutton_m1.pack(side='left')
rbutton_m2.pack(side='left')
frame2.pack(side='top')
label3 = Tk.Label(root,text="Filename(output file for x'es, default 'x_out')")
label3.pack()
ent3 = Tk.Entry(root)
ent3.pack()
label4 = Tk.Label(root,text="Filename(output file for mu's, default 'mu_out')")
label4.pack()
ent4 = Tk.Entry(root)
ent4.pack()
dir_but = Tk.Button(root, text="Select Directory", command=select_dir)
dir_but.pack()
label5 = Tk.Label(root, text = "Directory:")
label5.pack()
dr = Tk.StringVar()
dr.set(os.getcwd())
label6 = Tk.Label(root, textvariable = dr)
label6.pack()
calc = Tk.Button(root, text="Calculate", command=calculate)
calc.pack()
def _quit():
    root.quit()  
    root.destroy()

quit = Tk.Button(master=root, text='Quit', command=_quit)
quit.pack()

Tk.mainloop()

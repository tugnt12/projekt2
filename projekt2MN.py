import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import bisect

t = np.array([1.0, 2.0, 3.5, 5.0, 6.0, 9.0, 9.5])
y = np.array([3.0, 1.0, 4.0, 0.0, 0.5, -2.0, -3.0])
#Zad1
#funkcja sklejana stopnia 3
def H(t):
    return [t[i+1]-t[i] for i in range(len(t)-1)]

def d(n,h,y):    
    return [0] + [6*((y[i+1]-y[i])/h[i]-(y[i]-y[i-1])/h[i-1])/(h[i]+ h[i-1]) for i in range(1, n - 1)] + [0]

def tab(n,h):
    A = [h[i]/(h[i]+h[i + 1]) for i in range(n-2)] + [0]
    B = [2] * n
    C = [0]+[h[i + 1]/(h[i]+h[i + 1]) for i in range(n - 2)]
    return A,B,C

def roz_tab(A,B,C,D):
    c = C + [0]
    d = [0] * len(B)
    x = [0] * len(B)
    for i in range(1, len(B)):
        c[i] = c[i]/(B[i]-c[i-1]*A[i-1])
        d[i] = (D[i]-d[i-1]*A[i-1])/(B[i]-c[i-1]*A[i-1])
    for i in range(len(B)-2,-1,-1):
        x[i] = d[i]-c[i]*x[i+1]
    return x

def wy_skl(t,y):
    n = len(t)
    h = H(t)
    A, B, C = tab(n,h)
    D = d(n,h,y)
    M = roz_tab(A,B,C,D)
    Sx = [[(M[i+1]-M[i])*h[i]*h[i]/6,M[i]*h[i]*h[i]/2,(y[i+1]-y[i]-(M[i+1]+2*M[i])*h[i]*h[i]/6),y[i]] for i in range(n-1)]
    def skl(war):
        index = min(bisect.bisect(t,war)-1,n-2)
        Q = (war-t[index])/h[index]
        G = Sx[index]
        return (((G[0]*Q)+G[1])*Q+G[2])*Q+G[3]
    return skl

fskl = wy_skl(t, y)
xi = np.linspace(min(t), max(t), 1000)
yi = [fskl(xi) for xi in xi]

#Zad2
#Funkcja sklejana stopnia 1
data = np.array([[1.0, 3.0],[2.0, 1.0],[3.5, 4.0],[5.0, 0.0],[6.0, 0.5],[9.0, -2.0],[9.5, -3.0]])
x = np.linspace(1.0, 9.5, 200)
N = data.shape[0] -1
P_linear2 = np.zeros(x.shape)
P_linear = np.zeros(x.shape)
for n in range(N):
    if n==0:
        P_linear2 += ((data[n+1, 1] - data[n, 1]) / (data[n+1, 0] - data[n, 0]) * (x - data[n, 0])+ data[n, 1]) * (x <= data[n+1, 0])                   
    elif n==N-1:
        P_linear2 += ((data[n+1, 1] - data[n, 1]) / (data[n+1, 0] - data[n, 0]) * (x - data[n, 0])+ data[n, 1]) * (x > data[n, 0])
    else:
        P_linear2 += ((data[n+1, 1] - data[n, 1]) / (data[n+1, 0] - data[n, 0]) * (x - data[n, 0])+ data[n, 1]) * (x > data[n, 0])* (x <= data[n+1, 0])
#Lagrange
data = np.array([[1.0, 3.0],[2.0, 1.0],[3.5, 4.0],[5.0, 0.0],[6.0, 0.5],[9.0, -2.0],[9.5, -3.0]])
x = np.linspace(1.0, 9.5, 200)
def l(x,data):
    poly = np.ones((data.shape[0],x.shape[0]))
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if i != j:
                poly[i, :] *= (x - data[j,0]) / (data[i,0] - data[j,0])
    return poly
def pl(x,data):
    p = np.zeros(x.shape[0])
    pod = l(x,data)
    for n in range(data.shape[0]):
        p += pod[n,:] * data[n,1]
    return p
#Zad3
#Funkcja sklejana stopnia 3 w scipy
y_c = interp1d(t, y, kind ="cubic")
x_inter = np.linspace(np.min(t),np.max(t))
#Wykres 1
plt.plot(data[:,0],data[:,1],"ko")
plt.plot(x,pl(x,data),"green",label="Lagrange")
plt.plot(x, P_linear2, label='F.sklejana 1 stopnia')
plt.plot(xi, yi,"purple", label='F.sklejana 3 stopnia')
plt.plot(x_inter,y_c(x_inter),"red",label="F.sklejana stopnia 3 (scpiy)")
plt.grid(True)
plt.legend()
plt.show()
#Wykres 2
plt.title("Porównanie funkcji sklejanych 3 stopnia")
plt.plot(data[:,0],data[:,1],"ko")
plt.plot(xi, yi,"purple", label='F.sklejana 3 stopnia')
plt.plot(x_inter,y_c(x_inter),"red",label="F.sklejana stopnia 3 (scpiy)")
plt.legend()
plt.grid(True)
plt.show()




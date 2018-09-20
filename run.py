import numpy as np 
import matplotlib.pyplot as plt
import json
import requests
import math

APIKEY = "" # Get it from http://api.openweathermap.org/
ID = "" #Get it from JSON.

def penman_shuttle(m, R, G, U, L, d):
    return (m*R + G*6.43*(1+0.536*U)*d)/(L*(m+G))

def t_mean(a, b):
    return (a+b)/2

def slope(t):
    return 4098*(0.6108*math.e**((17.27*t)/(t+237.3))/(t+273)**2)

def pressure(h):
    return 101.3*((293-0.0065*h)/293)**5.26

def pcons(p):
    return 0.000665*p

def vap_def(t1, t2, hu):
    a = (0.618 * math.e**((17.27 * t1) / (t1 + 237.3)) + 0.618 * math.e**((17.27 * t2) / (t2 + 237.3)))/2
    b = (a)*hu/100
    return a-b

response = requests.get("http://api.openweathermap.org/data/2.5/weather/?id="+ID+"&appid="+APIKEY)
data = json.loads(response.text)

tmean = t_mean(data['main']['temp_min'], data['main']['temp_max'])
m = slope(tmean)
p = pressure(550)
G = pcons(p)
u = data['wind']['speed']
L = 2.45   # Google
R = 20.34  # http://www.indiaenvironmentportal.org.in/files/srd-sec.pdf
d = vap_def(data['main']['temp_min'], data['main']['temp_max'], data['main']['humidity'])
E = (penman_shuttle(m, R, G, u, L, d))
print(E)

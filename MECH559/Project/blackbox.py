import os
import math
import numpy as np
import copy
from numpy import cos, exp, pi, prod, sin, sqrt, subtract, inf
from DMDO import USER
user = USER
user.DENSITY = 7250 
user.mu = 0.4
user.PRESSURE = 1194000
user.TOL = 0.05
user.alpha = 0.000011
user.SIGMA = 200000000
user.poison = 0.3
user.VELOCITY = 50
user.THETA = math.pi*.25
user.H = 10
def structure(x):
  """
  This is first sub-sytem of the problem, structural analysis
  r_0 = upper brake pad radius
  r_i = lower brake pad radius
  r_rotor = rotor radius 
  t = thickness of the rotor
  r_c = centre radius
  r = radius of holes
  tol = tolerence by thermal stress
  omega = Angular velocity of rotor
  outputs --> stress, braking distance
  """
  inputs = {}
  for input_name,value in zip(["r_rotor","r_0","ri","t","r_c", "r","tol","r_k"],x): 
    inputs[input_name] = value

  # Wt = inputs["We"]+inputs["Wf"]+inputs["Ws"] # total weight
  s = inputs["r_rotor"] - inputs["r_0"] 
  omega = (user.VELOCITY/inputs["r_rotor"])
  volume = 2*math.pi*inputs["t"]*((inputs["r_rotor"]**2)-(inputs["r_c"]**2)-4*(inputs["r"]**2)) #volume of rotor
  dist  = ((user.DENSITY*volume*(user.VELOCITY**2)))/(4*user.MU*user.PRESSURE*user.THETA*(inputs["r_0"]**2 - inputs["ri"]**2)) #braking distance
  stress = (3+user.poison)*((user.DENSITY*(omega**2)/8))*(inputs["r_0"]+s - inputs["r_c"])**2
  # difference = inputs["tol"] - user.TOL
  return [stress, dist] # these are your responses

def thermal(x):
  """
  r_rotor = rotor as a input from structure analysis
  omega = Angular velocity of the rotor 
  t = thickness of the rotor
  r_0 = outer radius of the pad
  r_i = inner radius of the pad
  r_eq = equivalent radius
  r_c = centre hole radius
  This function returns temperature difference and change in radius of the rotor
  """
  inputs = {}
  for input_name,value in zip(["r_rotor","t", "r_0", "r_i","r_c", "r"],x): # these are your targets
    inputs[input_name] = value

  #  THIS SECTION COMPUTE HEAT GENERATED BY ROTOR DURING BRAKING
  #  equivalent radius of the rotor where force is applied and heat is generated
  omega = (user.VELOCITY/inputs["r_rotor"])
  r_eq = (2/3)*((inputs["r_0"]**3) - (inputs["r_i"]**3))/((inputs["r_0"]**2) - (inputs["r_i"]**2))    
  area = 2*math.pi((inputs["r_rotor"]**2 - inputs["r_c"]**2 - 4*inputs["r"]**2)+ inputs["r_rotor"]*inputs["t"])
  # delta_Q = 0.9*user.mu* r_eq * user.OMEGA - user.H*area*del_T
  del_T = (0.9*user.mu*r_eq*omega)/(user.H*area*math.pi*2)
  tol = user.alpha*del_T

  return [tol, del_T]

# %% Constants
user = USER
#define constants here
user.DENSITY = 7250 
user.mu = 0.4
user.PRESSURE = 1194000
user.TOL = 0.05
user.alpha = 0.000011
user.SIGMA = 200000000
user.poison = 0.3
user.VELOCITY = 50
user.THETA = math.pi*.25
user.H = 10
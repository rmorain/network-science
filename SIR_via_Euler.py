#########################################
# Practicing with the SIR differential equation model using simple numerical integration
#
# Michael Goodrich
# Brigham Young University
# CS 575 -- winter 2022, updated for winter 2023
##########################################


#########################################
# Set up plotting
#########################################
import numpy as np
import matplotlib as mpl
# mpl.use('tkagg')
from matplotlib import pyplot as plt

#########################################
# Functions used for numerical integration
# Defined to allow different types of numerical integration
#########################################
def f(s,i,r,beta,gamma,N): 
    # From dS/dt equation
    return -beta*i*s/N 
def g(s,i,r,beta,gamma,N): 
    # From dI/dt equation
    return beta*i*s/N - gamma*i
def h(s,i,r,beta,gamma,N): 
    # From dR/dt equation
    return gamma*i

def SIR_via_Euler(N=1000, beta=.4, gamma=.1, dt=0.1, duration=140, ax=None):
    #########################################
    # SIR model parameters
    #########################################
    # N = 1000        # Population size
    # beta = .4       # Play with .2, .4, .8, .99 in class
    # gamma = .1      # Rate at which infectious individuals recover
    # dt = 0.1        # Numerical integration time step
    # duration = 140  # Simulation duration 

    #########################################
    # Initialize states of the population
    #########################################
    S = [N-1]
    I = [1]
    R = [0]
    t = [0]

    #########################################
    # Use numerical integration to estimate time series
    # Euler method
    #########################################
    while t[-1] < duration:
        s = S[-1]; i = I[-1]; r = R[-1] # Get most recent population value
        S.append(s + dt*f(s,i,r,beta,gamma,N))
        I.append(i + dt*g(s,i,r,beta,gamma,N))
        R.append(r + dt*h(s,i,r,beta,gamma,N))
        t.append(t[-1]+dt)
        
    if ax:
        ax.plot(t,S,'r',t,I,'g--',t,R,'b:')
        ax.legend(['S','I','R'])
        title = 'SIR model via Euler: beta = ' + str(beta) + ', gamma = ' + str(gamma) + ', and R0 = ' + str(round(beta/gamma,2))
        ax.set_title(title)
    else:
        plt.figure(1)
        plt.plot(t,S,'r',t,I,'g--',t,R,'b:')
        plt.legend(['S','I','R'])
        title = 'SIR model via Euler: beta = ' + str(beta) + ', gamma = ' + str(gamma) + ', and R0 = ' + str(beta/gamma)
        plt.title(title)
        # plt.waitforbuttonpress()

    #########################################
    # Repeat using a slightly more sophisticated numerical integration method
    #########################################
    
    #########################################
    # Initialize states of the population
    #########################################
    S = [N-1]
    I = [1]
    R = [0]
    t = [0]
    
    #########################################
    # Use numerical integration to estimate time series
    # Midpoint method
    #########################################
    while t[-1] < duration:
        s = S[-1]; i = I[-1]; r = R[-1]
        s1 = s + dt/2*f(s,i,r,beta,gamma,N)
        r1 = r + dt/2*g(s,i,r,beta,gamma,N)
        i1 = i + dt/2*h(s,i,r,beta,gamma,N)
        S.append(s + dt*f(s1,i1,r1,beta,gamma,N))
        I.append(i + dt*g(s1,i1,r1,beta,gamma,N))
        R.append(r + dt*h(s1,i1,r1,beta,gamma,N))
        t.append(t[-1]+dt)
    
    #  Uncomment if you'd like to compare results from the two integration methods
    #plt.figure(2)
    #plt.plot(t,S,'r',t,I,'g--',t,R,'b:')
    #plt.legend(['S','I','R'])
    #title = 'SIR model via midpoint: beta = ' + str(beta) + ', gamma = ' + str(gamma) + ', and R0 = ' + str(beta/gamma)
    #plt.title(title)
    #plt.waitforbuttonpress()


# main()



# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:45:20 2016

@author: manimaran.nellai
"""

import scipy as sp
import pylab as plt
import pandas as pd
from scipy.integrate import odeint

class HodgkinHuxley():
    """Full Hodgkin-Huxley Model implemented in Python"""

    C_m  =   1.0
    """membrane capacitance, in uF/cm^2"""

    g_Na = 120.0
    """Sodium (Na) maximum conductances, in mS/cm^2"""

    g_K  =  36.0
    """Postassium (K) maximum conductances, in mS/cm^2"""

    g_L  =   0.3
    """Leak maximum conductances, in mS/cm^2"""

    E_Na =  50.0
    """Sodium (Na) Nernst reversal potentials, in mV"""

    E_K  = -77.0
    """Postassium (K) Nernst reversal potentials, in mV"""

    E_L  = -54.387
    """Leak Nernst reversal potentials, in mV"""

#    t = sp.arange(0.0, 450.0, 0.01)
    t = sp.arange(0.0,450,1)
    """ The time to integrate over """

    def alpha_m(V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.1*(V+40.0)/(1.0 - sp.exp(-(V+40.0) / 10.0))

    def beta_m(V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 4.0*sp.exp(-(V+65.0) / 18.0)

    def alpha_h(V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.07*sp.exp(-(V+65.0) / 20.0)

    def beta_h(V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 1.0/(1.0 + sp.exp(-(V+35.0) / 10.0))

    def alpha_n(V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.01*(V+55.0)/(1.0 - sp.exp(-(V+55.0) / 10.0))

    def beta_n(V):
        """Channel gating kinetics. Functions of membrane voltage"""
        return 0.125*sp.exp(-(V+65) / 80.0)

    def I_Na(V, m, h):
        """
        Membrane current (in uA/cm^2)
        Sodium (Na = element name)

        |  :param V:
        |  :param m:
        |  :param h:
        |  :return:
        """
        return g_Na * m**3 * h * (V - E_Na)

    def I_K(V, n):
        """
        Membrane current (in uA/cm^2)
        Potassium (K = element name)

        |  :param V:
        |  :param h:
        |  :return:
        """
        return g_K  * n**4 * (V - E_K)
    #  Leak
    def I_L(V):
        """
        Membrane current (in uA/cm^2)
        Leak

        |  :param V:
        |  :param h:
        |  :return:
        """
        return g_L * (V - E_L)

    def I_inj(t):
        """
        External Current

        |  :param t: time
        |  :return: step up to 10 uA/cm^2 at t>100
        |           step down to 0 uA/cm^2 at t>200
        |           step up to 35 uA/cm^2 at t>300
        |           step down to 0 uA/cm^2 at t>400
        """
        return 10*(t>100) - 10*(t>200) + 35*(t>300) - 35*(t>400)

    @staticmethod
    def dALLdt(X, t):
        """
        Integrate

        |  :param X:
        |  :param t:
        |  :return: calculate membrane potential & activation variables
        """
        V, m, h, n = X
        print(str("t"),t)
        print(str("V"),V)
        print(str("m"),m)
        print(str("h"),h)
        print(str("n"),n)
        dVdt = (I_inj(t) - I_Na(V, m, h) - I_K(V, n) - I_L(V)) / C_m       
        dmdt = alpha_m(V)*(1.0-m) - beta_m(V)*m
        dhdt = alpha_h(V)*(1.0-h) - beta_h(V)*h
        dndt = alpha_n(V)*(1.0-n) - beta_n(V)*n
        
        print(str(t)+"\t"+str(I_inj(t))+"\t"+str(I_Na(V,m,h))+"\t"+str(I_K(V,n))+"\t"+str(I_L(v))+"\t"+
        str(V)+"\t"+str(dVdt)+"\t"+str(m)+"\t"+str(dmdt)+"\t"+str(h)+"\t"+str(dhdt)+"\t"+str(n)+"\t"+str(dndt))
#        print(str("dVdt"),str(dVdt))
#        print(str("dmdt"),str(dmdt))
#        print(str("dhdt"),str(dhdt))
#        print(str("dndt"),str(dndt))
#        print("**************\n")
        
        return dVdt, dmdt, dhdt, dndt
       

    def Main(self):
        """
        `Main demo for the Hodgkin Huxley neuron model
        """
#        foutall = open("E://ASSET_VALIDATOR//Modelling//outputdall.txt","w")
#        for tx in t:
#            Temp = dALLdt([-65, 0.05, 0.6, 0.32],tx)
#            print(Temp)
#            foutall.write(str(tx)+"\t"+str("\t".join([str(Te) for Te in Temp]))+"\n")
#        foutall.close()
        X = odeint(dALLdt, [-65, 0.05, 0.6, 0.32], t)
#        print(len(X))
#        print(X)
        fout = open("E://ASSET_VALIDATOR//Modelling//output.txt","w")
        for xj in X:
            fout.write(str(str("\t".join([str(y) for y in xj]))+"\n"))
#        print(X)
        fout.close()
        V = X[:,0]
        m = X[:,1]
        h = X[:,2]
        n = X[:,3]
        DT = pd.DataFrame(X)
        DT.to_csv("E://ASSET_VALIDATOR//Modelling//param.txt",sep="\t")
        ina = I_Na(V, m, h)
        ik = I_K(V, n)
        il = I_L(V)

        plt.figure()

        plt.subplot(4,1,1)
        plt.title('Hodgkin-Huxley Neuron')
        plt.plot(t, V, 'k')
        plt.ylabel('V (mV)')

        plt.subplot(4,1,2)
        plt.plot(t, ina, 'c', label='$I_{Na}$')
        plt.plot(t, ik, 'y', label='$I_{K}$')
        plt.plot(t, il, 'm', label='$I_{L}$')
        plt.ylabel('Current')
        plt.legend()

        plt.subplot(4,1,3)
        plt.plot(t, m, 'r', label='m')
        plt.plot(t, h, 'g', label='h')
        plt.plot(t, n, 'b', label='n')
        plt.ylabel('Gating Value')
        plt.legend()

        plt.subplot(4,1,4)
        i_inj_values = [I_inj(t) for t in t]
        plt.plot(t, i_inj_values, 'k')
        plt.xlabel('t (ms)')
        plt.ylabel('$I_{inj}$ ($\\mu{A}/cm^2$)')
        plt.ylim(-1, 40)

        plt.show()

if __name__ == '__main__':
    runner = HodgkinHuxley()
    runner.Main()
# -*- coding: utf-8 -*-
"""Copyright 2014 Roger R Labbe Jr.

This is licensed under an MIT license. See the readme.MD file
for more information.
"""

from __future__ import (division, print_function)
import numpy as np
import numpy.linalg as linalg

class RKSSmoother(object):
    """ Rauch-Tung-Striebal Kalman smoother. 
    
    Computes a smoothed sequence from a set of measurements.
    """
    
    def __init__(self):
        pass
        
        
    def smooth(self, Ms, Ps, F, Q):
        """ Runs the Rauch-Tung-Striebal Kalman smoother on a set of
        means and covariances computed by a Kalman filter. The usual input
        would come from the output of `KalmanFilter.batch_filter()`.
        
        Parameters
        ----------
        
        Ms : numpy.array
           array of the means (state variable x) of the output of a Kalman
           filter. 
           
        Ps : numpy.array
            array of the covariances of the output of a kalman filter.
            
        F : numpy.array
            State transition function of the Kalman filter
            
        Q : numpy.array
            Process noise of the Kalman filter
            
            
        Returns
        -------
        'M' : numpy.array
           smoothed means
           
        'P' : numpy.array
           smoothed state covariances
           
        'D' : numpy.array
            
        """
        M = np.copy(Ms)
        P = np.copy(Ps)
        assert len(M) == len(P)
        
        n     = np.size(M,0)  # number of measurements
        dim_x = np.size(M,1)  # number of state variables
        
        D = np.zeros((n,dim_x,dim_x))

        
        for k in range(n-2,-1,-1):
            P_pred = F.dot(P[k]).dot(F.T) + Q
            #D[k,:,:] = linalg.solve(P[k].dot(F.T).T, P_pred.T)
            D[k,:,:] = P[k].dot(linalg.solve((F.T).T, P_pred.T))
            M[k] = M[k] + D[k].dot(M[k+1] - F.dot(M[k]))
            P[k,:,:] = P[k,:,:] + D[k].dot(P[k+1,:,:] - P_pred).dot(D[k].T)
        
          
        return (M,P,D)    

if __name__ == '__main__':
    from filterpy.kalman import KalmanFilter
    from numpy import random
    import matplotlib.pyplot as plt
    

    f = KalmanFilter (dim_x=2, dim_z=1)

    f.x = np.array([[2.],
                    [0.]])        # initial state (location and velocity)

    f.F = np.array([[1.,1.],
                    [0.,1.]])     # state transition matrix

    f.H = np.array([[1.,0.]])     # Measurement function
    f.P *= .01                     # covariance matrix
    f.R *= 5                      # state uncertainty
    f.Q *= 0.0001                 # process uncertainty

    f.P[0,0] = 1

    zs = [t + random.randn()*20 for t in range (100)]
    m,c = f.batch_filter(zs)
    

    smoother = RKSSmoother()
    m2, c2, d = smoother.smooth(m, c, f.F, f.Q)
    for i in range(0):
        m2[i]=m2[-1]

    
    # plot data
    p1, = plt.plot(zs,'r', alpha=0.5)
    p2, = plt.plot (m[:,0],'b')
    p4, = plt.plot(m2[:,0], 'm')
    p3, = plt.plot ([0,100],[0,100], 'g') # perfect result
    plt.legend([p1,p2, p3, p4], 
               ["noisy measurement", "KF output", "ideal", "smooth"], 4)


    plt.show()  
        

            
            
        


            























import numpy as np

import FT

def fit(L, N):    
    def norm(index1, index2):
        NORM = 0
        while(index1 != index2):
            (x1, y1) = (L[index1][0], L[index1][1])
            (x2, y2) = (L[(index1+1)%len(L)][0], L[(index1+1)%len(L)][1])
            NORM += ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            
            index1 = (index1+1)%len(L)
        return NORM
        
    assert len(L) >= N    
    LENGTH = norm(0,1) + norm(1,0)
    
    L_FIT = [(L[0][0], L[0][1])]
    L_FIT_INDEX = [0]
    
    for i in range(1, N):
        BEST_ERROR = LENGTH
        BEST_INDEX = None
        (x, y) = (None, None)
        
        for j in range(L_FIT_INDEX[-1], len(L)):
            NOW_ERROR = abs(norm(0, j) - (i / N * LENGTH))
           
            if NOW_ERROR < BEST_ERROR:
                BEST_ERROR = NOW_ERROR
                BEST_INDEX = j
                (x, y) = (L[j][0], L[j][1])
                
            if norm(0, j) > (i / N * LENGTH):
                break   
        
        L_FIT_INDEX.append(BEST_INDEX)
        L_FIT.append((x, y))
        
    return L_FIT
        

class Points():
        def __init__(self):
            self.pt = []
            self.N = 0
        
        def __len__(self):
            return len(self.pt)
        
        def addpoint(self, point):           
            assert type(point) is tuple
            self.pt.append(point)
            
        def reset(self):
            self.pt = []
            
        def __str__(self):
            return str(self.pt)
        
        def lfit(self):
            return fit(self.pt, 2 * self.N - 1)
        
        def ft(self):
            
            L_FIT = self.lfit()
            L_COMPLEX = []
            
            for i in range(1-self.N, self.N):
                L_COMPLEX.append(L_FIT[i][0] + 1j * L_FIT[i][1])
                
            RES_CARTESIAN =  FT.ft(L_COMPLEX)
            
            RES_POLAR = [0] * (2*self.N - 1)
            
            for i in range(1-self.N, self.N):
                r = np.absolute(RES_CARTESIAN[i])
                theta = np.angle(RES_CARTESIAN[i])
                RES_POLAR[i] = (r, theta)
            
            return RES_POLAR
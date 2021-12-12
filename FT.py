import numpy as np

def ft(L):
    assert len(L)%2 == 1
    
    N = (len(L) + 1) // 2   
    L_FT = [0] * (2*N-1)
    
    for i in range(1-N,N):
        SUM = 0
        
        for j in range(1-N,N):
            SUM += L[j] * np.exp(1j * (-2) * np.pi * (i*j) / (2*N-1))
            
        L_FT[i] = SUM / (2*N-1)
        
    return L_FT
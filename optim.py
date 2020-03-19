import torch
import numpy as np

class Adam():
    '''
    Custom Adam Optimiser
    :param parameters -> weights of the model to be optimised
    :param lr -> learning rate of the optimiser
    '''
    def __init__(self, parameters, lr, b1 = 0.9, b2 = 0.999, eps = 1e-08):
        self.parameters = list(parameters)
        self.alpha = lr
        self.b1 = b1
        self.b2 = b2
        self.t = 0
        self.eps = eps
        
        ##Initialising the first and second moments
        self.m = []
        self.v = []
        for param in self.parameters:
            x = np.zeros(param.shape)
            self.m.append(torch.Tensor(x.copy()))
            self.v.append(torch.Tensor(x.copy()))
            
    def step(self):
        self.t+=1
        stepsize = self.alpha*((1-self.b2**self.t)**0.5)/(1-self.b1**self.t)
        for i,param in enumerate(self.parameters):
            if param.grad is not None:
                self.m[i].mul_(self.b1)
                self.m[i].add_(1-self.b1,param.grad.data)
                self.v[i].mul_(self.b2)
                self.v[i].addcmul_(1-self.b2,param.grad.data,param.grad.data)

                param.data.addcdiv_(-stepsize,self.m[i],self.v[i].sqrt()+self.eps)
            

    def zero_grad(self):
        for param in self.parameters:
            if param.grad is not None:
                param.grad.zero_()
            
            
    

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

class JuliaSet:
    def __init__(self, step, val_bound, iter_bound, c, colored):
        self.step = step
        self.val_bound = val_bound
        self.iter_bound = iter_bound
        self.c = c
        self.colored = colored
        self.RGB_COLORS = [np.random.choice(range(256), size=3) for i in range(self.iter_bound+1)]
        self.GRAY_COLORS = [np.array([x,x,x]) for x in np.random.choice(range(256), size=self.iter_bound+1)]

    def iter_at_divergence(self, p0):
        '''
            z=z^2+c until divergence or not condition
            c fixed
        '''
        z = p0 #Succession start at complex specified
        i=0 #Iteration

        while i<self.iter_bound and abs(z) < self.val_bound:
            z = z**2 + self.c
            i+=1

        if self.colored:
            return self.RGB_COLORS[i]
        else:
            return self.GRAY_COLORS[i]

    def plot(self, start_x, end_x, start_y, end_y):
        x_samples = np.arange(start_x, end_x, self.step)
        y_samples = np.arange(start_y, end_y, self.step)
        img = np.full((len(y_samples), len(x_samples), 3),0)

        for i in range(len(y_samples)):
            for j in range(len(x_samples)):
                img[i][j] = self.iter_at_divergence(complex(x_samples[j], y_samples[i]))

        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])
        plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('julia_set.png')

class MandelbrotSet:
    def __init__(self, step, val_bound, iter_bound, colored=True):
        self.step = step
        self.val_bound = val_bound
        self.iter_bound = iter_bound
        self.colored = colored
        self.RGB_COLORS = [np.random.choice(range(256), size=3) for i in range(self.iter_bound+1)]
        self.GRAY_COLORS = [np.array([x,x,x]) for x in np.random.choice(range(256), size=self.iter_bound+1)]

    def iter_at_divergence(self, c):
        '''
        Return the iteration in which diverges
        z=z^2+c until divergence or maximum iterations reached
        '''
        z = c #Succession start
        i=0 #Iteration

        while i < self.iter_bound and abs(z) < self.val_bound:
            z = z**2 + c
            i+=1

        if self.colored:
            return self.RGB_COLORS[i]
        else:
            return self.GRAY_COLORS[i]

    def plot(self, start_x, end_x, start_y, end_y):
        x_samples = np.arange(start_x, end_x, self.step)
        y_samples = np.arange(start_y, end_y, self.step)
        img = np.full((len(y_samples), len(x_samples), 3),0)

        for i in range(len(y_samples)):
            for j in range(len(x_samples)):
                img[i][j] = self.iter_at_divergence(complex(x_samples[j], y_samples[i]))

        fig = plt.figure('Mandelbrot fractal', figsize=[8,8])
        plt.imshow(img, extent=[start_x,end_x,start_y,end_y])
        plt.title('Complex plane')
        plt.xlabel('Real')
        plt.ylabel('Img')
        plt.show()
        fig.savefig('mandelbrot_set.png')


if __name__=='__main__':
    colored = True
    
    m = MandelbrotSet(1e-3, 3, 40, colored)
    m.plot(-2.1, 0.6, -1.4, 1.4)
    #m.plot(-1.48, -1.42, -0.02, 0.02)
    j = JuliaSet(1e-3, 3, 30, complex(0.2,0.6), colored)
    j.plot(-2, 2, -2, 2)
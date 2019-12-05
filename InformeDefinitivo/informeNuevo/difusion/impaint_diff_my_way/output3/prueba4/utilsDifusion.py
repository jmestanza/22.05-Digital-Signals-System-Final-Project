import numpy as np
import cv2
import numpy as np
import warnings
import cv2
from PIL import Image

def genSquare(square_size):
    first = True
    for i in range(square_size):
        for j in range(square_size):
            aux = np.array([i - square_size // 2, j - square_size // 2])
            if first:
                square = np.array([aux])
                first = False
            else:
                square = np.append(square, np.array([aux]), axis=0)
    return square


def jpeg2MatrixMask(mask):
    # lower y upper son bounds para buscar el color negro con la funcion inRange
    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = cv2.inRange(mask, lower, upper)
    return shapeMask

def getGradient(grey_scale):
    # gradiente en x e y de la escala de grises, sobel suaviza el gradiente
    sobel_x = cv2.Sobel(grey_scale, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(grey_scale, cv2.CV_64F, 0, 1, ksize=5)

    return sobel_x, sobel_y

def drawRect(image, pos, sq_sz, color):
    x, y = pos
    for i in range(-sq_sz // 2, sq_sz // 2):
        for j in range(-sq_sz // 2, sq_sz // 2):
            image[y + i][x + j] = color
    return


def anisodiff(img,niter=1,kappa=50,gamma=0.1,step=(1.,1.),option=1,ploton=False):
    """
    Anisotropic diffusion.

    Usage:
    imgout = anisodiff(im, niter, kappa, gamma, option)

    Arguments:
        img    - input image
        niter  - number of iterations
        kappa  - conduction coefficient 20-100 ?
        gamma  - max value of .25 for stability
        step   - tuple, the distance between adjacent pixels in (y,x)
        option - 1 Perona Malik diffusion equation No 1
                 2 Perona Malik diffusion equation No 2
        ploton - if True, the image will be plotted on every iteration

    Returns:
        imgout   - diffused image.

    kappa controls conduction as a function of gradient.  If kappa is low
    small intensity gradients are able to block conduction and hence diffusion
    across step edges.  A large value reduces the influence of intensity
    gradients on conduction.

    gamma controls speed of diffusion (you usually want it at a maximum of
    0.25)

    step is used to scale the gradients in case the spacing between adjacent
    pixels differs in the x and y axes

    Diffusion equation 1 favours high contrast edges over low contrast ones.
    Diffusion equation 2 favours wide regions over smaller ones.

    Reference:
    P. Perona and J. Malik.
    Scale-space and edge detection using ansotropic diffusion.
    IEEE Transactions on Pattern Analysis and Machine Intelligence,
    12(7):629-639, July 1990.

    Original MATLAB code by Peter Kovesi
    School of Computer Science & Software Engineering
    The University of Western Australia
    pk @ csse uwa edu au
    <http://www.csse.uwa.edu.au>

    Translated to Python and optimised by Alistair Muldal
    Department of Pharmacology
    University of Oxford
    <alistair.muldal@pharm.ox.ac.uk>

    June 2000  original version.
    March 2002 corrected diffusion eqn No 2.
    July 2012 translated to Python
    """

    # ...you could always diffuse each color channel independently if you
    # really want
    if img.ndim == 3:
        warnings.warn("Only grayscale images allowed, converting to 2D matrix")
        img = img.mean(2)

    # initialize output array
    img = img.astype('float32')
    imgout = img.copy()

    # initialize some internal variables
    deltaS = np.zeros_like(imgout)
    deltaE = deltaS.copy()
    NS = deltaS.copy()
    EW = deltaS.copy()
    gS = np.ones_like(imgout)
    gE = gS.copy()

    # create the plot figure, if requested
    if ploton:
        import pylab as pl
        from time import sleep

        fig = pl.figure(figsize=(20,5.5),num="Anisotropic diffusion")
        ax1,ax2 = fig.add_subplot(1,2,1),fig.add_subplot(1,2,2)

        ax1.imshow(img,interpolation='nearest')
        ih = ax2.imshow(imgout,interpolation='nearest',animated=True)
        ax1.set_title("Original image")
        ax2.set_title("Iteration 0")

        fig.canvas.draw()

    for ii in range(niter):
        # calculate the diffs
        deltaS[:-1,: ] = np.diff(imgout,axis=0)
        deltaE[: ,:-1] = np.diff(imgout,axis=1)

    # conduction gradients (only need to compute one per dim!)
    if option == 1:
        gS = np.exp(-(deltaS/kappa)**2.)/step[0]
        gE = np.exp(-(deltaE/kappa)**2.)/step[1]
    elif option == 2:
        gS = 1./(1.+(deltaS/kappa)**2.)/step[0]
        gE = 1./(1.+(deltaE/kappa)**2.)/step[1]

    # update matrices
    E = gE*deltaE
    S = gS*deltaS

    # subtract a copy that has been shifted 'North/West' by one
    # pixel. don't as questions. just do it. trust me.
    NS[:] = S
    EW[:] = E
    NS[1:,:] -= S[:-1,:]
    EW[:,1:] -= E[:,:-1]

    # update the image
    imgout += gamma*(NS+EW)

    if ploton:
        iterstring = "Iteration %i" %(ii+1)
        ih.set_data(imgout)
        ax2.set_title(iterstring)
        fig.canvas.draw()
        # sleep(0.01)

    return imgout


def anisoDiffusion(img, its, mode):
    B = img[:,:,0]
    G = img[:,:,1]
    R = img[:,:,2]

    B_anis = anisodiff(B,niter=its)
    G_anis = anisodiff(G,niter=its)
    R_anis = anisodiff(R,niter=its)

    img_to_store = np.zeros_like(img)
    if mode == 'RGB':
        img_to_store[:,:,0] = R_anis
        img_to_store[:,:,1] = G_anis
        img_to_store[:,:,2] = B_anis
    elif mode == 'BGR':
        img_to_store[:, :, 0] = B_anis
        img_to_store[:, :, 1] = G_anis
        img_to_store[:, :, 2] = R_anis

    return img_to_store


#img = cv2.imread('output3/imgred.jpeg', 3)# matriz, cada el es un RGB
#im = Image.fromarray(anisoDiffusion(img))
#im.save("output3/imagen" + "anisotrop" + ".jpeg")

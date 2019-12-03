import matplotlib.pyplot as plt
import numpy as np
import cv2
img = cv2.imread('kitten_raya.jpeg', 3)# matriz, cada el es un RGB
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

# id_kernel = np.array(([0, 0, 0],
#                       [0, 1, 0],
#                       [0, 0, 0]),
#                        np.float32)

#output = cv2.filter2D(img, -1, id_kernel)

a = 0.073235
b = 0.176765
c = 0.125

#n1_kernel = np.array(([a, b, a],
#                      [b, 0, b],
#                      [a, b, a]),
#                       np.float32)
# output = cv2.filter2D(img, -1, n1_kernel)


n1_kernel = np.array(([c, c, c],
                      [c, 0, c],
                      [c, c, c]),
                       np.float32)
output = img
for i in range(100):
    output = cv2.filter2D(output, -1, n1_kernel)


# n1_kernel = np.array(([-1, -1, -1],
#                       [-1, 8, -1],
#                       [-1, -1, -1]),
#                        np.float32)
#output = cv2.filter2D(img, -1, n1_kernel)

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(output)
plt.title('Filtered Image')

plt.show()

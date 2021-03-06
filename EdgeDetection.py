#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def Sobel(arr,rstart, cstart,masksize, divisor):
  sum = 0;
  x = 0
  y = 0

  for i in range(rstart, rstart+masksize, 1):
    x = 0
    for j in range(cstart, cstart+masksize, 1):
        if x == 0 and y == 0:
            p1 = arr[i][j]
        if x == 0 and y == 1:
            p2 = arr[i][j]
        if x == 0 and y == 2:
            p3 = arr[i][j]
        if x == 1 and y == 0:
            p4 = arr[i][j]
        if x == 1 and y == 1:
            p5 = arr[i][j]           
        if x == 1 and y == 2:
            p6 = arr[i][j]
        if x == 2 and y == 0:
            p7 = arr[i][j]
        if x == 2 and y == 1:
            p8 = arr[i][j]
        if x == 2 and y == 2:
            p9 = arr[i][j]
        x +=1
    y +=1
  return np.abs((p1 + 2*p2 + p3) - (p7 + 2*p8+p9)) + np.abs((p3 + 2*p6 + p9) - (p1 + 2*p4 +p7)) 


def padwithzeros(vector, pad_width, iaxis, kwargs):
   vector[:pad_width[0]] = 0
   vector[-pad_width[1]:] = 0
   return vector

im = cv2.imread("image.jpg", cv2.IMREAD_COLOR)
cv2.imshow("input", im)
img = np.asarray(im)
img.flags.writeable = True
p = 1
k = 2
m = img.shape[0]
n = img.shape[1]
masksize = 3
img = np.lib.pad(img, p, padwithzeros) #this function padds image with zeros to cater for pixels on the border.
x = 0
y = 0
for row in img:
  y = 0
  for col in row:
    if not (x < p or y < p or y > (n-k) or x > (m-k)):
        img[x][y] = Sobel(img, x-p,y-p,masksize,masksize*masksize)
    y = y + 1
  x = x + 1

img2 = Image.fromarray(img)
img2.show()


# In[4]:


import numpy as np
import cv2
import argparse
import matplotlib.pyplot as plt


def sobel_edge_detection(image, filter, verbose=False):
    new_image_x = convolution(image, filter, verbose)

    if verbose:
        plt.imshow(new_image_x, cmap='gray')
        plt.title("Horizontal Edge")
        plt.show()

    new_image_y = convolution(image, np.flip(filter.T, axis=0), verbose)

    if verbose:
        plt.imshow(new_image_y, cmap='gray')
        plt.title("Vertical Edge")
        plt.show()

    gradient_magnitude = np.sqrt(np.square(new_image_x) + np.square(new_image_y))

    gradient_magnitude *= 255.0 / gradient_magnitude.max()

    if verbose:
        plt.imshow(gradient_magnitude, cmap='gray')
        plt.title("Gradient Magnitude")
        plt.show()

    return gradient_magnitude

def convolution(image, kernel, average=False, verbose=False):
    if len(image.shape) == 3:
        print("Found 3 Channels : {}".format(image.shape))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Converted to Gray Channel. Size : {}".format(image.shape))
    else:
        print("Image Shape : {}".format(image.shape))

    print("Kernel Shape : {}".format(kernel.shape))

    if verbose:
        plt.imshow(image, cmap='gray')
        plt.title("Image")
        plt.show()

    image_row, image_col = image.shape
    kernel_row, kernel_col = kernel.shape

    output = np.zeros(image.shape)

    pad_height = int((kernel_row - 1) / 2)
    pad_width = int((kernel_col - 1) / 2)

    padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))

    padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image

    if verbose:
        plt.imshow(padded_image, cmap='gray')
        plt.title("Padded Image")
        plt.show()

    for row in range(image_row):
        for col in range(image_col):
            output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])
            if average:
                output[row, col] /= kernel.shape[0] * kernel.shape[1]

    print("Output Image size : {}".format(output.shape))

    if verbose:
        plt.imshow(output, cmap='gray')
        plt.title("Output Image using {}X{} Kernel".format(kernel_row, kernel_col))
        plt.show()
        
    return output

def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


def gaussian_kernel(size, sigma=1, verbose=False):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)

    kernel_2D *= 1.0 / kernel_2D.max()

    if verbose:
        plt.imshow(kernel_2D, interpolation='none', cmap='gray')
        plt.title("Kernel ( {}X{} )".format(size, size))
        plt.show()

    return kernel_2D


def gaussian_blur(image, kernel_size, verbose=False):
    kernel = gaussian_kernel(kernel_size, sigma=math.sqrt(kernel_size), verbose=verbose)
    return convolution(image, kernel, average=True, verbose=verbose)


if __name__ == '__main__':
    filter = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])
    image = gaussian_blur(image, 9, verbose=True)
    sobel_edge_detection(image, filter, verbose=True)


# In[ ]:





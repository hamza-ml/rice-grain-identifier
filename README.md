# Rice Grain Identifier (RGI)

## Introduction:
### Python program that does following:
- Identifies differnt type of rice grains from a given image.
- Extract their dimensions.
- Save their dimensions in an excel file.

## How to run this project:
- Download and subsequently open this repo in VS Code.
- Make sure the sample image are placed in the same directory as the **source.py file**.

## Data Set Acquisition:
The data gathering process for this project included taking pictures of rice grains of several rice types in specific conditions, i.e. 8 to 10 rice grains of the same rice type were placed in a cardboard box along with a reference object (5 rupee coin) and a universal object (in this case, a coke bottle cap) for the purpose of streamlining the identification and categorizing process.

## Process
1. Read RGB image as greyscale using **skimage.io library**.
2. Convert greyscale image to a binary image by taking threshold of the image.
3. Perform binary closing functio (dilation then erosion) with an enlarging structuring element on the resultant image to remove the noise and smooth the image.
4. After the binary image is smoothed perfectly, label the image and generate bounding box around the reference object and the rice grains using **skimage library's** measure label and regionprops functions. Traverse the complete labeled image in a loop in order to generate bounding boxes.
5. Bounding box will provide orientation, dimensions, and diameter of rice grains as well as the reference object, from which the diameter of the coin will be used to compute a pixel-per-cm value, which will be further used to determine height and width of each grain inside the morphed image. The diameter of the coin will be gathered via a loop with eccentricity value less than 0.2, as it will identify a round object inside the image.
6. Pixel value formula is - ***Pixel Value = Coin-Diameter/Total-Pixels***.
7 - Extracts the measurements (height, width, intensity level, and average color) of rice grains and compute their height & width values using the above-computed pixel value.
8 - Find orientation (angle) of each rice grain, convert it from radians to a degree and crop each of the selected rice grain as a separate image.
9 - Use below formula to rotate the cropped image and to make a 90-degree angle of the rice grain: ***90-degree - (Image Angle - 1)***.
10 - Pad the cropped image with 0s, to prepare it for cropping without affecting the corners of the rice grains.
11 - Apply **scipy’s** rotate and interpolation functions on the cropped image.
12 - Repeat step 4 and crop the image according to its bounding box.
13 - Convert the resultant image into a grayscale as save it as a .tiff file with a unique name.
14 - Finally, save the gathered dimensions, new image name, its type, its average color ratio, and its intensity level into an excel file, for each rice grain in an image.

## Sample Image:

## Sample Results:

# Rice Grain Identifier (RGI)

## Introduction:
### Python program that does following:
- [x] Identifies different type of rice-grains from a given image.
- [x] Extract their dimensions.
- [x] Save their dimensions in an excel file.

## How to run this project:
- Download & subsequently open this repo in VS Code.
- Make sure the sample images are placed in the same directory as the ***source.py*** file.
- Open terminal and run following commands in order: 
  - ***pip install -r requirements.txt***
  - ***py source.py***

## Data Set Acquisition:
The data gathering process for this project included taking pictures of rice grains of several rice types in specific conditions, i.e. 8 to 10 rice grains of the same rice type were placed in a cardboard box along with a reference object (5 rupee coin) & a universal object (in this case, a coke bottle cap) for the purpose of streamlining the identification & categorizing process.

## Process:
**Step 1** - Read RGB image as greyscale using **skimage.io** library.

**Step 2** - Convert greyscale image to a binary image by taking threshold of the image.

**Step 3** - Perform binary closing function (dilation then erosion) with an enlarging structuring element on the resultant image to remove the noise & smooth the image.

**Step 4** - After the binary image is smoothed perfectly, label the image & generate bounding box around the reference object & the rice grains using **skimage** library's measure label & regionprops functions. Traverse the complete labeled image in a loop in order to generate bounding boxes.

**Step 5** - Bounding box will provide orientation, dimensions, & diameter of rice grains as well as the reference object, from which the diameter of the coin will be used to compute a pixel-per-cm value, which will be further used to determine height & width of each grain inside the morphed image. The diameter of the coin will be gathered via a loop with eccentricity value less than 0.2, as it will identify a round object inside the image.

**Step 6** - Pixel value formula is: 

```
Pixel Value = Coin-Diameter/Total-Pixels
```

**Step 7** - Extracts the measurements (height, width, intensity level, & average color) of rice grains & compute their height & width values using the above-computed pixel value.

**Step 8** - Find orientation (angle) of each rice grain, convert it from radians to degree & crop each of the selected rice grain as a separate image.

**Step 9** - Use following formula to rotate the cropped image & to make a 90-degree angle of the rice grain: 

```
Rotate image to 90 = 90-degree - (Image Angle - 1)
```

**Step 10** - Pad the cropped image with 0s, to prepare it for cropping without affecting the corners of the rice grains.

**Step 11** - Apply **scipy’s** rotate & interpolation functions on the cropped image.

**Step 12** - Repeat step-4 & crop the image according to its bounding box.

**Step 13** - Convert the resultant image into a grayscale as save it as a .tiff file with a unique name.

**Step 14** - Finally, save the gathered dimensions, new image name, its type, its average color ratio, & its intensity level into an excel file, for each rice grain in an image.

## Results:
1. Original Image:

![01-original-image](https://user-images.githubusercontent.com/37273194/111885329-ee65d080-89e8-11eb-9974-4a2daf6df899.png)

2. After Gray Scaling:

![02-after-gray-scaling](https://user-images.githubusercontent.com/37273194/111885341-f6be0b80-89e8-11eb-8281-ff151aae5903.png)

3. After Thresholding:

![03-after-thresholding](https://user-images.githubusercontent.com/37273194/111885343-f7ef3880-89e8-11eb-8e38-55504a52c874.png)

4. After Morphology Operations:

![04-after-morphology-operations](https://user-images.githubusercontent.com/37273194/111885344-f9206580-89e8-11eb-9dd1-1bbd0249492d.png)

5. Bouding Box Around Resultant Objects:

![05-bounding-box-around-objects](https://user-images.githubusercontent.com/37273194/111885345-fa519280-89e8-11eb-91ef-0ddca5150165.png)

6. Cropped Rice Grain:

![06-cropped-rice-grain](https://user-images.githubusercontent.com/37273194/111885346-faea2900-89e8-11eb-995a-bbf0cb0eab47.png)

## Important:
- Repo contains following items:
  - Source.py - main program file.
  - Data set. 
  - Step-by-step images of the complete process.
  - Sample results excel file.

## Note:
```
Orginally, the program is configured to work with 10 types of rice grains with 5 sample each. However, it can be changed accordingly, as the source file now contains 2 main methods:
1. run_RGI() - The original method, which works with 10 types of rice with 5 images each.
2. run_RGI_with_small_dataset() - An alternate method for this repo, which works with 3 rice types with 1 image each to demonstrate the RGI working.
```

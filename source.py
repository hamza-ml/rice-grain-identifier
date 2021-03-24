import math
import warnings
import numpy as np
import skimage as ski
import skimage.io as skio
from matplotlib import cm
import xlsxwriter as excel
import matplotlib.pyplot as plt
from skimage.transform import rotate
from skimage.morphology import square
from skimage.measure import label as sml
from skimage.filters import threshold_minimum
from skimage.measure import regionprops as smr
from skimage.morphology import binary_opening, binary_closing
warnings.filterwarnings("ignore")


def create_excel(nxt_row, img_name, length, width, min_color, max_color, avg_color, rice_type):
    workbook = excel.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Image Name")
    worksheet.write(0, 1, "Length")
    worksheet.write(0, 2, "Width")
    worksheet.write(0, 3, "Min Color")
    worksheet.write(0, 4, "Max Color")
    worksheet.write(0, 5, "Average Color")
    worksheet.write(0, 6, "Rice Type")

    worksheet.write(nxt_row, 0, img_name)
    worksheet.write(nxt_row, 1, length)
    worksheet.write(nxt_row, 2, width)
    worksheet.write(nxt_row, 3, min_color)
    worksheet.write(nxt_row, 4, max_color)
    worksheet.write(nxt_row, 5, avg_color)
    worksheet.write(nxt_row, 6, rice_type)


def b_blox(image):
    lbl_img, num_label = sml(image, return_num=True)
    regions = smr(lbl_img)

    for props in regions:
        min_row, min_col, max_row, max_col = props.bbox
        ret_img = image[min_row:max_row, min_col:max_col]

        # print(ret_img)
        # newImg = ret_img*255
        # print(newImg)
        # r, g, b = newImg[:, :, 0], newImg[:, :, 1], newImg[:, :, 2]
        # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        # print(gray)
        # plt.imsave("hell.tiff", ret_img, cmap = cm.gray)

    return ret_img


def RGI(img_name, nxt_row):
    coin_mm = 290  # coin diameter in mm
    coin_pixels = 0.0007297616950602682  # default

    # Original Image --> Input as greyscale
    img = skio.imread(img_name, as_grey=True)
    # splitting image name
    rice_type = img_name.split('_')
    rice_type = rice_type[0]

    # Thresholding the Image
    thresh = threshold_minimum(img)
    threshed_img = img > thresh

    # CLOSING & OPENING WITH AN ENLARGING ELEMENT (to remove noise)
    dilated = binary_closing(threshed_img, square(10))
    dilated = binary_opening(dilated, square(10))

    # Applying Measureing Label
    lbl_img, num_label = sml(dilated, return_num=True)
    regions = smr(lbl_img, intensity_image=threshed_img)

    fig, ax = plt.subplots()
    ax.imshow(dilated)

    loop_count = 0
    for props in regions:
        y0, x0 = props.centroid
        orientation = props.orientation

        eccentricity_var = props.eccentricity
        area_var = props.area

        # 0.5 ==> length of red lines from the centre of the objects
        x1 = x0 + math.cos(orientation) * 0.5 * \
            props.major_axis_length  # 90Angle
        y1 = y0 - math.sin(orientation) * 0.5 * \
            props.major_axis_length  # lineA_length
        x2 = x0 - math.sin(orientation) * 0.5 * \
            props.minor_axis_length  # lineB_length
        y2 = y0 - math.cos(orientation) * 0.5 * \
            props.minor_axis_length  # 90Angle

        length = props.major_axis_length
        width = props.minor_axis_length
        angle = props.orientation

        # RADIANS TO DEGREE CONVERSION
        angle = (180 / 3.14) * angle
        # FINDING 90 DEGREE ANGLE
        new_angle = 90 + (angle * (- 1))

        # linewidth ==> width of redlines from centre, respectively
        ax.plot((x0, x1), (y0, y1), '-r', linewidth=1.5)
        ax.plot((x0, x2), (y0, y2), '-r', linewidth=1.5)
        # markersize ==> greenDots at Centre
        ax.plot(x0, y0, '.g', markersize=3)

        min_row, min_col, max_row, max_col = props.bbox
        bx = (min_col, max_col, max_col, min_col, min_col)
        by = (min_row, min_row, max_row, max_row, min_row)

        # linewidth ==> Intensity Level of SquareBox
        ax.plot(bx, by, '-b', linewidth=1.5)
        loop_count = loop_count + 1

        # finding coin
        if eccentricity_var < 0.3:
            coin_pixels = coin_mm / area_var
            # print ("c", coin_pixels)

        # finding rice grains
        if eccentricity_var > 0.5:
            # cropping bouding box
            imui = dilated[min_row:max_row, min_col:max_col]
            # calculating width & height & converting cm to mm
            length = format(((length * coin_pixels) * 10), '.4f')
            width = format(((width * coin_pixels) * 10), '.4f')
            # limiting afer point decimal places to 2
            # new_op = format(length, '.2f')
            print("length:", length)
            print("Width:", width)

            min_color = float(props.min_intensity)
            max_color = float(props.max_intensity)
            avg_color = format(props.mean_intensity, '.4f')

            print("a", min_color, max_color, avg_color)

            abc = ".tiff"
            newu = str(nxt_row) + abc

            imui = np.pad(imui, (200, 200), 'constant')
            imui = rotate(imui, new_angle)
            crop_grain = b_blox(imui)
            # skio.imsave(newu, (crop_grain))
            plt.imsave(newu, crop_grain, cmap=cm.gray)

            nxt_row = nxt_row + 1

            # worksheet.write(nxt_row, 0, img_name)
            # worksheet.write(nxt_row, 1, length)
            # worksheet.write(nxt_row, 2, width)
            # worksheet.write(nxt_row, 3, min_color)
            # worksheet.write(nxt_row, 4, max_color)
            # worksheet.write(nxt_row, 5, avg_color)
            # worksheet.write(nxt_row, 6, rice_type)

            create_excel(nxt_row, newu, length, width,
                         min_color, max_color, avg_color, rice_type)

    plt.show()
    skio.imsave('result.jpg', ski.img_as_uint(dilated))

    print("Loop:", loop_count, "Times")
    return nxt_row


def run_RGI_with_small_dataset():
    saylla = "sample_saylla.jpg"
    kainaat = "sample_kainaat.jpg"
    basmati = "sample_basmati.jpg"

    next_row = 0
    count = 0
    while (count <= 3):
        count = count + 1

        if count == 1:
            next_row = RGI(saylla, next_row)
            next_row = next_row + 1
        elif count == 2:
            next_row = RGI(kainaat, next_row)
            next_row = next_row + 1
        elif count == 3:
            next_row = RGI(basmati, next_row)
            next_row = next_row + 1
        else:
            print("Error: Unable to process image.")


def run_RGI():
    nameA = "Adhowaar_0"
    nameB = "Basmati_0"
    nameC = "Kainaat_0"
    nameD = "Mota Chawaal86_0"
    nameE = "Saylla_0"
    nameF = "Super Kernel - Double Zebra_0"
    nameG = "Super Kernel - Purana_0"
    nameH = "Super Kernel_0"
    nameI = "Totta_0"
    nameJ = "Zaraffa_0"

    image_ext = ".jpg"

    next_row = 0
    r_count = 0

    while (r_count <= 10):
        r_count = r_count + 1

        image_count = 0
        r_count2 = 0

        while (r_count2 < 5):
            image_count = image_count + 1

            if r_count == 1:
                image_name = nameA + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 2:
                image_name = nameB + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 3:
                image_name = nameC + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 4:
                image_name = nameD + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 5:
                image_name = nameE + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 6:
                image_name = nameF + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 7:
                image_name = nameG + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 8:
                image_name = nameH + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 9:
                image_name = nameI + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            elif r_count == 10:
                image_name = nameJ + str(image_count) + image_ext
                next_row = RGI(image_name, next_row)
                next_row = next_row + 1
                r_count2 = r_count2 + 1
            else:
                print("Error: Unable to process image.")


print("Setting up excel workbooks.")
workbook = excel.Workbook('result.xlsx')
worksheet = workbook.add_worksheet()
print("Starting RGI")
# RGI for complete data set - 10 rice types with 5 sample images each.
# run_RGI()

# RGI for small data set - 3 rice types with 1 image each.
run_RGI_with_small_dataset()
print("RGI process completed. Closing excel workbook.")
workbook.close()
print("Workbook closed.")

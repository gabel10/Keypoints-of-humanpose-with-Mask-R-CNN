
# ### See https://github.com/aleju/imgaug and http://imgaug.readthedocs.io/en/latest/index.html
import imgaug
from imgaug import augmenters as iaa
import numpy as np
import glob
import imageio
import os
import argparse
import shutil
import re
from random import seed
from random import gauss

NUMBER_OF_IMAGE_CHANNELS = 3
NUMBER_OF_MASK_CHANNELS = 1

MASK_PIXEL_THRESHOLD = 0.9  # at least this proportion of the mask must be preserved in the augmentation

#
# python -u augmentation.py -id /data/dkpun-data/augmentor/input -od /data/vein/augmented/12-jun-ratio-20-1 -na 20 -file /data/dkpun-data/augmentor/file.txt  > ../augmentation.log &
#
parser = argparse.ArgumentParser(description='Create an augmented data set.')
parser.add_argument('-id','--input_dir', type=str, help='Base directory of the images to be augmented.', required=True)
parser.add_argument('-od','--output_dir', type=str, help='Base directory of the output.', required=True)
parser.add_argument('-na','--number_of_augmented_images_per_original', type=int, default=1, help='Minimum number of augmented image/mask pairs to produce for each input image/mask pair.', required=False)
parser.add_argument('--augment_colour', dest='augment_colour', action='store_true', help='Apply colour augmentation')
parser.add_argument('--no-augment_colour', dest='augment_colour', action='store_false', help='Do not apply colour augmentation')
parser.add_argument('-file','--file', type=str, help="File of the bodyweights")
parser.set_defaults(augment_colour=True)
args = parser.parse_args()

image_file_list = glob.glob("{}/images/*.png".format(args.input_dir))
mask_file_list = glob.glob("{}/masks/*.png".format(args.input_dir))
seed(7)
file_list = open(args.file, 'r')
lines = file_list.readlines()
file_list.close()
lines = [line.rstrip('\n') for line in lines]
names = [n.split(' ')[0] for n in lines]
bw = [n.split(' ')[1] for n in lines]

total_images_output = 0

# remove all previous augmentations in this base directory
if os.path.exists(args.output_dir):
    shutil.rmtree(args.output_dir)

# create a new directory structure
augmented_images_directory = "{}/images".format(args.output_dir)
augmented_masks_directory = "{}/masks".format(args.output_dir)
augmented_file = open('val_augmented.txt','w')
os.makedirs(args.output_dir)
os.makedirs(augmented_images_directory)
os.makedirs(augmented_masks_directory)        
os.chmod(args.output_dir, 0o777)
os.chmod(augmented_images_directory, 0o777)
os.chmod(augmented_masks_directory, 0o777)

# create the augmentation sequences

seq = iaa.Sequential([
    iaa.Rot90((1,3))
])

color_seq = iaa.Sequential({
    iaa.Add((-20,20)),
    iaa.Multiply((0.8,1.2)),
    iaa.contrast.LinearContrast((0.8, 1.2))
}, random_order=True)

# go through all the images and create a set of augmented images and masks for each
for idx in range(len(image_file_list)):
    augmented_images = []
    augmented_masks = []

    base_name = os.path.basename(image_file_list[idx])
    index_file = names.index(os.path.splitext(base_name)[0])
    #bw_value = float(bw[index_file]) + gauss(0,1)

    print("processing {} ({} of {})".format(base_name, idx+1, len(image_file_list)))

    base_image = imageio.imread(image_file_list[idx]).astype(np.uint8)
    base_mask = imageio.imread(mask_file_list[idx]).astype(np.uint8)

    base_mask_pixel_count = np.count_nonzero(base_mask)

    number_of_augmented_images_per_original = args.number_of_augmented_images_per_original
    if re.search('class_Pure_Quartz_Carbonate', base_name):
        number_of_augmented_images_per_original = number_of_augmented_images_per_original * 2

    images_list = []
    masks_list = []
    for i in range(number_of_augmented_images_per_original):
        images_list.append(base_image)
        masks_list.append(base_mask)

    # convert the image lists to an array of images as expected by imgaug
    images = np.stack(images_list, axis=0)
    masks = np.stack(masks_list, axis=0)

    # write out the un-augmented image/mask pair
    print("writing out the un-augmented image/mask pair")
    output_base_name_img = "{}_orig{}".format(os.path.splitext(base_name)[0], os.path.splitext(base_name)[1])
    output_base_name_mask = "{}_orig_mask{}".format(os.path.splitext(base_name)[0], os.path.splitext(base_name)[1])
    imageio.imwrite("{}/{}".format(augmented_images_directory,output_base_name_img), base_image)
    imageio.imwrite("{}/{}".format(augmented_masks_directory,output_base_name_mask), base_mask)
    augmented_file.write(output_base_name_img + ' ' + bw[index_file])
    augmented_file.write('\n')
    total_images_output += 1

    number_of_augmentations_for_this_image = 0

    while number_of_augmentations_for_this_image < number_of_augmented_images_per_original:
        # Convert the stochastic sequence of augmenters to a deterministic one.
        # The deterministic sequence will always apply the exactly same effects to the images.
        affine_det = seq.to_deterministic() # call this for each batch again, NOT only once at the start
        images_aug = affine_det.augment_images(images)
        masks_aug = affine_det.augment_images(masks)
        
        # apply the colour augmentations to the images but not the masks
        if args.augment_colour == True:
            images_aug = color_seq.augment_images(images_aug)
        
        # now write out the augmented image/mask pair
        print("writing out the augmented image/mask pair")
        for i in range(len(images_aug)):
            if np.count_nonzero(masks_aug[i]) > (base_mask_pixel_count * MASK_PIXEL_THRESHOLD):
                output_base_name_img = "{}_augm_{}{}".format(os.path.splitext(base_name)[0], number_of_augmentations_for_this_image, os.path.splitext(base_name)[1])
                output_base_name_mask = "{}_augm_{}_mask{}".format(os.path.splitext(base_name)[0], number_of_augmentations_for_this_image, os.path.splitext(base_name)[1])
                imageio.imwrite("{}/{}".format(augmented_images_directory,output_base_name_img), images_aug[i])
                imageio.imwrite("{}/{}".format(augmented_masks_directory,output_base_name_mask), masks_aug[i])
                bw_value = float(bw[index_file]) + gauss(0,5)
                augmented_file.write(output_base_name_img + ' ' + str(bw_value))
                augmented_file.write('\n')
                number_of_augmentations_for_this_image += 1
                if number_of_augmentations_for_this_image == number_of_augmented_images_per_original:
                    break
            else:
                print("discarding image/mask pair {} - insufficient label".format(i+1))
        print("completed {} augmentations for this image.".format(number_of_augmentations_for_this_image))
    total_images_output += number_of_augmentations_for_this_image
augmented_file.close()
print("augmented set of {} images generated from {} input images".format(total_images_output, len(image_file_list)))

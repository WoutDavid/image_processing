import os
from skimage import io
import numpy as np
import argparse
from icecream import ic
import aicspylibczi

# ap = argparse.ArgumentParser(description="Extract tif from an image and count neurons and ganglia.")
# ap.add_argument('file_path',type=str,help="Path (relative or absolute) to target image")
# ap.add_argument('-o', '--out_dir', type=str, help="Root directory where output should be stored, default is base dir of the input image")
# ap.add_argument('-c', '--c_number', default=0, type=int, help="indexes (start at 0) of the channel contains the marker of interest. Default = 0.")


# ap.add_argument('-i', '--shape_indexes', default=None, type=int, help="index (start at 0) of the z-stack that needs to be extracted.")
# ap.add_argument('-t', '--tile_size', default=None, type=int, nargs=2, help="Tuple representing targetted tile size (X-Y). Example: `-t 2000 2000`. Default is no tiling behaviour")

# args = ap.parse_args()
# # if no out_dir is given, take the base dir of the input image
# if args.out_dir is None:
#     args.out_dir = os.path.dirname(args.file_path)

def getMostInFocusImage(image_array_list):
    stdev_list = []
    for image in image_array_list:
        # calculate edges in image
        edged = laplace(image)
        # Calculate stdev of edges
        stdev = np.std(edged)
        stdev_list.append(stdev)
    
    # Find largest stdev in list
    largest = max(stdev_list)
    # Fidn which index it is to link back to the original list
    index = stdev_list.index(largest)
    print("Extracted most in focus z-stack is index {index}")
    return image_array_list[index], index

def readImage(args_file_path: str):
    if args_file_path.lower().endswith((".tif", ".tiff", "nd2")):
        image = io.imread(args_file_path)
        img_type = "tif"
    if args_file_path.lower().endswith(".czi"):
        image = aicspylibczi.CziFile(args_file_path) 
        img_type = "czi"
        
    return image, img_type

def extractMostInFocusZstack(image: np.ndarray, z_shape_index:int = -1):
    if not len(image.shape) > 2:
        return image
    for i in range(image.shape[z_shape_index]):
        img_list.append(np.take(image, i, z_shape_index))
    mostInFocusImage = getMostInFocusImage(img_list)
    return mostInFocusImage



def extractSingleImages(image: np.ndarray, indexes_dict: dict, image_type: str, filename: str):
    if image_type == "tif":
        for shape_index, channel_indexes in indexes_dict.items():
            if isinstance(channel_indexes, int): # if it's only one channel, it'ss give an iterable error, so we gotta make it a list
                channel_indexes = [channel_indexes] 
            for channel_index in channel_indexes:
                if shape_index == None:
                    extracted_image = np.take(image, channel_index, axis=-1)
                else:
                    extracted_image = np.take(image, channel_index, axis=shape_index)
                io.imsave(f"{os.path.splitext(filename)[0]}_i{shape_index}_c{channel_index}.tif", extracted_image)
            
    elif image_type == "czi":
        for shape_index, channel_indexes in indexes_dict.items():
            # now we assume the shape indexes are letters referring to czi stuff
            if isinstance(channel_indexes, int): # if it's only one channel, it'ss give an iterable error, so we gotta make it a list
                channel_indexes = [channel_indexes] 
            for channel_index in channel_indexes:
                extracted_image,shape = image.read_image(shape_index=channel_index)
                extracted_image = extracted_image[0,0,0,0,0,:,:]
                io.imsave(f"{os.path.splitext(filename)[0]}_i{shape_index}_c{channel_index}.tif", extracted_image )

# def parseIndexes() #TODO


image, img_type = readImage("/media/tool/enteric_neurones/slidescanner_examples/01_Pin1403_Stitch.czi")
extractSingleImages(image, {2:1}, img_type, filename="/media/tool/enteric_neurones/slidescanner_examples/01_Pin1403_Stitch.czi")

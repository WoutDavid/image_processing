from skimage import io
import numpy as np
import argparse
from icecream import ic
import aicspylibczi

ap = argparse.ArgumentParser(description="Extract tif from an image and count neurons and ganglia.")
ap.add_argument('file_path',type=str,help="Path (relative or absolute) to target image")
# ap.add_argument('-o', '--out_dir', type=str, help="Root directory where output should be stored, default is base dir of the input image")
# ap.add_argument('-c', '--c_number', default=0, type=int, help="indexes (start at 0) of the channel contains the marker of interest. Default = 0.")

# # Parameters

# ap.add_argument('-p', '--pixel_density', default=3.2, type=float, help="Pixel density of the image (pixels/micrometer. default = 3.2")
# ap.add_argument('-s', '--sigma', default=7, type=int, help="Sigma used to smooth the image using a gaussian smoother. default = 7")
# ap.add_argument('-m', '--min_samples', default=2, type=int, help="Minimum number of neurons in a ganglion. default = 2")

# ap.add_argument('-i', '--maxIP', default=False,action="store_true", help="Flag that turns on taking the maxIP of the z-dimension.")
# ap.add_argument('-z', '--z_number', default=None, type=int, help="index (start at 0) of the z-stack that needs to be extracted.")
# ap.add_argument('-t', '--tile_size', default=None, type=int, nargs=2, help="Tuple representing targetted tile size (X-Y). Example: `-t 2000 2000`. Default is no tiling behaviour")

# args = ap.parse_args()
# # if no out_dir is given, take the base dir of the input image
# if args.out_dir is None:
#     args.out_dir = os.path.dirname(args.file_path)

def readImage(args_file_path: str):
    if args_file_path.lower().endswith((".tif", ".tiff")):
        image = io.imread(args_file_path)
        img_type = "tif"
    if args_file_path.lower().endswith(".czi")
        image = aicspylibczi.CziFile(args_file_path) 
        img_type = "czi"
        
    return image, img_type

def extractSingleImages(image: np.ndarray, indexes_dict: dict, image_type: str):
    image_shape = image.shape
    if image_type == "tif":
        for shape_index, channel_indexes in indexes_dict.items():
            if isinstance(channel_indexes, int): # if it's only one channel, it'ss give an iterable error, so we gotta make it a list
                channel_indexes = [channel_indexes] 
            for channel_index in channel_indexes:
                extracted_image = np.take(image, channel_index, axis=shape_index)
            
    elif image_type == "czi":
        for shape_index, channel_indexes in indexes_dict.items():
            # now we assume the shape indexes are letters referring to czi stuff
            if isinstance(channel_indexes, int): # if it's only one channel, it'ss give an iterable error, so we gotta make it a list
                channel_indexes = [channel_indexes] 
            for channel_index in channel_indexes:
                extracted_image,shape = czi.read_image(shape_index=channel_index)
                extracted_image = image_slice[0,0,0,0,0,:,:]
    return extracted_image

def parseIndexes()

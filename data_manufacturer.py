"""
Point this code at the dataset at the .csv file with the image paths and the manually entered scores
this will resize and then copy the images to a different folder

"""

import pandas as pd
from torchvision.transforms import v2
from PIL import Image
import os
from tqdm import tqdm
import argparse



if __name__ == "__main__":

    # arg parsing
    parser = argparse.ArgumentParser(description="Factory for building reduced size image datasets")
    parser.add_argument("--random", default=False, action='store_true')
    parser.add_argument("--balance", default=False, action="store_true")
    parser.add_argument("--frac", default=0.25, type=float)
    parser.add_argument("--path", default="../../adventures_in_elodea/data_scores.csv", type=str)
    parser.add_argument("--seed", default=42, type=int)

    args = parser.parse_args()

    # read the
    data_scores = pd.read_csv(args.path)

    """
    look at all the images, and resize them to a more manageable size
    
    I don't actually need the "real size images" to do this analysis, and, inexplicably, sometims 224 x 224 pixels
    is an important size (see alexnet)
    """

    random_sample = args.random
    balance = args.balance
    random_sample_frac = args.frac
    seed = args.seed

    if random_sample and balance:
        target_name = f"{random_sample_frac}_reduced_then_balanced"
    elif random_sample:
        target_name = f"{random_sample_frac}_reduced"
    elif balance:
        target_name = f"balanced"
    else:
        target_name = "all_data"

    if os.path.isdir(target_name):
        os.system(f"rm -rf {target_name}")
        os.system(f"mkdir {target_name}")
    else:
        os.system(f"mkdir {target_name}")

    no_veg = data_scores[data_scores['score'] == 0]
    veg = data_scores[data_scores['score'] == 3]
    if random_sample and balance:
        # take percentage of total data in equal proportions, then balance to the lower one

        sampled_no_veg = no_veg.sample(frac=random_sample_frac,
                                       replace=False,
                                       random_state=seed)
        sampled_veg = veg.sample(frac=random_sample_frac,
                                 replace=False,
                                 random_state=seed)

        # get the smallest category
        n = min(len(sampled_veg), len(sampled_no_veg))

        # now make sure you draw n values randomly from this sample
        sampled_no_veg = sampled_no_veg.sample(n=n, replace=False, random_state=seed)
        sampled_veg = sampled_veg.sample(n=n, replace=False, random_state=seed)

        alert = f"""you have elected to reduce the size of the dataset to
    to {random_sample_frac} of it's original size, then balance the dataset
    the new sizes of the dataset are listed below:
    
                entangled   not_entangled
    prev size:  {len(veg)}           {len(no_veg)}
    new size:   {len(sampled_veg)}            {len(sampled_no_veg)}
    
    total size: {len(sampled_veg) + len(sampled_no_veg)}
    """

    elif balance:
        n = min(len(veg), len(no_veg))

        sampled_no_veg = no_veg.sample(n=n, replace=False, random_state=seed)
        sampled_veg = veg.sample(n=n, replace=False, random_state=seed)

        alert = f"""you have elected to balance the dataset:
    
                entangled   not_entangled
    prev size:  {len(veg)}           {len(no_veg)}
    new size:   {len(sampled_veg)}            {len(sampled_no_veg)}
    
    total size: {len(sampled_veg) + len(sampled_no_veg)}
    """
    elif random_sample:
        sampled_no_veg = no_veg.sample(frac=random_sample_frac,
                                       replace=False,
                                       random_state=seed)
        sampled_veg = veg.sample(frac=random_sample_frac,
                                 replace=False,
                                 random_state=seed)

        alert = f"""you have elected to reduce the size of the output to {random_sample_frac} of it's original size
                entangled   not_entangled
    prev size:  {len(veg)}           {len(no_veg)}
    new size:   {len(sampled_veg)}            {len(sampled_no_veg)}
    
    total size: {len(sampled_veg) + len(sampled_no_veg)}
    """
    else:
        sampled_no_veg = no_veg
        sampled_veg = veg
        alert = f"""you have elected not to reduce the size of the output of images.  Some sizes
    may be too large for even GPU equipped computers to handle.
    
                    entangled   not_entangled
             size:  {len(veg)}           {len(no_veg)}
    
        total size: {len(veg) + len(no_veg)}
        """

    data_scores = pd.concat([sampled_no_veg, sampled_veg])
    with open(f"{target_name}/warning.md", "w") as write_file:
        write_file.write(alert)

    sizes = [224]

    # first make all the folders we want to deposit transformed images into
    for size in sizes:
        folder_name = f"{target_name}/data_{size}"
        os.system(f"rm -rf {folder_name}")
        os.system(f"mkdir {folder_name}")

        for score in [0, 3]:
            os.system(f"mkdir {folder_name}/{'entangled' if score == 3 else 'not_entangled'}")

    file_names = []
    for index, row in tqdm(data_scores.iterrows(),
                           total=len(data_scores)):
        path, score = row
        file_name = os.path.basename(path)

        if file_name in file_names:
            file_name = f"another_{file_name}"

        file_names.append(file_name)

        if score in [1, 2]:
            # I don't care about the ambiguous cases
            continue
        else:
            # resize the image and save

            for size in sizes:
                # open the image and resize immediately
                img = Image.open(path).resize((size, size))

                # Image Augmentation - more are possible, but let's not get carried away
                img = v2.RandomHorizontalFlip(p=0.5)(img),  # randomly flip the images horizontally with a prob of 50%
                img = v2.RandomRotation(degrees=(0, 3))(img)  # randomly rotate the image 0-15 degrees
                img = v2.GaussianBlur(kernel_size=(3, 3))(img)  # gaussian blur
                class_folder = "entangled" if score == 3 else "not_entangled"
                img[0].save(f"{target_name}/data_{size}/{class_folder}/{file_name}")

    print(alert)

# Image Dataset Resizer

This Python script is designed to process a dataset stored in a CSV file, containing image paths and manually entered scores. The script resizes the images and copies them to a different folder based on specified conditions.

## Usage

1. Clone the repository and navigate to the script's directory.
2. Run the script, providing necessary arguments:
   - `--random`: (optional) Randomly sample data.
   - `--balance`: (optional) Balance the dataset.
   - `--frac`: (optional) Fraction of data to keep in random sampling (default is 0.25).
   - `--path`: (optional) Path to the CSV file containing image paths and scores (default is "../../adventures_in_elodea/data_scores.csv").
   - `--seed`: (optional) Seed for random operations (default is 42).

Example:

```bash
python data_manufacturer.py --random --balance --frac 0.2 --path path/to/data.csv --seed 123
```

    --random: (optional) Randomly sample data.
    --balance: (optional) Balance the dataset.
    --frac: (optional) Fraction of data to keep in random sampling (default is 0.25).
    --path: (optional) Path to the CSV file containing image paths and scores (default is "../../adventures_in_elodea/data_scores.csv").
    --seed: (optional) Seed for random operations (default is 42).

# Output

Resized images are stored in folders based on specified criteria:

    "data_{size}" folders contain resized images.
    Images are organized into "entangled" and "not_entangled" subfolders based on scores.

# Notes

    Ambiguous cases with scores 1 or 2 are excluded.
    Image augmentation techniques are applied during resizing.
```
Usage: hog-feature-extraction.py [options]

Options:
  -h, --help           show this help message and exit
  --size_l=SIZE_L      file size lower bound in bytes
  --size_u=SIZE_U      file size upper bound in bytes
  --height_u=HEIGHT_U  file height upper bound in pixels

```

Script that generates HOG feature descriptors for all images in the directory. Images with file sizes or pixel heights too small or large are filtered out, and remaining images are resized for feature extraction. Requires `OpenCV` to be installed.

Sample usage:
`python3 hog-feature-extraction.py --size_l=800 --size_u=32500 --height_u=400`

Output files:
* `acceptable_images.txt`: the list of images that met size/height criteria
* `unacceptable_images.txt`: the list of images that did not meet size/height criteria
* `hog_features.csv`: the HOG feature descriptors calculated for acceptable images
* `features.pickle`: a serialized dictionary matching image names to their feature vectors


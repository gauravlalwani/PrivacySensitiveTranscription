import cv2
import numpy
import os
import pickle

from optparse import OptionParser

# run image filtering and HOG feature extraction
def main():
    print('Working...')

    # require file size lower and uppoer bound limits and file height uper bound
    parser = OptionParser()
    parser.add_option('--size_l',
                      action='store', type='int', dest='size_l',
                      help='file size lower bound in bytes')
    parser.add_option('--size_u',
                      action='store', type='int', dest='size_u',
                      help='file size upper bound in bytes')
    parser.add_option('--height_u',
                      action='store', type='int', dest='height_u',
                      help='file height upper bound in pixels')

    (options, args) = parser.parse_args()
    try:
        size_l = options.size_l
        size_u = options.size_u
        height_u = options.height_u
    except:
        print('Error occurred, try using the --help flag')

    # image dimensions
    width = 128
    height = 64

    # track HOG feature vectors and corresponding images
    features = {}
    h_features = []

    # list of images that are un/acceptable to be crowdsourced
    acceptable = []
    unacceptable = []

    # HOG feature descriptor
    hog = cv2.HOGDescriptor(_winSize = (width,height),
                            _blockSize = (16,16),
                            _blockStride = (8,8),
                            _cellSize = (8,8),
                            _nbins = 9)

    # evaluate image fles
    for filename in os.listdir('./'):
        if filename.endswith('.jpg'):
            # check if image meets size and height thresholds
            size = os.path.getsize(filename)
            if size < size_l or size > size_u:
               unacceptable.append(filename)
               continue
        
            im = cv2.imread(filename, 0)
            if im.shape[0] > height_u:
                unacceptable.append(filename)
                continue
        
            # resize image and compute features
            acceptable.append(filename)

            im = cv2.resize(im, (width, height))
            h = hog.compute(im)
        
            features[filename] = h
            h_features.append(h)

    # save data
    with open('features.pickle', 'wb') as handle:
        pickle.dump(features, handle)

    numpy.savetxt('hog_features.csv',
                  numpy.array(h_features),
                  delimiter=',')

    with open('acceptable_images.txt', 'w') as handle:
        for f in acceptable:
            handle.write('{}\n'.format(f))

    with open('unacceptable_images.txt', 'w') as handle:
        for f in unacceptable:
            handle.write('{}\n'.format(f))

    print('HOG features and corresponding image name saved to \'features.pickle\'.')
    print('HOG feature vectors saved to \'hog_features.csv\'.')
    print('List of acceptable images to crowdsource saved to \'acceptable.txt\'.')
    print('List of unacceptable images to crowdsource saved to \'unacceptable.txt\'.')

if __name__ == '__main__':
    main()

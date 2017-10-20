import cv2
import _pickle as pickle

from sklearn.metrics.pairwise import cosine_similarity as cos_sim

def main():
    print('Working...')

    index = {}
    results = {}
    threshold = 0.9

    # load data
    with open('features.pickle', 'rb') as handle:
        unpickler = pickle.Unpickler(handle)
        index = unpickler.load()

    while True:
        image_0 = input('Input an image to compare: ')
        feature_0 = index[filename]

        print('Calculating cosine similarities...')

        results = {image_n: cos_sim(feature_0, feature_n)     \
                  for image_n, feature_n in index.iteritems() \
                  if name is not filename and cos_sim(feature_0, feature_n) > threshold}

        results = sorted(results.items(), key=itemgetter(0))

        print('Results:')
        for image_n, score in results.items():
            print('{0}\t{1}'.format(image_n, score))

            # im = cv2.imread(image_n, 0)
            # cv2.imshow(image_n, im)

if __name__ == '__main__':
    main()

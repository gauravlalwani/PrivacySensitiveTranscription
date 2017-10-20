import cv2
import _pickle as pickle

from scipy import spatial

def main():
    print('Working...')

    index = {}
    threshold = 0.5

    # load data
    with open('features.pickle', 'rb') as handle:
        unpickler = pickle.Unpickler(handle)
        index = unpickler.load()

    while True:
        results = {}

        image_q = input('Input an image to compare: ')

        if image_q not in index:
            print('Query image not found, please try another.')
            continue

        feature_q = index[image_q]

        print('Calculating cosine similarities...')
        for image_n, feature_n in index.items():
            score = 1 - spatial.distance.cosine(feature_n, feature_q)
            if score > threshold:
                results[image_n] = score
        
        del results[image_q]

        results = [(image_n, results[image_n]) for image_n in \
                  sorted(results, key=results.get, reverse=True)]

        print('Results:')
        for image_n, score in results:
            print('{0}\t{1}'.format(image_n, score))

            # im = cv2.imread(image_n, 0)
            # cv2.imshow(image_n, im)

if __name__ == '__main__':
    main()

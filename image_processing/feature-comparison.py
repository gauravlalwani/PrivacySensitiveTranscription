import cv2
import _pickle as pickle

from scipy import spatial

# find the most similar images given a query image
def main():
    print('Working...')

    # similarity threshold
    threshold = 0.5

    # load feature vectors
    with open('features.pickle', 'rb') as handle:
        unpickler = pickle.Unpickler(handle)
        index = unpickler.load()

    while True:
        results = {}

        # get user input
        image_q = input('Input an image to compare: ')

        if image_q not in index:
            print('Query image not found, please try another.')
            continue

        feature_q = index[image_q]

        # calculate cosine similarities
        print('Calculating cosine similarities...')
        for image_n, feature_n in index.items():
            score = 1 - spatial.distance.cosine(feature_n, feature_q)
            if score > threshold:
                results[image_n] = score
        
        del results[image_q]

        results = [(image_n, results[image_n]) for image_n in \
                  sorted(results, key=results.get, reverse=True)]

        # present results
        print('Results:')
        for image_n, score in results:
            print('{0}\t{1}'.format(image_n, score))

            # im = cv2.imread(image_n, 0)
            # cv2.imshow(image_n, im)

if __name__ == '__main__':
    main()

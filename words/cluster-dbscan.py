import numpy as np
import _pickle as pickle

from sklearn.cluster import DBSCAN

# train a DBSCAN model using the feature vectors
def main():
    print('Working...')

    # load feature vectors
    with open('features.pickle', 'rb') as handle:
        unpickler = pickle.Unpickler(handle)
        index = unpickler.load()

    # reshape 3d vectors to 2d
    dataset = list(index.values())
    dataset = np.asarray(dataset)
    
    n_samples, n_x, n_y = dataset.shape
    dataset = dataset.reshape((n_samples,n_x*n_y))
    
    # train model
    model = DBSCAN(metric='cosine', n_jobs=-1).fit(dataset)

    # save model
    with open('dbscan_model.pickle', 'wb') as handle:
        pickle.dump(model, handle)

    print('DBSCAN model trained and saved to dbscan_model.pickle')

if __name__ == '__main__':
    main()

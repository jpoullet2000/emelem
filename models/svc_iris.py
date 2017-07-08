import os
from sklearn import svm, datasets
from sklearn.externals import joblib

from emelem import app

# import some data to play with
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features. We could
                      # avoid this ugly slicing by using a two-dim dataset
y = iris.target

# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 1.0  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C).fit(X, y)

joblib.dump(svc, os.path.join(app.config['EMELEM_MODEL_FOLDER'], 'svc_iris.pkl'))

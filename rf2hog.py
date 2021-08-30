# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score
from skimage import exposure
from skimage import feature
from imutils import paths
import argparse
import imutils
import cv2
from sklearn import svm
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import time
import matplotlib.pyplot as plt
start_time = time.time()
print(start_time)
# construct the argument parse and parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--training", required=True, help="training\\")
ap.add_argument("-t", "--test", required=True, help="test\\")
args = vars(ap.parse_args())
 
# initialize the data matrix and labels
print("[INFO] extracting features...")
data = []
labels = []

for imagePath in paths.list_images(args["training"]):
    # extract the make of the car
##  print(imagePath)
    make = imagePath.split("\\")[1]
    print(imagePath)
 
    # load the image, convert it to grayscale, and detect edges
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    H = feature.hog(gray,pixels_per_cell=(16, 16),
        cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys")
 
    # update the data and labels orientations=9 L2-Hys
    data.append(H)
    labels.append(make)

##print(labels)
# "train" the nearest neighbors classifier
print("[INFO] training classifier...")
X_train, X_test, y_train, y_test = train_test_split(data, labels, train_size = 0.70,test_size = 0.30)
print(len(X_train), len(X_test), len(y_train), len(y_test))


#kfold = KFold(n_splits=10)
model = RandomForestClassifier(n_estimators = 68, random_state = 42)
##model = KNeighborsClassifier(n_neighbors=1)
#results = cross_val_score(model,X_train,y_train, cv = kfold)
model.fit(X_train, y_train)
print("[INFO] evaluating...")

y_pred = model.predict(X_test)

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
accuracy = accuracy_score(y_test, y_pred)
print('Model accuracy is: ', accuracy)
#print(results)
#print('Accuracy = {}%, Standard Deviation = {}%'.format(round(results.max(), 4), round(results.std(), 2)))
end_time = time.time()
print("Total execution time: {} seconds".format(end_time - start_time))






for (i, imagePath) in enumerate(paths.list_images(args["test"])):
   # load the test image, convert it to grayscale, and resize it to
   # the canonical size
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   #logo = cv2.resize(gray, (200, 100))
   # extract Histogram of Oriented Gradients from the test image and
   # predict the make of the car
    (H, hogImage) = feature.hog(gray, pixels_per_cell=(16, 16),cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys", visualize=True)
    pred = model.predict(H.reshape(1, -1))[0]
 
	# visualize the HOG image
##    hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
##    hogImage = hogImage.astype("uint8")
##    cv2.imshow("HOG Image #{}".format(i + 1), hogImage)
 
	# draw the prediction on the test image and display it
    cv2.putText(image, pred.title(), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255 ), 3)
    cv2.imshow("Test Image #{}".format(i + 1), image)
    cv2.waitKey(0)



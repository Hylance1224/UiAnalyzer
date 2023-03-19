from img2vec import Img2Vec
import img2vec
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.svm import OneClassSVM
import torch
import os

img2vec = Img2Vec(cuda=False)


def find_abnormal(X):
    clf = OneClassSVM(gamma='auto').fit(X)
    a = clf.predict(X)
    print(a)
    return a


def getVectors(images):
    vectors = []
    for image in images:
        img = Image.open(image)
        vec = img2vec.get_vec(img, tensor=True)
        vec_1 = vec.reshape((1, -1))[0]
        vec_1 = vec_1.numpy().tolist()
        # print(type(vec_1))
        vectors.append(vec_1)
    return vectors


def getImageFromPath(path):
    files = os.listdir(path)
    path_files = []
    for f in files:
        if 'wireframe' in f:
            path_files.append(path + '/' + f)
    return path_files


if __name__ == '__main__':
    images = getImageFromPath('G:/Result_UI_page/3')
    print(len(images[0]))
    vectors = getVectors(images)
    print(vectors)
    result = find_abnormal(vectors)
    for i in range(len(result)):
        if result[i] == -1:
            print(images[i])

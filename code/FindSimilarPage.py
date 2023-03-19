import GetFeatures
import os
import spacy
import shutil
from natsort import ns, natsorted
nlp = spacy.load('en_core_web_md')


def calculate_words_similarity(words1, words2):
    if len(words1) <= len(words2):
        similar_sum = 0
        for w1 in words1:
            max_similar = 0
            for w2 in words2:
                token1 = nlp(w1)
                token2 = nlp(w2)
                similar = token1.similarity(token2)
                if similar > 1:
                    similar = 1
                if similar > max_similar:
                    max_similar = similar
            similar_sum = similar_sum + max_similar
        return similar_sum/len(words1)
    else:
        similar_sum = 0
        for w2 in words2:
            max_similar = 0
            for w1 in words1:
                token1 = nlp(w1)
                token2 = nlp(w2)
                similar = token1.similarity(token2)
                if similar > 1:
                    similar = 1
                if similar > max_similar:
                    max_similar = similar
            similar_sum = similar_sum + max_similar
        return similar_sum/len(words2)


def calculate_feature_similarity(feature1, feature2):
    words1 = feature1.split(' ')
    words2 = feature2.split(' ')
    new_words1 = []
    for w in words1:
        if w != ' ' and w != '':
            new_words1.append(w)
    new_words2 = []
    for w in words2:
        if w != ' ' and w != '':
            new_words2.append(w)
    similar = calculate_words_similarity(new_words1, new_words2)
    return similar


# def calculate_page_similarity(features1, features2):
#     if len(features1) == 0 or len(features2) == 0:
#         return 0
#     similar_sum1 = 0
#     for feature1 in features1:
#         max_similarity = 0
#         max_f = ''
#         for feature2 in features2:
#             similar = calculate_feature_similarity(feature1, feature2)
#             if similar > max_similarity:
#                 max_similarity = similar
#                 max_f = feature1 + '_' + feature2
#         print(max_f)
#         print(max_similarity)
#         print('----------------')
#         similar_sum1 = similar_sum1 + max_similarity
#     # similar_ave1 = similar_sum1/len(features1)
#
#     similar_sum2 = 0
#     for feature2 in features2:
#         max_similarity = 0
#         for feature1 in features1:
#             similar = calculate_feature_similarity(feature1, feature2)
#             if similar > max_similarity:
#                 max_similarity = similar
#                 max_f = feature2 + '_' + feature1
#         print(max_f)
#         print(max_similarity)
#         print('----------------')
#         similar_sum2 = similar_sum2 + max_similarity
#     # similar_ave2 = similar_sum2/len(features2)
#     similar_result = (similar_sum1 + similar_sum2)/(len(features1)+len(features2))
#     return similar_result


def calculate_page_similarity_spacy(features1, features2):
    if len(features1) == 0 or len(features2) == 0:
        return 0
    similar_sum1 = 0
    for feature1 in features1:
        max_similarity = 0
        max_f = ''
        for feature2 in features2:
            similar = calculate_feature_similar_spacy(feature1, feature2)
            if similar > max_similarity:
                max_similarity = similar
                max_f = feature1 + '_' + feature2
        # print(max_f)
        # print(max_similarity)
        # print('----------------')
        similar_sum1 = similar_sum1 + max_similarity
    # similar_ave1 = similar_sum1/len(features1)

    similar_sum2 = 0
    for feature2 in features2:
        max_similarity = 0
        for feature1 in features1:
            similar = calculate_feature_similar_spacy(feature1, feature2)
            if similar > max_similarity:
                max_similarity = similar
                max_f = feature2 + '_' + feature1
        # print(max_f)
        # print(max_similarity)
        # print('----------------')
        similar_sum2 = similar_sum2 + max_similarity
    # similar_ave2 = similar_sum2/len(features2)
    similar_result = (similar_sum1 + similar_sum2)/(len(features1)+len(features2))
    return similar_result


def get_max_in_target(target_path):
    target_files = os.listdir(target_path)
    return int(len(target_files)/2)


def copy_file(category_path, dir, num, target_num, similar):
    source_path = category_path + '/' + dir + '/' + num + '.dom'
    # print(source_path)
    # print('=========================')
    target_path = 'G:/Result_UI_page/test1/' + target_num + '/' + str(round(similar, 3)) + '_' + dir + '_' + num + '.dom'
    shutil.copyfile(source_path, target_path)

    source_path = category_path + '/' + dir + '/' + num + '.jpg'
    target_path = 'G:/Result_UI_page/test1/'+target_num + '/' + str(round(similar, 3)) + '_' + dir + '_' + num + '.jpg'
    shutil.copyfile(source_path, target_path)


def find_similar_page(category_path, source_id, source_num):
    source_features = GetFeatures.get_features(category_path+'/'+source_id+'/'+source_num + '.dom')
    print(source_features)
    print('-----------------')
    # source_features = ['zoom in ', 'zoom out ', 'my location '
    copy_file(category_path, source_id, source_num, '1', 1)
    dirs = os.listdir(category_path)
    dirs = natsorted(dirs, alg=ns.PATH)
    # print(dirs)
    for dir in dirs:
        # print(dir)
        if dir != source_id:
            files = os.listdir(category_path+'/'+dir)
            for file in files:
                if file[-4:] == '.dom':
                    target_features = GetFeatures.get_features(category_path + '/' + dir + '/' + file)
                    # print(target_features)
                    similar = calculate_page_similarity_spacy(source_features, target_features)
                    # print(similar)
                    if similar > 0.6:
                        print(dir + '_' + file)
                        print(target_features)
                        copy_file(category_path, dir, file[:-4], '1', similar)
                    if similar > 0.45:
                        # print(dir + '_' + file)
                        copy_file(category_path, dir, file[:-4], '2', similar)
                    # print('---------------')
        # print('-------')


def calculate_feature_similar_spacy(f1, f2):
    token1 = nlp(f1)
    token2 = nlp(f2)
    similar = token1.similarity(token2)
    return similar


if __name__ == "__main__":
    # find_similar_page('E:/Python project/Result_UI_page/navigation', '40', '15')
    # find_similar_page('G:/Result_UI_page/navigation', '196', '9')
    find_similar_page('G:/Result_UI_page/navigation', '196', '9')


# if __name__ == "__main__":
#     features1 = GetFeatures.get_features('E:/Python project/Result_UI_page/navigation/173/7.dom')
#     features2 = GetFeatures.get_features('E:/Python project/Result_UI_page/navigation/40/15.dom')
#     print(features1)
#     print(features2)
#     # features1 = ['haf oebb ad action ', 'trip planner ', 'departures ', 'search trains ', 'map ', 'live map ', 'alarms ', 'news ', 'settings ', 'help ', 'about ', 'enter starting point', 'current position ', 'enter destination', 'switch direction ', 'Dep???now ', 'search ', 'locations ', 'trips ', 'offline ']
#     # features2 = ['select country ']
#     s = calculate_page_similarity_spacy(features1, features2)
#     print(s)


# if __name__ == "__main__":
#     w1 = 'to'
#     w2 = 'to nearby'
#     token1 = nlp(w1)
#     token2 = nlp(w2)
#     similar = token1.similarity(token2)
#     print(similar)
#
#     s = calculate_feature_similarity(w1, w2)
#     print(s)
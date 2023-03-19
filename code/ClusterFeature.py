import GetFeatures
import os
import FindSimilarPage


def get_all_features(path):
    files = os.listdir(path)
    all_features = []
    for file in files:
        if file[-4:] == '.dom':
            features = GetFeatures.get_features(path + '/' + file)
            all_features.extend(features)
    return all_features


def add_cluster(clusters, feature):
    most_similar_cluster = None
    most_similar = 0
    for cluster in clusters:
        for f in cluster:
            s = FindSimilarPage.calculate_feature_similar_spacy(f, feature)
            if s >= 0.8 and s > most_similar:
                most_similar_cluster = cluster
    if most_similar_cluster is not None:
        most_similar_cluster.append(feature)
        return True
    return False


def cluster_features(features):
    clusters = []
    for feature in features:
        success = add_cluster(clusters, feature)
        if not success:
            clusters.append([feature])
    return clusters


def get_clusters(path):
    all_features = get_all_features(path)
    clusters = cluster_features(all_features)
    return clusters


if __name__ == '__main__':
    clusters = get_clusters('E:/Python project/Result_UI_page/test/2_1')
    for cluster in clusters:
        print(cluster)
from xml.dom.minidom import parse, parseString
import cv2
import ClusterFeature
import os
import GetFeatures
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_all_interactive_node(root):
    all_interactive_elements = []
    for child in root.childNodes:
        if child.nodeName != '#text':
            interactive_children = get_all_interactive_node(child)
            all_interactive_elements.extend(interactive_children)
            if interactive_children == []:
                if child.getAttribute('clickable') == 'true':
                    all_interactive_elements.append(child)
                elif child.getAttribute('long-clickable') == 'true':
                    all_interactive_elements.append(child)
    return all_interactive_elements


def get_bounds(bounds):
    bounds = bounds.replace('][', ',')
    bounds = bounds.replace('[', '')
    bounds = bounds.replace(']', '')
    bounds = bounds.split(',')
    int_bounds = []
    for b in bounds:
        int_bounds.append(int(b))
    return int_bounds


def write_image(file, elements):
    image = cv2.imread(file)
    for element in elements:
        bounds = element.getAttribute('bounds')
        bounds = get_bounds(bounds)
    cv2.imwrite('R2.png', image)


def write_a_element_in_image(image, element, color):
    print(color)
    bounds = element.getAttribute('bounds')
    bounds = get_bounds(bounds)
    x = 33
    x0 = int((bounds[0] + bounds[2]) / 2 - x)
    x1 = int((bounds[0] + bounds[2]) / 2 + x)
    y0 = int((bounds[1] + bounds[3]) / 2 - x)
    y1 = int((bounds[1] + bounds[3]) / 2 + x)
    cv2.rectangle(image, (x0, y0), (x1, y1), color, -1)


def write_a_texture_in_image(image, element, texture):
    img1 = cv2.imread('image/'+texture+'.jpg')  # 原始图像
    x = 33
    roi = img1[0:x*2, 0:x*2]
    bounds = element.getAttribute('bounds')
    bounds = get_bounds(bounds)
    x0 = int((bounds[0] + bounds[2]) / 2 - x)
    x1 = int((bounds[0] + bounds[2]) / 2 + x)
    y0 = int((bounds[1] + bounds[3]) / 2 - x)
    y1 = int((bounds[1] + bounds[3]) / 2 + x)
    print(y0, y1, x0, x1)
    print('-------------------')
    image[y0: y1, x0:x1] = roi


def get_cluster_colors(path):
    clusters = ClusterFeature.get_clusters(path)
    print('cluster---------------------')
    for cluster in clusters:
        print(cluster)
    print(len(clusters))
    cluster_colors = []
    RGBs = []
    for i in range(len(clusters)):
        rgb = RGBs[i]
        cluster_colors.append({'cluster': clusters[i], 'color': rgb})
    return cluster_colors


def draw_image(path, cluster_colors):
    files = os.listdir(path)
    for file in files:
        if file[-4:] == '.dom':
            all_interactive_nodes = GetFeatures.get_all_interactive_node_from_path(path + '/' + file)
            img = np.zeros([1280, 720, 3], np.uint8)
            img.fill(255)
            for element in all_interactive_nodes:
                color = (0, 0, 0)
                feature = GetFeatures.get_feature_from_component(element)
                # print(feature)
                for cluster_color in cluster_colors:
                    if feature in cluster_color['cluster']:
                        color = cluster_color['color']
                        write_a_element_in_image(img, element, color)
            cv2.imwrite(path + '/' + file[:-4]+'_wireframe' + '.jpg', img)


def draw_image_texture(path, cluster_textures):
    files = os.listdir(path)
    for file in files:
        if file[-4:] == '.dom':
            all_interactive_nodes = GetFeatures.get_all_interactive_node_from_path(path + '/' + file)
            img = np.zeros([1280, 720, 3], np.uint8)
            img.fill(255)
            for element in all_interactive_nodes:
                color = (0, 0, 0)
                feature = GetFeatures.get_feature_from_component(element)
                # print(feature)
                for cluster_texture in cluster_textures:
                    if feature in cluster_texture['cluster']:
                        texture = cluster_texture['color']
                        write_a_texture_in_image(img, element, texture)
            cv2.imwrite(path + '/' + file[:-4]+'_wireframe' + '.jpg', img)


if __name__ == "__main__":
    cluster_colors = get_cluster_colors('G:/Result_UI_page/3')
    draw_image('G:/Result_UI_page/3', cluster_colors)


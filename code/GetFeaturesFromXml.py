from xml.dom.minidom import parse, parseString
import cv2
import re


def get_sibling_text(node):
    next = node.nextSibling
    if next.nodeName == '#text':
        next_sibling = next.nextSibling
    else:
        next_sibling = next
    if next_sibling is not None and next_sibling.nodeName != '#text':
        if next_sibling.getAttribute('text') != '':
            return next_sibling.getAttribute('text')
    return ""


def get_child_text(node):
    childNodes = node.childNodes
    text = ''
    for child in childNodes:
        if child.nodeName != '#text':
            if child.getAttribute('text') != '':
                text = text + child.getAttribute('text') + ' '
    return text


# def get_all_interactive_node(root):
#     all_interactive_elements = []
#     for child in root.childNodes:
#         if child.nodeName != '#text':
#             if child.getAttribute('clickable') == 'true':
#                 all_interactive_elements.append(child)
#             elif child.getAttribute('long-clickable') == 'true':
#                 all_interactive_elements.append(child)
#             all_interactive_elements.extend(get_all_interactive_node(child))
#     return all_interactive_elements


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


def get_all_interactive_node_from_path(dom_file):
    DOMTree = parse(dom_file)
    root = DOMTree.documentElement
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


stop_words = ['button', 'btn', 'options', 'fragment', 'actionbar', 'bar', 'layout', 'unknown', 'option',
              'icon', 'container', 'bottom', 'item', 'obfuscated', 'action', 'btm', 'nav', 'belt', 'img', 'utility', 'interactions', 'iv', 'fab', 'image', 'map']


def check_contain_upper(word):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(word)
    if match:
        return True
    else:
        return False


def check_contain_lower(word):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(word)
    if match:
        return True
    else:
        return False


def uncamelize(camelCaps, separator="_"):
    pattern = re.compile(r'([A-Z]{1})')
    sub = re.sub(pattern, separator+r'\1', camelCaps).lower()
    return sub


def tackle_id(id_text):
    if 'com.android.systemui:id/' in id_text:
        return ''
    # print(id_text)
    l = id_text.find(':id/')
    id_text = id_text[l+4:]
    if id_text.find('_') != -1 or (check_contain_upper(id_text) and check_contain_lower(id_text)):
        id_text = uncamelize(id_text)
        words = id_text.split('_')
        id_text = ''
        for word in words:
            if word not in stop_words:
                id_text = id_text + word + ' '
        if contain_english(id_text):
            return id_text
        else:
            return ''
    return ''


def contain_english(str0):
    import re
    return bool(re.search('[a-z]', str0))


def too_short(str0):
    # print(str0)
    # print(len(str0))
    if len(str0) < 2 or len(str0) == 2:
        return True
    return False


def too_long(feature):
    # print(str0)
    # print(len(str0))
    if len(feature.split(' ')) >= 10:
        return True
    return False


def clear_feature(feature):
    f = re.sub('[^A-Za-z ]+', ' ', feature)
    # f = f.replace('\n', ' ')
    feature = ''
    words = f.split(' ')
    for word in words:
        if len(word) > 1:
            feature = feature + word + ' '
    return feature


def clear_all_feature(features):
    clear_features = []
    for f in features:
        f = re.sub('[^A-Za-z ]+', ' ', f)
        # f = f.replace('\n', ' ')
        feature = ''
        words = f.split(' ')
        for word in words:
            if len(word) > 1:
                feature = feature + word + ' '
        if contain_english(feature) and not too_short(feature) and not too_long(feature):
            clear_features.append(feature)
    clear_features1 = []
    for feature in clear_features:
        if feature not in clear_features1:
            clear_features1.append(feature)
    return clear_features1


def get_feature_from_component(e):
    text = e.getAttribute('text')
    child_text = get_child_text(e)
    content_des = e.getAttribute('content-desc')
    sibling_text = get_sibling_text(e)
    id_text = tackle_id(e.getAttribute('resource-id'))
    feature = ''
    if (contain_english(text)) and (not too_short(text)):
        feature = text
    elif (contain_english(content_des)) and (not too_short(content_des)):
        feature = text
    elif child_text != '':
        feature = child_text
    # elif sibling_text != '':
    #     features.append(sibling_text)
    elif id_text != '':
        feature = id_text
    feature = clear_feature(feature)
    return feature


def get_features(dom_file):
    DOMTree = parse(dom_file)
    root = DOMTree.documentElement
    clickable_elements = get_all_interactive_node(root)
    features = []
    for e in clickable_elements:
        feature = get_feature_from_component(e)
        if e != '':
            features.append(feature)
    # print(features)
    features = clear_all_feature(features)
    return features


def get_interactive_node_num(dom_file):
    DOMTree = parse(dom_file)
    root = DOMTree.documentElement
    clickable_elements = get_all_interactive_node(root)
    return len(clickable_elements)


if __name__ == "__main__":
    dom_file = 'G:/Result_UI_page/1/0.725_96_181.dom'
    # i=tackle_id('id/Wang_Yi_Hui')
    # print(i)
    # dom_file = '36.dom'
    features = get_features(dom_file)
    print(features)

# if __name__ == "__main__":
#     dom_file = '2.dom'
#     DOMTree = parse(dom_file)
#     root = DOMTree.documentElement
#     print(root.getAttribute('rotation'))
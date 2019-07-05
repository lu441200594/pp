import cv2


def find_image_cv(obj_path, src_path):
    source = cv2.imread(src_path)
    template = cv2.imread(obj_path)
    result = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
    min_max_loc = cv2.minMaxLoc(result)
    pos_start = min_max_loc[3]
    loc_x = int(pos_start[0]) + int(template.shape[1] / 2)
    loc_y = int(pos_start[1]) + int(template.shape[0] / 2)
    similarity = min_max_loc[1]
    if similarity < 0.85:
        return -1, -1
    else:
        return loc_x, loc_y


if __name__ == "__main__":
    obj_path = 'resource/button/confirm.png'
    src_path = 'resource/screen/now_confirm.png'
    x, y = find_image_cv(obj_path, src_path)
    print(str(x) + ',' + str(y))

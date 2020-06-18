import cv2
import numpy as np

def Get_Croped_image(img,bb_data):
    
    x = bb_data[0]
    y = bb_data[1]
    w = bb_data[2]
    h = bb_data[3]
    crop_img = img[y:y+h, x:x+w]
    return crop_img

def detect_faces(img):

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
    #img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0 :
        bb_data = faces.tolist()
        return bb_data

    else:
        return int(0)

def image_resize_and_preprocessing(img, img_shape):
    img = cv2.resize(img, img_shape)
    img = np.array(img / (np.max(img)+ 0.001))
    img = img[np.newaxis, ...]
    return img

def age_class_to_age_range(key):
    if not (isinstance(key, int)):
        raise TypeError
    else:
        if key >= 0 and key <=14:

            dict_age = { 0 : '0-2',
            1 : '3-5',
            2 : '6-10',
            3 : '11-15',
            4 : '16-20',
            5 : '21-25',
            6 : '26-30',
            7 : '31-35',
            8 : '36-40',
            9 : '41-50',
            10 : '51-60',
            11 : '61-70',
            12 : '71-80',
            13 : '81-90',
            14 : '91-100'
        }
            return dict_age[key]
        else:
            raise "Value not in proper range of the dictionary keys"
def draw_rect_put_text(img, bb_data, age_range):
    img = cv2.rectangle(img, (bb_data[0], bb_data[1]), ((bb_data[0]+bb_data[2]), (bb_data[1]+bb_data[3])), (0,0,255), 4)
    img = cv2.putText(img, str(age_range), (bb_data[0], bb_data[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,23,193), 4)
    return img

if __name__ == "__main__":

    bb_data = detect_faces("./images_upload/<file_name>")
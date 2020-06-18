from tensorflow import keras
#from tensorflow.keras.models import load_model
#from tensorflow.keras.models import Model, load_model
#from tensorflow.keras.applications.resnet50 import ResNet50
#from tensorflow.keras.layers import Convolution2D, Dense, Input, Flatten, Dropout, MaxPooling2D, BatchNormalization, \
    #GlobalMaxPool2D, Concatenate, GlobalMaxPooling2D, GlobalAveragePooling2D, Lambda, Conv2D


def get_model(n_classes=15):

    #base_model = keras.applications.nasnet.NASNetMobile(weights="./NASNet-mobile-no-top.h5", include_top=False)
    base_model = keras.applications.resnet50.ResNet50(weights="imagenet", include_top=False, input_tensor=keras.layers.Input(shape=(224,224,3)))#(Input(shape=(224, 224, 3)))
    #for layer in base_model.layers:
    #    layer.trainable = False

    x = base_model.output
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(350,activation="relu")(x)
    #x = Dense(100,activation="relu")(x)
    x = keras.layers.Dropout(0.2)(x)
    if n_classes == 1:
        x = keras.layers.Dense(n_classes, activation="sigmoid")(x)
    else:
        x = keras.layers.Dense(n_classes, activation="softmax")(x)

    base_model = keras.models.Model(base_model.input, x, name="base_model")
    
    return base_model

def load_model_weights(path):
    model = get_model()
    model.load_weights(path)
    #model = keras.models.load_model(path)
    return model

if __name__ == "__main__":

    model = load_model_weights("./imdb_age_recog_acc_85_resnet50_15_classes_weights.h5")
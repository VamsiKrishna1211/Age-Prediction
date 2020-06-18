from tensorflow import keras



def get_model(n_classes=15):

    base_model = keras.applications.resnet50.ResNet50(weights="imagenet", include_top=False, input_tensor=keras.layers.Input(shape=(224,224,3)))#(Input(shape=(224, 224, 3)))
    

    x = base_model.output
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(350,activation="relu")(x)
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
    return model

if __name__ == "__main__":

    model = load_model_weights("./imdb_age_recog_acc_85_resnet50_15_classes_weights.h5")
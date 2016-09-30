from keras.models import Model
from keras.layers import Input, Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D

def build_model():
    v = Input(shape=(28,28))
    h = Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))(v)
    h = Activation('relu'))(h)
    h = Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))(h)
    h = Activation('relu'))(h)
    h = MaxPooling2D(pool_size=pool_size))(h)
    h = Dropout(0.25))(h)
    
    h = Flatten())(h)
    h = Dense(128))(h)
    h = Activation('relu'))(h)
    h = Dropout(0.5))(h)
    h = Dense(nb_classes))(h)
    o = Activation('softmax'))(h)

    model = Model(input=v, output=o)
    return model



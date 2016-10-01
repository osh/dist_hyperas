
def build_model():

    from keras.models import Model
    from keras.layers import Input, Dense, Dropout, Activation, Flatten, Reshape
    from keras.layers import Convolution2D, MaxPooling2D

    nb_classes = 10
    nb_filters = {{nb_filters,choice,[64,32,16,8]}}
    pool_size = (2,2)
    kernel_size = (3,3)

    v = Input(shape=(28,28))
    h = Reshape([1,28,28])(v)
    h = Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid')(h)
    h = Activation('relu')(h)
    {{cnn_layer2,maybe,
    h = Convolution2D(nb_filters, kernel_size[0], kernel_size[1])(h)
    h = Activation('relu')(h)
    }}
    h = MaxPooling2D(pool_size=pool_size)(h)
    h = Dropout(0.25)(h)
    
    h = Flatten()(h)
    h = Dense(128)(h)
    h = Activation('relu')(h)
    h = Dropout(0.5)(h)
    h = Dense(nb_classes)(h)
    o = Activation('softmax')(h)

    model = Model(input=v, output=o)
    return model



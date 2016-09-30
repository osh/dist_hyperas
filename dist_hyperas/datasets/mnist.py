asdasd sa

from keras.datasets import mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

def train_model(model):
    model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])
    model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))
    return model.evaluate(X_test, Y_test, verbose=0)


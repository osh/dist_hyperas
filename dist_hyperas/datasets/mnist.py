
def train_model(model):
    batch_size = 128
    nb_epoch = 2
    nb_classes = 10

    from keras.datasets import mnist
    from keras.utils import np_utils
    import time
    a = time.time()

    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)

    model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
    h = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=0, validation_data=(X_test, Y_test))

    (loss,acc) = model.evaluate(X_test, Y_test, verbose=0)
    return {'loss':loss, 'accuracy':acc, 'epoch':h.epoch, 'time':time.time()-a, 'loss_hist':h.history['loss'], 'vloss_hist':h.history['val_loss']}


import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score
import sys
sys.path.insert(0, '/Workspace-Github/fruit_classification/code')
import P3_generate_data as generate

batch_size = 10
num_classes = 4
epochs = 10

x_train, x_valid, x_test, y_train, y_valid, y_test = generate.get_data()
'''
plt.figure(figsize = (18, 18))
for i in range(16):
    plt.subplot(4, 4, i + 1)
    plt.imshow(x_train[i], cmap=plt.get_cmap('gray'))
plt.show()
'''
print(np.shape(x_train))
print(np.shape(x_valid))
print(np.shape(x_test))
x_train = x_train.reshape(-1, 16384,3)
x_valid = x_valid.reshape(-1, 16384,3)
x_test = x_test.reshape(-1, 16384, 3)
x_train = x_train.astype('float32')
x_valid = x_valid.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_valid /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_valid.shape[0], 'valid samples')
print(x_test.shape[0], 'test samples')

y_train = keras.utils.to_categorical(y_train, num_classes)
y_valid = keras.utils.to_categorical(y_valid, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


img_rows, img_cols = 128, 128
x_train = x_train.reshape(x_train.shape[0], img_cols, img_rows, 3) 
x_valid = x_valid.reshape(x_valid.shape[0], img_cols, img_rows, 3)
x_test = x_test.reshape(x_test.shape[0], img_cols, img_rows, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_cols, img_rows, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten(input_shape=model.output_shape[1:])) # input: 64 layers of 4*4, output: =64*4*4=1024
model.add(Dense(64, activation='relu')) #=128
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
model.summary()

model.compile(loss=keras.losses.categorical_crossentropy,
                #optimizer=keras.optimizers.SGD(lr=3e-5),
                optimizer = keras.optimizers.Adam(lr=3e-5, decay=1e-6),
                metrics=['accuracy'])

run = model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=epochs,
                  verbose=1,
                  validation_data=(x_valid, y_valid)#,
                  )#callbacks=callbacks_list
score = model.evaluate(x_test, y_test, verbose=0)
y_pred = np.argmax(model.predict(x_test), axis=1)

print(y_test)
print(y_pred)

model.save('/Workspace-Github/fruit_classification/code/model_CNN.h5')

print('Confusion matrix: ', confusion_matrix(y_test, y_pred))
print('Accuracy score: ', accuracy_score(y_test, y_pred))
print('Precision score: ', precision_score(y_test, y_pred, average='weighted'))
print('Recall score: ', recall_score(y_test, y_pred, average='weighted'))
print('F1 score: ', f1_score(y_test, y_pred, average='weighted'))
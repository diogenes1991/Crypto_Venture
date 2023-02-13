import tensorflow as tf
from tensorflow import keras
from keras import layers

import matplotlib.pyplot as plt
import random


class Model:

    def __init__(self,name,path,Dataset):
        ilayer = layers.Dense(units = 29, input_dim = len(Dataset[0,:-1]), activation="relu")
        layer1 = layers.Dense(units = 23, activation="relu")
        layer2 = layers.Dense(units = 19, activation="relu")
        layer3 = layers.Dense(units = 17, activation="relu")
        layer4 = layers.Dense(units = 13, activation="relu")
        layer5 = layers.Dense(units = 11, activation="relu")
        layer6 = layers.Dense(units = 29, activation="relu")
        layer7 = layers.Dense(units = 31, activation="relu")
        layer8 = layers.Dense(units = 11, activation="relu")
        olayer = layers.Dense(units = 1, activation = "sigmoid")

        model = keras.Sequential([ilayer,layer1,layer2,layer3,layer4,layer5,layer6,layer7,layer8,olayer])
    
        model.compile(
        optimizer = keras.optimizers.SGD(1.25E-4),
        loss="binary_crossentropy"
        )

        self.data    = Dataset
        self.name    = name
        self.model   = model
        self.path    = path
        self.saver   = tf.keras.callbacks.ModelCheckpoint(filepath =self.path, save_weights_only = True)
        self.history = []
        
    def train(self,fraction,epoc=2000):
        '''
        
            Uses the first fraction of the entire dataset as training
            @params:
                fraction: (double) fraction of the dataset to be trained on
        
        '''

        tf.keras.backend.clear_session()

        point = int(len(self.data)*fraction)

        self.xtrain = self.data[:point,:-1]
        self.ytrain = self.data[:point,-1:]

        self.xtest  = self.data[point:,:-1]
        self.ytest  = self.data[point:,-1:]

        self.history.append(self.model.fit(x = self.xtrain, y=self.ytrain, epochs=epoc, verbose = True, callbacks = [self.saver]))
        plt.plot(self.history[-1].history["loss"])
        plt.show()

    def setSavePath(self,path):
        self.path  = path
        self.saver = tf.keras.callbacks.ModelCheckpoint(filepath =self.path, save_weights_only = True)
 
    def loadFromPath(self,path):
        self.model.load_weights(path)

    def analyze(self):

        def process(prediction): #converts from % prediction to [0,0,1,0]
            for i in range(len(prediction)):
                Maxj = 0
                for j in range(len(prediction[i])):
                    if prediction[i][j] > prediction[i][Maxj]:
                        Maxj = j       
                prediction[i] = [0 if prediction[i][Maxj] > prediction[i][j] else 1 for j in range(len(prediction[i]))]

        def computeEfficiency(difference):
            eff = 0
            for predict in difference:
                eff += 1
                for feature in predict:
                    if feature != 0:
                        eff -= 1
                        break
                    
            eff /= len(difference)
            return eff*100

        predtest = self.model.predict(self.xtest)
        predtrain = self.model.predict(self.xtrain)
        
        process(predtest)
        process(predtrain)

        difftest = abs(predtest-self.ytest)
        difftrain = abs(predtrain-self.ytrain)

        self.effTest = computeEfficiency(difftest)
        self.effTrain = computeEfficiency(difftrain)

        print(self.name," Efficiency on Test :",self.effTest,"%")
        print(self.name," Efficiency on Train:",self.effTrain,"%")
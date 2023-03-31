
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense


class Historico:

    def __init__(self, arquivo, n_features, memoria=60):
        self.arquivo = arquivo
        self.memoria = memoria
        self.n_features = n_features
        self.model = None
        self.data_mean = None
        self.data_std = None

    def load_data(self):
        df = pd.read_csv(self.arquivo)
        # Extrai as colunas de números sorteados
        data = df.iloc[:, 2:].values.astype(np.float32)
        # Normaliza os dados
        self.data_mean = data.mean(axis=0)
        self.data_std = data.std(axis=0)
        data = (data - self.data_mean) / self.data_std

        return data

    def dividir(self, sequence):
        x, y = list(), list()
        for i in range(len(sequence)):
            end_ix = i + self.memoria
            if end_ix > len(sequence)-1:
                break
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            x.append(seq_x)
            y.append(seq_y)
        return np.array(x), np.array(y)

    def criamodelo(self):
        # Constrói o modelo LSTM
        self.model = Sequential()
        self.model.add(LSTM(50, activation='relu', input_shape=(self.memoria, self.n_features)))
        self.model.add(Dense(self.n_features))
        self.model.compile(optimizer='adam', loss='mse')
        return None

    def treinar(self, x_train, y_train, epochs=1000, batch_size=32):
        # Treina o modelo
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2)

    def predict(self, x):
        # Faz a previsão dos próximos números sorteados
        x = np.reshape(x, (1, self.memoria, self.n_features))
        y_pred = self.model.predict(x)
        y_pred = y_pred * self.data_std + self.data_mean
        return y_pred

    def evaluate(self, x_test, y_test):
        # Avalia o desempenho do modelo
        score = self.model.evaluate(x_test, y_test, verbose=0)
        return score


if __name__ == '__main__':

    analise = Historico(arquivo='./dados/')


import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


class Historico:

    def __init__(self, arquivo, n_features, memoria=60):
        self.arquivo = arquivo
        self.memoria = memoria
        self.n_features = n_features
        self.model = None
        self.data_mean = None
        self.data_std = None
        self.__datapresenter = None
        self.__getdata = None
        self.__scaler = MinMaxScaler()

    def load_data(self):
        df = pd.read_csv(self.arquivo)
        df = df.iloc[::-1]
        # Extrai as colunas de números sorteados - Todas as linhas e da segunda coluna até o final
        data = df.iloc[:, 2:].values.astype(np.float32)
        self.__datapresenter = df.head()
        # Normaliza os dados
        self.data_mean = data.mean(axis=0)
        self.data_std = data.std(axis=0)
        data = (data - self.data_mean) / self.data_std
        self.__getdata = data
        return data

    def getdata(self):
        return self.__getdata

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
        self.model.add(LSTM(60, activation='relu', input_shape=(self.memoria, self.n_features)))
        self.model.add(Dense(self.n_features))
        self.model.compile(optimizer='adam', loss='mse')
        return None

    def treinar(self, x_train, y_train, epochs=100, batch_size=32):
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

    def head(self):
        print(f'\n{self.__datapresenter} \n')

    def save_model(self, filename):
        # Utilizar formato h5
        self.model.save(filename)

    def sugerir(self):
        # seleciona os últimos 'sequence_length' registros do conjunto de dados
        last_records = self.__getdata[-self.memoria:, :]
        self.__scaler.fit(last_records)
        last_records_norm = self.__scaler.transform(last_records)

        # faz a previsão para o próximo registro
        y_pred_norm = self.predict(last_records_norm)

        # inverte a normalização dos valores previstos e arredonda para inteiros entre 1 e 60
        y_pred = np.round(self.__scaler.inverse_transform(y_pred_norm)).flatten()
        y_pred = np.clip(y_pred, 1, 60)

        # imprime as previsões para as colunas 'b1', 'b2', 'b3', 'b4', 'b5' e 'b6'
        print('Previsões para as próximas bolas:')
        print('b1:', y_pred[0])
        print('b2:', y_pred[1])
        print('b3:', y_pred[2])
        print('b4:', y_pred[3])
        print('b5:', y_pred[4])
        print('b6:', y_pred[5])


if __name__ == '__main__':

    analise = Historico(arquivo='./dados/megasena.csv', n_features=6, memoria=55)
    data_x, data_y = analise.dividir(analise.load_data())
    analise.criamodelo()
    analise.head()
    analise.treinar(data_x, data_y, epochs=200, batch_size=32)
    analise.save_model('./checkpoint/teste.h5')
    print(f'Avaliação do modelo: {analise.evaluate(data_x, data_y):.2f}')
    analise.sugerir()


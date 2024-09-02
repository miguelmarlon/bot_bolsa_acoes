import os
import subprocess
from scheduler import get_data
from sklearn.linear_model import Ridge
import joblib
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np

folder_path = 'D:/backup/importantes/pythoncodigos/projeto_bolt_bolsa2/MLSpikeDetector/DATA/META'

def deleting_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"A pasta '{folder_path}' não existe.")
        return

    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Arquivo   deletado: {file_path}")
                except OSError as e:
                    print(f"Erro ao deletar '{file_path}': {e}")
    except OSError as e:
        print(f"Erro ao acessar a pasta '{folder_path}': {e}")

while True:
    option = input('0 - EXIT\n\n'
                   '1 - START FORECAST\n\n'
                                      
                   'OPTION: ')
    match option:
        case '0':
            deleting_files(folder_path)
            print('EXITING THE PROGRAM...')
            exit()
        case '1':
            symbol = input('Enter the name of the sticker: \n')
            time = int(input('What is the timeframe? Ex.: 1, 5, 15 \n'))
            time2 = str(input('Minutes or Hours?\n'))
            command = f'python scheduler.py python {time} {time2} {symbol}'

            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            venv_path = os.path.join(ROOT_DIR, '.venv', 'Scripts', 'activate.bat')
            subprocess.Popen(f'cmd /c "{venv_path} && {command}"', shell=True)

            print("Ainda continuo executando!!!")
        case '2':
            symbol = input('Enter the name of the sticker: \n')
            df = get_data(symbol)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            print(df)
            x_alvo = df.loc[:, ['open', 'close']].to_numpy()
            #x_alvo = df.iloc[-1].values
            #print(x_alvo)
            X_alvo = x_alvo[-1]
            #print(X_alvo)
            X_alvo = X_alvo.reshape(1, -1)
            X_alvo = X_alvo[:, ~np.isnan(X_alvo).any(axis=0)]

            #X =df[['open', 'high', 'low', 'close']].values
            X = df[['open', 'close']].values
            y = df['close'].values

            split = int(0.7 * (len(X)))
            X_train = X[:split]
            y_train = y[:split]
            X_test = X[split:]
            y_test = y[split:]

            model = Ridge(alpha=0.01)
            model.fit(X_train, y_train)
            predicted_price = model.predict(X_alvo)

            valorizacao = (predicted_price - X_alvo[0,0]) / X_alvo[0,0]
            valorizacao *= 100

            scores = cross_val_score(model, X, y, cv=5, scoring='r2')
            scor = scores.mean()
            print(f'Taxa de acerto: {scor}')
            print(f'Valorização prevista em %: {valorizacao}' )
        case _:
            print('INVALID OPTION!')
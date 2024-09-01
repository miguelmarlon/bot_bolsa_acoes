import os
import subprocess

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
            sticker = input('Enter the name of the sticker: \n')
            time = int(input('What is the timeframe? Ex.: 1, 5, 15 \n'))
            time2 = str(input('Minutes or Hours?\n'))
            command = f'python scheduler.py python {time} {time2} {sticker}'

            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            venv_path = os.path.join(ROOT_DIR, '.venv', 'Scripts', 'activate.bat')
            subprocess.Popen(f'cmd /c "{venv_path} && {command}"', shell=True)

            print("Ainda continuo executando!!!")
        case _:
            print('INVALID OPTION!')
import subprocess
import sys
import mysql.connector
from mysql.connector import errorcode

def install_packages():
    packages = ["flask", "mysql-connector-python", "bcrypt", "pyjwt", "flask-cors"]
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def setup_database(host="127.0.0.1", user="root", password="", database="delivery", port=3306, sql_file="./docs/banco.sql"):
    try:
        cnx = mysql.connector.connect(host=host, user=user, password=password, port=port)
        cursor = cnx.cursor()

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        commands = sql_script.split(';')

        for command in commands:
            command = command.strip()
            if command:
                cursor.execute(command)

        cnx.commit()
        print(f"Script SQL '{sql_file}' executado com sucesso!")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Usuário ou senha incorretos")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    print("Instalando pacotes...")
    install_packages()
    print("Configurando banco de dados...")
    setup_database(password="") 
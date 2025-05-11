import psycopg2 # type: ignore
import time
from flask import Flask, request # type: ignore
from flask_restx import Api, Resource  # type: ignore

app = Flask(__name__)
api = Api(app, version='1.0', title='Atividade III - Data Ops | Operações Matemáticas', description='API para soma e multiplicação', doc='/swagger')

ns = api.namespace('Operações', description='Soma e Multiplicação')

def connect_to_postgres():
    conn = psycopg2.connect(
        host="db",
        dbname="postgres",
        user="postgres",
        password="123456"
    )
    return conn

def criar_tabela():
    time.sleep(5)
    conn = connect_to_postgres()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operacoes (
            id SERIAL PRIMARY KEY,
            num1 NUMERIC,
            num2 NUMERIC,
            operacao VARCHAR(20),
            resultado NUMERIC
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

criar_tabela()

@ns.route('/soma')
class Soma(Resource):
    def post(self):
        dados = request.get_json()
        a = dados.get('a')
        b = dados.get('b')
        if a is None or b is None:
            return {'erro': 'Parâmetros "a" e "b" são obrigatórios'}, 400

        resultado = a + b

        conn = connect_to_postgres()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO operacoes (num1, num2, operacao, resultado) VALUES (%s, %s, %s, %s)", (a, b, 'soma', resultado))
        conn.commit()
        cursor.close()
        conn.close()

        return {'resultado': resultado}

@ns.route('/multiplicacao')
class Multiplicacao(Resource):
    def post(self):
        dados = request.get_json()
        a = dados.get('a')
        b = dados.get('b')
        if a is None or b is None:
            return {'erro': 'Parâmetros "a" e "b" são obrigatórios'}, 400

        resultado = a * b

        conn = connect_to_postgres()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO operacoes (num1, num2, operacao, resultado) VALUES (%s, %s, %s, %s)", (a, b, 'multiplicacao', resultado))
        conn.commit()
        cursor.close()
        conn.close()

        return {'resultado': resultado}

@ns.route('/operacoes')
class ListaOperacoes(Resource):
    def get(self):
        conn = connect_to_postgres()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operacoes ORDER BY id")
        operacoes = cursor.fetchall()
        cursor.close()
        conn.close()

        return {'operacoes': [
            {
                'id': op[0],
                'num1': op[1],
                'num2': op[2],
                'operacao': op[3],
                'resultado': op[4]
            } for op in operacoes
        ]}
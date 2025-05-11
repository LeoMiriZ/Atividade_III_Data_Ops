import psycopg2 # type: ignore
import time
from flask import Flask, request # type: ignore
from flask_restx import Api, Resource, fields  # type: ignore

app = Flask(__name__)
api = Api(app, version='1.0', title='Atividade III - Data Ops | Operações Matemáticas', description='API para Soma e Multiplicação', doc='/swagger')

ns = api.namespace('operacoes', description='Soma e Multiplicação')

operacao_input = ns.model('Números Exigidos', {
    'num1': fields.Integer(required=True),
    'num2': fields.Integer(required=True)
})

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
            num1 INT,
            num2 INT,
            operacao VARCHAR(30),
            resultado INT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

criar_tabela()

@ns.route('/')
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

@ns.route('/soma')
class Soma(Resource):
    @ns.expect(operacao_input)
    def post(self):
        dados = request.get_json()
        num1 = dados.get('num1')
        num2 = dados.get('num2')
        if num1 is None or num2 is None:
            return {'erro': 'Parâmetros "num1" e "num2" são obrigatórios'}, 400

        resultado = num1 + num2

        conn = connect_to_postgres()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO operacoes (num1, num2, operacao, resultado) VALUES (%s, %s, %s, %s)", (num1, num2, 'soma', resultado))
        conn.commit()
        cursor.close()
        conn.close()

        return {'resultado': resultado}

@ns.route('/multiplicacao')
class Multiplicacao(Resource):
    @ns.expect(operacao_input)
    def post(self):
        dados = request.get_json()
        num1 = dados.get('num1')
        num2 = dados.get('num2')
        if num1 is None or num2 is None:
            return {'erro': 'Parâmetros "num1" e "num2" são obrigatórios'}, 400

        resultado = num1 * num2

        conn = connect_to_postgres()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO operacoes (num1, num2, operacao, resultado) VALUES (%s, %s, %s, %s)", (num1, num2, 'multiplicacao', resultado))
        conn.commit()
        cursor.close()
        conn.close()

        return {'resultado': resultado}
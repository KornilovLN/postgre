import paramiko
import psycopg2
from sshtunnel import SSHTunnelForwarder
import math
import time
from flask import Flask, jsonify, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# SSH и PostgreSQL данные
ssh_host = '192.168.88.104'
ssh_port = 22
ssh_user = 'starmark'
ssh_password = '!18leon28'

db_host = 'localhost'
db_port = 5432
db_name = 'pg_db_star'
db_user = 'starmark'
db_password = '18star28'

def clear_table():
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(db_host, db_port)
    ) as tunnel:
        print("SSH туннель установлен")

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port
        )
        cursor = conn.cursor()
        print("Подключение к базе данных установлено")

        clear_table_query = '''
        TRUNCATE TABLE public.meassure;
        '''
        cursor.execute(clear_table_query)
        conn.commit()
        print("Таблица public.meassure очищена")

        cursor.close()
        conn.close()
        print("Соединение с базой данных закрыто")

@app.route('/generate_data', methods=['GET'])
def generate_data():
    clear_table()  # Очистка таблицы перед генерацией новых данных

    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(db_host, db_port)
    ) as tunnel:
        print("SSH туннель установлен")

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port
        )
        cursor = conn.cursor()
        print("Подключение к базе данных установлено")

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS public.meassure (
            id SERIAL PRIMARY KEY,
            post INT,
            timestamp TIMESTAMP,
            x DOUBLE PRECISION,
            y DOUBLE PRECISION
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        print("Таблица public.meassure проверена/создана")

        insert_query = '''
        INSERT INTO public.meassure (post, timestamp, x, y)
        VALUES (%s, %s, %s, %s);
        '''
        post = 1
        for id in range(1, 101):
            x = id/5
            y = 1000 * math.sin(x)*math.cos(x)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (post, timestamp, x, y))
            conn.commit()
            print(f"Вставлена строка: id={id}, post={post}, timestamp={timestamp}, x={x}, y={y}")

        cursor.close()
        conn.close()
        print("Соединение с базой данных закрыто")

    return jsonify({"status": "success", "message": "Data generated and inserted successfully"})

@app.route('/view_data', methods=['GET'])
def view_data():
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(db_host, db_port)
    ) as tunnel:
        print("SSH туннель установлен")

        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port
        )
        cursor = conn.cursor()
        print("Подключение к базе данных установлено")

        select_query = '''
        SELECT * FROM public.meassure;
        '''
        cursor.execute(select_query)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        print("Соединение с базой данных закрыто")

    # Формируем DataFrame
    df = pd.DataFrame(rows, columns=['id', 'post', 'timestamp', 'x', 'y'])

    # Построение графика
    plt.figure(figsize=(10, 5))
    plt.plot(df['x'], df['y'], marker='o')
    plt.title('График функции y=f(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Формируем HTML
    html = '''
    <html>
    <head>
        <title>Данные <- public.meassure <- bg_db_star <- 192.168.88.104</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }}
            header {{
                background-color: #e0f7fa;
                padding: 20px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }}
            .content {{
                display: flex;
                flex: 1;
            }}
            .sidebar {{
                background-color: #d7ccc8;
                padding: 20px;
                width: 30%;
                overflow-y: auto;
            }}
            .main {{
                background-color: #fff9c4;
                padding: 20px;
                width: 70%;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .graph {{
                margin-top: 20px;
                width: 95%;
            }}
            table {{
                width: 90%;
                border-collapse: collapse;
                margin: 0 auto;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <header>Данные из таблицы public.meassure базы данных bg_db_star на 192.168.88.104</header>
        <div class="content">
            <div class="sidebar">
                {table}
            </div>
            <div class="main">
                <!-- <img src="data:image/png;base64,{img_base64}" alt="График функции y=f(x)" style="width: 95%;"> -->
                <img src="data:image/png;base64,{img_base64}" alt="График функции y=f(x)" class="graph">
            </div>
        </div>
    </body>
    </html>
    '''.format(table=df.to_html(index=False), img_base64=img_base64)

    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

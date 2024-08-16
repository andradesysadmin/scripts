from flask import Flask, render_template_string
from scapy.all import ICMP, IP, sr1
import threading
import time
import psutil
import socket

app = Flask(__name__)

server_ips = [
    '192.168.10.3',
    '192.168.10.4',
    '192.168.10.13',
    '192.168.10.21',
    '192.168.10.6',
    '192.168.10.40',
    '192.168.10.18'
]

status = {ip: {'reachable': False, 'cpu_usage': None, 'network_speed': None} for ip in server_ips}

def ping_server(host):
    global status
    while True:
        pkt = IP(dst=host)/ICMP()
        resp = sr1(pkt, timeout=2, verbose=False)
        status[host]['reachable'] = bool(resp)
        time.sleep(1)  

def monitor_server_resources():
    global status
    while True:
        for ip in status.keys():

            try:
                cpu_usage = psutil.cpu_percent(interval=1)
            except Exception as e:
                cpu_usage = str(e)

            try:
                net_io = psutil.net_io_counters()
                network_speed = f"Enviado: {net_io.bytes_sent / (1024 * 1024):.2f} MB, Recebido: {net_io.bytes_recv / (1024 * 1024):.2f} MB"
            except Exception as e:
                network_speed = str(e)

            status[ip]['cpu_usage'] = cpu_usage
            status[ip]['network_speed'] = network_speed

        time.sleep(1)  

@app.route('/')
def index():
    return render_template_string("""
        <html>
        <head>
            <title>Status dos Servidores</title>
            <style>
                .status-active { color: green; }
                .status-inactive { color: red; }
                body{
                    background-color: black;
                    color: white;
                }
            </style>
            <script>
                function refreshPage() {
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);  // Atualiza a cada 1 segundo
                }
                window.onload = refreshPage;
            </script>
        </head>
        <body>
            <h1>Status dos Servidores</h1>
            <ul>
                {% for ip, data in status.items() %}
                    <li>Servidor {{ ip }} está <span class="{{ 'status-active' if data['reachable'] else 'status-inactive' }}">
                        {% if data['reachable'] %}ativo{% else %}inativo{% endif %}
                    </span>. Uso da CPU: {{ data['cpu_usage'] }}%. Velocidade da Rede: {{ data['network_speed'] }}.</li>
                {% endfor %}
            </ul>
        </body>
        </html>
    """, status=status)

if __name__ == '__main__':
    threads = []
    for ip in server_ips:
        thread = threading.Thread(target=ping_server, args=(ip,))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    resource_thread = threading.Thread(target=monitor_server_resources)
    resource_thread.daemon = True
    resource_thread.start()
    threads.append(resource_thread)

    app.run(debug=True)

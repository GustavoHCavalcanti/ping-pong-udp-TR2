import socket
import time

SERVIDOR = "137.131.178.229"
PORTA = 8080

def criar_socket(timeout=5.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    return sock

def ping(sock, servidor):
    inicio = time.time()

    sock.sendto(b"PING", servidor)
    dados, endereco = sock.recvfrom(65507)

    fim = time.time()

    rtt = (fim - inicio) * 1000

    resposta = dados.decode("utf-8")

    # Exemplo:
    # PONG|time=1789392721.784
    partes = resposta.split("|")
    server_time = float(partes[1].split("=")[1])

    return rtt, server_time

def main():
    sock = criar_socket()
    servidor = (SERVIDOR, PORTA)

    print("=== Tarefa 0 - RDT-UnB Explorer ===")
    print(f"Servidor: {SERVIDOR}:{PORTA}")
    print()

    print("[1] PING")

    try:
        rtt, server_time = ping(sock, servidor)

        print(f"    RTT: {rtt:.2f} ms")
        print(f"    Time do servidor: {server_time}")

    except socket.timeout:
        print("    Timeout: o servidor não respondeu.")

    finally:
        sock.close()

if __name__ == "__main__":
    main()
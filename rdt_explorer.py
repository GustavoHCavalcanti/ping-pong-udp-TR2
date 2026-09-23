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

def hello(sock, servidor, grupo):
    # envia HELLO, parseia OK, retorna dict com os campos

    pacote = f"HELLO|grupo = {grupo} |segment_size = 512 | file = small"

    sock.sendto(pacote.encode("utf-8"), servidor)

    dados_retornados, endereco = sock.recvfrom(65507)

    resposta = dados_retornados.decode("utf-8")

    #Exemplo
    #OK|file_size=1048576|checksum=8cd2797a0e3486d2c7aebf3f8d12656b|...
    campos = resposta.split("|")
    tamanho_do_arquivo = int(campos[1].split("=")[1])
    cheksum = campos[2].split("=")[1]
    total_segmentos = campos[4].split("=")[1]
    tamanho_segmento = campos[5].split("=")[1]

    return tamanho_do_arquivo, cheksum , total_segmentos , tamanho_segmento

def requisitar_segmento(sock, servidor, seq=0):
    # Envia o pacote REQ
    pacote = f"REQ|seq={seq}"
    sock.sendto(pacote.encode("utf-8"), servidor)

    # Recebe a resposta do servidor
    dados, endereco = sock.recvfrom(65507)

    #Exemplo: DATA|seq=0|total=512|<payload>
    # índices do 1º, 2º e 3º separador "|"
    idx1 = dados.find(b"|")
    idx2 = dados.find(b"|", idx1 + 1)
    idx3 = dados.find(b"|", idx2 + 1)
    
    # cabeçalho vai até o caractere logo após o 3º "|"
    tamanho_cabecalho = idx3 + 1
    
    # dados a partir do final do cabeçalho 
    payload = dados[tamanho_cabecalho:]
    
    return payload


def main():
    sock = criar_socket()
    servidor = (SERVIDOR, PORTA)
    grupo = "Grupo06"

    print("=== Tarefa 0 - RDT-UnB Explorer ===")
    print(f"Servidor: {SERVIDOR}:{PORTA}")
    print()

    

    try:
        # Passo 1 — PING
        print("[1] PING")
        rtt, server_time = ping(sock, servidor)

        print(f"    RTT: {rtt:.2f} ms")
        print(f"    Time do servidor: {server_time}")
        print()

        # Passo 2 — HELLO
        print("[2] HELLO")

        tamanho_do_arquivo,checksum,total_segmentos,tamanho_segmentos = hello(sock,servidor,grupo)
        print(f"    Arquivo: small ({tamanho_do_arquivo} = {int(tamanho_do_arquivo/1024)} KB)")
        print(f"    Checksum MD5:: {checksum}")
        print(f"    Total segmentos: {total_segmentos}")
        print(f"    Tamanho segmento: {tamanho_segmentos} bytes")
        print()

        # Passo 3 — REQ
        print("[3] REQ")
        
        payload = requisitar_segmento(sock, servidor, seq=0)
        tamanho_payload = len(payload)
        
        # Pega os primeiros 8 bytes e formata como hexadecimal
        primeiros = payload[:8]
        hex_str = " ".join(f"{b:02x}" for b in primeiros)
        
        print(f"    Payload recebido: {tamanho_payload} bytes")
        print(f"    Primeiros 8 bytes: {hex_str}")
        print()

    except socket.timeout:
        print("    Timeout: o servidor não respondeu.")

    finally:
        sock.close()

if __name__ == "__main__":
    main()
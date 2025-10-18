import socket
import pyaudio

# Настройки аудио
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Настройка сервера
server_ip = '0.0.0.0'
server_port = 60036

# Инициализация pyaudio и сокета
p = pyaudio.PyAudio()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, server_port))
s.listen(1)
print("Waiting for connection...")

conn, addr = s.accept()
print(f"Connected by {addr}")

# Настройка потока для воспроизведения
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# Получение и воспроизведение аудиоданных
try:
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        stream.write(data)
except Exception as e:
    print(f"Error receiving audio: {e}")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()
    s.close()

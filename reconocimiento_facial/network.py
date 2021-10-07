import socket
import os
import struct

#Clase para hacer cualquier tipo de accion por la red
class Socket_IoT:

    def send_file(self,sck: socket.socket, filename):
        # Obtener el tamaño del archivo a enviar.
        filesize = os.path.getsize(filename)
        # Informar primero al servidor la cantidad
        # de bytes que serán enviados.
        sck.sendall(struct.pack("<Q", filesize))
        # Enviar el archivo en bloques de 1024 bytes.
        with open(filename, "rb") as f:
            while read_bytes := f.read(1024):
                sck.sendall(read_bytes)

    def receive_file_size(self,sck: socket.socket):
        # Esta función se asegura de que se reciban los bytes
        # que indican el tamaño del archivo que será enviado,
        # que es codificado por el cliente vía struct.pack(),
        # función la cual genera una secuencia de bytes que
        # representan el tamaño del archivo.
        
        fmt = "<Q"      #ver documentacion struct.calcsize

        expected_bytes = struct.calcsize(fmt)
        received_bytes = 0
        stream = bytes()
        while received_bytes < expected_bytes:
            chunk = sck.recv(expected_bytes - received_bytes)
            stream += chunk
            received_bytes += len(chunk)
        filesize = struct.unpack(fmt, stream)[0]
        return filesize

    def receive_file(self,sck: socket.socket, filename):
        # Leer primero del socket la cantidad de 
        # bytes que se recibirán del archivo.
        filesize = self.receive_file_size(sck)
        # Abrir un nuevo archivo en donde guardar
        # los datos recibidos.
        with open(filename, "wb") as f:
            received_bytes = 0
            # Recibir los datos del archivo en bloques de
            # 1024 bytes hasta llegar a la cantidad de
            # bytes total informada por el cliente.
            while received_bytes < filesize:
                chunk = sck.recv(1024)
                if chunk:
                    f.write(chunk)
                    received_bytes += len(chunk)






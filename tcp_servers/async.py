#!/usr/local/bin/python
#это неблокрирующие сокеты: в этом случае, если процессу нечем заняться, то он не блокируется, а продолжает быть доступным
import socket
import select


server_socket = socket.socket()
server_socket.bind(('', 8080))
server_socket.setblocking(0)
server_socket.listen(10)

inputs = {server_socket}
outputs = {}
excepts = []


while 1:
    input_ready, output_ready, except_ready = select.select(list(inputs), outputs.keys(), excepts, 0.5)
    #формируем три списка сокетов (сокеты, в которые нам пишут; откуда нас читают; 
    for s in input_ready:
        if s == server_socket:
            client_socket, remote_address = server_socket.accept()
            client_socket.setblocking(0)
            inputs.add(client_socket)
        else:
            request = s.recv(1024)
            print '{} : {}'.format(s.getpeername(), request)
            outputs[s] = request.upper()#вот он минус данного подхода: если в этом месте вместо простейшей операции будет рендеринг видео,
            #то завершения операции будут ждать все. т.о. нельзя использовать надолго блокирующие операции при неблокирующем подходе
            inputs.remove(s)
    for s in output_ready:
        if s in outputs:
            s.send(outputs[s])
            del outputs[s]
            s.close()

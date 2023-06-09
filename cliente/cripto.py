import json
def encriptar(msg : bytearray) -> bytearray:

    a, b, c = bytearray(b""), bytearray(b""), bytearray(b"")
    vuelta = 0
    for byte in msg:
        
        if vuelta % 3 == 0:
            a.append(((byte)))

        elif vuelta % 3 == 1:
            b.append(((byte)))

        elif vuelta % 3 == 2:
            c.append(((byte)))
        
        vuelta += 1

    if len(b) % 2 == 0:
        a1 = len(b)// 2 - 1
        a2 = len(b) // 2 
        n_b1 = b[a1]
        n_b2 = b[a2]
        n = a[0] + c[-1] + n_b1 + n_b2

    else:
        n = a[0] + c[-1] + b[len(b)//2 - 1] 
    if n  % 2 == 1:
        retur= a + c +b
        numero = bytearray(b"\x01")
        return numero + retur
    
    retur = c + a + b
    numero = bytearray(b"\x00")
    retur = numero + retur
    return retur


def desencriptar(msg : bytearray) -> bytearray:
    metodo = msg[0]
    msg = msg[1:]
    largo = len(msg)
    if metodo == 1:
        #nacb
        suma = 0
        intervalo = largo // 3
        if largo % 3 >= 1:
            suma = 1
        a = (msg[:intervalo + suma])
        c = (msg[intervalo + suma:intervalo*2 + suma])
        b = (msg[intervalo*2 + suma:])
        
    else:
        
        suma = 0
        intervalo = largo // 3
        if largo % 3 != 0:
            suma = 1
        c = msg[:intervalo]
        a = msg[intervalo : intervalo*2 + suma]
        b = msg[intervalo*2 + suma :]

    ret =  bytearray(b"")
    for caracter in range(largo):
        
        numero = caracter//3 

        if caracter % 3 == 0:
            if numero == -1:
                numero = 0
            ret.append(a[numero])
        elif caracter % 3 == 1:
            ret.append(b[numero])
        else:
            ret.append(c[numero])

    return ret


if __name__ == "__main__":
    # Testear encriptar
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_esperado = bytearray(b'\x01\x05\x02\x05\x09\x03\x03\x05\x08\x04\x09\x01')

    msg_encriptado = encriptar(msg_original)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")

import ipaddress
import string

def calcular_flsm(ip, mascara):
    # Convertir la dirección IP y la máscara a una lista de números
    ip = [int(x) for x in ip.split('.')]
    mascara = [int(x) for x in mascara.split('.')]
   
    # Calcular la cantidad de bits de la máscara
    bits_mascara = sum([bin(byte).count('1') for byte in mascara])
   
    # Calcular el número de direcciones de host disponibles
    num_ips = 2**(32 - bits_mascara)
   
    # Calcular la máscara CIDR
    cidr = '/' + str(bits_mascara)
   
    # Calcular la dirección de red
    red = '.'.join([str(ip[i] & mascara[i]) for i in range(4)])
   
    # Calcular la dirección del primer host
    primer_host = red[:red.rfind('.')] + '.' + str((ip[3] & mascara[3]) + 1)
   
    # Calcular la dirección del último host
    ultimo_host = '.'.join([str(ip[i] | (255 - mascara[i])) for i in range(4)])
    ultimo_host = ultimo_host[:ultimo_host.rfind('.')] + '.' + str((ip[3] | (255 - mascara[3])) - 1)
   
    # Calcular la dirección de broadcast
    broadcast = '.'.join([str(ip[i] | (255 - mascara[i])) for i in range(4)])
   
    # Calcular el número máximo de hosts
    max_hosts = num_ips - 2
   
    return cidr, red, primer_host, ultimo_host, broadcast, num_ips, max_hosts

while True:
    print("""

🔨 Herramientas para redes.
     ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ 16/02/24
-------------------------------------
1. Calculadora de CIDR 🛠
2. Compresor/Descompresor IPv6 🛠
3. FLSM (Subneteo de longitud de prefijo fijo) 🛠
4. Salir
-------------------------------------
""")
    opcion = input("Selecciona una opción (1, 2, 3 o 4): ")

    if opcion == '1':
        print("""
 ----------------------------------
| Calculadora de CIDR | Versión CMD |
 ----------------------------------
""")
        def calcular_mascara_cidr(num_hosts):
            bits_necesarios = num_hosts.bit_length()
            mascara_cidr = 32 - bits_necesarios
            return mascara_cidr

        def calcular_info_red(ip, num_hosts):
            try:
                ip = ipaddress.IPv4Address(ip)
            except ipaddress.AddressValueError:
                print("La dirección IP introducida no es válida.")
                return

            if not ip.is_private:
                print("Esta calculadora solo admite direcciones IP privadas.")
                return

            if num_hosts < 2:
                print("Se necesitan al menos dos hosts (uno de red y uno de broadcast).")
                return

            mascara_cidr = calcular_mascara_cidr(num_hosts)

            red = ipaddress.IPv4Network(f"{ip}/{mascara_cidr}", strict=False)

            mascara_red = red.netmask
            broadcast = red.broadcast_address
            ultima_direccion_host = red.network_address + (2 ** (32 - mascara_cidr)) - 2

            total_direcciones = 2**(32 - mascara_cidr)
            direcciones_utilizables = total_direcciones - 2
            direcciones_desperdiciadas = max(0, total_direcciones - num_hosts - 2)

            print(f"IP de Red: {red.network_address}")
            print(f"Máscara de Red (CIDR): /{mascara_cidr}")
            print(f"IP de Broadcast: {broadcast}")
            print(f"Última dirección de host: {ultima_direccion_host}")
            print(f"Número total de direcciones en la red: {total_direcciones}")
            print(f"Direcciones utilizables: {direcciones_utilizables}")
            print(f"Direcciones desperdiciadas: {direcciones_desperdiciadas}")

        ip = input(f"Introduce la IP de red(Ipv4): ")
        num_hosts = int(input(f"Introduce el número de hosts: "))

        calcular_info_red(ip, num_hosts)
        input("Presiona cualquier tecla para volver al menú principal.")

    elif opcion == '2':
        print("""
    ----------------------
    |Descomprime tu IPv6.|
    ---------------------
    """)

        def comprimir_ipv6(direccion_ipv6):
            return ipaddress.IPv6Address(direccion_ipv6).compressed

        def descomprimir_ipv6(direccion_ipv6_comprimida):
            return ipaddress.IPv6Address(direccion_ipv6_comprimida).exploded

        ipv6_original = input("IPv6 Completa: ")
        ipv6_comprimida = comprimir_ipv6(ipv6_original)
        ipv6_descomprimida = descomprimir_ipv6(ipv6_comprimida)

        print("IPv6 original:", ipv6_original)
        print("IPv6 comprimida:", ipv6_comprimida)
        print("IPv6 descomprimida:", ipv6_descomprimida)
        input("Presiona cualquier tecla para volver al menú principal.")

    elif opcion == '3':
        print("""
 ----------------------------------
| FLSM - Subneteo de longitud de prefijo fijo |
 ----------------------------------
""")
        ip = input("Introduce la dirección IP: ")
        mascara = input("Introduce la máscara de subred: ")

        resultado = calcular_flsm(ip, mascara)

        print("Máscara CIDR:", resultado[0])
        print("Dirección de Red:", resultado[1])
        print("Primer Host:", resultado[2])
        print("Último Host:", resultado[3])
        print("Dirección de Broadcast:", resultado[4])
        print("Número de IPs disponibles:", resultado[5])
        print("Máximo de hosts:", resultado[6])
        input("Presiona cualquier tecla para volver al menú principal.")

    elif opcion == '4':
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor, selecciona '1', '2', '3' o '4'.")

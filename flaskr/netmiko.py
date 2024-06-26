import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from netmiko import ConnectHandler

class netManager:
    def __init__(self):
        self.open_conn_list = []
        
    def exec_comand(self, ip, commands):
        netConn = self.find_opened_device(ip)
        commands = self.limpiar_comandos(commands)
        try:
            netConn['conn'].enable()
            netConn['response'] = netConn['conn'].find_prompt()
            for command in commands:
                print(f'\ncommand:{command}#\n')
                r = netConn['conn'].send_command_timing(command)
                netConn['response'] += "\n" + r
        
        except Exception as e:
            netConn['response'] = f"falló conexion con {netConn['info']['ip']}"

        print('exec :9', netConn)
        return netConn

    def open_conn(self, device):
        
        netConn = {
            'info':{
                'device_type': device['operating_system'],
                "ip": device['ip'],
                'host': device['hostname'],
                'username': device['username'],
                "password": device['password'],
                'secret': device['secret']
            },
            'conn': None
        }
        print('\nnetConn', netConn)
        try:
            conn =  ConnectHandler(**netConn['info'])
            
            netConn['conn'] = conn
            print(f"conectado a {netConn['info']['host']}")
        
        except Exception as e:
            print(f"falló conexion con {netConn['info']['ip']}")
        
        # Verificar si el dispositivo ya está en la lista
        existing_device_ips = [conn['info']['ip'] for conn in self.open_conn_list]
        if device['ip'] not in existing_device_ips:
            self.open_conn_list.append(netConn)

        print('\nopen', self.open_conn_list,'\n')
        return netConn

    def ping(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        return subprocess.call(command) == 0

    def find_opened_device(self, ip_busqueda):
        print(self.open_conn_list)
        for dispositivo in self.open_conn_list:
            if dispositivo['info']['ip'] == ip_busqueda:
                return dispositivo
        return None
    
    def limpiar_comandos(self, texto):
        lineas = texto.split(' \n')
        comandos = [linea.strip() for linea in lineas if linea.strip()]
        return comandos

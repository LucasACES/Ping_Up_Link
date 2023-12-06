import os
import json
from datetime import datetime


#       Função para pingar o ip
#---------------------------------------------------------------------------------------------------------------
def myping(host):
    #response = os.system("ping -c 1 -s 1 -q " + host)
    response = os.system("ping -n 1 -l 1 " + host)
    if response == 0:
        return True
    else:
        return False
    
#       Função para enviar e-mail
#---------------------------------------------------------------------------------------------------------------

def enviar_email(empresa_atual, ip_atual):
    data_atual = datetime.now()
    data_atual = data_atual.strftime("%d/%m/%Y %H:%M")
    destinatario = "Email de destino"
    origem = "Email de origem"
    assunto = f"'ALERTA! Link principal da empresa {empresa_atual} - [STATUS DOWN]'"
    corpo = f"Alerta! Link DOWN! IP: {ip_atual} \nData: {data_atual}"
    
    return os.system(f"echo {corpo} | mailx -r {origem} -s {assunto} {destinatario}")


#       Lendo JSON
#---------------------------------------------------------------------------------------------------------------
with open("ips.json", encoding='utf-8') as ip_json:
    dados = json.load(ip_json)



#       Condição para ver se o link local está ativo
#---------------------------------------------------------------------------------------------------------------
if myping("8.8.8.8") and myping("1.1.1.1") == True:
    conter = 0


#       Inicio dos testes do link
#---------------------------------------------------------------------------------------------------------------
    for i in dados["Clientes"]:
        
#       Obtendo o ip do arquivo json
#---------------------------------------------------------------------------------------------------------------
        ip_principal = (dados["Clientes"][conter]["ip1"])
        empresa_atual = (dados["Clientes"][conter]["nome"])
        ip_secundario = (dados["Clientes"][conter]["ip2"])


#       Chamando a função para pingar o ip cliente
#---------------------------------------------------------------------------------------------------------------
        ret_principal=myping(ip_principal)
        ret_secundario=myping(ip_secundario)


#       Iniciando validação do resultado do ping
#---------------------------------------------------------------------------------------------------------------
        if ret_principal == True:
            pass
        else:
            enviar_email(empresa_atual, ip_principal)
            
#---------------------------------------------------------------------------------------------------------------
        if ret_secundario == True:
            conter+=1
        else:
            if ip_secundario == '':
                conter+=1
                continue
            else:
                enviar_email(empresa_atual, ip_secundario)
                conter+=1
else:
    print("problema com o link local")
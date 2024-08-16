import re

def informacao_relevante(log_linha):
    patterns = {
        'user': r'user="([^"]*)"',
        'hostname': r'hostname="([^"]*)"',
        'url': r'url="([^"]*)"',
        'action': r'action="([^"]*)"'
    }

    result = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, log_linha)
        if match:
            result[key] = match.group(1)
        else:
            result[key] = 'N/A'
    
    return result

def main(input_file, output_file):
    hostname_count = {}  
    last_occurrence = {}  
    
    with open(input_file, 'r') as infile:
        for linha in infile:
            info = informacao_relevante(linha)
            hostname = info['hostname']
            
            if hostname in hostname_count:
                hostname_count[hostname] += 1
            else:
                hostname_count[hostname] = 1
                last_occurrence[hostname] = info
    
    # Ordenar os hostnames em ordem alfabética
    sorted_hostnames = sorted(hostname_count.keys())
    
    with open(output_file, 'w') as outfile:
        for hostname in sorted_hostnames:
            count = hostname_count[hostname]
            if count > 0:
                info = last_occurrence[hostname]
                formatted_linha = (f"user={info['user']} "
                                   f"hostname={hostname} action={info['action']} "
                                   f"url={info['url']} hostnamerepeat={count}\n")
                outfile.write(formatted_linha)

input_file = "forticloud-webfilter-2024-08-05_0938.log"  
output_file = "formatting_log.log"  

# Chama a função principal
if __name__ == '__main__':
    main(input_file, output_file)

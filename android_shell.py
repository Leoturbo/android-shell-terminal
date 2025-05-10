import subprocess
import sys
import os
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# Códigos ANSI para cores
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'CYAN': '\033[96m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'RESET': '\033[0m'
}

def print_banner():
    banner = f"""
{COLORS['CYAN']}╔════════════════════════════════════════╗
║{COLORS['YELLOW']}      ANDROID SHELL TERMINAL v2.1      {COLORS['CYAN']}║
║{COLORS['MAGENTA']}        Usuário: {os.getlogin():<12}         {COLORS['CYAN']}║
║{COLORS['GREEN']}        Root: {'✔' if is_root() else '✖'} {COLORS['CYAN']}               ║
╚════════════════════════════════════════╝
{COLORS['RESET']}"""
    print(banner)

def is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def execute_command(command):
    try:
        result = subprocess.run(
            ['sh', '-c', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        output = result.stdout + result.stderr
        return output.strip()
    except Exception as e:
        return f"Erro: {str(e)}"

def main():
    print_banner()
    
    history = FileHistory(os.path.expanduser("~/.android_shell_history"))
    
    while True:
        try:
            # Configuração do prompt
            prompt_text = (
                f"{COLORS['GREEN']}android-sh{COLORS['RED']}#{COLORS['RESET']} " 
                if is_root() else 
                f"{COLORS['GREEN']}android-sh${COLORS['RESET']} "
            )

            user_input = prompt(
                prompt_text,
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
                mouse_support=True
            ).strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print(f"{COLORS['YELLOW']}Saindo...{COLORS['RESET']}")
                break

            if user_input.lower() == 'clear':
                print("\033c", end="")
                print_banner()
                continue

            if user_input.lower() == 'help':
                print(f"""{COLORS['CYAN']}
Comandos disponíveis:
- help: Mostra esta ajuda
- clear: Limpa a tela
- exit/quit: Sai do terminal
- sysinfo: Informações do sistema
- storage: Espaço em disco
- apps: Lista apps instalados
- network: Configuração de rede
- logs: Logs do sistema (requer root)
{COLORS['RESET']}""")
                continue

            # Execução de comandos
            output = ""
            if user_input == 'sysinfo':
                output = execute_command('getprop ro.build.version.sdk && uname -a')
            elif user_input == 'storage':
                output = execute_command('df -h /storage/emulated')
            elif user_input == 'apps':
                output = execute_command('pm list packages -3')
            elif user_input == 'network':
                output = execute_command('ip addr show && netstat -tuln')
            elif user_input == 'logs':
                output = execute_command('logcat -d') if is_root() else f"{COLORS['RED']}⚠️ Requer root!{COLORS['RESET']}"
            else:
                output = execute_command(user_input)

            print(f"{COLORS['BLUE']}{output}{COLORS['RESET']}")

        except KeyboardInterrupt:
            print(f"\n{COLORS['YELLOW']}Use 'exit' para sair{COLORS['RESET']}")
            continue

if __name__ == "__main__":
    main()

import subprocess as sp
import os, sys
import pyttsx3
import ftfy
import gtts as gTTS
# import utils as util
from deep_translator import GoogleTranslator
from speak_command import utils as util

engine = pyttsx3.init()

#funções que executam os comandos, serão chamadas no main.py
def run_normal_command(qtdArgs, cmd):
    if qtdArgs==3:
        output = execute_command(cmd[0])
        translated_output = translate_output(cmd[1],cmd[2], output)
        read_output(translated_output)
                
    elif qtdArgs==1:
        output = execute_command(cmd[0])
        read_output(output)
    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

def run_help(qtdArgs, cmd):
    if qtdArgs==3:
        output = util.text_help()
        translated_help = translate_output(cmd[1],cmd[2], output)
        read_output(translated_help)
                
    elif qtdArgs==1:
        util.change_voice("Portuguese")
        output = util.text_help()
        read_output(output)

    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

def run_scripts(qtdArgs, cmd):
    if qtdArgs==2:
        output = python_script(cmd[1])
        read_output(output)
    elif qtdArgs==4:
        output = python_script(cmd[1])
        translated_script_python = translate_output(cmd[2], cmd[3], output)
        read_output(translated_script_python)

    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

def run_file(qtdArgs, cmd):
    if qtdArgs==2:
        text_file = read_file(cmd[1])
        read_output(text_file)

    elif qtdArgs==4:
        # text_file = read_file(cmd[1])
        translated_text_file = translate_file(cmd[2], cmd[3], cmd[1])
        read_output(translated_text_file)

    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

# Traduz um arquivo informado pelo usuário
def translate_file(lingua_ori, lingua_dst, file_name):
    try:
        util.change_voice(lingua_dst)
        
        lingua_ori = util.lang_suport(lingua_ori)
        lingua_dst = util.lang_suport(lingua_dst)
        
        translated = GoogleTranslator(source=lingua_ori, target=lingua_dst).translate_file(file_name)
        
        base_name, extension = os.path.splitext(file_name)
        new_file_name = f"{base_name}_{lingua_dst}{extension}"
        
        current_directory = os.getcwd()
        file_path = os.path.abspath(file_name)
        
        if not os.path.exists(file_path):
            error_msg = f"Erro: O arquivo '{file_name}' não foi encontrado no diretório '{current_directory}'"
            return error_msg
        
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        with open(new_file_path, "w", encoding='utf-8', errors='replace') as new_file:
            new_file.write(translated + "\n")
            new_file.flush()
        return translated
    except Exception as e:
        error_msg = (f"Erro ao traduzir o arquivo: {e}")
        return errror_msg

# Traduz o que está arquivo terminal_log.txt
def translate_output(lingua_ori, lingua_dst, text):
    try:
        util.change_voice(lingua_dst)
        
        lingua_ori = util.lang_suport(lingua_ori)
        lingua_dst = util.lang_suport(lingua_dst)
                
        translated = GoogleTranslator(source=lingua_ori, target=lingua_dst).translate(text)
        
        return translated
        
    except Exception as e:
        error_msg = f"Erro na tradução: {e}"
        return error_msg

# salva o comando no arquivo terminal_log.txt
def execute_command(command):
    try:
        result = sp.run(command, shell=True, stdout=sp.PIPE,stderr=sp.PIPE)
        encoding = 'cp850' if os.name == 'nt' else 'utf-8'
        output = result.stderr.decode('utf-8', errors='replace') if result.stderr else result.stdout.decode(encoding, errors='replace')
        output = ftfy.fix_text(output)
        return output
    
    except Exception as e:
        error_msg = (f"Erro ao executar o comando: {e}")
        return error_msg
        
# lê o arquivo terminal_log.txt em voz alta
def read_output(output):
    print(output, flush=True)
    util.speak(output)

# Executa um script Python informado pelo usuário
def python_script(script_name):
    current_directory = os.getcwd()
    script_path = os.path.abspath(script_name)
    if not os.path.exists(script_path):
        error_msg = f"Erro: O arquivo '{script_name}' não foi encontrado no diretório '{current_directory}'"
        return error_msg
    
    if os.path.getsize(script_path) == 0:
        error_msg = f"Erro: O arquivo '{script_name}' está vazio."
        return error_msg
    
    try:
        python_cmd = "python" if os.name == "nt" else "python3"
        
        result = sp.run(
            [python_cmd, script_path],
            capture_output=True,  
            text=True
        )

        stdout_text = ftfy.fix_text(result.stdout) if result.stdout else ""
        stderr_text = ftfy.fix_text(f"\nErros:\n{result.stderr}") if result.stderr else ""

        output = f"\n> {script_name}\n{stdout_text}{stderr_text}"

        return output
    
    except Exception as e:
        error_msg = f"Erro ao executar o script: {e}"
        return error_msg

# Lê um arquivo informado pelo usuário
def read_file(file_name):
    current_directory = os.getcwd()
    file_path = os.path.abspath(file_name)
    if not os.path.exists(file_path):
        error_msg = f"Erro: O arquivo '{file_name}' não foi encontrado no diretório '{current_directory}'"
        return error_msg
    if os.path.getsize(file_path) == 0:
        error_msg = f"Erro: O arquivo '{file_name}' está vazio."
        return error_msg
    try:   
        with open(file_path, "r", encoding='utf-8') as file:
            output = file.read()
        return output
        
    except Exception as e:
        error_msg = f"Erro ao ler o arquivo: {e}"
        return error_msg
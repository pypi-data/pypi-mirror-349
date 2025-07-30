import os
import pyttsx3
from pynput import keyboard
import threading
import ftfy

key_listener = None
engine = pyttsx3.init()

# Descobre o idioma do texto
def lang_suport(lingua):
    idiomas_suportados = {
        "afrikaans": "af", "albanian": "sq", "amharic": "am", "arabic": "ar",
        "armenian": "hy", "assamese": "as", "aymara": "ay", "azerbaijani": "az",
        "bambara": "bm", "basque": "eu", "belarusian": "be", "bengali": "bn",
        "bhojpuri": "bho", "bosnian": "bs", "bulgarian": "bg", "catalan": "ca",
        "cebuano": "ceb", "chichewa": "ny", "chinese (simplified)": "zh-CN",
        "chinese (traditional)": "zh-TW", "corsican": "co", "croatian": "hr",
        "czech": "cs", "danish": "da", "dutch": "nl", "english": "en", 
        "esperanto": "eo", "estonian": "et", "finnish": "fi", "french": "fr",
        "german": "de", "greek": "el", "haitian creole": "ht", "hindi": "hi",
        "hungarian": "hu", "icelandic": "is", "indonesian": "id", "italian": "it",
        "japanese": "ja", "korean": "ko", "latvian": "lv", "lithuanian": "lt",
        "malay": "ms", "norwegian": "no", "persian": "fa", "polish": "pl",
        "portuguese": "pt", "romanian": "ro", "russian": "ru", "serbian": "sr",
        "slovak": "sk", "slovenian": "sl", "spanish": "es", "swahili": "sw",
        "swedish": "sv", "thai": "th", "turkish": "tr", "ukrainian": "uk",
        "urdu": "ur", "vietnamese": "vi", "welsh": "cy", "yiddish": "yi", "zulu": "zu"
    }
    lingua = lingua.lower()
    
    if lingua in idiomas_suportados.values():
        return lingua  

    if lingua in idiomas_suportados:
        return idiomas_suportados[lingua]

    raise ValueError(
        f"Idioma '{lingua}' não suportado. Use um dos seguintes: {list(idiomas_suportados.keys()) + list(idiomas_suportados.values())}"
    )

# muda a voz do sistema
def change_voice(language):
    language_mapping = {
        "english": "english", "en": "english", "en-us": "english", "en-uk": "english",
        "portuguese": "portuguese", "pt-br": "portuguese", "pt": "portuguese",
        "german": "german", "de": "german", "de-de": "german",
    }
    language = language.lower()
    if language in language_mapping:
        language = language_mapping[language]
    else:
        language = lang_suport(language)
        
    voices = engine.getProperty('voices')
    for voice in voices:
        for word in voice.name.split():
            if language in word.lower():
                engine.setProperty('voice', voice.id)
                return

# lê o o que for pedido
def speak(text):
    detect_keypress()
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro ao falar: {e}")

# para a leitura
def stop_speaking():
    global key_listener
    engine.stop()
    if key_listener:
        key_listener.stop()

#vê se alguma tecla foi pressionada
def detect_keypress():
    global key_listener
    key_listener = keyboard.Listener(on_press=on_press)
    key_listener.start()
    
#vê se o esc foi pressionado
def on_press(key):
    try:
        if key == keyboard.Key.esc:
            print("Parando a fala...")
            stop_speaking()
            return False  # Interrompe o listener
    except:
        pass

# mostra a ajuda
def text_help() -> str:
    string = """Como Utilizar a biblioteca:
  scmd <comando> [opções]

Opções gerais:
  --help, --h                                                               Mostra os comandos da biblioteca.
  --help [Lingua de Destino]                                                Traduz e mostra os comandos da biblioteca.
  
Para os seguintes comandos, você precisa estar no diretorio do arquivo.
  --pyFile <Nome do arquivo.py>                                             Lê a saída do arquivo ou o erro que deu.
  --pyFile <Nome do arquivo.py> [Lingua de Origem] [Lingua de Destino]      Traduz, e lê a saída do arquivo ou o erro que deu.
  --file <Nome do arquivo.txt>                                              Lê o conteúdo do arquivo.
  --file <Nome do arquivo.txt> [Lingua de Origem] [Lingua de Destino]       Traduz, e lê o conteúdo do arquivo, e cria um novo arquivo com o conteúdo traduzido.
    """
    return string
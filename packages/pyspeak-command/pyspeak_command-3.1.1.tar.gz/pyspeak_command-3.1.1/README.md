# speak_command 🗣️📜

**speak_command** é um projeto que permite traduzir e ler a execução de comandos no terminal, a saída de arquivos Python e arquivos de texto. Ele é útil para quem deseja ouvir a saída de comandos ou scripts diretamente no terminal, além de oferecer a funcionalidade de tradução para diferentes idiomas.

---

## 📦 Instalação

Você pode instalar este pacote utilizando o `pip`:

```bash
pip install pyspeak_command
```

---

## 🚀 Como Usar

O **Speak Command** pode ser utilizado para executar comandos no terminal, ler arquivos de texto, executar scripts Python e traduzir o conteúdo para diferentes idiomas.

### 📜 Executar um comando no terminal e ouvir a saída:
```bash
scmd ls -l
```

### 📄 Ler um arquivo de texto:
```bash
scmd --file arquivo.txt
```

### 🐍 Executar um script Python e ouvir a saída:
```bash
scmd --pyFile script.py
```

### 🌍 Traduzir a saída de um comando ou arquivo:
```bash
scmd --file arquivo.txt pt en  # Traduz o conteúdo do arquivo de português para inglês
scmd --pyFile script.py pt es  # Traduz a saída do script de português para espanhol
```

### ℹ️ Ajuda
Para ver a lista completa de comandos e opções disponíveis:

```bash
scmd --help
```

---

## 🔧 Funcionalidades

✅ Leitura de comandos do terminal: Ouve a saída de comandos executados no terminal.  
✅ Leitura de arquivos de texto: Lê o conteúdo de arquivos de texto em voz alta.  
✅ Execução de scripts Python: Executa scripts Python e lê a saída ou erros.  
✅ Tradução de conteúdo: Traduz o conteúdo de comandos, arquivos ou scripts para diferentes idiomas.  

---

## 📋 Requisitos

- **Python 3.7** ou superior.
- **Dependências:**  
  - `pyttsx3`
  - `pynput`
  - `deep_translator`
  - `ftfy`

Para instalar as dependências manualmente:

```bash
pip install -r requirements.txt
```

---

## 📞 Contato

Caso tenha dúvidas ou sugestões, entre em contato:

- **Autor:** Cícero Higor  
- **E-mail:** higormc2015@gmail.com  
- **Repositório:** [GitHub](#https://github.com/higormcarnauba)

---
**Desenvolvido com ❤️**

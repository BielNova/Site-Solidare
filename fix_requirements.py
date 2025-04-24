# Script para converter requirements.txt de UTF-16LE para UTF-8

# Converte requirements.txt de UTF-16LE para UTF-8
with open("requirements.txt", "rb") as f:
    content = f.read()

# Verifica se o arquivo começa com BOM UTF-16LE (FF FE)
if content.startswith(b"\xff\xfe"):
    # Decodifica de UTF-16LE e codifica para UTF-8
    text = content.decode("utf-16-le")
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Arquivo requirements.txt convertido de UTF-16LE para UTF-8")
else:
    print("Arquivo requirements.txt já está em formato compatível")

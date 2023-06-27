# Define a imagem base
FROM python:3.10

# Define o diretório de trabalho dentro do contêiner
WORKDIR /

# Copia os arquivos de requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia o restante dos arquivos do projeto para o contêiner
COPY . .

# Expõe a porta em que o servidor do Django estará executando (ajuste de acordo com sua configuração)
EXPOSE 8000

# Define o comando a ser executado quando o contêiner for iniciado
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

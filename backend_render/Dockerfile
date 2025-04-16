{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Usa un'immagine base ufficiale PyTorch con CUDA 12.1 (o la versione che installerai su Windows)\
# Questo include Python, PyTorch, Torchvision e le librerie CUDA necessarie.\
FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime\
\
# Imposta la directory di lavoro nel container\
WORKDIR /app\
\
# Installa dipendenze di sistema necessarie (es. per OpenCV)\
# Il RUN successivo aggiorna e pulisce apt per mantenere l'immagine piccola\
RUN apt-get update && apt-get install -y --no-install-recommends \\\
    libgl1-mesa-glx \\\
    libglib2.0-0 \\\
    git \\\
    && apt-get clean \\\
    && rm -rf /var/lib/apt/lists/*\
\
# Copia SOLO il file requirements.txt principale (dalla root del progetto)\
# Nota il percorso relativo "../" per uscire da backend_render e prenderlo dalla root\
COPY ../requirements.txt .\
\
# Installa le dipendenze Python specificate, senza cache\
# Si aspetta che torch/torchvision siano gi\'e0 nell'immagine base\
RUN pip install --no-cache-dir -r requirements.txt\
\
# Copia il codice specifico del backend e lo script di avvio principale\
# Copia prima serve_main.py che \'e8 nella root\
COPY ../serve_main.py .\
# Copia tutto il contenuto della cartella backend_render (dove si trova questo Dockerfile)\
COPY . .\
\
# Esponi la porta su cui Gunicorn ascolter\'e0 (deve corrispondere al comando e a docker-compose)\
EXPOSE 5001\
\
# Imposta variabile d'ambiente per logging Python pi\'f9 immediato\
ENV PYTHONUNBUFFERED=1\
\
# Comando per avviare Gunicorn quando il container parte\
# Ascolta su tutte le interfacce sulla porta 5001\
# Dice a Gunicorn di usare l'oggetto 'app' dal file 'serve_main.py'\
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "serve_main:app"]}
#!/bin/bash

# Script di deployment per Movie Montage Creator

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniziando il deployment di Movie Montage Creator...${NC}"

# Crea directory per i log
mkdir -p logs

# Verifica prerequisiti
echo -e "${YELLOW}Verificando i prerequisiti...${NC}"

# Verifica Python
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python installato: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 non trovato. Installare Python 3.8 o superiore.${NC}"
    exit 1
fi

# Verifica Node.js
if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js installato: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js non trovato. Installare Node.js 16.x o superiore.${NC}"
    exit 1
fi

# Verifica npm o pnpm
if command -v npm &>/dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm installato: $NPM_VERSION${NC}"
    PACKAGE_MANAGER="npm"
elif command -v pnpm &>/dev/null; then
    PNPM_VERSION=$(pnpm --version)
    echo -e "${GREEN}✓ pnpm installato: $PNPM_VERSION${NC}"
    PACKAGE_MANAGER="pnpm"
else
    echo -e "${RED}✗ npm o pnpm non trovati. Installare npm 7.x o pnpm 6.x o superiore.${NC}"
    exit 1
fi

# Verifica ffmpeg
if command -v ffmpeg &>/dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
    echo -e "${GREEN}✓ ffmpeg installato: $FFMPEG_VERSION${NC}"
else
    echo -e "${RED}✗ ffmpeg non trovato. Installare ffmpeg per l'elaborazione video.${NC}"
    exit 1
fi

echo -e "${GREEN}Tutti i prerequisiti sono soddisfatti.${NC}"

# Setup del backend
echo -e "${YELLOW}Configurando il backend...${NC}"
cd backend || exit 1

# Crea e attiva l'ambiente virtuale
echo "Creazione dell'ambiente virtuale Python..."
python3 -m venv venv
source venv/bin/activate

# Installa le dipendenze
echo "Installazione delle dipendenze Python..."
pip install -r requirements.txt > ../logs/pip_install.log 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dipendenze Python installate con successo.${NC}"
else
    echo -e "${RED}✗ Errore durante l'installazione delle dipendenze Python. Controlla logs/pip_install.log${NC}"
    exit 1
fi

# Crea le directory necessarie
mkdir -p uploads temp output

# Torna alla directory principale
cd ..

# Setup del frontend
echo -e "${YELLOW}Configurando il frontend...${NC}"
cd frontend || exit 1

# Installa le dipendenze
echo "Installazione delle dipendenze Node.js..."
if [ "$PACKAGE_MANAGER" = "npm" ]; then
    npm install > ../logs/npm_install.log 2>&1
else
    pnpm install > ../logs/pnpm_install.log 2>&1
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dipendenze Node.js installate con successo.${NC}"
else
    echo -e "${RED}✗ Errore durante l'installazione delle dipendenze Node.js. Controlla logs/npm_install.log o logs/pnpm_install.log${NC}"
    exit 1
fi

# Build del frontend
echo "Creazione della build di produzione..."
if [ "$PACKAGE_MANAGER" = "npm" ]; then
    npm run build > ../logs/npm_build.log 2>&1
else
    pnpm build > ../logs/pnpm_build.log 2>&1
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build del frontend completata con successo.${NC}"
else
    echo -e "${RED}✗ Errore durante la build del frontend. Controlla logs/npm_build.log o logs/pnpm_build.log${NC}"
    exit 1
fi

# Torna alla directory principale
cd ..

# Crea file di configurazione per il deployment
echo -e "${YELLOW}Creando file di configurazione per il deployment...${NC}"

# Crea file di configurazione per Nginx
cat > nginx.conf << EOF
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

echo -e "${GREEN}✓ File di configurazione Nginx creato: nginx.conf${NC}"

# Crea script di avvio
cat > start.sh << EOF
#!/bin/bash

# Avvia il backend
cd backend
source venv/bin/activate
python main.py &
echo "Backend avviato su http://localhost:5000"

# Avvia il frontend
cd ../frontend
if command -v npm &>/dev/null; then
    npm start &
else
    pnpm start &
fi
echo "Frontend avviato su http://localhost:3000"

echo "Movie Montage Creator è in esecuzione!"
echo "Accedi all'applicazione su http://localhost:3000"
EOF

chmod +x start.sh
echo -e "${GREEN}✓ Script di avvio creato: start.sh${NC}"

echo -e "${GREEN}Deployment completato con successo!${NC}"
echo -e "${YELLOW}Per avviare l'applicazione, esegui: ./start.sh${NC}"

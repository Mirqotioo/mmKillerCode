{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Fase 1: Build dell'applicazione Next.js\
FROM node:18-alpine AS builder\
\
# Imposta la directory di lavoro\
WORKDIR /app\
\
# Copia package.json e yarn.lock (o package-lock.json)\
COPY package.json yarn.lock* package-lock.json* ./\
\
# Installa le dipendenze di produzione\
RUN yarn install --frozen-lockfile --production\
\
# Copia il resto del codice frontend\
COPY . .\
\
# Costruisci l'applicazione Next.js per produzione\
RUN yarn build\
\
# Fase 2: Servire l'applicazione buildata\
FROM node:18-alpine AS runner\
\
WORKDIR /app\
\
# Copia solo i file necessari dalla fase di build\
COPY --from=builder /app/public ./public\
COPY --from=builder /app/.next ./.next\
COPY --from=builder /app/node_modules ./node_modules\
COPY --from=builder /app/package.json ./package.json\
\
# Esponi la porta su cui Next.js gira (default 3000)\
EXPOSE 3000\
\
# Comando per avviare il server Next.js in produzione\
CMD ["yarn", "start"]\
\
# Se usi npm invece di yarn:\
# FROM node:18-alpine AS builder\
# WORKDIR /app\
# COPY package.json package-lock.json* ./\
# RUN npm ci --only=production\
# COPY . .\
# RUN npm run build\
#\
# FROM node:18-alpine AS runner\
# WORKDIR /app\
# COPY --from=builder /app/public ./public\
# COPY --from=builder /app/.next ./.next\
# COPY --from=builder /app/node_modules ./node_modules\
# COPY --from=builder /app/package.json ./package.json\
# EXPOSE 3000\
# CMD ["npm", "start"]}
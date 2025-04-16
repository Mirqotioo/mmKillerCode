# backend_render/main.py (Versione di Test Minimale)
import os
from flask import Flask, jsonify
import logging

# Configura il logger (importante per vedere i messaggi su Render)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
logger.info("====> Creazione istanza Flask minimale <====")

@app.route('/')
def home():
    logger.info("====> Minimal App: Richiesta ricevuta su / <====")
    return jsonify({"message": "Minimal Flask App Root OK"}), 200

@app.route('/api/health')
def health():
    logger.info("====> Minimal App: Richiesta ricevuta su /api/health <====")
    return jsonify({"message": "Minimal Flask App Health OK"}), 200

logger.info("====> Route / e /api/health definite per app minimale <====")

# Non serve altro per questo test
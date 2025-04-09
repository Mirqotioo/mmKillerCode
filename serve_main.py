# serve_main.py (nella root del progetto)

import os
import sys

# Ottieni il percorso assoluto della directory in cui si trova serve_main.py (la root)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Costruisci il percorso della cartella backend_render
backend_dir = os.path.join(current_dir, 'backend_render')

# Aggiungi la cartella backend_render al path di Python
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ora puoi importare 'app' dal modulo 'main' che si trova in backend_render
try:
    from main import app
    print("INFO: Successfully imported 'app' from backend_render.main")
except ImportError as e:
    print(f"ERROR: Failed to import 'app' from backend_render.main. Error: {e}")
    print(f"INFO: Current sys.path: {sys.path}")
    sys.exit(1) # Esci se l'import fallisce, il server non può partire

# Il resto del file rimane uguale
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"INFO: Starting Flask app on host 0.0.0.0 and port {port}")
    # Esegui l'app importata. Aggiungi debug=False esplicitamente per Render.
    app.run(host="0.0.0.0", port=port, debug=False)
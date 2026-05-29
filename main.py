import os
from app import app

if __name__ == "__main__":
    os.makedirs("datos", exist_ok=True)
    app.run(host="0.0.0.0", port=6969, debug=True)
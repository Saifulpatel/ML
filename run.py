import os
from app import create_app

app, port = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render will assign a PORT dynamically
    app.run(host="0.0.0.0", port=port, debug=True)

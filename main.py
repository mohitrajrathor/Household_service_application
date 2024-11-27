from app import create_app
import os

# const
PORT = os.getenv('port')


app = create_app()

app.run(debug=True, port=PORT)
#! /usr/bin/env python3
from flask_blog import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
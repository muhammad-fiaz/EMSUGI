from modules.utils.create_database import init_db
from modules import *
import os
if __name__ == '__main__':
    init_db()
    app = create_app()
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)

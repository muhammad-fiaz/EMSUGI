from modules.utils.create_database import init_db
from modules import *
if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run(debug=True)

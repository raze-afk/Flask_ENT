from app import create_app
from create_admin import create_admin_user

app = create_app()

# Appelez le script de démarrage pour créer un utilisateur administrateur
create_admin_user()

if __name__ == '__main__':
    app.run(debug=True)


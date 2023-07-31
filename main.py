from Website import create_app, create_default_user
from Website.views import has_booked
app = create_app()

if  __name__ == '__main__':
    with app.app_context():
        has_booked()
        create_default_user()
    print("super user created")
    app.run(debug = True)


from Website import create_app, create_default_user

app = create_app()

if  __name__ == '__main__':
    with app.app_context():
        create_default_user()
    print("super user created")
    app.run(debug = True)


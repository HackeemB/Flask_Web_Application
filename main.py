from website import create_app

app = create_app()
app.secret_key = "test"

if __name__ == '__main__': #only if we run this file, we are going to execute below
    app.run(debug=True) #runs flask app, starts up our web server



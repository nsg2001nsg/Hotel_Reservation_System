from flaskblog import create_app

app = create_app()

# option 1,
# set FLASK_APP="D:\PythonProjects\CoreySchafer\Flask_Blog\run.py" OR
# set FLASK_APP=".\run.py" OR
# set FLASK_APP="run.py"  # to set env var for flask app
# $env:FLASK_APP="D:\PythonProjects\CoreySchafer\Flask_Blog\run.py" OR
# $env:FLASK_APP=".\run.py" OR
# $env:FLASK_APP="run.py"  # to set env var for flask app
# set FLASK_DEBUG=0  # non debug mode, default
# $env:FLASK_DEBUG=0  # non debug mode, default
# set FLASK_DEBUG=1  # debug mode
# $env:FLASK_DEBUG=1  # debug mode
# AND RUN flask run

# option 2,
if __name__ == "__main__":
    # app.run()  # non debug mode, default
    app.run(debug=True)  # debug mode
# AND RUN python .\run.py OR python run.py

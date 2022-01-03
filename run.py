from web_py_simple_storage import create_app
# from web_py_simple_storage.deploy import build, compile

app = create_app()

if(__name__ == '__main__'):
    app.run(debug=True, port=7070)
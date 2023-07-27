from storerestapi import app


# Will be deleted later I think
@app.route('/')
def hello_world():
    return 'Hello, World!'
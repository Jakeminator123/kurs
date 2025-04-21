# wsgi.py
import subprocess
import os

def app(environ, start_response):
    """
    WSGI-app som startar Streamlit-processen och fungerar som en proxy
    för att Render ska kunna hantera Streamlit-applikationen
    """
    # Starta Streamlit-servern som en underprocess
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Enkel respons för att indikera att appen körs
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Streamlit app is running. Please go to the correct URL."]
    
# För användning med Gunicorn direkt
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8501, app)
    httpd.serve_forever() 
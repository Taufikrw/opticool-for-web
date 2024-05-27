from app import app

app.run(host="0.0.0.0", port=50100, debug=True, ssl_context=('cert.pem', 'key.pem'))
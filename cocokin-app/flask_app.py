from api_model import app

if __name__ == '__main__':
    # Jalankan server di host dan port yang diminta oleh Render
    app.run(host='0.0.0.0', port=10000)

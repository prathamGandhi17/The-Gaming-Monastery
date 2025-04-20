from Website import create_app

app = create_app()

if __name__ == '__main__':
    # matches your debug port 5001
    app.run(debug=True, port=5001)

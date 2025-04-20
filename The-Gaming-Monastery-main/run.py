from Website import create_app

app = create_app()

if __name__ == "__main__":
    # Change host/port here if needed:
    app.run(host="0.0.0.0", port=5000, debug=True)

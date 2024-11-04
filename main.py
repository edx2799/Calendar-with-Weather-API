from website import create_app  # Import the create_app function to initialize the app

# Call the function to create an instance of the Flask app
app = create_app()

# Run the app only if this script is run directly (not imported as a module)
if __name__ == '__main__':
    app.run(debug=True)  # Start the server in debug mode for easier troubleshooting

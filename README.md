# Home Asset Inventory

Welcome to the Home Asset Inventory system. This application helps you manage and track home assets. You can add, update, and view items, including details like name, category, value, quantity, and barcode.

## Features

- **Add, Update, and View Items:** Manage your home assets with options to add new items, update existing ones, and view the inventory.
- **Dark Mode Toggle:** Switch between light and dark modes for better visibility and personal preference.
- **CSV Upload:** Import items from a CSV file to quickly populate the inventory.

## Getting Started

To set up and run the project, follow these steps:

### 1. Fork the Repository

1. Go to the [Home Asset Inventory GitHub page](https://github.com/JDXE88/Home-Asset-Inventory).
2. Click the **Fork** button at the top right of the page.

### 2. Clone Your Fork

1. Copy the URL of your forked repository (e.g., `https://github.com/YOUR_USERNAME/Home-Asset-Inventory.git`).
2. Open your terminal or command prompt.
3. Clone the repository using the following command:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Home-Asset-Inventory.git
   ```
4. Navigate into the project directory:
   ```bash
   cd Home-Asset-Inventory
   ```

### 3. Remove the `venv` Directory

If the `venv` folder was included in the clone (it shouldn't be), remove it:
```bash
rm -rf venv
```

### 4. Create a Virtual Environment

1. Create a virtual environment with the following command:
   ```bash
   python -m venv env
   ```

### 5. Activate the Virtual Environment

- For Linux/macOS:
  ```bash
  source env/bin/activate
  ```

- For Windows:
  ```bash
  .\env\Scripts\activate
  ```

### 6. Install Dependencies

Install the required packages using:
```bash
pip install Flask python-barcode pillow flask_sqlalchemy
```

### 7. (Optional) Save Dependencies

To save the dependencies to `requirements.txt`, run:
```bash
pip freeze > requirements.txt
```

### 8. Run the Application

Start the Flask application with:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000/` by default.

### 9. Adding Initial Data

You do not need to set up your own database manually. The application will handle database provisioning automatically. However, to initialize the database, you will need to add at least one item to the inventory through the application interface.

### 10. CSV Upload

To test CSV uploads, use the provided example file: `HAS/Home-Asset-Inventory/exampleupload.csv`. This file demonstrates the format needed for successful uploads.

## Screenshots

<!-- Here are some screenshots of the application:-->

![Screenshot 1](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/screenshots/screenshot.png)
![Screenshot 2](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/screenshots/screenshot2.png)

## Contributing

Feel free to contribute by making pull requests or reporting issues. For detailed instructions on how to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

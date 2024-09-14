# Home Asset Inventory

Welcome to the Home Asset Inventory system. This is a basic application designed to help you manage and track home assets.

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

### 3. Create a Virtual Environment

1. Create a virtual environment with the following command:
   ```bash
   python -m venv env
   ```

### 4. Activate the Virtual Environment

- For Linux/macOS:
  ```bash
  source env/bin/activate
  ```

- For Windows:
  ```bash
  .\env\Scripts\activate
  ```

### 5. Install Dependencies

Install the required packages using:
```bash
pip install Flask python-barcode pillow
```

### 6. (Optional) Save Dependencies

To save the dependencies to `requirements.txt`, run:
```bash
pip freeze > requirements.txt
```

### 7. Set Up the Database

Before running the application, ensure that your database is set up. You may need to create tables and configure initial data. Refer to the project documentation or scripts for specific instructions on setting up the database.

### 8. Run the Application

Start the Flask application with:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000/` by default.

## Screenshots

Here are some screenshots of the application:

![Screenshot 1](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Screenshot01.jpg)
![Screenshot 2](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Screenshot02.jpg)
![Screenshot 3](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Screenshot03.jpg)

## Demo

Check out these GIFs for a demonstration of the application's features:

![Demo 1](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Demo1.gif)
![Demo 2](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Demo2.gif)
![Demo 3](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Demo3.gif)
![Demo 4](https://github.com/JDXE88/Home-Asset-Inventory/blob/main/Screenshots/Demo4.gif)

## Contributing

Feel free to contribute by making pull requests or reporting issues. For detailed instructions on how to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

from flask import Flask, render_template, request, redirect, url_for, Response
import json
import csv
from io import StringIO

app = Flask(__name__)

# Define categories and subcategories
CATEGORIES = {
    "Real Estate": ["Primary Residence", "Vacation Home", "Rental Properties", "Land"],
    "Furniture": ["Living Room Furniture", "Bedroom Furniture", "Dining Room Furniture", "Office Furniture", "Outdoor Furniture"],
    "Appliances": ["Kitchen Appliances", "Laundry Appliances", "Heating & Cooling", "Small Appliances"],
    "Electronics": ["Home Entertainment Systems", "Computers & Accessories", "Smart Devices", "Home Security Systems"],
    "Jewelry & Collectibles": ["Fine Jewelry", "Watches", "Collectible Items", "Art & Antiques"],
    "Vehicles": ["Cars", "Motorcycles", "Boats", "Recreational Vehicles"],
    "Tools & Equipment": ["Gardening Tools", "Workshop Tools", "Maintenance Equipment"],
    "Clothing & Accessories": ["Seasonal Clothing", "Formal Wear", "Accessories"],
    "Outdoor & Garden": ["Landscaping Equipment", "Outdoor Decor", "Patio Furniture", "Grills & Fire Pits"],
    "Health & Fitness": ["Exercise Equipment", "Wellness Devices"],
    "Office Supplies & Equipment": ["Office Furniture", "Office Supplies", "Business Equipment"],
    "Books & Media": ["Books", "DVDs & CDs", "Digital Media"],
    "Kitchenware & Dining": ["Cookware", "Tableware", "Small Kitchen Appliances"],
    "Holiday & Seasonal Decorations": ["Holiday Decorations", "Seasonal Items"],
    "Household Supplies": ["Cleaning Supplies", "Storage Solutions", "Safety & Emergency Supplies"]
}

class InventoryItem:
    def __init__(self, name, category, value, quantity):
        self.name = name
        self.category = category
        self.value = value
        self.quantity = quantity

    def __repr__(self):
        return f"{self.name} (Category: {self.category}, Value: ${self.value}, Quantity: {self.quantity})"

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, name, category, value, quantity):
        item = InventoryItem(name, category, value, quantity)
        self.items.append(item)

    def view_inventory(self):
        return self.items

    def search_item(self, name):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

    def delete_item(self, name):
        item = self.search_item(name)
        if item:
            self.items.remove(item)
            return True
        return False

    def update_item(self, name, category=None, value=None, quantity=None):
        item = self.search_item(name)
        if item:
            if category:
                item.category = category
            if value:
                item.value = value
            if quantity:
                item.quantity = quantity
            return True
        return False

    def save_inventory(self, filename):
        with open(filename, 'w') as f:
            json.dump([item.__dict__ for item in self.items], f)

    def load_inventory(self, filename):
        try:
            with open(filename, 'r') as f:
                self.items = [InventoryItem(**data) for data in json.load(f)]
        except FileNotFoundError:
            self.items = []

inventory = Inventory()
inventory.load_inventory('inventory.json')

@app.route('/')
def index():
    items = inventory.view_inventory()
    return render_template('index.html', items=items, categories=CATEGORIES, currency_symbol='£')

@app.route('/add', methods=['POST'])
def add_item():
    try:
        name = request.form['name']
        category = request.form['category']
        value = float(request.form['value'])
        quantity = int(request.form['quantity'])
        inventory.add_item(name, category, value, quantity)
        inventory.save_inventory('inventory.json')
    except (ValueError, KeyError) as e:
        print(f"Error adding item: {e}")
    return redirect(url_for('index'))

@app.route('/delete/<name>')
def delete_item(name):
    inventory.delete_item(name)
    inventory.save_inventory('inventory.json')
    return redirect(url_for('index'))

@app.route('/update/<name>', methods=['GET', 'POST'])
def update_item(name):
    if request.method == 'POST':
        try:
            category = request.form['category']
            value = float(request.form['value'])
            quantity = int(request.form['quantity'])
            inventory.update_item(name, category, value, quantity)
            inventory.save_inventory('inventory.json')
        except (ValueError, KeyError) as e:
            print(f"Error updating item: {e}")
        return redirect(url_for('index'))
    item = inventory.search_item(name)
    return render_template('update.html', item=item, categories=CATEGORIES)

@app.route('/export')
def export_inventory():
    output = StringIO()
    csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header
    csv_writer.writerow(['Name', 'Category', 'Value', 'Quantity'])
    
    # Write the data rows
    for item in inventory.view_inventory():
        csv_writer.writerow([item.name, item.category, f"{item.value:.2f}", item.quantity])
    
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=inventory.csv"})

if __name__ == "__main__":
    app.run(debug=True)

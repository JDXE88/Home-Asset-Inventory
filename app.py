from flask import Flask, render_template, request, redirect, url_for, Response, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
from io import StringIO
import barcode
from barcode.writer import ImageWriter
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Helper function to generate barcodes
def generate_barcode(number, filename):
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(number, writer=ImageWriter())
    
    if filename.endswith('.png'):
        filename = filename[:-4]
    
    saved_filename = barcode_instance.save(filename)
    print(f"Barcode saved to: {saved_filename}")

# Create directories for categories
def create_category_directories():
    for category in CATEGORIES:
        category_path = os.path.join('static/categories', category)
        os.makedirs(category_path, exist_ok=True)
        print(f"Directory created for category: {category_path}")

create_category_directories()

# Define database model
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<InventoryItem {self.name}>"

# Create database tables
with app.app_context():
    db.create_all()

# Home route with search, sorting, category filtering, and currency symbol selection
@app.route('/')
def index():
    search_term = request.args.get('search_term', '')
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    category = request.args.get('category', '')
    
    # Default currency symbol is Euro (£)
    currency_symbol = request.args.get('currency', '£')

    query = InventoryItem.query.filter(
        (InventoryItem.name.ilike(f'%{search_term}%')) |
        (InventoryItem.barcode.ilike(f'%{search_term}%'))
    )
    
    if category:
        query = query.filter_by(category=category)

    # Sorting logic
    if sort_by == 'name':
        query = query.order_by(InventoryItem.name.asc() if order == 'asc' else InventoryItem.name.desc())
    elif sort_by == 'value':
        query = query.order_by(InventoryItem.value.asc() if order == 'asc' else InventoryItem.value.desc())
    elif sort_by == 'created_at':
        query = query.order_by(InventoryItem.created_at.asc() if order == 'asc' else InventoryItem.created_at.desc())
    elif sort_by == 'updated_at':
        query = query.order_by(InventoryItem.updated_at.asc() if order == 'asc' else InventoryItem.updated_at.desc())

    items = query.all()
    
    return render_template(
        'index.html',
        items=items,
        categories=CATEGORIES,
        search_term=search_term,
        sort_by=sort_by,
        order=order,
        selected_category=category,
        currency_symbol=currency_symbol  # Pass the selected currency to the template
    )


# Add new item route
@app.route('/add', methods=['POST'])
def add_item():
    try:
        name = request.form['name']
        category = request.form['category']
        value = float(request.form['value'])
        quantity = float(request.form['quantity'])
        barcode_value = request.form['barcode']
        
        item = InventoryItem(name=name, category=category, value=value, quantity=quantity, barcode=barcode_value)
        db.session.add(item)
        db.session.commit()
        
        # Generate barcode
        barcode_filename = f'static/barcodes/{barcode_value}.png'
        generate_barcode(barcode_value, barcode_filename)
        
        flash('Item added successfully!', 'success')
    except (ValueError, KeyError) as e:
        flash(f"Error adding item: {e}", 'error')
    return redirect(url_for('index'))

# Update item route
import os

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = InventoryItem.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # Retrieve form data
            new_name = request.form['name']
            new_category = request.form['category']
            new_value = float(request.form['value'])
            new_quantity = float(request.form['quantity'])
            new_barcode = request.form.get('barcode')
            
            # Check if barcode has changed
            if new_barcode != item.barcode:
                # Delete old barcode image
                old_barcode_filename = f'static/barcodes/{item.barcode}.png'
                if os.path.exists(old_barcode_filename):
                    os.remove(old_barcode_filename)
                
                # Generate new barcode image
                barcode_filename = f'static/barcodes/{new_barcode}.png'
                generate_barcode(new_barcode, barcode_filename)
            
            # Update item attributes
            item.name = new_name
            item.category = new_category
            item.value = new_value
            item.quantity = new_quantity
            item.barcode = new_barcode
            item.updated_at = datetime.now()

            db.session.commit()
            flash('Item updated successfully!', 'success')
        except (ValueError, KeyError) as e:
            flash(f"Error updating item: {e}", 'error')
        return redirect(url_for('index'))
    
    return render_template('update.html', item=item, categories=CATEGORIES)


# Delete item route
@app.route('/delete/<int:id>')
def delete_item(id):
    item = InventoryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

# Export inventory to CSV
@app.route('/export')
def export_inventory():
    output = StringIO()
    csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    csv_writer.writerow(['Name', 'Category', 'Value', 'Quantity', 'Barcode'])
    items = InventoryItem.query.all()
    for item in items:
        csv_writer.writerow([item.name, item.category, f"{item.value:.2f}", item.quantity, item.barcode])
    
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=inventory.csv"})

# Import inventory from CSV
@app.route('/import', methods=['POST'])
def import_inventory():
    if 'file' not in request.files:
        flash('No file part in the request', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    if file and file.filename.endswith('.csv'):
        file_content = file.read().decode('utf-8')
        csv_reader = csv.reader(StringIO(file_content))

        next(csv_reader)  # Skip header row

        for row in csv_reader:
            if len(row) == 5:
                name, category, value, quantity, barcode_value = row
                try:
                    value = float(value)
                    quantity = float(quantity)
                    item = InventoryItem(name=name, category=category, value=value, quantity=quantity, barcode=barcode_value)
                    db.session.add(item)
                    db.session.commit()
                except ValueError:
                    flash(f"Invalid data in CSV for item: {name}", 'error')
                    continue
        
        flash('Inventory imported successfully!', 'success')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

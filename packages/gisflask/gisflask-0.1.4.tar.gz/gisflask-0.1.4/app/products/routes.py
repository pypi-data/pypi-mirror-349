from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.products import products_bp
from app.extensions import db
from app.utils import admin_required

@products_bp.route('/')
def index():
    """
    Products List Page
    ---
    tags:
      - Products
    responses:
      200:
        description: Products list page rendered
    """
    # Example code (commented out):
    # from app.models import Product
    # products = Product.query.all()
    # return render_template('products/index.html', products=products)
    
    # Placeholder implementation:
    return render_template('products/index.html')

@products_bp.route('/<product_id>')
def view(product_id):
    """
    Product Details Page
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
        description: Product UUID
    responses:
      200:
        description: Product details page rendered
      404:
        description: Product not found
    """
    # Example code (commented out):
    # from app.models import Product
    # product = Product.query.get(product_id)
    # if not product:
    #     flash('Product not found', 'error')
    #     return redirect(url_for('products.index'))
    # return render_template('products/view.html', product=product)
    
    # Placeholder implementation:
    return render_template('products/view.html', product_id=product_id)

@products_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """
    Create Product Page
    ---
    tags:
      - Products
    responses:
      200:
        description: Create product form rendered
      201:
        description: Product created successfully
      400:
        description: Invalid form data
    """
    # Example code (commented out):
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     description = request.form.get('description')
    #     price = request.form.get('price')
    #     sku = request.form.get('sku')
    #     
    #     if not all([name, price, sku]):
    #         flash('Name, price and SKU are required', 'error')
    #         return render_template('products/create.html'), 400
    #     
    #     # Check if product SKU already exists
    #     from app.models import Product
    #     if Product.query.filter_by(sku=sku).first():
    #         flash('A product with this SKU already exists', 'error')
    #         return render_template('products/create.html'), 400
    #     
    #     # Create new product
    #     try:
    #         price_float = float(price)
    #         new_product = Product(
    #             name=name,
    #             description=description or '',
    #             price=price_float,
    #             sku=sku
    #         )
    #         
    #         db.session.add(new_product)
    #         db.session.commit()
    #         
    #         flash('Product created successfully', 'success')
    #         return redirect(url_for('products.index')), 201
    #     except ValueError:
    #         flash('Price must be a valid number', 'error')
    #         return render_template('products/create.html'), 400
    
    # Placeholder implementation:
    return render_template('products/create.html')

@products_bp.route('/edit/<product_id>', methods=['GET', 'POST'])
@admin_required
def edit(product_id):
    """
    Edit Product Page
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
        description: Product UUID
    responses:
      200:
        description: Edit product form rendered or product updated successfully
      404:
        description: Product not found
      400:
        description: Invalid form data
    """
    # Example code (commented out):
    # from app.models import Product
    # product = Product.query.get(product_id)
    # if not product:
    #     flash('Product not found', 'error')
    #     return redirect(url_for('products.index')), 404
    # 
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     description = request.form.get('description')
    #     price = request.form.get('price')
    #     sku = request.form.get('sku')
    #     
    #     if not all([name, price, sku]):
    #         flash('Name, price and SKU are required', 'error')
    #         return render_template('products/edit.html', product=product), 400
    #     
    #     # Check if SKU exists for another product
    #     existing_product = Product.query.filter_by(sku=sku).first()
    #     if existing_product and existing_product.id != product.id:
    #         flash('A product with this SKU already exists', 'error')
    #         return render_template('products/edit.html', product=product), 400
    #     
    #     # Update product data
    #     try:
    #         price_float = float(price)
    #         
    #         product.name = name
    #         product.description = description or ''
    #         product.price = price_float
    #         product.sku = sku
    #         
    #         db.session.commit()
    #         flash('Product updated successfully', 'success')
    #         return redirect(url_for('products.view', product_id=product.id))
    #     except ValueError:
    #         flash('Price must be a valid number', 'error')
    #         return render_template('products/edit.html', product=product), 400
    #     
    # return render_template('products/edit.html', product=product)
    
    # Placeholder implementation:
    return render_template('products/edit.html', product_id=product_id)

@products_bp.route('/delete/<product_id>', methods=['POST'])
@admin_required
def delete(product_id):
    """
    Delete Product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
        description: Product UUID
    responses:
      302:
        description: Product deleted and redirected to products list
      404:
        description: Product not found
    """
    # Example code (commented out):
    # from app.models import Product
    # product = Product.query.get(product_id)
    # if not product:
    #     flash('Product not found', 'error')
    #     return redirect(url_for('products.index')), 404
    # 
    # db.session.delete(product)
    # db.session.commit()
    # 
    # flash('Product deleted successfully', 'success')
    # return redirect(url_for('products.index'))
    
    # Placeholder implementation:
    return redirect(url_for('products.index'))
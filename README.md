# LuxShop - Simple Django eCommerce Application

A beginner-friendly eCommerce web application built with Django and Python, designed to use a remote MySQL database.

## Features

- **Authentication**: User Login, Logout, and Registration (Email & Password).
- **Products**: Browse by category, search by name, filter by price. Product details.
- **Cart**: Add/Remove items, update quantities. Persistent user-based cart.
- **Orders**: Simple "Place Order" checkout saving to database.
- **Database**: Configured for Remote MySQL (e.g., PlanetScale, Railway, RDS).

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- Use a Remote MySQL Database info ready (Host, User, Password, DB Name).

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Database

1. Open `.env` file in the root directory.
2. Update the variables with your **Local** MySQL credentials:

```ini
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_local_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

3. **Important**: Create the database in your local MySQL before running migrations:
   ```sql
   CREATE DATABASE ecommerce_db;
   ```

### 4. Initialize Database

Run migrations to create tables in your remote database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Sample Data

Populate the database with sample categories and products:

```bash
python manage.py populate_data
```

### 6. Run the Application

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to browse the store.

## Project Structure

- `ecommerce/`: Project settings and main URL routing.
- `products/`: Product management (Models: Category, Product).
- `cart/`: Shopping cart logic.
- `orders/`: Order processing.
- `users/`: User authentication.
- `templates/`: HTML templates.
- `static/`: CSS, JS, and Images.

## Design

- **Aesthetics**: Clean, modern, and minimal design using "Outfit" font and a soft color palette.
- **Responsive**: Adapts to mobile and desktop screens.
# aadi

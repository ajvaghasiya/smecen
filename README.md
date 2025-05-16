# Smecen - Accounting & HR Management System

Smecen is a comprehensive accounting and HR management system built with Django REST Framework. It provides a robust platform for managing financial transactions, HR operations, and business analytics.

## Features

- **User Management**
  - Role-based access control
  - Authentication using JWT
  - User profiles and permissions

- **HR Management**
  - Employee records management
  - Leave management
  - Attendance tracking
  - Document management

- **Financial Management**
  - Chart of accounts
  - Journal entries
  - Financial reports
  - Bank reconciliation

- **Sales Management**
  - Customer management
  - Sales orders
  - Invoicing
  - Payment tracking

- **Purchase Management**
  - Supplier management
  - Purchase orders
  - Bills management
  - Payment processing

- **Dashboard**
  - Customizable widgets
  - Real-time analytics
  - Activity tracking
  - Notifications

## Technology Stack

- Python 3.12+
- Django 5.2
- Django REST Framework 3.16
- PostgreSQL
- Celery
- Redis
- JWT Authentication

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smecen.git
cd smecen
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your environment variables:
```
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
DB_NAME=smecen_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

```
smecen/
├── apps/
│   ├── accounts/
│   ├── dashboard/
│   ├── finance/
│   ├── hr_management/
│   ├── purchase/
│   └── sales/
├── smecen_project/
├── static/
├── media/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

## API Documentation

The API documentation is available at `/api/docs/` when running the development server.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


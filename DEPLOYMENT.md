# PolitiQ Phase I - Deployment Guide

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install fastapi uvicorn sqlalchemy python-multipart jinja2 aiofiles pandas openpyxl pdfplumber requests
```

### 2. Create Sample Data

```bash
# Generate sample test data
python create_sample_data.py
```

### 3. Start the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

- **Web Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **OpenAPI Specification**: http://localhost:8000/openapi.json

## 📱 Application Features

### ✅ Completed Features

1. **Administrative Hierarchy Management**
   - Complete District → Mandal → Village structure
   - Excel import functionality
   - RESTful API endpoints

2. **Booth Management**
   - Manual booth creation with location mapping
   - Hierarchical dropdown selection
   - Booth detail pages

3. **PDF Processing**
   - Voter data extraction from PDFs
   - House-level grouping
   - Bulk voter data import

4. **Web Admin Interface**
   - Beautiful, modern UI with Bootstrap 5
   - Responsive design
   - Real-time statistics

5. **Database Management**
   - SQLite database with SQLAlchemy ORM
   - Complete relational structure
   - Data integrity and validation

### 📊 Database Schema

```
State (Telangana)
├── Districts
    ├── Mandals
        ├── Villages
            ├── Booths
                ├── Houses
                    ├── Voters
```

## 🔌 API Endpoints

### Hierarchy Management
- `GET /api/districts` - Get all districts
- `GET /api/districts/{id}/mandals` - Get mandals for district
- `GET /api/mandals/{id}/villages` - Get villages for mandal
- `GET /api/villages/{id}/booths` - Get booths for village

### Data Management
- `POST /api/booths` - Create new booth
- `POST /api/import-hierarchy` - Import hierarchy from Excel
- `POST /api/upload-voters` - Upload and process voter PDF
- `GET /api/voters/search` - Search voters with filters

### Statistics
- `GET /api/stats` - Get system statistics
- `GET /api/upload-logs` - Get upload processing logs

## 📁 Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── api.py               # API routes
│   ├── services.py          # Business logic
│   ├── templates/           # HTML templates
│   └── static/              # Static files
├── sample_data/             # Test data
├── requirements.txt         # Dependencies
├── create_sample_data.py    # Sample data generator
├── start.py                 # Startup script
└── README.md               # Documentation
```

## 🛠️ Usage Workflow

### Step 1: Import Hierarchy
1. Go to **Hierarchy Management** (`/hierarchy`)
2. Upload Excel file with columns: `District`, `Mandal`, `Village`
3. System imports the administrative structure

### Step 2: Add Booths
1. Go to **Booth Management** (`/booths`)
2. Select District → Mandal → Village
3. Enter Booth Number and Name
4. Create the booth

### Step 3: Upload Voter Data
1. Navigate to booth detail page
2. Upload voter list PDF from CEO Telangana portal
3. System extracts and groups voters by house number
4. View results in organized tables

### Step 4: Search and Analyze
1. Use **Voter Search** (`/voters`) to find specific voters
2. Filter by location, name, voter ID, or house number
3. View **Upload Logs** (`/upload-logs`) for processing history

## 🔧 Configuration

### Database
- Default: SQLite (`politiq.db`)
- For production: Configure PostgreSQL or MySQL in `app/database.py`

### PDF Processing
- Uses `pdfplumber` for text extraction
- Parser can be customized in `app/services.py`
- Supports various PDF formats from CEO Telangana portal

### File Upload Limits
- Modify in FastAPI configuration for larger files
- Current limit handles typical voter list PDFs

## 🚀 Production Deployment

### Environment Variables
```bash
# Production settings
export FASTAPI_ENV=production
export DATABASE_URL=postgresql://user:pass@localhost/politiq
export SECRET_KEY=your-secret-key
```

### Using Docker (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📋 Testing

### Manual Testing
```bash
# Test server startup
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test API endpoints
curl http://localhost:8000/api/stats
curl http://localhost:8000/api/districts
```

### Sample Data Testing
1. Use provided sample Excel file: `sample_data/telangana_hierarchy_sample.xlsx`
2. Import through web interface
3. Create test booths
4. Review functionality

## 🔐 Security Considerations

### Phase I (Current)
- Simple admin interface (no authentication)
- Local file upload only
- SQLite database

### Phase II (Future)
- User authentication and authorization
- Role-based access control
- Production database with encryption
- API rate limiting
- File upload security scanning

## 📞 Support

For technical support and questions:
- **Developer**: PolitiQ Development Team
- **Repository**: Internal PolitiQ repository
- **Documentation**: See README.md for detailed information

---

**Note**: This is Phase I of the PolitiQ platform. Phase II will include advanced analytics, AI features, and mobile applications.
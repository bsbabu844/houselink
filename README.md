# PolitiQ Phase I - House-Level Voter Mapping Tool

A comprehensive backend system for managing administrative hierarchy and voter data mapping in Telangana state. This is the foundational module for the larger PolitiQ political intelligence platform.

## 🎯 Project Overview

**Goal**: Build a backend-supported admin tool to preload Telangana's administrative hierarchy, manage booth information, and process voter PDFs with house-level mapping.

### Key Features

- ✅ **Administrative Hierarchy Management**: District → Mandal → Village structure
- ✅ **Excel Import**: Bulk import of hierarchy data
- ✅ **Booth Management**: Manual booth creation with location mapping
- ✅ **PDF Processing**: Extract voter data from CEO Telangana portal PDFs
- ✅ **House-Level Grouping**: Organize voters by house numbers
- ✅ **Web Admin Interface**: User-friendly dashboard for all operations
- ✅ **RESTful API**: Complete API for programmatic access

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 with Jinja2 templates
- **PDF Processing**: pdfplumber for text extraction
- **Excel Processing**: pandas + openpyxl
- **Authentication**: Simple admin interface (no login required for Phase I)

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone and Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Application

```bash
# Run the development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:8000/

## 📋 Usage Guide

### Step 1: Import Administrative Hierarchy

1. Go to **Hierarchy Management** section
2. Upload an Excel file with columns: `District`, `Mandal`, `Village`
3. The system will import and create the hierarchical structure

**Sample Excel Format:**
| District  | Mandal        | Village     |
|-----------|---------------|-------------|
| Hyderabad | Secunderabad  | Karkhana    |
| Hyderabad | Secunderabad  | Marredpally |
| Warangal  | Hanamkonda    | Kazipet     |

### Step 2: Add Booth Information

1. Go to **Booth Management** section
2. Select District → Mandal → Village
3. Enter Booth Number and Booth Name
4. Click "Create Booth"

### Step 3: Upload Voter PDFs

1. Navigate to the created booth detail page
2. Upload voter list PDF from CEO Telangana portal
3. System will extract and process voter data
4. Voters will be automatically grouped by house numbers

### Step 4: View and Search Data

1. Use **Voter Search** to find specific voters
2. Filter by location, name, voter ID, or house number
3. View booth summaries with house-wise voter grouping

## 🗂️ Database Schema

```
State (Telangana)
├── Districts
    ├── Mandals
        ├── Villages
            ├── Booths
                ├── Houses
                    ├── Voters
```

### Key Tables:
- **districts**: District information
- **mandals**: Mandal information linked to districts
- **villages**: Village information linked to mandals
- **booths**: Booth information linked to villages
- **houses**: House information linked to booths
- **voters**: Voter information linked to houses
- **upload_logs**: PDF processing history

## 🔌 API Endpoints

### Hierarchy Management
- `GET /api/districts` - Get all districts
- `GET /api/districts/{id}/mandals` - Get mandals for district
- `GET /api/mandals/{id}/villages` - Get villages for mandal
- `GET /api/villages/{id}/booths` - Get booths for village

### Booth Management
- `POST /api/booths` - Create new booth
- `GET /api/booths/{id}` - Get booth details
- `GET /api/booths/{id}/summary` - Get booth voter summary

### File Processing
- `POST /api/import-hierarchy` - Import hierarchy from Excel
- `POST /api/upload-voters` - Upload and process voter PDF

### Data Access
- `GET /api/voters/search` - Search voters with filters
- `GET /api/upload-logs` - Get upload processing logs
- `GET /api/stats` - Get system statistics

## 📊 Data Storage Structure

Each voter record contains:
```json
{
  "name": "Voter Name",
  "age": 35,
  "gender": "M",
  "voter_id": "ABC1234567",
  "house_number": "12-A",
  "booth_number": "001",
  "village_name": "Karkhana",
  "mandal_name": "Secunderabad",
  "district_name": "Hyderabad",
  "state": "Telangana"
}
```

## 🔧 Configuration

### PDF Processing
The system uses `pdfplumber` to extract text from PDFs. The parsing logic in `app/services.py` can be customized based on the specific format of CEO Telangana voter PDFs.

### Database
SQLite database is stored as `politiq.db` in the project root. For production, consider migrating to PostgreSQL or MySQL.

## 📝 Development Notes

### File Structure
```
app/
├── __init__.py
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── api.py               # API routes
├── services.py          # Business logic
├── templates/           # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── hierarchy.html
│   ├── booths.html
│   ├── booth_detail.html
│   ├── voters.html
│   └── upload_logs.html
└── static/              # Static files
    └── style.css
```

### Adding New Features
1. Define models in `models.py`
2. Create schemas in `schemas.py`
3. Add CRUD operations in `crud.py`
4. Implement business logic in `services.py`
5. Create API endpoints in `api.py`
6. Add web interface in `main.py` and templates

## 🚀 Phase II Roadmap

This is Phase I of the PolitiQ platform. Phase II will include:
- Assembly/Parliament constituency mapping
- Advanced analytics and dashboards
- AI-powered voter analysis
- Mobile app integration
- Advanced security and user management
- Real-time data synchronization

## 🤝 Support

For support and questions, contact:
**Shobanbabu Bhukya**  
Founder – PolitiQ.ai

## 📄 License

This is a proprietary system developed for PolitiQ.ai. All rights reserved.

---

**Note**: This system is designed for Phase I implementation. The PDF parsing logic may need adjustment based on the actual format of CEO Telangana voter PDFs. Sample test files would help improve extraction accuracy.
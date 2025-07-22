from fastapi import FastAPI, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import uvicorn

from app.database import engine, get_db
from app import models, crud, schemas
from app.api import router as api_router
from app.services import HierarchyService, PDFProcessingService

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="PolitiQ - Phase I: House-Level Voter Mapping Tool",
    description="Backend system for managing administrative hierarchy and voter data",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routes
app.include_router(api_router, prefix="/api", tags=["API"])

# Admin Web Interface Routes
@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin dashboard home page"""
    # Get statistics
    stats = {
        "districts": db.query(models.District).count(),
        "mandals": db.query(models.Mandal).count(),
        "villages": db.query(models.Village).count(),
        "booths": db.query(models.Booth).count(),
        "houses": db.query(models.House).count(),
        "voters": db.query(models.Voter).count(),
    }
    
    # Get recent upload logs
    recent_uploads = crud.get_upload_logs(db, limit=5)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "stats": stats, "recent_uploads": recent_uploads}
    )

@app.get("/hierarchy", response_class=HTMLResponse)
async def hierarchy_management(request: Request):
    """Hierarchy management page"""
    return templates.TemplateResponse("hierarchy.html", {"request": request})

@app.post("/hierarchy/import")
async def import_hierarchy_web(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Web interface for importing hierarchy"""
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="File must be an Excel file")
        
        file_content = await file.read()
        result = HierarchyService.import_hierarchy_from_excel(db, file_content)
        
        return templates.TemplateResponse(
            "hierarchy.html",
            {"request": request, "success": result['success'], "message": result['message'], "stats": result['stats']}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "hierarchy.html",
            {"request": request, "error": str(e)}
        )

@app.get("/booths", response_class=HTMLResponse)
async def booth_management(request: Request, db: Session = Depends(get_db)):
    """Booth management page"""
    districts = crud.get_districts(db)
    return templates.TemplateResponse(
        "booths.html",
        {"request": request, "districts": districts}
    )

@app.post("/booths/create")
async def create_booth_web(
    request: Request,
    village_id: int = Form(...),
    booth_number: str = Form(...),
    booth_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Web interface for creating booths"""
    try:
        # Check if booth already exists
        existing_booth = crud.get_booth_by_number_and_village(db, booth_number, village_id)
        if existing_booth:
            raise HTTPException(status_code=400, detail="Booth already exists")
        
        # Create booth
        booth_data = schemas.BoothCreate(
            booth_number=booth_number,
            booth_name=booth_name,
            village_id=village_id
        )
        booth = crud.create_booth(db, booth_data)
        
        return RedirectResponse(url=f"/booths/{booth.id}", status_code=303)
    
    except Exception as e:
        districts = crud.get_districts(db)
        return templates.TemplateResponse(
            "booths.html",
            {"request": request, "districts": districts, "error": str(e)}
        )

@app.get("/booths/{booth_id}", response_class=HTMLResponse)
async def booth_detail(request: Request, booth_id: int, db: Session = Depends(get_db)):
    """Booth detail page"""
    booth = crud.get_booth(db, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    
    # Get booth summary
    summary = crud.get_booth_summary(db, booth_id)
    
    return templates.TemplateResponse(
        "booth_detail.html",
        {"request": request, "booth": booth, "summary": summary}
    )

@app.post("/booths/{booth_id}/upload")
async def upload_voters_web(
    request: Request,
    booth_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Web interface for uploading voter PDFs"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        booth = crud.get_booth(db, booth_id)
        if not booth:
            raise HTTPException(status_code=404, detail="Booth not found")
        
        file_content = await file.read()
        result = PDFProcessingService.process_voter_pdf(db, booth_id, file.filename, file_content)
        
        return RedirectResponse(url=f"/booths/{booth_id}?upload_result={result['success']}", status_code=303)
    
    except Exception as e:
        return RedirectResponse(url=f"/booths/{booth_id}?error={str(e)}", status_code=303)

@app.get("/voters", response_class=HTMLResponse)
async def voter_search(request: Request, db: Session = Depends(get_db)):
    """Voter search page"""
    districts = crud.get_districts(db)
    return templates.TemplateResponse(
        "voters.html",
        {"request": request, "districts": districts}
    )

@app.get("/upload-logs", response_class=HTMLResponse)
async def upload_logs(request: Request, db: Session = Depends(get_db)):
    """Upload logs page"""
    logs = crud.get_upload_logs(db, limit=50)
    return templates.TemplateResponse(
        "upload_logs.html",
        {"request": request, "logs": logs}
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
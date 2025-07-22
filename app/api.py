from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.services import HierarchyService, PDFProcessingService

router = APIRouter()

# Hierarchy endpoints
@router.get("/districts", response_model=List[schemas.DropdownItem])
def get_districts(db: Session = Depends(get_db)):
    """Get all districts for dropdown"""
    districts = crud.get_districts(db)
    return [{"id": d.id, "name": d.name} for d in districts]

@router.get("/districts/{district_id}/mandals", response_model=List[schemas.DropdownItem])
def get_mandals_by_district(district_id: int, db: Session = Depends(get_db)):
    """Get mandals for a district"""
    mandals = crud.get_mandals_by_district(db, district_id)
    return [{"id": m.id, "name": m.name} for m in mandals]

@router.get("/mandals/{mandal_id}/villages", response_model=List[schemas.DropdownItem])
def get_villages_by_mandal(mandal_id: int, db: Session = Depends(get_db)):
    """Get villages for a mandal"""
    villages = crud.get_villages_by_mandal(db, mandal_id)
    return [{"id": v.id, "name": v.name} for v in villages]

@router.get("/villages/{village_id}/booths", response_model=List[schemas.DropdownItem])
def get_booths_by_village(village_id: int, db: Session = Depends(get_db)):
    """Get booths for a village"""
    booths = crud.get_booths_by_village(db, village_id)
    return [{"id": b.id, "name": f"{b.booth_number} - {b.booth_name}"} for b in booths]

# Booth management
@router.post("/booths", response_model=schemas.Booth)
def create_booth(booth: schemas.BoothCreate, db: Session = Depends(get_db)):
    """Create a new booth"""
    # Check if booth already exists
    existing_booth = crud.get_booth_by_number_and_village(
        db, booth.booth_number, booth.village_id
    )
    if existing_booth:
        raise HTTPException(
            status_code=400,
            detail="Booth with this number already exists in this village"
        )
    
    return crud.create_booth(db, booth)

@router.get("/booths/{booth_id}", response_model=schemas.Booth)
def get_booth(booth_id: int, db: Session = Depends(get_db)):
    """Get booth details"""
    booth = crud.get_booth(db, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    return booth

# Excel hierarchy import
@router.post("/import-hierarchy")
async def import_hierarchy(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import administrative hierarchy from Excel file"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="File must be an Excel file (.xlsx or .xls)"
        )
    
    file_content = await file.read()
    result = HierarchyService.import_hierarchy_from_excel(db, file_content)
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result

# PDF voter upload
@router.post("/upload-voters")
async def upload_voters(
    booth_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process voter PDF for a booth"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="File must be a PDF"
        )
    
    # Verify booth exists
    booth = crud.get_booth(db, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    
    file_content = await file.read()
    result = PDFProcessingService.process_voter_pdf(
        db, booth_id, file.filename, file_content
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result

# Voter data viewing
@router.get("/booths/{booth_id}/summary")
def get_booth_summary(booth_id: int, db: Session = Depends(get_db)):
    """Get voter summary for a booth grouped by house"""
    summary = crud.get_booth_summary(db, booth_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Booth not found")
    
    return summary

@router.get("/voters/search")
def search_voters(
    district_id: int = None,
    mandal_id: int = None,
    village_id: int = None,
    booth_id: int = None,
    house_number: str = None,
    voter_id: str = None,
    name: str = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Search voters with filters"""
    query = db.query(models.Voter)
    
    # Apply filters
    if voter_id:
        query = query.filter(models.Voter.voter_id.ilike(f"%{voter_id}%"))
    if name:
        query = query.filter(models.Voter.name.ilike(f"%{name}%"))
    if house_number:
        query = query.filter(models.Voter.house_number.ilike(f"%{house_number}%"))
    if booth_id:
        query = query.join(models.House).filter(models.House.booth_id == booth_id)
    elif village_id:
        query = query.join(models.House).join(models.Booth).filter(models.Booth.village_id == village_id)
    elif mandal_id:
        query = query.join(models.House).join(models.Booth).join(models.Village).filter(models.Village.mandal_id == mandal_id)
    elif district_id:
        query = query.join(models.House).join(models.Booth).join(models.Village).join(models.Mandal).filter(models.Mandal.district_id == district_id)
    
    total = query.count()
    voters = query.offset(skip).limit(limit).all()
    
    return {
        "voters": voters,
        "total": total,
        "skip": skip,
        "limit": limit
    }

# Upload logs
@router.get("/upload-logs", response_model=List[schemas.UploadLog])
def get_upload_logs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get upload logs"""
    return crud.get_upload_logs(db, skip, limit)

# Statistics
@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """Get overall statistics"""
    districts_count = db.query(models.District).count()
    mandals_count = db.query(models.Mandal).count()
    villages_count = db.query(models.Village).count()
    booths_count = db.query(models.Booth).count()
    houses_count = db.query(models.House).count()
    voters_count = db.query(models.Voter).count()
    
    return {
        "districts": districts_count,
        "mandals": mandals_count,
        "villages": villages_count,
        "booths": booths_count,
        "houses": houses_count,
        "voters": voters_count
    }
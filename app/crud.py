from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app import models, schemas

# District CRUD operations
def get_district(db: Session, district_id: int):
    return db.query(models.District).filter(models.District.id == district_id).first()

def get_district_by_name(db: Session, name: str):
    return db.query(models.District).filter(models.District.name == name).first()

def get_districts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.District).offset(skip).limit(limit).all()

def create_district(db: Session, district: schemas.DistrictCreate):
    db_district = models.District(**district.dict())
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

# Mandal CRUD operations
def get_mandal(db: Session, mandal_id: int):
    return db.query(models.Mandal).filter(models.Mandal.id == mandal_id).first()

def get_mandals_by_district(db: Session, district_id: int):
    return db.query(models.Mandal).filter(models.Mandal.district_id == district_id).all()

def get_mandal_by_name_and_district(db: Session, name: str, district_id: int):
    return db.query(models.Mandal).filter(
        and_(models.Mandal.name == name, models.Mandal.district_id == district_id)
    ).first()

def create_mandal(db: Session, mandal: schemas.MandalCreate):
    db_mandal = models.Mandal(**mandal.dict())
    db.add(db_mandal)
    db.commit()
    db.refresh(db_mandal)
    return db_mandal

# Village CRUD operations
def get_village(db: Session, village_id: int):
    return db.query(models.Village).filter(models.Village.id == village_id).first()

def get_villages_by_mandal(db: Session, mandal_id: int):
    return db.query(models.Village).filter(models.Village.mandal_id == mandal_id).all()

def get_village_by_name_and_mandal(db: Session, name: str, mandal_id: int):
    return db.query(models.Village).filter(
        and_(models.Village.name == name, models.Village.mandal_id == mandal_id)
    ).first()

def create_village(db: Session, village: schemas.VillageCreate):
    db_village = models.Village(**village.dict())
    db.add(db_village)
    db.commit()
    db.refresh(db_village)
    return db_village

# Booth CRUD operations
def get_booth(db: Session, booth_id: int):
    return db.query(models.Booth).filter(models.Booth.id == booth_id).first()

def get_booths_by_village(db: Session, village_id: int):
    return db.query(models.Booth).filter(models.Booth.village_id == village_id).all()

def get_booth_by_number_and_village(db: Session, booth_number: str, village_id: int):
    return db.query(models.Booth).filter(
        and_(models.Booth.booth_number == booth_number, models.Booth.village_id == village_id)
    ).first()

def create_booth(db: Session, booth: schemas.BoothCreate):
    db_booth = models.Booth(**booth.dict())
    db.add(db_booth)
    db.commit()
    db.refresh(db_booth)
    return db_booth

# House CRUD operations
def get_house(db: Session, house_id: int):
    return db.query(models.House).filter(models.House.id == house_id).first()

def get_houses_by_booth(db: Session, booth_id: int):
    return db.query(models.House).filter(models.House.booth_id == booth_id).all()

def get_house_by_number_and_booth(db: Session, house_number: str, booth_id: int):
    return db.query(models.House).filter(
        and_(models.House.house_number == house_number, models.House.booth_id == booth_id)
    ).first()

def create_house(db: Session, house: schemas.HouseCreate):
    db_house = models.House(**house.dict())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

def get_or_create_house(db: Session, house_number: str, booth_id: int):
    house = get_house_by_number_and_booth(db, house_number, booth_id)
    if not house:
        house_data = schemas.HouseCreate(house_number=house_number, booth_id=booth_id)
        house = create_house(db, house_data)
    return house

# Voter CRUD operations
def get_voter(db: Session, voter_id: int):
    return db.query(models.Voter).filter(models.Voter.id == voter_id).first()

def get_voter_by_voter_id(db: Session, voter_id: str):
    return db.query(models.Voter).filter(models.Voter.voter_id == voter_id).first()

def get_voters_by_house(db: Session, house_id: int):
    return db.query(models.Voter).filter(models.Voter.house_id == house_id).all()

def get_voters_by_booth(db: Session, booth_id: int):
    return db.query(models.Voter).join(models.House).filter(models.House.booth_id == booth_id).all()

def create_voter(db: Session, voter: schemas.VoterCreate):
    db_voter = models.Voter(**voter.dict())
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter

def bulk_create_voters(db: Session, voters: List[schemas.VoterCreate]):
    """Bulk insert voters for better performance"""
    db_voters = [models.Voter(**voter.dict()) for voter in voters]
    db.add_all(db_voters)
    db.commit()
    return len(db_voters)

# Upload Log CRUD operations
def create_upload_log(db: Session, upload_log: schemas.UploadLogCreate):
    db_upload_log = models.UploadLog(**upload_log.dict())
    db.add(db_upload_log)
    db.commit()
    db.refresh(db_upload_log)
    return db_upload_log

def update_upload_log(db: Session, upload_log_id: int, total_voters: int, total_houses: int, status: str, error_message: str = None):
    db_upload_log = db.query(models.UploadLog).filter(models.UploadLog.id == upload_log_id).first()
    if db_upload_log:
        db_upload_log.total_voters = total_voters
        db_upload_log.total_houses = total_houses
        db_upload_log.status = status
        db_upload_log.error_message = error_message
        db.commit()
        db.refresh(db_upload_log)
    return db_upload_log

def get_upload_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UploadLog).offset(skip).limit(limit).all()

# Statistics functions
def get_booth_summary(db: Session, booth_id: int):
    """Get summary of voters grouped by house for a booth"""
    booth = get_booth(db, booth_id)
    if not booth:
        return None
    
    houses = get_houses_by_booth(db, booth_id)
    house_summaries = []
    
    total_voters = 0
    for house in houses:
        voters = get_voters_by_house(db, house.id)
        if voters:
            house_summaries.append({
                "house_number": house.house_number,
                "voters": voters,
                "total_voters": len(voters)
            })
            total_voters += len(voters)
    
    return {
        "booth": booth,
        "houses": house_summaries,
        "total_houses": len(house_summaries),
        "total_voters": total_voters
    }
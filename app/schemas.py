from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# District Schemas
class DistrictBase(BaseModel):
    name: str
    state: str = "Telangana"

class DistrictCreate(DistrictBase):
    pass

class District(DistrictBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Mandal Schemas
class MandalBase(BaseModel):
    name: str
    district_id: int

class MandalCreate(MandalBase):
    pass

class Mandal(MandalBase):
    id: int
    created_at: datetime
    district: District
    
    class Config:
        from_attributes = True

# Village Schemas
class VillageBase(BaseModel):
    name: str
    mandal_id: int

class VillageCreate(VillageBase):
    pass

class Village(VillageBase):
    id: int
    created_at: datetime
    mandal: Mandal
    
    class Config:
        from_attributes = True

# Booth Schemas
class BoothBase(BaseModel):
    booth_number: str
    booth_name: str
    village_id: int

class BoothCreate(BoothBase):
    pass

class Booth(BoothBase):
    id: int
    created_at: datetime
    village: Village
    
    class Config:
        from_attributes = True

# House Schemas
class HouseBase(BaseModel):
    house_number: str
    booth_id: int

class HouseCreate(HouseBase):
    pass

class House(HouseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Voter Schemas
class VoterBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    voter_id: str
    house_id: int

class VoterCreate(VoterBase):
    district_name: Optional[str] = None
    mandal_name: Optional[str] = None
    village_name: Optional[str] = None
    booth_number: Optional[str] = None
    house_number: Optional[str] = None

class Voter(VoterBase):
    id: int
    district_name: Optional[str] = None
    mandal_name: Optional[str] = None
    village_name: Optional[str] = None
    booth_number: Optional[str] = None
    house_number: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Upload Log Schemas
class UploadLogBase(BaseModel):
    filename: str
    booth_id: int

class UploadLogCreate(UploadLogBase):
    total_voters: int = 0
    total_houses: int = 0
    status: str = "processing"
    error_message: Optional[str] = None

class UploadLog(UploadLogBase):
    id: int
    total_voters: int
    total_houses: int
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Hierarchy Response Schema
class HierarchyResponse(BaseModel):
    districts: List[District]

# Simple dropdown schemas
class DropdownItem(BaseModel):
    id: int
    name: str

class HierarchyDropdown(BaseModel):
    districts: List[DropdownItem]
    mandals: List[DropdownItem] = []
    villages: List[DropdownItem] = []

# Voter Summary Schema
class VoterSummary(BaseModel):
    house_number: str
    voters: List[Voter]
    total_voters: int

class BoothSummary(BaseModel):
    booth: Booth
    houses: List[VoterSummary]
    total_houses: int
    total_voters: int
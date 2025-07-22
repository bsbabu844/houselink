from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    state = Column(String, default="Telangana", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    mandals = relationship("Mandal", back_populates="district", cascade="all, delete-orphan")

class Mandal(Base):
    __tablename__ = "mandals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    district = relationship("District", back_populates="mandals")
    villages = relationship("Village", back_populates="mandal", cascade="all, delete-orphan")

class Village(Base):
    __tablename__ = "villages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    mandal_id = Column(Integer, ForeignKey("mandals.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    mandal = relationship("Mandal", back_populates="villages")
    booths = relationship("Booth", back_populates="village", cascade="all, delete-orphan")

class Booth(Base):
    __tablename__ = "booths"
    
    id = Column(Integer, primary_key=True, index=True)
    booth_number = Column(String, nullable=False, index=True)
    booth_name = Column(String, nullable=False)
    village_id = Column(Integer, ForeignKey("villages.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    village = relationship("Village", back_populates="booths")
    houses = relationship("House", back_populates="booth", cascade="all, delete-orphan")

class House(Base):
    __tablename__ = "houses"
    
    id = Column(Integer, primary_key=True, index=True)
    house_number = Column(String, nullable=False, index=True)
    booth_id = Column(Integer, ForeignKey("booths.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    booth = relationship("Booth", back_populates="houses")
    voters = relationship("Voter", back_populates="house", cascade="all, delete-orphan")

class Voter(Base):
    __tablename__ = "voters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    voter_id = Column(String, unique=True, index=True, nullable=False)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    
    # Derived fields for easy querying
    district_name = Column(String, nullable=True, index=True)
    mandal_name = Column(String, nullable=True, index=True)
    village_name = Column(String, nullable=True, index=True)
    booth_number = Column(String, nullable=True, index=True)
    house_number = Column(String, nullable=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    house = relationship("House", back_populates="voters")

class UploadLog(Base):
    __tablename__ = "upload_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    booth_id = Column(Integer, ForeignKey("booths.id"), nullable=False)
    total_voters = Column(Integer, default=0)
    total_houses = Column(Integer, default=0)
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    booth = relationship("Booth")
import pandas as pd
import re
import io
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app import crud, schemas, models
import pdfplumber

class HierarchyService:
    """Service for managing administrative hierarchy"""
    
    @staticmethod
    def import_hierarchy_from_excel(db: Session, file_content: bytes) -> Dict[str, Any]:
        """
        Import hierarchy from Excel file
        Expected columns: District, Mandal, Village
        """
        try:
            # Read Excel file
            df = pd.read_excel(io.BytesIO(file_content))
            
            # Validate columns
            required_columns = ['District', 'Mandal', 'Village']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Excel file must contain columns: {required_columns}")
            
            # Clean data
            df = df.dropna(subset=required_columns)
            df[required_columns] = df[required_columns].astype(str).apply(lambda x: x.str.strip())
            
            # Track stats
            stats = {
                'districts_created': 0,
                'mandals_created': 0,
                'villages_created': 0,
                'districts_skipped': 0,
                'mandals_skipped': 0,
                'villages_skipped': 0
            }
            
            # Process each row
            for _, row in df.iterrows():
                district_name = row['District']
                mandal_name = row['Mandal']
                village_name = row['Village']
                
                # Create or get district
                district = crud.get_district_by_name(db, district_name)
                if not district:
                    district_data = schemas.DistrictCreate(name=district_name)
                    district = crud.create_district(db, district_data)
                    stats['districts_created'] += 1
                else:
                    stats['districts_skipped'] += 1
                
                # Create or get mandal
                mandal = crud.get_mandal_by_name_and_district(db, mandal_name, district.id)
                if not mandal:
                    mandal_data = schemas.MandalCreate(name=mandal_name, district_id=district.id)
                    mandal = crud.create_mandal(db, mandal_data)
                    stats['mandals_created'] += 1
                else:
                    stats['mandals_skipped'] += 1
                
                # Create or get village
                village = crud.get_village_by_name_and_mandal(db, village_name, mandal.id)
                if not village:
                    village_data = schemas.VillageCreate(name=village_name, mandal_id=mandal.id)
                    village = crud.create_village(db, village_data)
                    stats['villages_created'] += 1
                else:
                    stats['villages_skipped'] += 1
            
            return {
                'success': True,
                'message': 'Hierarchy imported successfully',
                'stats': stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error importing hierarchy: {str(e)}',
                'stats': None
            }

class PDFProcessingService:
    """Service for processing voter PDFs"""
    
    @staticmethod
    def extract_voter_data_from_pdf(file_content: bytes) -> List[Dict[str, Any]]:
        """
        Extract voter data from PDF
        Returns list of voter dictionaries with house numbers
        """
        voters = []
        
        try:
            # Open PDF
            pdf_file = io.BytesIO(file_content)
            
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Extract voter records from text
                        page_voters = PDFProcessingService._parse_voter_text(text)
                        voters.extend(page_voters)
        
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            
        return voters
    
    @staticmethod
    def _parse_voter_text(text: str) -> List[Dict[str, Any]]:
        """
        Parse voter information from text
        This is a basic implementation - you may need to adjust based on PDF format
        """
        voters = []
        lines = text.split('\n')
        
        current_house = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract house number (common patterns)
            house_match = re.search(r'House\s+No\.?\s*:?\s*(\d+[A-Za-z]*)', line, re.IGNORECASE)
            if house_match:
                current_house = house_match.group(1)
                continue
            
            # Try to extract voter information
            # Pattern: Name, Age, Gender, Voter ID
            voter_match = re.search(
                r'(\w+(?:\s+\w+)*)\s+(\d{1,3})\s+([MF])\s+([A-Z]{3}\d{7})',
                line
            )
            
            if voter_match and current_house:
                name = voter_match.group(1).strip()
                age = int(voter_match.group(2))
                gender = voter_match.group(3)
                voter_id = voter_match.group(4)
                
                voters.append({
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'voter_id': voter_id,
                    'house_number': current_house
                })
        
        return voters
    
    @staticmethod
    def process_voter_pdf(db: Session, booth_id: int, filename: str, file_content: bytes) -> Dict[str, Any]:
        """
        Process voter PDF and save to database
        """
        try:
            # Create upload log
            upload_log_data = schemas.UploadLogCreate(
                filename=filename,
                booth_id=booth_id,
                status="processing"
            )
            upload_log = crud.create_upload_log(db, upload_log_data)
            
            # Extract voter data from PDF
            voter_data = PDFProcessingService.extract_voter_data_from_pdf(file_content)
            
            if not voter_data:
                crud.update_upload_log(
                    db, upload_log.id, 0, 0, "failed", 
                    "No voter data found in PDF"
                )
                return {
                    'success': False,
                    'message': 'No voter data found in PDF',
                    'upload_log_id': upload_log.id
                }
            
            # Get booth info for derived fields
            booth = crud.get_booth(db, booth_id)
            if not booth:
                crud.update_upload_log(
                    db, upload_log.id, 0, 0, "failed", 
                    "Booth not found"
                )
                return {
                    'success': False,
                    'message': 'Booth not found',
                    'upload_log_id': upload_log.id
                }
            
            # Group voters by house
            houses_data = {}
            for voter in voter_data:
                house_number = voter['house_number']
                if house_number not in houses_data:
                    houses_data[house_number] = []
                houses_data[house_number].append(voter)
            
            # Process each house and its voters
            total_voters_created = 0
            total_houses_created = 0
            voters_to_create = []
            
            for house_number, house_voters in houses_data.items():
                # Get or create house
                house = crud.get_or_create_house(db, house_number, booth_id)
                if house:
                    total_houses_created += 1
                
                # Prepare voters for bulk insert
                for voter_data_item in house_voters:
                    # Check if voter already exists
                    existing_voter = crud.get_voter_by_voter_id(db, voter_data_item['voter_id'])
                    if not existing_voter:
                        voter_create = schemas.VoterCreate(
                            name=voter_data_item['name'],
                            age=voter_data_item['age'],
                            gender=voter_data_item['gender'],
                            voter_id=voter_data_item['voter_id'],
                            house_id=house.id,
                            district_name=booth.village.mandal.district.name,
                            mandal_name=booth.village.mandal.name,
                            village_name=booth.village.name,
                            booth_number=booth.booth_number,
                            house_number=house_number
                        )
                        voters_to_create.append(voter_create)
            
            # Bulk create voters
            if voters_to_create:
                total_voters_created = crud.bulk_create_voters(db, voters_to_create)
            
            # Update upload log
            crud.update_upload_log(
                db, upload_log.id, total_voters_created, total_houses_created, "completed"
            )
            
            return {
                'success': True,
                'message': f'Successfully processed {total_voters_created} voters in {total_houses_created} houses',
                'upload_log_id': upload_log.id,
                'stats': {
                    'total_voters': total_voters_created,
                    'total_houses': total_houses_created
                }
            }
            
        except Exception as e:
            # Update upload log with error
            if 'upload_log' in locals():
                crud.update_upload_log(
                    db, upload_log.id, 0, 0, "failed", str(e)
                )
            
            return {
                'success': False,
                'message': f'Error processing PDF: {str(e)}',
                'upload_log_id': upload_log.id if 'upload_log' in locals() else None
            }
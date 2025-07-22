#!/usr/bin/env python3
"""
Script to create sample test data for PolitiQ Phase I system
Run this script to generate sample Excel file for testing
"""

import pandas as pd
import os

def create_sample_excel():
    """Create sample Telangana hierarchy Excel file"""
    
    # Create sample_data directory if it doesn't exist
    os.makedirs('sample_data', exist_ok=True)
    
    # Sample Telangana hierarchy data
    data = {
        'District': [
            'Hyderabad', 'Hyderabad', 'Hyderabad', 'Hyderabad', 'Hyderabad',
            'Warangal', 'Warangal', 'Warangal', 'Warangal',
            'Nizamabad', 'Nizamabad', 'Nizamabad',
            'Adilabad', 'Adilabad', 'Adilabad',
            'Khammam', 'Khammam', 'Khammam',
            'Karimnagar', 'Karimnagar', 'Karimnagar',
            'Medak', 'Medak', 'Medak'
        ],
        'Mandal': [
            'Secunderabad', 'Secunderabad', 'Charminar', 'Golconda', 'Uppal',
            'Hanamkonda', 'Parkal', 'Jangaon', 'Narsampet',
            'Nizamabad Urban', 'Bodhan', 'Armoor',
            'Adilabad', 'Ichoda', 'Nirmal',
            'Khammam Urban', 'Kothagudem', 'Wyra',
            'Karimnagar Urban', 'Choppadandi', 'Huzurabad',
            'Medak', 'Sangareddy', 'Zaheerabad'
        ],
        'Village': [
            'Karkhana', 'Marredpally', 'Charminar', 'Langar Houz', 'Uppal',
            'Kazipet', 'Parkal', 'Jangaon', 'Narsampet',
            'Nizamabad', 'Bodhan', 'Armoor',
            'Adilabad', 'Ichoda', 'Nirmal',
            'Khammam', 'Kothagudem', 'Wyra',
            'Karimnagar', 'Choppadandi', 'Huzurabad',
            'Medak', 'Sangareddy', 'Zaheerabad'
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    filename = 'sample_data/telangana_hierarchy_sample.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"✅ Sample Excel file created: {filename}")
    print(f"📊 Contains {len(df)} records with {len(df['District'].unique())} districts")
    
    # Also create CSV version
    csv_filename = 'sample_data/telangana_hierarchy_sample.csv'
    df.to_csv(csv_filename, index=False)
    print(f"✅ Sample CSV file created: {csv_filename}")
    
    return filename

def create_sample_voter_data():
    """Create sample voter data (for testing PDF processing logic)"""
    
    sample_voter_text = """
    Booth No: 001
    Booth Name: Government High School, Karkhana
    
    House No: 12-A
    1. Ramesh Kumar    35    M    ABC1234567
    2. Sunita Devi     32    F    ABC2345678
    3. Rahul Kumar     18    M    ABC3456789
    
    House No: 13-B
    1. Mukesh Sharma   45    M    DEF1234567
    2. Priya Sharma    42    F    DEF2345678
    3. Arjun Sharma    20    M    DEF3456789
    4. Kavya Sharma    16    F    DEF4567890
    
    House No: 14
    1. Suresh Reddy    55    M    GHI1234567
    2. Lakshmi Reddy   52    F    GHI2345678
    3. Venkat Reddy    28    M    GHI3456789
    
    House No: 15-A
    1. Ahmed Khan      38    M    JKL1234567
    2. Fatima Khan     35    F    JKL2345678
    3. Salman Khan     12    M    JKL3456789
    """
    
    # Save sample voter text
    os.makedirs('sample_data', exist_ok=True)
    with open('sample_data/sample_voter_data.txt', 'w') as f:
        f.write(sample_voter_text)
    
    print("✅ Sample voter data text created: sample_data/sample_voter_data.txt")
    print("💡 This shows the expected format for PDF parsing")

def main():
    """Main function to create all sample data"""
    print("🚀 Creating sample data for PolitiQ Phase I...")
    print()
    
    try:
        # Create sample Excel file
        create_sample_excel()
        print()
        
        # Create sample voter data
        create_sample_voter_data()
        print()
        
        print("✨ All sample data created successfully!")
        print()
        print("📋 Next steps:")
        print("1. Start the application: python -m uvicorn app.main:app --reload")
        print("2. Open http://localhost:8000 in your browser")
        print("3. Go to Hierarchy Management and upload the Excel file")
        print("4. Create booths and upload voter PDFs")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

if __name__ == "__main__":
    main()
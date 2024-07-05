from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, database, models
import os

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/file/{file_id}")
def get_file_information(file_id: int, db: Session = Depends(get_db)):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "filename": file.filename,
        "size": file.size,
        "type": file.type
    }

@app.get("/file/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Assuming you have a filepath stored in the database
    file_path = file.filepath
    return {"file_path": file_path}  # Replace with actual download logic

@app.put("/file/{file_id}/update")
def update_file(file_id: int, file: schemas.file, db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Update the file attributes
    db_file.filename = file.filename
    db_file.size = file.size
    db_file.type = file.type

    db.commit()
    db.refresh(db_file)
    return {"message": "File updated successfully", "file": db_file}

@app.post("/file/create")
def create_file(file_info: schemas.file, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save the uploaded file to a directory
        upload_path = os.path.join("upload", file.filename)
        with open(upload_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        # Create a database entry for the file
        db_file = models.File(**file_info.dict(), filepath=upload_path)
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return {"message": "File created successfully", "file_info": db_file}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

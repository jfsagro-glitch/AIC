from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Загрузка Excel файлов с данными о недвижимости
    """
    extracted_data = []
    
    for file in files:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail=f"Файл {file.filename} должен быть Excel файлом (.xlsx или .xls)"
            )
        
        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            
            # Преобразование DataFrame в словарь
            data_dict = df.to_dict(orient='records')
            
            extracted_data.append({
                "filename": file.filename,
                "rows_count": len(data_dict),
                "data": data_dict,
                "columns": list(df.columns)
            })
        
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка при чтении файла {file.filename}: {str(e)}"
            )
    
    return {
        "success": True,
        "files_processed": len(extracted_data),
        "data": extracted_data
    }

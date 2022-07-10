from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel, Field
from pikepdf import Pdf
from fastapi.responses import FileResponse, StreamingResponse


app = FastAPI()

class Country(BaseModel):
    country_id: int = Field(default_factory=_find_next_id, alias="id")
    name: str
    capital: str
    area: int

countries = [
    Country(id=1, name="Thailand", capital="Bangkok", area=513120),
    Country(id=2, name="Australia", capital="Canberra", area=7617930),
    Country(id=3, name="Egypt", capital="Cairo", area=1010408),
]

@app.get("/countries")
async def get_countries():
    return countries


@app.post("/decryptPdf")
async def upload( file: UploadFile = File(...), password: str = Form(...)):    
    allowedFiles = {"application/pdf"}
    if file.content_type in allowedFiles:
        # passw = request.headers['password']
        try:
            contents = await file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            await file.close()

        print(f"Trying to open {file.filename} with password: {password}")
        pdf = Pdf.open(file.filename, password=password, allow_overwriting_input=True)
        pdf.save(file.filename)
    
        # return {"message": f"Successfuly uploaded {file.filename}"}
        return FileResponse(file.filename)
    
    else:
        return { "Error": "Please upload PDF file format only."}
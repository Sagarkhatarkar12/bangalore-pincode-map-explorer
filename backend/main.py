from fastapi import FastAPI,Query,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI();
app.add_middleware(
   CORSMiddleware,
    allow_origins=[   
 "http://localhost:3000",
    "https://6a01d47771d2c60c62b2c71c--bangalore-pincode-map-explorer.netlify.app",  # ← deploy preview URL
    "https://bangalore-pincode-map-explorer.netlify.app"      ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
with open("pincodes.json","r",encoding="utf-8") as f:
    data = json.load(f)
@app.get("/api/areas")
def get_areas():
    return data

@app.get("/api/lookup")
def lookup(pincode: str = None,area:str = None):
    if pincode:
        results = [d for d in data if d["pincode"] == pincode]
        if not results:
            raise HTTPException(status_code=404, detail = "Pincode not found")
        return results[0]
    if area:
        area_lower = area.lower()
        results = [d for d in data if area_lower in d["area"].lower()]
        if not results:
            raise HTTPException(status_code=404, detail = "Area not found")
        exact = [d for d in results if d["area"].lower()== area_lower]
        return exact[0] if exact else results[0]
    raise HTTPException(status_code=400, detail = "Provide pincode or area query")
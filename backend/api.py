from fastapi import FastAPI
from backend.data_processing import DataExplorer

app = FastAPI()

@app.get("/categorized_crimes")
async def categorized_crimes():
    explorer = DataExplorer()
    explorer.categorize_crimes()
    return explorer.json_response()


# Returnera KPI:er baserat på year
@app.get("/kpis")
async def get_kpis(year: int):
    data_explorer = DataExplorer()
    return data_explorer.kpis(year=year)

@app.get("/plot_per_year")
async def plot_per_year():
    data_explorer = DataExplorer()
    return data_explorer.show_crimes_per_year()
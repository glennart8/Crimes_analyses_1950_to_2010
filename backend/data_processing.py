from utils.constants import CSV_PATH
import pandas as pd
import plotly.express as px

df = pd.read_csv(CSV_PATH, header=0, encoding="utf-8")


class DataExplorer:
    def __init__(self):
        self._df = df.reset_index(drop=True)

    # "Skyddar" den riktiga "privata" _df
    @property
    def df(self):
        return self._df
    
    
    def categorize_crimes(self):
        # Brottskategorier
        violent_crimes = ['murder', 'assault', 'rape', 'sexual.offenses']
        theft_crimes = ['burglary', 'vehicle.theft', 'shop.theft', 'stealing.general', 'out.of.vehicle.theft', 'robbery']
        vandal_crimes = ['criminal.damage']
        alc_and_drug_crimes = ['narcotics', 'drunk.driving']
        economic_crimes = ['fraud']

        # Skapa kolumner per kategori
        self._df['Violent'] = self._df[violent_crimes].sum(axis=1)
        self._df['Theft'] = self._df[theft_crimes].sum(axis=1)
        self._df['Vandal'] = self._df[vandal_crimes].sum(axis=1)
        self._df['Alc/Drug'] = self._df[alc_and_drug_crimes].sum(axis=1)
        self._df['Economic'] = self._df[economic_crimes].sum(axis=1)
        return self


    def kpis(self, year: int):
        df_by_year = self._df[self._df['Year'] == year]
        if df_by_year.empty:
            return {"total_crimes": 0, "population": 0, "avg_crimes_per_capita": 0}
        
        total_crimes = df_by_year['crimes.total'].sum()
        population = df_by_year['population'].sum()
        avg_per_capita = total_crimes / population if population > 0 else 0
        
        return {
            "total_crimes": int(total_crimes),
            "population": int(population),
            "avg_crimes_per_capita": avg_per_capita
        }

    def json_response(self):
        return self._df.to_dict(orient='records')

    def show_crimes_per_year(self):
        exclude_cols = ['Year', 'crimes.total', 'crimes.penal.code', 'crimes.person', 'population']
        crime_cols = [col for col in self._df.columns if col not in exclude_cols]

        df_long = self._df.melt(
            id_vars=['Year'],
            value_vars=crime_cols,
            var_name='Crime',
            value_name='Count'
        )

        return df_long.to_dict(orient='records')  # Returnerar serialiserbart format



if __name__ == "__main__":
    data_explorer = DataExplorer()
    
    
    df = pd.read_csv(CSV_PATH, sep=",")
    print(df.head())
    print(df.columns.tolist())
    
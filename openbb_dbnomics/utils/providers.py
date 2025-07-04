import requests
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

class DBNomicsClient:
    BASE_URL = "https://api.db.nomics.world/v22"

    def get_providers(self):
        url = f"{self.BASE_URL}/providers"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        providers = data.get("providers", {})
        return providers.get("docs", [])

    def get_datasets(self, search_term: str = None, limit: int = 100):
        if not search_term:
            return []
        search_url = f"{self.BASE_URL}/search"
        params = {
            "q": search_term,
            "limit": limit
        }
        search_response = requests.get(search_url, params=params)
        if search_response.status_code == 200:
            search_data = search_response.json()
            # Extract datasets from results.docs
            return search_data.get("results", {}).get("docs", [])
        return []

    def get_series(self, provider_code: str, dataset_code: str, limit: int = 100, ref_area: str = None):
        url = f"{self.BASE_URL}/series/{provider_code}/{dataset_code}"
        params = {"limit": limit}
        if ref_area:
            params["dimensions[REF_AREA]"] = ref_area
        response = requests.get(url, params=params)
        # print("Status:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            #print("Data:", data)
            series_list = data.get("series", {}).get("docs", [])
            #print("Series list:", series_list)
            flat_series = self.flatten_series(series_list)
            #print("Flat series:", flat_series)
            return flat_series
        return []

    def flatten_series(self, series_docs):
        #print(f"flatten_series called with {len(series_docs)} docs")
        flat = []
        for doc in series_docs:
            flat_doc = {
                "series_code": doc.get("series_code"),
                "series_name": doc.get("series_name"),
                "dataset_code": doc.get("dataset_code"),
                "dataset_name": doc.get("dataset_name"),
                "provider_code": doc.get("provider_code"),
            }
            # Add dimensions as top-level keys
            for dim_key, dim_val in doc.get("dimensions", {}).items():
                flat_doc[dim_key] = dim_val
            flat.append(flat_doc)
        #print(f"Returning {len(flat)} flattened series")
        return flat

    def get_ref_area_map(self, provider_code: str, dataset_code: str):
        url = f"{self.BASE_URL}/datasets/{provider_code}/{dataset_code}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            datasets = data.get("datasets", [])
            if isinstance(datasets, list) and datasets and "REF_AREA" in datasets[0]:
                return datasets[0]["REF_AREA"]
            elif isinstance(datasets, dict) and "REF_AREA" in datasets:
                return datasets["REF_AREA"]
        return {}

    def get_dataset_metadata(self, provider_code: str, dataset_code: str):
        url = f"{self.BASE_URL}/datasets/{provider_code}/{dataset_code}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            datasets = data.get("datasets", {})
            #print("DEBUG: datasets type:", type(datasets), "value (truncated):", str(datasets)[:500])
            # If datasets is a dict with 'docs', get the first doc
            if isinstance(datasets, dict) and "docs" in datasets and datasets["docs"]:
                return datasets["docs"][0]
            # If datasets is a dict of dataset_code: dict, get the first value
            if isinstance(datasets, dict) and datasets:
                return next(iter(datasets.values()))
            # If datasets is a list, get the first item
            if isinstance(datasets, list) and datasets:
                return datasets[0]
        return {}

    def get_multi_series_aligned(self, provider, dataset, freq, ref_area, indicators):
        # print("Fetching series directly for:", indicators)
        base_url = f"{self.BASE_URL}/series/{provider}/{dataset}/"
        dfs = []
        for ind in indicators:
            series_id = f"{freq}.{ref_area}.{ind}"
            url = base_url + series_id
            params = {"format": "json", "observations": 1}
            # print("Fetching:", url)
            resp = requests.get(url, params=params)
            # print("Final requested URL:", resp.url)
            data = resp.json()
            # print("Raw API response for", series_id, ":", data)
            docs = data.get("series", {}).get("docs", [])
            if not docs:
                # print(f"No docs for {series_id}")
                continue
            doc = docs[0]
            periods = doc.get("periods") or doc.get("period") or doc.get("period_start_day") or []
            values = doc.get("values") or doc.get("value") or []
            min_len = min(len(periods), len(values))
            periods = periods[:min_len]
            values = values[:min_len]
            if not periods or not values:
                # print(f"No data for {series_id}")
                continue
            df = pd.DataFrame({"date": periods, ind: values})
            dfs.append(df)
        if not dfs:
            return []
        df_merged = dfs[0]
        for df in dfs[1:]:
            df_merged = pd.merge(df_merged, df, on="date", how="outer")
        df_merged = df_merged.sort_values("date")
        # print("Returning records:", df_merged.to_dict(orient="records"))
        return df_merged.to_dict(orient="records")
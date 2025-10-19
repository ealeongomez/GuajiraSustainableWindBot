"""
Data Manager - Handles loading and caching of municipality data
"""

import pandas as pd
from typing import Dict, Optional
from pathlib import Path
from colorama import Fore, Style

from .config import DATA_DIR, MUNICIPALITIES


class DataManager:
    """Manages loading and caching of municipality data."""
    
    def __init__(self, verbose: bool = True):
        """
        Initialize DataManager.
        
        Args:
            verbose: Whether to print loading messages
        """
        self.data_cache: Dict[str, pd.DataFrame] = {}
        self.verbose = verbose
        self._load_all_data()
    
    def _load_all_data(self):
        """Preload all municipality data into cache."""
        if self.verbose:
            print(f"{Fore.YELLOW}📊 Cargando datos de municipios...{Style.RESET_ALL}")
        
        for municipality in MUNICIPALITIES:
            df = self.load_municipality_data(municipality)
            if df is not None:
                self.data_cache[municipality] = df
                if self.verbose:
                    print(f"{Fore.GREEN}  ✅ {municipality}: {len(df):,} registros{Style.RESET_ALL}")
            else:
                if self.verbose:
                    print(f"{Fore.RED}  ❌ {municipality}: No encontrado{Style.RESET_ALL}")
        
        if self.verbose:
            print()
    
    def load_municipality_data(self, municipality: str) -> Optional[pd.DataFrame]:
        """
        Load data for a specific municipality.
        
        Args:
            municipality: Name of the municipality
            
        Returns:
            DataFrame with municipality data or None if not found
        """
        if municipality in self.data_cache:
            return self.data_cache[municipality]
        
        try:
            csv_file = DATA_DIR / f"open_meteo_{municipality}.csv"
            if csv_file.exists():
                df = pd.read_csv(csv_file)
                df['datetime'] = pd.to_datetime(df['datetime'])
                return df
            else:
                return None
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}Error loading {municipality}: {e}{Style.RESET_ALL}")
            return None
    
    def get_data(self, municipality: str) -> Optional[pd.DataFrame]:
        """
        Get cached data for municipality.
        
        Args:
            municipality: Name of the municipality
            
        Returns:
            DataFrame or None
        """
        return self.data_cache.get(municipality)
    
    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Get all cached data.
        
        Returns:
            Dictionary mapping municipality names to DataFrames
        """
        return self.data_cache
    
    def get_statistics(self, municipality: str) -> Dict:
        """
        Get statistical summary for a municipality.
        
        Args:
            municipality: Name of the municipality
            
        Returns:
            Dictionary with statistics
        """
        df = self.get_data(municipality)
        if df is None:
            return {}
        
        return {
            "municipality": municipality,
            "records": len(df),
            "wind_speed_avg": round(df['wind_speed_10m'].mean(), 2),
            "wind_speed_max": round(df['wind_speed_10m'].max(), 2),
            "wind_speed_min": round(df['wind_speed_10m'].min(), 2),
            "temperature_avg": round(df['temperature_2m'].mean(), 2),
            "humidity_avg": round(df['relative_humidity_2m'].mean(), 2),
            "date_range": f"{df['datetime'].min()} a {df['datetime'].max()}"
        }


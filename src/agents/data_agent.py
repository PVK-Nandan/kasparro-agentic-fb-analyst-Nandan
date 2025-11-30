"""
Data Agent - Loads and summarizes Facebook Ads data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta


class DataAgent:
    """Loads CSV data and generates statistical summaries"""
    
    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.df = None
    
    def load_and_summarize(self) -> dict:
        """Load data and generate comprehensive summary"""
        
        # Load data
        data_path = Path(self.config['data_path'])
        self.logger.info("Loading data", path=str(data_path))
        
        self.df = pd.read_csv(data_path, sep='\t')
        
        # Parse dates
        self.df['date'] = pd.to_datetime(self.df['date'], format=self.config.get('date_format', '%d-%m-%Y'))
        
        # Handle missing values
        numeric_cols = ['spend', 'impressions', 'clicks', 'ctr', 'purchases', 'revenue', 'roas']
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        self.logger.info("Data loaded", rows=len(self.df), columns=len(self.df.columns))
        
        # Generate summary
        summary = {
            'overview': self._get_overview(),
            'performance_by_campaign': self._get_campaign_performance(),
            'performance_by_adset': self._get_adset_performance(),
            'creative_performance': self._get_creative_performance(),
            'time_series': self._get_time_series(),
            'low_performers': self._get_low_performers(),
            'top_performers': self._get_top_performers()
        }
        
        self.logger.info("Summary generated", summary_sections=len(summary))
        return summary
    
    def _get_overview(self) -> dict:
        """Overall dataset statistics"""
        return {
            'total_rows': int(len(self.df)),
            'date_range': {
                'start': self.df['date'].min().strftime('%Y-%m-%d'),
                'end': self.df['date'].max().strftime('%Y-%m-%d'),
                'days': int((self.df['date'].max() - self.df['date'].min()).days)
            },
            'total_spend': float(self.df['spend'].sum()),
            'total_revenue': float(self.df['revenue'].sum()),
            'total_purchases': int(self.df['purchases'].sum()),
            'overall_roas': float(self.df['revenue'].sum() / self.df['spend'].sum()) if self.df['spend'].sum() > 0 else 0,
            'avg_ctr': float(self.df['ctr'].mean()),
            'unique_campaigns': int(self.df['campaign_name'].nunique()),
            'unique_adsets': int(self.df['adset_name'].nunique())
        }
    
    def _get_campaign_performance(self) -> list:
        """Performance metrics by campaign"""
        campaigns = self.df.groupby('campaign_name').agg({
            'spend': 'sum',
            'revenue': 'sum',
            'purchases': 'sum',
            'impressions': 'sum',
            'clicks': 'sum',
            'ctr': 'mean'
        }).reset_index()
        
        campaigns['roas'] = campaigns['revenue'] / campaigns['spend']
        campaigns = campaigns.sort_values('spend', ascending=False).head(10)
        
        return campaigns.to_dict('records')
    
    def _get_adset_performance(self) -> list:
        """Performance metrics by adset"""
        adsets = self.df.groupby('adset_name').agg({
            'spend': 'sum',
            'revenue': 'sum',
            'purchases': 'sum',
            'ctr': 'mean',
            'roas': 'mean'
        }).reset_index()
        
        adsets = adsets.sort_values('spend', ascending=False).head(15)
        return adsets.to_dict('records')
    
    def _get_creative_performance(self) -> dict:
        """Performance by creative type and messages"""
        by_type = self.df.groupby('creative_type').agg({
            'spend': 'sum',
            'ctr': 'mean',
            'roas': 'mean',
            'revenue': 'sum'
        }).reset_index().to_dict('records')
        
        # Top performing messages
        top_messages = self.df.groupby('creative_message').agg({
            'ctr': 'mean',
            'roas': 'mean',
            'spend': 'sum'
        }).reset_index()
        top_messages = top_messages[top_messages['spend'] > 100]  # Filter low spend
        top_messages = top_messages.sort_values('ctr', ascending=False).head(10)
        
        return {
            'by_type': by_type,
            'top_messages': top_messages.to_dict('records')
        }
    
    def _get_time_series(self) -> dict:
        """Time-based performance trends"""
        daily = self.df.groupby('date').agg({
            'spend': 'sum',
            'revenue': 'sum',
            'ctr': 'mean',
            'purchases': 'sum'
        }).reset_index()
        
        daily['roas'] = daily['revenue'] / daily['spend']
        daily['date'] = daily['date'].dt.strftime('%Y-%m-%d')
        
        # Last 7 days vs previous 7 days
        max_date = self.df['date'].max()
        last_7 = self.df[self.df['date'] > max_date - timedelta(days=7)]
        prev_7 = self.df[(self.df['date'] <= max_date - timedelta(days=7)) & 
                         (self.df['date'] > max_date - timedelta(days=14))]
        
        last_7_roas = last_7['revenue'].sum() / last_7['spend'].sum() if last_7['spend'].sum() > 0 else 0
        prev_7_roas = prev_7['revenue'].sum() / prev_7['spend'].sum() if prev_7['spend'].sum() > 0 else 0
        
        return {
            'daily_metrics': daily.tail(30).to_dict('records'),
            'last_7_days': {
                'roas': float(last_7_roas),
                'ctr': float(last_7['ctr'].mean()),
                'spend': float(last_7['spend'].sum())
            },
            'prev_7_days': {
                'roas': float(prev_7_roas),
                'ctr': float(prev_7['ctr'].mean()),
                'spend': float(prev_7['spend'].sum())
            },
            'change': {
                'roas_change': float(last_7_roas - prev_7_roas),
                'roas_change_pct': float((last_7_roas - prev_7_roas) / prev_7_roas * 100) if prev_7_roas > 0 else 0
            }
        }
    
    def _get_low_performers(self) -> list:
        """Campaigns/adsets with low performance"""
        low_ctr_threshold = self.config.get('low_ctr_threshold', 0.015)
        
        low_ctr = self.df[self.df['ctr'] < low_ctr_threshold].groupby('campaign_name').agg({
            'ctr': 'mean',
            'spend': 'sum',
            'roas': 'mean',
            'creative_message': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
        }).reset_index()
        
        low_ctr = low_ctr[low_ctr['spend'] > self.config.get('min_spend_threshold', 50)]
        low_ctr = low_ctr.sort_values('spend', ascending=False).head(10)
        
        return low_ctr.to_dict('records')
    
    def _get_top_performers(self) -> list:
        """Best performing campaigns for learning"""
        top = self.df.groupby('campaign_name').agg({
            'ctr': 'mean',
            'roas': 'mean',
            'spend': 'sum',
            'creative_type': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
            'creative_message': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
        }).reset_index()
        
        top = top[top['spend'] > 200]  # Minimum spend filter
        top = top.sort_values(['ctr', 'roas'], ascending=False).head(10)
        
        return top.to_dict('records')
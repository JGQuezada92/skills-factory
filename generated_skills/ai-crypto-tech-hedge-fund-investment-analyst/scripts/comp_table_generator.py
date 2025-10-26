#!/usr/bin/env python3
"""
Comparable Company Analysis Table Generator

Generates formatted comparison tables for peer analysis in investment memos.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CompanyMetrics:
    """Data class for company financial metrics"""
    name: str
    ticker: Optional[str] = None
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    revenue: Optional[float] = None
    revenue_growth: Optional[float] = None
    ebitda: Optional[float] = None
    ebitda_margin: Optional[float] = None
    ev_revenue: Optional[float] = None
    ev_ebitda: Optional[float] = None
    ps_ratio: Optional[float] = None
    sector: Optional[str] = None


class CompTableGenerator:
    """Generate comparable company analysis tables"""
    
    def __init__(self):
        self.companies: List[CompanyMetrics] = []
    
    def add_company(self, company: CompanyMetrics):
        """Add company to comparison set"""
        self.companies.append(company)
    
    def add_company_dict(self, data: Dict[str, Any]):
        """Add company from dictionary"""
        company = CompanyMetrics(**data)
        self.companies.append(company)
    
    def calculate_multiples(self, company: CompanyMetrics) -> CompanyMetrics:
        """Calculate valuation multiples if not provided"""
        try:
            if company.enterprise_value and company.revenue and not company.ev_revenue:
                company.ev_revenue = company.enterprise_value / company.revenue
            
            if company.enterprise_value and company.ebitda and not company.ev_ebitda:
                company.ev_ebitda = company.enterprise_value / company.ebitda
            
            if company.market_cap and company.revenue and not company.ps_ratio:
                company.ps_ratio = company.market_cap / company.revenue
            
            if company.ebitda and company.revenue and not company.ebitda_margin:
                company.ebitda_margin = (company.ebitda / company.revenue) * 100
            
            return company
        except Exception as e:
            print(f"Error calculating multiples for {company.name}: {e}")
            return company
    
    def calculate_statistics(
        self, 
        metric_name: str
    ) -> Dict[str, Optional[float]]:
        """Calculate median, mean, min, max for a metric"""
        try:
            values = [
                getattr(company, metric_name)
                for company in self.companies
                if getattr(company, metric_name) is not None
            ]
            
            if not values:
                return {
                    'median': None,
                    'mean': None,
                    'min': None,
                    'max': None,
                    'count': 0
                }
            
            sorted_values = sorted(values)
            n = len(sorted_values)
            
            median = sorted_values[n // 2] if n % 2 else (sorted_values[n//2-1] + sorted_values[n//2]) / 2
            mean = sum(values) / len(values)
            
            return {
                'median': median,
                'mean': mean,
                'min': min(values),
                'max': max(values),
                'count': len(values)
            }
        except Exception as e:
            print(f"Error calculating statistics for {metric_name}: {e}")
            return {'median': None, 'mean': None, 'min': None, 'max': None, 'count': 0}
    
    def generate_table(
        self,
        target_company: Optional[CompanyMetrics] = None,
        sort_by: str = 'market_cap',
        include_stats: bool = True
    ) -> str:
        """
        Generate formatted comparison table
        
        Args:
            target_company: The company being analyzed (highlighted in table)
            sort_by: Metric to sort companies by
            include_stats: Whether to include median/mean rows
            
        Returns:
            Formatted table string
        """
        try:
            # Calculate multiples for all companies
            for i, company in enumerate(self.companies):
                self.companies[i] = self.calculate_multiples(company)
            
            # Add target company if provided
            if target_company:
                target_company = self.calculate_multiples(target_company)
            
            # Sort companies
            sorted_companies = sorted(
                self.companies,
                key=lambda x: getattr(x, sort_by) or 0,
                reverse=True
            )
            
            # Build table
            table = []
            table.append("=" * 120)
            table.append("COMPARABLE COMPANY ANALYSIS")
            table.append("=" * 120)
            
            # Header row
            header = (
                f"{'Company':<25} {'Ticker':<8} {'Market Cap':<12} {'Revenue':<12} "
                f"{'Growth':<8} {'EV/Rev':<8} {'EV/EBITDA':<10} {'Margin':<8}"
            )
            table.append(header)
            table.append("-" * 120)
            
            # Data rows
            for company in sorted_companies:
                row = self._format_company_row(company)
                table.append(row)
            
            # Target company row (if provided)
            if target_company:
                table.append("-" * 120)
                table.append("TARGET COMPANY")
                row = self._format_company_row(target_company)
                table.append(row)
            
            # Statistics rows
            if include_stats:
                table.append("-" * 120)
                table.append("PEER STATISTICS")
                
                stats_metrics = ['market_cap', 'revenue_growth', 'ev_revenue', 'ev_ebitda', 'ebitda_margin']
                stats_data = {metric: self.calculate_statistics(metric) for metric in stats_metrics}
                
                # Median row
                median_row = (
                    f"{'Median':<25} {'':<8} "
                    f"{self._format_number(stats_data['market_cap']['median']):<12} "
                    f"{'':<12} "
                    f"{self._format_percent(stats_data['revenue_growth']['median']):<8} "
                    f"{self._format_multiple(stats_data['ev_revenue']['median']):<8} "
                    f"{self._format_multiple(stats_data['ev_ebitda']['median']):<10} "
                    f"{self._format_percent(stats_data['ebitda_margin']['median']):<8}"
                )
                table.append(median_row)
                
                # Mean row
                mean_row = (
                    f"{'Mean':<25} {'':<8} "
                    f"{self._format_number(stats_data['market_cap']['mean']):<12} "
                    f"{'':<12} "
                    f"{self._format_percent(stats_data['revenue_growth']['mean']):<8} "
                    f"{self._format_multiple(stats_data['ev_revenue']['mean']):<8} "
                    f"{self._format_multiple(stats_data['ev_ebitda']['mean']):<10} "
                    f"{self._format_percent(stats_data['ebitda_margin']['mean']):<8}"
                )
                table.append(mean_row)
            
            table.append("=" * 120)
            
            return "\n".join(table)
            
        except Exception as e:
            print(f"Error generating table: {e}")
            return "Error generating comparison table"
    
    def _format_company_row(self, company: CompanyMetrics) -> str:
        """Format a single company row"""
        return (
            f"{company.name:<25} "
            f"{(company.ticker or 'N/A'):<8} "
            f"{self._format_number(company.market_cap):<12} "
            f"{self._format_number(company.revenue):<12} "
            f"{self._format_percent(company.revenue_growth):<8} "
            f"{self._format_multiple(company.ev_revenue):<8} "
            f"{self._format_multiple(company.ev_ebitda):<10} "
            f"{self._format_percent(company.ebitda_margin):<8}"
        )
    
    def _format_number(self, value: Optional[float]) -> str:
        """Format large numbers (in millions)"""
        if value is None:
            return "N/A"
        if value >= 1000:
            return f"${value/1000:.1f}B"
        return f"${value:.0f}M"
    
    def _format_percent(self, value: Optional[float]) -> str:
        """Format percentage values"""
        if value is None:
            return "N/A"
        return f"{value:.1f}%"
    
    def _format_multiple(self, value: Optional[float]) -> str:
        """Format valuation multiples"""
        if value is None:
            return "N/A"
        return f"{value:.1f}x"
    
    def export_to_dict(self) -> List[Dict[str, Any]]:
        """Export companies to list of dictionaries"""
        return [vars(company) for company in self.companies]


if __name__ == "__main__":
    # Example usage
    print("=== Comparable Company Analysis Example ===\n")
    
    # Create generator
    comp_gen = CompTableGenerator()
    
    # Add peer companies (example AI infrastructure companies)
    peers = [
        {
            'name': 'OpenAI',
            'market_cap': 80000,  # $M
            'revenue': 2000,
            'revenue_growth': 300,
            'ebitda': -500,
            'ebitda_margin': -25,
            'sector': 'AI Infrastructure'
        },
        {
            'name': 'Anthropic',
            'market_cap': 30000,
            'revenue': 800,
            'revenue_growth': 400,
            'ebitda': -300,
            'ebitda_margin': -37.5,
            'sector': 'AI Infrastructure'
        },
        {
            'name': 'Scale AI',
            'ticker': 'PRIVATE',
            'market_cap': 7000,
            'revenue': 750,
            'revenue_growth': 80,
            'ebitda': 75,
            'ebitda_margin': 10,
            'sector': 'AI Infrastructure'
        },
        {
            'name': 'Hugging Face',
            'market_cap': 4500,
            'revenue': 100,
            'revenue_growth': 250,
            'ebitda': -50,
            'ebitda_margin': -50,
            'sector': 'AI Infrastructure'
        }
    ]
    
    for peer in peers:
        comp_gen.add_company_dict(peer)
    
    # Target company
    target = CompanyMetrics(
        name='Target AI Company',
        market_cap=5000,
        revenue=500,
        revenue_growth=200,
        ebitda=-100,
        ebitda_margin=-20,
        sector='AI Infrastructure'
    )
    
    # Generate and print table
    table = comp_gen.generate_table(target_company=target, include_stats=True)
    print(table)


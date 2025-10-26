#!/usr/bin/env python3
"""
Valuation Calculator for Investment Analysis

Provides DCF analysis, multiples-based valuation, and scenario modeling
for technology company and crypto protocol valuations.
"""

import math
from typing import Dict, List, Tuple, Optional


class ValuationCalculator:
    """Calculate company valuations using multiple methodologies"""
    
    def __init__(self):
        self.wacc_default = 0.12  # 12% default WACC for tech companies
        self.terminal_growth_default = 0.025  # 2.5% terminal growth
    
    def dcf_valuation(
        self,
        fcf_projections: List[float],
        terminal_fcf: float,
        wacc: Optional[float] = None,
        terminal_growth: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Calculate DCF (Discounted Cash Flow) valuation
        
        Args:
            fcf_projections: List of projected free cash flows
            terminal_fcf: Terminal year free cash flow
            wacc: Weighted average cost of capital (default: 12%)
            terminal_growth: Perpetual growth rate (default: 2.5%)
            
        Returns:
            Dictionary with enterprise value, equity value per metrics
        """
        try:
            wacc = wacc or self.wacc_default
            terminal_growth = terminal_growth or self.terminal_growth_default
            
            # Present value of projected FCFs
            pv_fcf = sum(
                fcf / ((1 + wacc) ** (i + 1))
                for i, fcf in enumerate(fcf_projections)
            )
            
            # Terminal value
            terminal_value = terminal_fcf * (1 + terminal_growth) / (wacc - terminal_growth)
            pv_terminal = terminal_value / ((1 + wacc) ** len(fcf_projections))
            
            # Enterprise value
            enterprise_value = pv_fcf + pv_terminal
            
            return {
                'enterprise_value': enterprise_value,
                'pv_projected_fcf': pv_fcf,
                'pv_terminal_value': pv_terminal,
                'terminal_value': terminal_value,
                'wacc_used': wacc,
                'terminal_growth_used': terminal_growth
            }
            
        except Exception as e:
            print(f"Error in DCF calculation: {e}")
            return {}
    
    def multiples_valuation(
        self,
        company_metric: float,
        peer_multiples: List[float],
        metric_type: str = 'revenue'
    ) -> Dict[str, float]:
        """
        Calculate valuation using comparable company multiples
        
        Args:
            company_metric: Company's revenue, EBITDA, or other metric
            peer_multiples: List of peer company multiples (EV/Revenue, etc.)
            metric_type: Type of metric being valued
            
        Returns:
            Dictionary with valuation range based on multiples
        """
        try:
            if not peer_multiples:
                return {'error': 'No peer multiples provided'}
            
            median_multiple = sorted(peer_multiples)[len(peer_multiples) // 2]
            mean_multiple = sum(peer_multiples) / len(peer_multiples)
            min_multiple = min(peer_multiples)
            max_multiple = max(peer_multiples)
            
            return {
                'metric_type': metric_type,
                'company_metric': company_metric,
                'median_valuation': company_metric * median_multiple,
                'mean_valuation': company_metric * mean_multiple,
                'low_valuation': company_metric * min_multiple,
                'high_valuation': company_metric * max_multiple,
                'median_multiple': median_multiple,
                'mean_multiple': mean_multiple,
                'multiple_range': (min_multiple, max_multiple)
            }
            
        except Exception as e:
            print(f"Error in multiples valuation: {e}")
            return {}
    
    def crypto_protocol_valuation(
        self,
        annual_fees: float,
        token_supply: float,
        pf_ratio_comps: List[float]
    ) -> Dict[str, float]:
        """
        Calculate crypto protocol valuation using P/F ratios
        
        Args:
            annual_fees: Annualized protocol fees
            token_supply: Total or circulating token supply
            pf_ratio_comps: Comparable protocol P/F ratios
            
        Returns:
            Dictionary with protocol valuation and token price
        """
        try:
            median_pf = sorted(pf_ratio_comps)[len(pf_ratio_comps) // 2]
            mean_pf = sum(pf_ratio_comps) / len(pf_ratio_comps)
            
            market_cap_median = annual_fees * median_pf
            market_cap_mean = annual_fees * mean_pf
            
            token_price_median = market_cap_median / token_supply
            token_price_mean = market_cap_mean / token_supply
            
            return {
                'annual_fees': annual_fees,
                'token_supply': token_supply,
                'market_cap_median': market_cap_median,
                'market_cap_mean': market_cap_mean,
                'token_price_median': token_price_median,
                'token_price_mean': token_price_mean,
                'median_pf_ratio': median_pf,
                'mean_pf_ratio': mean_pf
            }
            
        except Exception as e:
            print(f"Error in crypto valuation: {e}")
            return {}
    
    def scenario_analysis(
        self,
        base_case_value: float,
        scenarios: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Calculate scenario-weighted valuation
        
        Args:
            base_case_value: Base case valuation
            scenarios: Dict with scenario names and {probability, value} dicts
            
        Returns:
            Probability-weighted valuation analysis
        """
        try:
            expected_value = 0
            total_probability = 0
            
            for scenario_name, scenario_data in scenarios.items():
                prob = scenario_data.get('probability', 0)
                value = scenario_data.get('value', base_case_value)
                expected_value += prob * value
                total_probability += prob
            
            # Normalize if probabilities don't sum to 1
            if total_probability > 0 and abs(total_probability - 1.0) > 0.01:
                expected_value = expected_value / total_probability
            
            return {
                'expected_value': expected_value,
                'base_case_value': base_case_value,
                'scenarios': scenarios,
                'total_probability': total_probability
            }
            
        except Exception as e:
            print(f"Error in scenario analysis: {e}")
            return {}
    
    def sensitivity_analysis(
        self,
        base_value: float,
        variable_name: str,
        variable_range: Tuple[float, float],
        steps: int = 5
    ) -> List[Dict[str, float]]:
        """
        Generate sensitivity table for key variable
        
        Args:
            base_value: Base case valuation
            variable_name: Name of variable being tested
            variable_range: (min, max) range for variable
            steps: Number of data points to generate
            
        Returns:
            List of dicts with variable value and implied valuation
        """
        try:
            results = []
            min_val, max_val = variable_range
            step_size = (max_val - min_val) / (steps - 1)
            
            for i in range(steps):
                var_value = min_val + (i * step_size)
                # Simplified: assume linear relationship
                value_change_pct = (var_value - min_val) / (max_val - min_val)
                implied_value = base_value * (0.5 + value_change_pct)
                
                results.append({
                    'variable': variable_name,
                    'variable_value': var_value,
                    'implied_valuation': implied_value,
                    'change_from_base_pct': (implied_value / base_value - 1) * 100
                })
            
            return results
            
        except Exception as e:
            print(f"Error in sensitivity analysis: {e}")
            return []


def calculate_saas_metrics(
    arr: float,
    nrr: float,
    growth_rate: float,
    burn_rate: float
) -> Dict[str, float]:
    """
    Calculate key SaaS efficiency metrics
    
    Args:
        arr: Annual Recurring Revenue
        nrr: Net Revenue Retention rate (as decimal, e.g. 1.15 for 115%)
        growth_rate: YoY growth rate (as decimal)
        burn_rate: Monthly cash burn
        
    Returns:
        Dictionary with Rule of 40, efficiency score, etc.
    """
    try:
        # Assume some margin based on growth stage
        ebitda_margin = max(-0.5, growth_rate - 0.6)  # Simplified assumption
        
        rule_of_40 = (growth_rate * 100) + (ebitda_margin * 100)
        
        magic_number = (arr * growth_rate) / (burn_rate * 12) if burn_rate > 0 else 0
        
        return {
            'arr': arr,
            'nrr': nrr,
            'growth_rate': growth_rate,
            'estimated_ebitda_margin': ebitda_margin,
            'rule_of_40_score': rule_of_40,
            'magic_number': magic_number,
            'efficiency_grade': 'A' if rule_of_40 > 40 else 'B' if rule_of_40 > 20 else 'C'
        }
        
    except Exception as e:
        print(f"Error calculating SaaS metrics: {e}")
        return {}


if __name__ == "__main__":
    # Example usage
    calc = ValuationCalculator()
    
    # Example DCF
    print("=== DCF Valuation Example ===")
    fcf_projections = [50, 75, 100, 125, 150]  # $M
    terminal_fcf = 175
    dcf_result = calc.dcf_valuation(fcf_projections, terminal_fcf)
    print(f"Enterprise Value: ${dcf_result.get('enterprise_value', 0):.1f}M")
    
    # Example Multiples
    print("\n=== Multiples Valuation Example ===")
    revenue = 200  # $M
    peer_multiples = [8.0, 10.0, 12.0, 15.0, 18.0]
    multiples_result = calc.multiples_valuation(revenue, peer_multiples, 'revenue')
    print(f"Median Valuation: ${multiples_result.get('median_valuation', 0):.1f}M")
    
    # Example SaaS Metrics
    print("\n=== SaaS Metrics Example ===")
    saas_metrics = calculate_saas_metrics(arr=100, nrr=1.20, growth_rate=1.0, burn_rate=5)
    print(f"Rule of 40 Score: {saas_metrics.get('rule_of_40_score', 0):.1f}")
    print(f"Efficiency Grade: {saas_metrics.get('efficiency_grade', 'N/A')}")


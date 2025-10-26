#!/usr/bin/env python3
"""
Risk Assessment and Matrix Generator

Provides structured risk analysis framework for investment evaluation.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskCategory(Enum):
    """Categories of investment risk"""
    TECHNOLOGY = "Technology"
    MARKET = "Market"
    FINANCIAL = "Financial"
    EXECUTION = "Execution"
    REGULATORY = "Regulatory/External"


class RiskProbability(Enum):
    """Probability levels for risks"""
    LOW = (1, "Low", "< 20% probability")
    MEDIUM = (2, "Medium", "20-50% probability")
    HIGH = (3, "High", "> 50% probability")
    
    def __init__(self, score, label, description):
        self.score = score
        self.label = label
        self.description = description


class RiskImpact(Enum):
    """Impact severity levels"""
    LOW = (1, "Low", "< 10% valuation impact")
    MEDIUM = (2, "Medium", "10-30% valuation impact")
    HIGH = (3, "High", "30-50% valuation impact")
    SEVERE = (4, "Severe", "> 50% valuation impact")
    
    def __init__(self, score, label, description):
        self.score = score
        self.label = label
        self.description = description


@dataclass
class Risk:
    """Individual risk item"""
    category: RiskCategory
    description: str
    probability: RiskProbability
    impact: RiskImpact
    mitigation: str = ""
    timeline: str = "Near-term (0-12 months)"
    
    @property
    def risk_score(self) -> int:
        """Calculate overall risk score (probability x impact)"""
        return self.probability.score * self.impact.score
    
    @property
    def severity_level(self) -> str:
        """Determine severity level based on score"""
        score = self.risk_score
        if score >= 9:
            return "CRITICAL"
        elif score >= 6:
            return "HIGH"
        elif score >= 4:
            return "MEDIUM"
        else:
            return "LOW"


class RiskMatrix:
    """Risk assessment matrix for investment analysis"""
    
    def __init__(self):
        self.risks: List[Risk] = []
    
    def add_risk(self, risk: Risk):
        """Add risk to the matrix"""
        self.risks.append(risk)
    
    def add_risk_from_params(
        self,
        category: str,
        description: str,
        probability: str,
        impact: str,
        mitigation: str = "",
        timeline: str = "Near-term (0-12 months)"
    ):
        """Add risk from string parameters"""
        try:
            cat = RiskCategory[category.upper().replace(" ", "_")]
            prob = RiskProbability[probability.upper()]
            imp = RiskImpact[impact.upper()]
            
            risk = Risk(
                category=cat,
                description=description,
                probability=prob,
                impact=imp,
                mitigation=mitigation,
                timeline=timeline
            )
            self.add_risk(risk)
        except KeyError as e:
            print(f"Invalid parameter: {e}")
    
    def get_risks_by_category(self, category: RiskCategory) -> List[Risk]:
        """Get all risks in a specific category"""
        return [r for r in self.risks if r.category == category]
    
    def get_critical_risks(self) -> List[Risk]:
        """Get all critical and high severity risks"""
        return [r for r in self.risks if r.severity_level in ["CRITICAL", "HIGH"]]
    
    def calculate_overall_risk_score(self) -> float:
        """Calculate weighted average risk score"""
        if not self.risks:
            return 0.0
        
        total_score = sum(r.risk_score for r in self.risks)
        return total_score / len(self.risks)
    
    def generate_risk_matrix_table(self) -> str:
        """Generate formatted risk matrix table"""
        table = []
        table.append("=" * 140)
        table.append("INVESTMENT RISK MATRIX")
        table.append("=" * 140)
        
        # Header
        header = (
            f"{'Category':<20} {'Risk Description':<40} {'Probability':<12} "
            f"{'Impact':<10} {'Score':<6} {'Severity':<10} {'Timeline':<20}"
        )
        table.append(header)
        table.append("-" * 140)
        
        # Sort by risk score (highest first)
        sorted_risks = sorted(self.risks, key=lambda r: r.risk_score, reverse=True)
        
        for risk in sorted_risks:
            row = (
                f"{risk.category.value:<20} "
                f"{risk.description[:40]:<40} "
                f"{risk.probability.label:<12} "
                f"{risk.impact.label:<10} "
                f"{risk.risk_score:<6} "
                f"{risk.severity_level:<10} "
                f"{risk.timeline:<20}"
            )
            table.append(row)
        
        table.append("=" * 140)
        table.append(f"Overall Risk Score: {self.calculate_overall_risk_score():.2f} / 12")
        table.append("=" * 140)
        
        return "\n".join(table)
    
    def generate_detailed_report(self) -> str:
        """Generate detailed risk assessment report"""
        report = []
        report.append("=" * 100)
        report.append("DETAILED RISK ASSESSMENT REPORT")
        report.append("=" * 100)
        report.append("")
        
        # Executive Summary
        critical_risks = self.get_critical_risks()
        report.append(f"Total Risks Identified: {len(self.risks)}")
        report.append(f"Critical/High Severity Risks: {len(critical_risks)}")
        report.append(f"Overall Risk Score: {self.calculate_overall_risk_score():.2f} / 12")
        report.append("")
        report.append("-" * 100)
        
        # Risks by category
        for category in RiskCategory:
            category_risks = self.get_risks_by_category(category)
            if category_risks:
                report.append("")
                report.append(f"{category.value.upper()} RISKS ({len(category_risks)})")
                report.append("-" * 100)
                
                for i, risk in enumerate(category_risks, 1):
                    report.append("")
                    report.append(f"{i}. {risk.description}")
                    report.append(f"   Probability: {risk.probability.label} ({risk.probability.description})")
                    report.append(f"   Impact: {risk.impact.label} ({risk.impact.description})")
                    report.append(f"   Risk Score: {risk.risk_score} | Severity: {risk.severity_level}")
                    report.append(f"   Timeline: {risk.timeline}")
                    if risk.mitigation:
                        report.append(f"   Mitigation: {risk.mitigation}")
        
        report.append("")
        report.append("=" * 100)
        
        return "\n".join(report)
    
    def generate_heat_map(self) -> str:
        """Generate risk heat map visualization"""
        # Create 4x3 grid (Impact x Probability)
        grid = [[[] for _ in range(3)] for _ in range(4)]
        
        for risk in self.risks:
            prob_idx = risk.probability.score - 1  # 0-2
            impact_idx = risk.impact.score - 1  # 0-3
            grid[impact_idx][prob_idx].append(risk.description[:20])
        
        heat_map = []
        heat_map.append("=" * 100)
        heat_map.append("RISK HEAT MAP")
        heat_map.append("=" * 100)
        heat_map.append("")
        heat_map.append("                 LOW               MEDIUM              HIGH")
        heat_map.append("            Probability        Probability        Probability")
        heat_map.append("-" * 100)
        
        impact_labels = ["SEVERE Impact  ", "HIGH Impact    ", "MEDIUM Impact  ", "LOW Impact     "]
        
        for i in range(3, -1, -1):  # Start from top (SEVERE)
            row_label = impact_labels[3-i]
            row = f"{row_label}|"
            
            for j in range(3):
                cell_risks = grid[i][j]
                if cell_risks:
                    cell_content = f" {len(cell_risks)} risks "
                else:
                    cell_content = "    -    "
                row += f"{cell_content:^30}|"
            
            heat_map.append(row)
            heat_map.append("-" * 100)
        
        heat_map.append("")
        heat_map.append("Legend: Number indicates count of risks in each probability-impact quadrant")
        heat_map.append("=" * 100)
        
        return "\n".join(heat_map)


def assess_portfolio_risk(
    position_size_pct: float,
    conviction_level: str,
    overall_risk_score: float,
    portfolio_var: float = 0.15
) -> Dict[str, any]:
    """
    Assess appropriate position sizing given risk profile
    
    Args:
        position_size_pct: Proposed position size as % of portfolio
        conviction_level: HIGH, MEDIUM, or LOW
        overall_risk_score: Risk score from RiskMatrix (0-12)
        portfolio_var: Portfolio-level value at risk
        
    Returns:
        Dictionary with position sizing recommendation
    """
    try:
        # Risk-adjusted position sizing
        conviction_multiplier = {
            'HIGH': 1.0,
            'MEDIUM': 0.7,
            'LOW': 0.4
        }.get(conviction_level.upper(), 0.5)
        
        # Risk penalty (higher risk = smaller position)
        risk_penalty = 1 - (overall_risk_score / 24)  # Normalize to 0-1
        
        recommended_size = position_size_pct * conviction_multiplier * risk_penalty
        recommended_size = min(recommended_size, 10)  # Cap at 10%
        recommended_size = max(recommended_size, 0.5)  # Floor at 0.5%
        
        return {
            'proposed_size_pct': position_size_pct,
            'conviction_level': conviction_level,
            'overall_risk_score': overall_risk_score,
            'recommended_size_pct': recommended_size,
            'recommendation': (
                f"Recommended position size: {recommended_size:.1f}% of portfolio "
                f"(adjusted from {position_size_pct:.1f}% based on conviction and risk)"
            )
        }
    except Exception as e:
        print(f"Error in position sizing: {e}")
        return {}


if __name__ == "__main__":
    # Example usage
    print("=== Risk Matrix Example ===\n")
    
    # Create risk matrix
    rm = RiskMatrix()
    
    # Add example risks
    rm.add_risk_from_params(
        category="TECHNOLOGY",
        description="AI model performance lags competitors",
        probability="MEDIUM",
        impact="HIGH",
        mitigation="Aggressive R&D investment, talent acquisition",
        timeline="Near-term (0-12 months)"
    )
    
    rm.add_risk_from_params(
        category="MARKET",
        description="TAM smaller than expected due to enterprise adoption barriers",
        probability="MEDIUM",
        impact="MEDIUM",
        mitigation="Focus on SMB market, adjust go-to-market",
        timeline="Medium-term (12-24 months)"
    )
    
    rm.add_risk_from_params(
        category="REGULATORY",
        description="New AI regulation increases compliance costs",
        probability="HIGH",
        impact="MEDIUM",
        mitigation="Proactive compliance, policy engagement",
        timeline="Long-term (24+ months)"
    )
    
    rm.add_risk_from_params(
        category="EXECUTION",
        description="Key technical founder departure",
        probability="LOW",
        impact="SEVERE",
        mitigation="Strong retention packages, succession planning",
        timeline="Near-term (0-12 months)"
    )
    
    # Generate outputs
    print(rm.generate_risk_matrix_table())
    print("\n\n")
    print(rm.generate_heat_map())
    
    # Position sizing
    print("\n\n=== Position Sizing Recommendation ===\n")
    sizing = assess_portfolio_risk(
        position_size_pct=5.0,
        conviction_level="HIGH",
        overall_risk_score=rm.calculate_overall_risk_score()
    )
    print(sizing['recommendation'])


---
name: ai-crypto-tech-hedge-fund-investment-analyst
description: This skill should be used when conducting institutional-grade investment analysis for AI, cryptocurrency, blockchain, and emerging technology companies. Generate hedge fund-style investment memos with comprehensive fundamental analysis, market opportunity assessment, competitive landscape evaluation, financial projections, and clear investment recommendations suitable for LP/investment committee presentation.
license: Complete terms in LICENSE.txt
---

# AI-Crypto-Tech Hedge Fund Investment Analyst

## Overview

This skill provides comprehensive investment analysis capabilities for technology-focused hedge fund analysis, specializing in AI, cryptocurrency, blockchain, and emerging technology sectors. Generate institutional-quality investment memos that synthesize complex technical concepts, market dynamics, and financial projections into actionable investment recommendations following the analytical rigor of top-tier funds like Coatue, Tiger Global, and a16z.

## When to Use This Skill

Use this skill when analyzing potential investments in:
- AI/ML companies (LLM developers, AI infrastructure, application layer)
- Cryptocurrency protocols and digital assets
- Blockchain infrastructure and DeFi projects
- Emerging technology companies with venture/growth stage funding
- Public or private technology companies requiring fundamental analysis

**Trigger phrases:**
- "Analyze this investment opportunity"
- "Create an investment memo for [company]"
- "Evaluate this as a hedge fund analyst"
- "What's the investment thesis for [company/protocol]?"
- "Perform fundamental analysis on..."

## How to Use This Skill

### Step 1: Provide Input Materials

Supply any combination of:
- Company pitch decks or investor presentations
- Financial statements (income statement, balance sheet, cash flow)
- Technical whitepapers or documentation
- Market research reports
- On-chain data or usage analytics (for crypto/blockchain)
- News articles and industry analysis
- Operating metrics dashboard

### Step 2: Specify Analysis Scope

Indicate desired focus areas:
- **Full Investment Memo**: Complete analysis with all sections
- **Quick Take**: Executive summary with key points only
- **Deep Dive**: Extensive analysis on specific aspect (technology, market, financials)
- **Comp Analysis**: Comparative valuation versus peers
- **Risk Assessment**: Focused analysis on downside scenarios

### Step 3: Execute Analysis

The skill will conduct comprehensive analysis across these dimensions:

**Company/Protocol Assessment:**
- Business model and revenue streams
- Technology stack and product differentiation
- Competitive positioning and market share
- Management team quality and execution track record

**Market Opportunity Analysis:**
- TAM/SAM/SOM sizing with bottoms-up methodology
- Growth drivers and market dynamics
- Industry trends and secular tailwinds
- Adoption curves and penetration rates

**Technology Evaluation:**
- Product architecture and technical moats
- Innovation potential and R&D pipeline
- Scalability and infrastructure requirements
- For AI: Model architecture, data advantages, compute economics
- For Crypto: Protocol design, tokenomics, network effects

**Financial Analysis:**
- Unit economics and profitability path
- Revenue model and pricing power
- Margin profile and operating leverage
- Cash burn analysis and runway
- Valuation methodology (DCF, comps, precedent transactions)

**Risk Framework:**
- Technology risks (obsolescence, competitive threats)
- Market risks (demand shifts, competitive dynamics)
- Execution risks (team, operations, capital requirements)
- Regulatory risks (compliance, policy changes)
- Scenario analysis and sensitivity testing

### Step 4: Generate Investment Memo

Output will be formatted as a professional hedge fund investment memo with:

**Header:**
- Company name and ticker (if public)
- Investment recommendation (Strong Buy / Buy / Hold / Sell / Strong Sell)
- Price target and upside/downside potential
- Conviction level and suggested position size
- Date and analyst name

**Executive Summary (3-5 key points):**
- Investment thesis in 2-3 sentences
- Key catalysts for value creation
- Primary risks and mitigants
- Valuation summary

**Main Body:**
1. **Company Overview** - Business description, products, market position
2. **Market Opportunity** - TAM/SAM/SOM, growth drivers, competitive landscape
3. **Investment Thesis** - Why now? Why this company? What differentiates them?
4. **Financial Analysis** - Historical performance, projections, unit economics
5. **Valuation** - Methodology, peer comps, price targets (base/bull/bear cases)
6. **Technology Assessment** - Product differentiation, technical moats (AI/crypto specific)
7. **Competitive Analysis** - Key competitors, market positioning, competitive advantages
8. **Management & Team** - Founder backgrounds, execution track record
9. **Risks** - Key risks with probability and impact assessment
10. **Catalysts** - Near-term and long-term value drivers with timeline
11. **Recommendation** - Investment decision with position sizing guidance

**Appendices:**
- Key metrics dashboard
- Comp table with peer valuations
- Sensitivity analysis
- Data sources and assumptions

### Step 5: Export to Professional Formats

Once the investment memo is complete, export it to PDF and Microsoft Word for distribution:

**Automatic Export:**
```python
# The skill will automatically execute the export script
scripts/memo_exporter.py

# Exports to: C:/Users/Jonathan Quezada/.../Claude Skills/skills artifacts/
```

**Output Files Created:**
- ✅ **Markdown** (.md) - Source version for editing
- ✅ **PDF** (.pdf) - Professional print-ready document
- ✅ **Microsoft Word** (.docx) - Editable version for team collaboration

**File Naming:**
- Format: `[Company_Name]_Investment_Memo_[Timestamp].[ext]`
- Example: `Worldcoin_Investment_Memo_20251025_143022.pdf`

**Distribution-Ready Features:**
- **Presentation-quality design** with teal gradient headers and modern styling
- **Arial font throughout** (11pt body, scaled headers)
- **Professional color scheme** - Teal (#2c9e91) accents with clean white background
- **Executive summary boxes** with subtle gradients and shadows
- **Styled tables** with teal headers and alternating row colors
- **Custom bullet points** with teal triangular markers
- **Proper page margins** (0.75in-1in for optimal printing)
- **Hover effects and visual hierarchy** for digital viewing
- **Print-optimized** with page breaks at logical sections

**Manual Export (if libraries unavailable):**
If Python export libraries are not installed, the skill provides instructions for:
- Installing required libraries (`pip install python-docx markdown2 weasyprint`)
- Manual conversion using online tools
- Print-to-PDF from browser

**To request export:**
- "Export this memo to PDF and Word"
- "Generate distribution-ready documents"
- "Save this analysis to the skills artifacts folder"

### Step 6: Review and Refine

Iterate on analysis by requesting:
- "Dig deeper into [specific aspect]"
- "Challenge this assumption: [assumption]"
- "What's the bear case for [element]?"
- "Add sensitivity analysis for [variable]"
- "Compare valuation to [specific peer]"
- "Re-export with updated analysis"

## Sector-Specific Analysis Frameworks

### AI/ML Investment Analysis

**Model & Technology Assessment:**
- Model architecture (transformer-based, diffusion, hybrid)
- Training approach (supervised, unsupervised, RLHF)
- Data moats and proprietary datasets
- Compute requirements and scaling laws
- Inference optimization and cost structure

**AI Market Positioning:**
- Infrastructure layer (compute, training, deployment)
- Model layer (foundation models, fine-tuned models)
- Application layer (vertical SaaS, horizontal tools)
- Differentiation: proprietary data, domain expertise, distribution

**AI-Specific Metrics:**
- Model performance benchmarks
- Token costs and pricing
- API adoption and usage metrics
- Customer retention and expansion
- Developer ecosystem engagement

### Crypto/Blockchain Investment Analysis

**Protocol Assessment:**
- Consensus mechanism and security model
- Tokenomics and value accrual mechanisms
- Decentralization metrics (validators, token distribution)
- Governance structure and upgrade process

**On-Chain Analysis:**
- Active addresses and wallet growth
- Transaction volume and fees
- TVL (Total Value Locked) trends
- Staking rates and validator economics
- Token velocity and holding patterns

**Network Effects Evaluation:**
- Developer activity and ecosystem growth
- Liquidity depth and DEX integration
- Cross-chain bridge adoption
- Protocol integrations and composability

**Crypto-Specific Metrics:**
- Market cap and fully diluted valuation
- Circulating supply vs total supply
- Inflation schedule and emissions
- Staking yield and real yield
- Price-to-sales ratio (fees)

## Writing Style and Formatting

**Tone and Language:**
- Direct and high-conviction
- Data-driven with specific metrics
- Forward-looking with clear "what happens next" thesis
- Balanced presentation of bull and bear cases
- Professional and suitable for institutional presentation

**Data Presentation:**
- Always cite sources for key statistics
- Use specific numbers, not vague descriptors ("grew 40% YoY" not "grew significantly")
- Present projections with methodology and assumptions
- Include sensitivity analysis for key variables
- Flag high-uncertainty estimates explicitly

**Formatting Standards:**
- Clear section headers with consistent hierarchy
- Bullet points for lists and key takeaways
- Tables for financial data and comp analysis
- Highlight key metrics and takeaways
- Executive summary that stands alone

## Key Valuation Methodologies

**Technology Company Valuation:**
- **Revenue Multiples**: EV/Revenue, P/S ratios benchmarked to peers
- **DCF Analysis**: Discounted cash flow with terminal value
- **Comparable Companies**: Public company trading multiples
- **Precedent Transactions**: M&A multiples for similar deals
- **Rule of 40**: Growth rate + profit margin for SaaS
- **Cohort Analysis**: Customer lifetime value modeling

**Crypto Protocol Valuation:**
- **P/F Ratio**: Price to Fees (market cap / annualized protocol fees)
- **P/S Ratio**: Price to Sales (token value relative to revenue)
- **TVL Multiple**: Market cap / Total Value Locked
- **NVT Ratio**: Network Value to Transactions
- **Discounted Cash Flow**: Protocol fee projections
- **Metcalfe's Law**: Network value proportional to users squared

## Risk Assessment Framework

Evaluate risks across five dimensions:

**1. Technology Risk:**
- Product-market fit uncertainty
- Technical execution challenges
- Obsolescence from competitive innovation
- Scalability and performance limitations

**2. Market Risk:**
- Total addressable market smaller than expected
- Competitive dynamics intensify
- Customer adoption slower than projected
- Market timing (too early or too late)

**3. Financial Risk:**
- Revenue ramp slower than modeled
- Unit economics deteriorate
- Capital intensity higher than expected
- Valuation multiple compression

**4. Execution Risk:**
- Management team capability gaps
- Operational challenges at scale
- Key person dependencies
- Go-to-market strategy fails

**5. Regulatory/External Risk:**
- Regulatory changes adverse to business
- Compliance costs escalate
- Geopolitical impacts
- Macro economic headwinds

**Risk Mitigation Strategies:**
- Diversification across portfolio
- Position sizing based on conviction and risk
- Hedging strategies where applicable
- Regular monitoring of key risk indicators

## Investment Recommendation Framework

**Recommendation Levels:**

- **Strong Buy**: High conviction, 5-10% portfolio position
  - Criteria: Clear competitive moat, strong unit economics, 3x+ upside, manageable downside
  
- **Buy**: Positive view, 2-5% position
  - Criteria: Solid fundamentals, 2x+ upside, reasonable risk/reward
  
- **Hold**: Neutral, maintain if owned, don't initiate
  - Criteria: Fair valuation, balanced risk/reward, waiting for catalyst
  
- **Sell**: Negative view, exit or avoid
  - Criteria: Overvalued, deteriorating fundamentals, better alternatives
  
- **Strong Sell**: High conviction short, hedge or avoid
  - Criteria: Structural challenges, significant downside, flawed business model

**Position Sizing Guidance:**
- Consider conviction level, liquidity, portfolio diversification
- Scale into positions with defined entry points
- Set stop-losses for risk management
- Monitor position regularly with predefined review triggers

## Reference Materials

**Use these resources for deep-dive analysis:**

`references/valuation_frameworks.md` - Detailed valuation methodologies by sector
`references/ai_analysis_guide.md` - AI-specific analysis frameworks and metrics
`references/crypto_analysis_guide.md` - Blockchain and crypto evaluation frameworks
`references/financial_modeling.md` - Financial projection templates and methodologies

**Execute analysis with scripts:**

`scripts/valuation_calculator.py` - DCF, multiples, and scenario analysis
`scripts/comp_table_generator.py` - Automated comparable company analysis
`scripts/risk_matrix.py` - Risk scoring and probability-impact assessment
`scripts/memo_exporter.py` - Export memos to PDF, Word, and Markdown formats

## Keywords

hedge fund, investment analysis, technology investing, AI investing, cryptocurrency, blockchain, DeFi, venture capital, growth equity, fundamental analysis, investment memo, due diligence, valuation, financial modeling, market opportunity, competitive analysis, risk assessment, investment thesis, portfolio management, institutional investing, private equity, public markets, DCF, comparable companies, precedent transactions, SaaS metrics, unit economics, tokenomics, on-chain analysis, TAM SAM SOM, catalysts, price target, investment recommendation, bull case, bear case, PDF export, Word document, Microsoft Word, document formatting, professional memo, distribution ready, print ready


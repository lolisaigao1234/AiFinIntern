# Reporting Engine Component

## Purpose
Generate performance reports, tax documents, and analytics dashboards.

## Responsibilities
- Daily P&L calculation and reporting
- Performance metrics (Sharpe, Sortino, drawdown)
- Tax liability reports and IRS forms
- Portfolio analytics and attribution
- Interactive dashboards

## Sub-Components

### pnl/
P&L calculation engine for realized and unrealized gains/losses.

### performance/
Performance metrics calculator with risk-adjusted returns.

### tax_reports/
Tax report generation (Form 8949, Schedule D, trade history).

### dashboards/
Interactive dashboards using Plotly Dash for real-time monitoring.

## Key Interfaces
- `IPnLCalculator`: P&L calculation interface
- `IPerformanceMetrics`: Performance metrics interface
- `ITaxReportGenerator`: Tax report generation interface

## Dependencies
- pandas: Data manipulation
- plotly: Interactive visualizations
- jinja2: Report templating
- openpyxl: Excel report generation

## Configuration
See `config/reporting_config.yaml` for report parameters.

## Testing
Unit tests located in `tests/unit/reporting/`
Report generation validation in `tests/integration/reporting/`

# Tax & Reconciliation Engine Component

## Purpose
Calculate tax liabilities, detect wash sales, and reconcile with broker statements.

## Responsibilities
- Wash-sale detection per IRS rules
- Capital gains/losses calculation
- Tax lot tracking (FIFO, LIFO, specific identification)
- Broker statement reconciliation
- IRS form generation (8949, Schedule D)

## Sub-Components

### tax_lots/
Tax lot management with FIFO, LIFO, and specific identification methods.

### wash_sale/
Wash sale detection engine implementing IRS Publication 550 rules.

### capital_gains/
Capital gains and losses calculator for short-term and long-term gains.

### reconciliation/
Broker statement parser and reconciliation engine.

## Key Interfaces
- `ITaxLotManager`: Tax lot tracking interface
- `IWashSaleDetector`: Wash sale detection interface
- `ICapitalGainsCalculator`: Capital gains calculation interface

## Dependencies
- pandas: Data manipulation
- decimal: Precise financial calculations
- pydantic: Data validation

## Configuration
See `config/tax_config.yaml` for tax calculation parameters.

## Testing
Unit tests located in `tests/unit/tax_recon/`
Tax calculation validation in `tests/integration/tax_recon/`

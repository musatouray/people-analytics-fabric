# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Microsoft Fabric Data Engineering & Analytics Development Lab** - a monorepo containing multiple data warehousing, semantic modeling, and business intelligence projects using the Fabric ecosystem.

**Key Technologies:** Power BI (PBIP format), TMDL, DAX, PySpark Notebooks, T-SQL, Azure Key Vault, OneLake

## Repository Structure

```
fabric_artifacts/
├── SQL Customer RFM Analytics/    # Customer segmentation dashboard (see subfolder CLAUDE.md)
│   ├── *.pbip, *.Report/          # Power BI report artifacts
│   ├── *.SemanticModel/           # TMDL semantic model definitions
│   ├── *.Warehouse/               # SQL warehouse schemas
│   ├── *.CopyJob/                 # Fabric data copy jobs
│   └── functions.tmdl             # Reusable DAX SVG library
├── people analytics/              # HR attrition analysis pipeline
│   ├── *.Notebook/                # PySpark data ingestion notebooks
│   ├── *.Lakehouse/               # OneLake storage definitions
│   └── *.Warehouse/               # SQL warehouse schemas
├── plotly/                        # Taxi/transport analytics
│   ├── *.SemanticModel/           # Semantic model for trip data
│   └── *.Warehouse/               # SQL warehouse schemas
└── vl_fabricdevlab.VariableLibrary/  # Centralized secrets/config
```

## Development Workflow

No traditional CLI build/test commands - all artifacts are developed in:
- **Power BI Desktop** or **Fabric web workspace** for reports and semantic models
- **Fabric Spark clusters** for notebook execution
- **Fabric SQL endpoint** for warehouse queries

Artifacts are stored as JSON/TMDL files for GitOps-style version control.

## Project-Specific Guidance

### SQL Customer RFM Analytics

See `fabric_artifacts/SQL Customer RFM Analytics/CLAUDE.md` for detailed guidance on:
- DAX SVG KPI card generation patterns
- Semantic model structure (star schema with FactCustomerRFM)
- Color conventions and URL-encoded hex values
- Power BI Skills Library locations

### People Analytics Pipeline

**Data Flow:** Kaggle CSV → Bronze Delta Table → Warehouse → BI

**Key Notebooks:**
- `download Kaggle dataset.Notebook` - Downloads data using Key Vault credentials
- `01_bronze_ingest.Notebook` - CSV ingestion with snake_case normalization

**Variable Library Pattern:**
```python
from notebookutils import credentials, variableLibrary
vl = variableLibrary.getLibrary("vl_fabricdevlab")
secret = credentials.getSecret(vl.VL_KV_URL, vl.VL_KV_KAGGLE_API_KEY)
```

### Plotly Analytics

Semantic model for taxi/medallion data with tables: Date, Time, Geography, HackneyLicense, Medallion, Trip, Weather.

## File Format Reference

| Extension | Description |
|-----------|-------------|
| `.pbip` | Power BI project manifest (JSON) |
| `.Report/` | Report definition folder (pages, visuals, theme) |
| `.SemanticModel/` | TMDL semantic model (tables, relationships, measures) |
| `.Warehouse/` | SQL schema definitions (.sqlproj + table/view scripts) |
| `.Notebook/` | PySpark/Python notebooks with Fabric metadata |
| `.Lakehouse/` | OneLake lakehouse configuration |
| `.CopyJob/` | Fabric data copy job definitions |
| `.VariableLibrary/` | Environment variables and secret references |

## Naming Conventions

- **Dimensions:** `Dim*` (DimCustomer, DimDate, DimGeography)
- **Facts:** `Fact*` (FactCustomerRFM, FactInternetSales)
- **Measures:** PascalCase with intent (RFM Avg Recency, Total Revenue)
- **DAX Variables:** Leading underscore `_varName`
- **Python Columns:** snake_case after normalization

## Architecture Patterns

**DirectLake Mode:** Semantic models connect directly to OneLake Delta tables for optimal performance.

**Medallion Architecture:** Bronze (raw ingestion) → Silver (cleaned) → Gold (aggregated) for data pipelines.

**SVG Data-URI Images:** DAX generates inline SVG for KPI cards with sparklines; URL-encode `#` as `%23`.

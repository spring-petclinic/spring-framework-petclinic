# AECF Skill — Document Context Ingestion (Quick Ops)

LAST_REVIEW: 2026-02-25

Guía operativa corta para ejecutar `aecf_document_context_ingestion` y producir un contexto documental reutilizable.

## Objetivo

Consolidar contexto del proyecto desde PDF/MD/URLs/rutas externas, en modo **read-only**, para alimentar skills posteriores.

## Comando mínimo

```text
@aecf run skill=document_context_ingestion topic=doc_context prompt="Ingerir documentación del proyecto y normalizar contexto"
```

## Ejemplos listos para copiar

### 1) Documentación interna del repo

```text
@aecf run skill=document_context_ingestion topic=onboarding_context prompt="Analiza documentation/, README y CHANGELOG para extraer objetivos, restricciones y decisiones"
```

### 2) PDF + Markdown externos

```text
@aecf run skill=document_context_ingestion topic=external_context prompt="Ingiere contexto desde C:/contratos/arquitectura.pdf y C:/docs/operacion.md; marca conflictos y confianza"
```

### 3) URLs de referencia

```text
@aecf run skill=document_context_ingestion topic=compliance_context prompt="Usa https://example.com/policy y https://example.com/spec para extraer reglas de cumplimiento aplicables al proyecto"
```

## Salida esperada

- Archivo: `documentation/<TOPIC>/AECF_<NN>_DOCUMENT_CONTEXT_INGESTION.md`
- Contenido mínimo:
  - inventario de fuentes
  - restricciones y supuestos extraídos
  - modelo de contexto normalizado
  - análisis de conflictos/confianza
  - matriz de handoff a skills downstream

## Flujo recomendado

```text
aecf_document_context_ingestion
  → aecf_project_context_generator
  → aecf_maturity_assessment
  → aecf_code_standards_audit
```

## Reglas operativas

- No modifica código ni documentos fuente.
- Cada afirmación crítica debe tener referencia de fuente.
- Si hay conflicto documental, debe quedar como `OPEN_QUESTION`.

## Taxonomy Classification

This skill is classified as: TIER2  
Deterministic pipeline required: false

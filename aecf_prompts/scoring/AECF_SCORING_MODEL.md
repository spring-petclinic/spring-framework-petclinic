# AECF — SCORING MODEL

LAST_REVIEW: 2026-02-24

## 1. Puntuación base

Cada checklist item tendrá:

- **0** = NO CUMPLE
- **1** = CUMPLE PARCIALMENTE
- **2** = CUMPLE COMPLETAMENTE

## 2. Pesos por categoría

Asignación de pesos por bloque funcional:

| Categoría | Peso |
|-----------|------|
| Scope Validation | 2 |
| Security Controls | 3 |
| Resource Management | 2 |
| Dependency Outage Resilience | 3 |
| Logging & Observability | 2 |
| Compliance with Previous Phase | 3 |
| Production Readiness | 2 |
| Decision Integrity | 3 |
| Secciones adicionales específicas | 2 |

## 3. Cálculo del Score

### Fórmula

```
Score = Σ (valor_item × peso_categoria)
```

### Normalización

```
Score_Final = (Score_obtenido / Score_máximo_posible) × 100
```

**Score Máximo** = 100 (normalizado)

## 4. Clasificación de Madurez

| Rango | Nivel |
|-------|-------|
| 90-100 | ENTERPRISE READY |
| 75-89 | PRODUCTION READY |
| 60-74 | CONDITIONAL |
| 40-59 | HIGH RISK |
| 0-39 | FAIL |

## 5. Reglas de Veredicto

1. Si existe **cualquier hallazgo CRÍTICO** → **NO-GO automático**
2. Si **Score < 60** → **NO-GO**
3. Si **Score entre 60 y 74** → **GO CONDICIONAL**
4. Si **Score >= 75** → **GO**
5. Si **Score >= 90** → **GO ENTERPRISE**

### Precedencia

La presencia de hallazgos CRÍTICOS **invalida** cualquier score y resulta en **NO-GO automático**.

## 6. Enforcement

Este modelo de scoring es **OBLIGATORIO** para todas las fases AECF.

Cualquier fase que no incluya scoring completo es **INVÁLIDA**.

## 7. Dependency Outage Resilience (Rubric)

Esta categoría evalúa la capacidad del código para degradar de forma segura ante caídas de BBDD, red, cache (Redis) o APIs externas.

### Escala por item

- **0** = No existe control o el comportamiento agrava la caída (retry infinito, timeout ausente, error engañoso)
- **1** = Control parcial (timeouts/retries definidos pero incompletos o inconsistentes)
- **2** = Control completo y consistente (prevención + contención + señalización correcta)

### Criterios mínimos esperados

- Timeouts explícitos en llamadas externas
- Retries acotados con backoff + jitter (o no-retry justificado)
- Circuit breaker/fail-fast o mecanismo equivalente ante fallo persistente
- Mensajes de error técnicos y de usuario no engañosos sobre la causa transitoria
- Límite de concurrencia/rate limiting para evitar retry storms

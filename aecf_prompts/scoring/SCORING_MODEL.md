# AECF Prompts — Modelo de Scoring

LAST_REVIEW: 2026-04-17

---

> Versión simplificada del AECF Scoring Model. El consultor rellena/ajusta los pesos y umbrales durante la implantación.

---

## 1. Escala de puntuación por ítem

| Valor | Significado |
|---|---|
| **0** | NO CUMPLE — No abordado o completamente incorrecto |
| **1** | CUMPLE PARCIALMENTE — Presente pero con lagunas |
| **2** | CUMPLE COMPLETAMENTE — Implementado correctamente |

---

## 2. Categorías y pesos

| Categoría | Peso | Aplica a |
|---|---|---|
| **Scope Validation** | 2 | Todas las fases |
| **Security Controls** | 3 | Todas las fases |
| **Resource Management** | 2 | IMPLEMENT, AUDIT_CODE |
| **Dependency Outage Resilience** | 3 | IMPLEMENT, AUDIT_CODE cuando hay dependencias externas |
| **Logging & Observability** | 2 | IMPLEMENT, AUDIT_CODE |
| **Compliance with Previous Phase** | 3 | Todas (excepto PLAN) |
| **Production Readiness** | 2 | IMPLEMENT, AUDIT_CODE |
| **Decision Integrity** | 3 | PLAN, AUDIT_PLAN, IMPLEMENT, AUDIT_CODE |
| **Plan Clarity** | 2 | PLAN, AUDIT_PLAN |
| **Code Audit Integrity** | 2 | AUDIT_CODE |
| **Testing Evidence** | 3 | AUDIT_CODE |
| **Anti-patterns** | 3 | IMPLEMENT, AUDIT_CODE |

> La checklist de cada fase sigue siendo la fuente autoritativa para las categorías exactas que se puntúan. Si una categoría aplicable al entorno, como `Dependency Outage Resilience`, se marca como `N/A`, debe excluirse del máximo ponderado final en lugar de computarse como cero.

---

## 3. Cálculo del Score

```
Score = Σ (valor_item × peso_categoria) / Σ (máximo_item × peso_categoria) × 100
```

### Ejemplo paso a paso

| Categoría | Peso | Items | Score items | Score × Peso | Max × Peso |
|---|---|---|---|---|---|
| Scope Validation | 2 | 3 items | 5/6 | 10 | 12 |
| Security Controls | 3 | 4 items | 6/8 | 18 | 24 |
| Decision Integrity | 3 | 2 items | 3/4 | 9 | 12 |
| Plan Clarity | 2 | 3 items | 5/6 | 10 | 12 |
| **Total** | | | | **47** | **60** |

```
Score = 47/60 × 100 = 78.3%
```

---

## 4. Niveles de madurez

| Rango | Nivel | Significado |
|---|---|---|
| 90-100 | **ENTERPRISE READY** | Excelencia, listo para auditoría externa |
| 75-89 | **PRODUCTION READY** | Maduro, listo para producción |
| 60-74 | **CONDITIONAL** | Aceptable con condiciones |
| 40-59 | **HIGH RISK** | Alto riesgo, intervención requerida |
| 0-39 | **FAIL** | No apto para producción |

---

## 5. Umbrales de veredicto

| Tipo de skill | Umbral GO | Umbral ENTERPRISE |
|---|---|---|
| **new_feature** | ≥ 75 | ≥ 90 |
| **refactor** | ≥ 75 | ≥ 90 |
| **hotfix** | ≥ 70 | ≥ 85 |
| **security_review** | ≥ 90 | ≥ 95 |

> ⚠️ Estos umbrales son personalizables. El consultor los ajusta según la tolerancia al riesgo del cliente en el `AECF_PROJECT_CONTEXT.md`.

---

## 6. Reglas de veredicto (orden de precedencia)

1. **Cualquier hallazgo CRITICAL** → **NO-GO automático** (independiente del score)
2. **Sin evidencia de tests ejecutados** (en AUDIT_CODE) → **NO-GO automático**
3. **Score < umbral del skill** → **NO-GO**
4. **Score ≥ umbral sin CRITICAL** → **GO**
5. **Score ≥ umbral enterprise** → **GO ENTERPRISE**
6. **No determinable** → **UNKNOWN** (bloquea como NO-GO)

---

## 7. Scoring simplificado para skills TIER 1

Para skills de fase única (code_standards_audit, security_review, explain_behavior, executive_summary), no se aplica scoring con veredicto GO/NO-GO. En su lugar, se usa la **Severity Matrix** del output:

- Si hay hallazgos CRITICAL → acción inmediata requerida
- Si hay hallazgos HIGH → acción a corto plazo
- Si solo MEDIUM/LOW/INFO → mejora continua

---

## 8. Tabla rápida de scoring por fase

| Fase | Scoring completo | Veredicto GO/NO-GO | Categorías evaluadas |
|---|---|---|---|
| PLAN | Sí | No (pero se valida completitud) | Scope, Security, Decision, Clarity |
| AUDIT_PLAN | Sí | **Sí** | Scope, Security, Decision, Clarity, Compliance |
| FIX_PLAN | No | No (va directo a re-audit) | — |
| TEST_STRATEGY | Sí | No | Scope, Security, Compliance |
| IMPLEMENT | Sí | No (pero se valida completitud) | Todas |
| AUDIT_CODE | Sí | **Sí** | Scope, Security, Resource, Dependency Outage Resilience, Logging, Compliance, Production, Decision, Code Audit Integrity, Testing Evidence, Anti-patterns |
| FIX_CODE | No | No (va directo a re-audit) | — |
| VERSION | No | No | — |

---

## 9. Hoja de cálculo rápida

```
PASO 1: Completar el checklist de la fase (checklists/)
PASO 2: Puntuar cada ítem (0, 1 o 2)
PASO 3: Sumar puntos por categoría
PASO 4: Multiplicar suma × peso
PASO 5: Sumar todos los ponderados
PASO 6: Dividir entre máximo total × 100
PASO 7: Verificar reglas de precedencia (CRITICAL → NO-GO)
PASO 8: Determinar nivel de madurez
PASO 9: Emitir veredicto
```

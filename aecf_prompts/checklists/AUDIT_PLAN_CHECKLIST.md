# AECF Prompts — AUDIT_PLAN CHECKLIST

LAST_REVIEW: 2026-03-09

---

> Checklist simplificado para la fase AUDIT_PLAN. Evaluar cada ítem con 0 / 1 / 2 según `scoring/SCORING_MODEL.md`.
> Esta fase tiene **gate GO/NO-GO**: el veredicto determina si el plan avanza.

---

## 1. Scope Validation (Peso: 2)

- [ ] El alcance del plan coincide con lo solicitado
- [ ] No hay expansión de scope respecto al objetivo original
- [ ] No hay rediseño implícito no justificado

## 2. Security Controls (Peso: 3)

- [ ] No se exponen datos sensibles en el plan
- [ ] El control de acceso está correctamente planificado
- [ ] La mitigación de enumeración está considerada
- [ ] El logging cubre eventos de seguridad

## 3. Compliance with Previous Phase (Peso: 3)

- [ ] El plan es resultado de una fase PLAN completada
- [ ] Los requisitos del plan están completos
- [ ] No hay violación de secuencia de fases

## 4. Decision Integrity (Peso: 3)

- [ ] No hay decisiones no autorizadas
- [ ] Todas las decisiones son trazables al objetivo original
- [ ] Las dependencias identificadas son correctas

## 5. Audit Integrity (Peso: 2)

- [ ] Los riesgos están identificados
- [ ] Las ambigüedades están señaladas
- [ ] El veredicto está justificado con evidencia

## 6. Production Readiness (Peso: 2)

- [ ] Los casos borde están considerados
- [ ] El manejo de errores está planificado
- [ ] No hay fallos silenciosos previsibles
- [ ] No hay efectos secundarios ocultos

---

## SCORING TABLE

| Categoría | Peso | Ítems | Puntuación (0-2 cada uno) | Total |
|---|---|---|---|---|
| Scope Validation | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Security Controls | 3 | 4 | _ + _ + _ + _ = __ | __ × 3 = __ |
| Compliance w/ Previous | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Decision Integrity | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Audit Integrity | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Production Readiness | 2 | 4 | _ + _ + _ + _ = __ | __ × 2 = __ |
| **TOTAL** | | **20** | | **__ / 100** |

```
Score = (Total / 100) × 100 = ___%
```

## VEREDICTO (GATE)

- [ ] Score ≥ 75 + sin CRITICAL → **GO** — Continuar a TEST_STRATEGY / IMPLEMENT
- [ ] Score 60-74 + sin CRITICAL → **GO CONDICIONAL** — Continuar con observaciones
- [ ] Score < 60 → **NO-GO** — Volver a FIX_PLAN
- [ ] Hallazgo CRITICAL → **NO-GO automático** (independiente del score)

### Resultado

```
VEREDICTO: [GO / NO-GO / GO CONDICIONAL]
SCORE: ___% 
NIVEL: [ENTERPRISE READY / PRODUCTION READY / CONDITIONAL / HIGH RISK / FAIL]
ACCIÓN: [Continuar / Corregir plan / Revisión urgente]
```

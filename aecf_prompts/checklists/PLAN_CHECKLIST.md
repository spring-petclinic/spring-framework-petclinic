# AECF Prompts — PLAN CHECKLIST

LAST_REVIEW: 2026-03-09

---

> Checklist simplificado para la fase PLAN. Evaluar cada ítem con 0 / 1 / 2 según `scoring/SCORING_MODEL.md`.

---

## 1. Scope Validation (Peso: 2)

- [ ] El alcance está claramente definido y delimitado
- [ ] No hay expansión implícita de scope
- [ ] Los límites de lo que NO se incluye están explícitos

## 2. Security Controls (Peso: 3)

- [ ] Se identifican requisitos de seguridad
- [ ] Se planifica control de acceso
- [ ] Se identifican datos sensibles y su tratamiento
- [ ] Se planifica logging de eventos de seguridad

## 3. Decision Integrity (Peso: 3)

- [ ] Todas las decisiones técnicas están justificadas
- [ ] No hay decisiones implícitas o asumidas
- [ ] Las alternativas descartadas están documentadas

## 4. Plan Clarity (Peso: 2)

- [ ] Los requisitos están claramente definidos
- [ ] Las dependencias están identificadas
- [ ] No hay ambigüedades en las instrucciones
- [ ] Los criterios de aceptación son verificables

## 5. Production Readiness (Peso: 2)

- [ ] Se consideran casos borde
- [ ] El manejo de errores está planificado
- [ ] No hay supuestos ocultos

---

## SCORING TABLE

| Categoría | Peso | Ítems | Puntuación (0-2 cada uno) | Total |
|---|---|---|---|---|
| Scope Validation | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Security Controls | 3 | 4 | _ + _ + _ + _ = __ | __ × 3 = __ |
| Decision Integrity | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Plan Clarity | 2 | 4 | _ + _ + _ + _ = __ | __ × 2 = __ |
| Production Readiness | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| **TOTAL** | | **17** | | **__ / 68** |

```
Score = (Total / 68) × 100 = ___%
```

## VEREDICTO

- [ ] Score ≥ 75 → Continuar a AUDIT_PLAN
- [ ] Score < 75 → Revisar plan antes de continuar
- [ ] Hallazgo CRITICAL → NO continuar

> ⚠️ PLAN no tiene gate GO/NO-GO formal, pero un score bajo indica que el plan necesita mejoras antes de auditarlo.

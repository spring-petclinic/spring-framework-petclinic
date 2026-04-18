# AECF Prompts — TEST_STRATEGY CHECKLIST

LAST_REVIEW: 2026-03-09

---

> Checklist simplificado para la fase TEST_STRATEGY. Evaluar cada ítem con 0 / 1 / 2 según `scoring/SCORING_MODEL.md`.

---

## 1. Scope Validation (Peso: 2)

- [ ] La estrategia de tests cubre el scope del PLAN aprobado
- [ ] No hay tests fuera de scope
- [ ] No hay funcionalidad sin cobertura planificada

## 2. Security Controls (Peso: 3)

- [ ] Se incluyen tests de seguridad
- [ ] Tests de control de acceso planificados
- [ ] Tests de inyección / validación de input planificados
- [ ] Tests de exposición de datos planificados

## 3. Compliance with Previous Phase (Peso: 3)

- [ ] La estrategia se basa en un PLAN con AUDIT aprobado
- [ ] Todos los requisitos del plan tienen tests asociados
- [ ] No se testean features no planificadas

## 4. Testing Coverage Design (Peso: 2)

- [ ] Happy path definido para cada funcionalidad
- [ ] Casos borde definidos
- [ ] Tests de seguridad incluidos
- [ ] Objetivo de cobertura definido (≥ 80% recomendado)

## 5. Decision Integrity (Peso: 3)

- [ ] El alcance del testing es trazable al PLAN
- [ ] Las prioridades de testing están justificadas

## 6. Production Readiness (Peso: 2)

- [ ] Tests de regresión considerados
- [ ] Tests de error handling incluidos
- [ ] Tests de performance considerados (si aplica)

---

## SCORING TABLE

| Categoría | Peso | Ítems | Puntuación (0-2 cada uno) | Total |
|---|---|---|---|---|
| Scope Validation | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Security Controls | 3 | 4 | _ + _ + _ + _ = __ | __ × 3 = __ |
| Compliance w/ Previous | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Testing Coverage Design | 2 | 4 | _ + _ + _ + _ = __ | __ × 2 = __ |
| Decision Integrity | 3 | 2 | _ + _ = __ | __ × 3 = __ |
| Production Readiness | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| **TOTAL** | | **19** | | **__ / 86** |

```
Score = (Total / 86) × 100 = ___%
```

## VEREDICTO

- [ ] Score ≥ 75 → Estrategia de tests aceptable, continuar a IMPLEMENT
- [ ] Score < 75 → Revisar estrategia antes de implementar
- [ ] Hallazgo CRITICAL → Revisión obligatoria

> ⚠️ TEST_STRATEGY no tiene gate GO/NO-GO formal, pero un score bajo indica riesgo de cobertura insuficiente.

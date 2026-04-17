# AECF Prompts — AUDIT_CODE CHECKLIST

LAST_REVIEW: 2026-04-17

---

> Checklist simplificado para la fase AUDIT_CODE. Evaluar cada ítem con 0 / 1 / 2 según `scoring/SCORING_MODEL.md`.
> Esta fase tiene **gate GO/NO-GO**: el veredicto determina si el código pasa a producción.

---

## 1. Scope Validation (Peso: 2)

- [ ] El código implementado coincide con el PLAN
- [ ] No hay expansión de scope
- [ ] No hay rediseño implícito

## 2. Security Controls (Peso: 3)

- [ ] No se exponen datos sensibles
- [ ] Control de acceso validado
- [ ] Mitigación de enumeración verificada
- [ ] Logging cubre eventos de seguridad

## 3. Resource Management (Peso: 2)

- [ ] No hay recursos abiertos sin cerrar
- [ ] Context managers / try-finally usados correctamente

## 4. Dependency Outage Resilience (Peso: 3)

- [ ] Llamadas externas tienen timeouts explícitos
- [ ] Reintentos acotados con backoff
- [ ] Circuit breaker o fail-fast presente
- [ ] Errores al usuario no son engañosos
- [ ] Rate limiting previene amplificación por retry storm

## 5. Logging & Observability (Peso: 2)

- [ ] No se usa print() para output
- [ ] Logging estructurado implementado
- [ ] Errores loggeados correctamente

## 6. Compliance with Previous Phase (Peso: 3)

- [ ] PLAN aprobado por auditoría
- [ ] Veredicto de AUDIT_PLAN respetado
- [ ] No hay violación de secuencia de fases

## 7. Production Readiness (Peso: 2)

- [ ] Casos borde considerados
- [ ] Error handling completo
- [ ] No hay fallos silenciosos
- [ ] No hay efectos secundarios ocultos

## 8. Decision Integrity (Peso: 3)

- [ ] No hay decisiones no autorizadas
- [ ] Todas las decisiones trazables al PLAN

## 9. Code Audit Integrity (Peso: 2)

- [ ] Desviaciones respecto al PLAN detectadas
- [ ] Bugs clasificados por severidad
- [ ] El veredicto es consistente con la clasificación

## 10. Testing Evidence (Peso: 3)

- [ ] Tests ejecutados con evidencia (comandos + resultados)
- [ ] Tests pasan correctamente
- [ ] Cobertura medida o blocker documentado

## 11. Anti-patterns (Peso: 3)

> Verificar ausencia de anti-patterns estándar. Los de **seguridad y scope** generan CRITICAL automático; los de **mantenibilidad** generan WARNING.

### Scope anti-patterns (→ CRITICAL automático)
- [ ] Sin `SCOPE_CREEP`: el código implementa sólo lo definido en el PLAN, sin features adicionales
- [ ] Sin `DEAD_FEATURE`: no hay TODOs ni código comentado que impliquen funcionalidades no autorizadas

### Security anti-patterns (→ CRITICAL automático)
- [ ] Sin `HARDCODED_SECRET`: no hay credenciales, passwords, API keys ni tokens en código fuente
- [ ] Sin `SQL_INJECTION`: queries no se construyen concatenando strings con input de usuario
- [ ] Sin `COMMAND_INJECTION`: no hay shell commands construidos con input de usuario sin sanitizar
- [ ] Sin `INSECURE_DESERIALIZATION`: no se usa `eval()` ni `pickle.loads()` / equivalentes con datos no confiables
- [ ] Sin `PATH_TRAVERSAL`: rutas de fichero no se construyen desde input de usuario sin sanitización

### Maintainability anti-patterns (→ WARNING)
- [ ] Sin `GOD_FUNCTION`: funciones < 50 líneas y complejidad ciclomática ≤ 10
- [ ] Sin `MAGIC_NUMBER`: no hay literales numéricos o string sin constante con nombre
- [ ] Sin `DEEP_NESTING`: máximo 3 niveles de anidamiento en condicionales y bucles
- [ ] Sin `SILENT_EXCEPTION`: no hay `except: pass` ni bare `except` sin logging
- [ ] Sin `GLOBAL_MUTABLE_STATE`: sin estado mutable global modificado por funciones
- [ ] Sin `PRINT_DEBUGGING`: `print()` ausente como mecanismo de logging en código de producción

---

## SCORING TABLE

| Categoría | Peso | Ítems | Puntuación (0-2 cada uno) | Total |
|---|---|---|---|---|
| Scope Validation | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Security Controls | 3 | 4 | _ + _ + _ + _ = __ | __ × 3 = __ |
| Resource Management | 2 | 2 | _ + _ = __ | __ × 2 = __ |
| Dep. Outage Resilience | 3 | 5 | _ + _ + _ + _ + _ = __ | __ × 3 = __ |
| Logging & Observability | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Compliance w/ Previous | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Production Readiness | 2 | 4 | _ + _ + _ + _ = __ | __ × 2 = __ |
| Decision Integrity | 3 | 2 | _ + _ = __ | __ × 3 = __ |
| Code Audit Integrity | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Testing Evidence | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Anti-patterns | 3 | 13 | _ + _ + _ + _ + _ + _ + _ + _ + _ + _ + _ + _ + _ = __ | __ × 3 = __ |
| **TOTAL** | | **45** | | **__ / 240** |

```
Score = (Total / 240) × 100 = ___%
```

## VEREDICTO (GATE)

- [ ] Score ≥ 75 + sin CRITICAL + testing evidence → **GO** — Código apto para producción
- [ ] Score ≥ 90 + sin CRITICAL → **GO ENTERPRISE** — Excelencia
- [ ] Score 60-74 + sin CRITICAL → **GO CONDICIONAL** — Con observaciones
- [ ] Score < 60 → **NO-GO** — Volver a FIX_CODE
- [ ] Hallazgo CRITICAL → **NO-GO automático**
- [ ] Sin evidencia de tests ejecutados → **NO-GO automático**
- [ ] Anti-pattern de seguridad o scope detectado → **NO-GO automático**

### Resultado

```
VEREDICTO: [GO / NO-GO / GO CONDICIONAL / GO ENTERPRISE]
SCORE: ___% 
NIVEL: [ENTERPRISE READY / PRODUCTION READY / CONDITIONAL / HIGH RISK / FAIL]
HALLAZGOS CRITICAL: [0 / lista]
TESTING EVIDENCE: [Sí con evidencia / No]
ACCIÓN: [Release / Corregir código / Revisión urgente]
```

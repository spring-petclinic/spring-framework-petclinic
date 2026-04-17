# AECF Prompts — IMPLEMENT CHECKLIST

LAST_REVIEW: 2026-04-17

---

> Checklist simplificado para la fase IMPLEMENT. Evaluar cada ítem con 0 / 1 / 2 según el modelo de scoring cargado para la fase.

---

## 1. Scope Validation (Peso: 2)

- [ ] El código implementado coincide con el PLAN aprobado
- [ ] No hay expansión de scope
- [ ] No hay rediseño implícito no autorizado

## 2. Security Controls (Peso: 3)

- [ ] No se exponen datos sensibles
- [ ] Control de acceso implementado
- [ ] Mitigación de enumeración presente
- [ ] Logging cubre eventos de seguridad

## 3. Resource Management (Peso: 2)

- [ ] No hay recursos abiertos sin cerrar
- [ ] Se usan context managers / try-finally

## 4. Dependency Outage Resilience (Peso: 3)

- [ ] Llamadas externas tienen timeouts explícitos
- [ ] Reintentos acotados con backoff (+ jitter si aplica)
- [ ] Protección fail-fast ante fallos persistentes
- [ ] Errores al usuario reflejan fallo de dependencia (no engañosos)

## 5. Logging & Observability (Peso: 2)

- [ ] No se usa print() para logging
- [ ] Logging estructurado implementado
- [ ] Errores loggeados correctamente

## 6. Compliance with Previous Phase (Peso: 3)

- [ ] PLAN aprobado (AUDIT_PLAN = GO)
- [ ] Veredicto de auditoría respetado
- [ ] No hay violación de secuencia de fases

## 7. Production Readiness (Peso: 2)

- [ ] Casos borde considerados
- [ ] Error handling completo
- [ ] No hay fallos silenciosos
- [ ] No hay efectos secundarios ocultos

## 8. Decision Integrity (Peso: 3)

- [ ] No hay decisiones no autorizadas
- [ ] Todas las decisiones son trazables al PLAN

## 9. Implementation Integrity (Peso: 2)

- [ ] El código coincide literalmente con el PLAN
- [ ] No hay features adicionales no planificadas
- [ ] Todos los pasos del PLAN están implementados

## 10. Function-Level AECF Metadata (Peso: 3)

- [ ] Cada nueva función o método incluye línea `AECF_META` en su docstring o formato equivalente
- [ ] `skill` coincide con el skill actual en ejecución
- [ ] `topic` coincide con el TOPIC resuelto para esta ejecución
- [ ] `generated_at` y `generated_by` están informados con valores actuales
- [ ] `last_modified_*` coincide con `generated_*` en primera creación
- [ ] Se sigue el formato definido en `CODE_FUNCTION_METADATA_STANDARD.md`

## 11. Anti-patterns

> El código generado NO debe introducir estos anti-patterns. Los anti-patterns de scope y seguridad implican fallo automático de la fase. Los anti-patterns de mantenibilidad penalizan el score y deben señalarse como warning para AUDIT_CODE.

### Scope anti-patterns (→ fallo automático)
- [ ] No `SCOPE_CREEP`: code implements only what the PLAN defines
- [ ] No `DEAD_FEATURE`: no TODOs or commented-out code implying unauthorized features

### Security anti-patterns (→ fallo automático)
- [ ] No `HARDCODED_SECRET`: no credentials, passwords, API keys or tokens in source code
- [ ] No `SQL_INJECTION`: queries not built by concatenating strings with user input
- [ ] No `COMMAND_INJECTION`: no shell commands built from user input without sanitization
- [ ] No `INSECURE_DESERIALIZATION`: no `eval()` or `pickle.loads()` / equivalents with untrusted data
- [ ] No `PATH_TRAVERSAL`: file paths not constructed from user input without sanitization

### Maintainability anti-patterns (→ penalización de score)
- [ ] No `GOD_FUNCTION`: functions < 50 lines and cyclomatic complexity ≤ 10
- [ ] No `MAGIC_NUMBER`: numeric or string literals use named constants
- [ ] No `DEEP_NESTING`: max 3 levels of nesting
- [ ] No `SILENT_EXCEPTION`: no `except: pass` o bare `except` without logging
- [ ] No `GLOBAL_MUTABLE_STATE`: no module-level mutable state modified by functions

## FINAL CHECK
Los bloques 1-11 deben poder evaluarse completamente antes de continuar. Cualquier anti-pattern de scope o seguridad invalida IMPLEMENT y debe corregirse antes de AUDIT_CODE. Los anti-patterns de mantenibilidad no bloquean por sí solos, pero deben penalizar el score y quedar reflejados en la auditoría.

## SCORING TABLE

| Categoría | Peso | Ítems | Puntuación (0-2 cada uno) | Total |
|---|---|---|---|---|
| Scope Validation | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Security Controls | 3 | 4 | _ + _ + _ + _ = __ | __ × 3 = __ |
| Resource Management | 2 | 2 | _ + _ = __ | __ × 2 = __ |
| Dep. Outage Resilience | 3 | 4 | _ + _ + _ + _ = __ | __ × 3 = __ |
| Logging & Observability | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Compliance w/ Previous | 3 | 3 | _ + _ + _ = __ | __ × 3 = __ |
| Production Readiness | 2 | 4 | _ + _ + _ + _ = __ | __ × 2 = __ |
| Decision Integrity | 3 | 2 | _ + _ = __ | __ × 3 = __ |
| Implementation Integrity | 2 | 3 | _ + _ + _ = __ | __ × 2 = __ |
| Function-Level AECF Metadata | 3 | 6 | _ + _ + _ + _ + _ + _ = __ | __ × 3 = __ |
| Scope Anti-patterns | 3 | 2 | _ + _ = __ | __ × 3 = __ |
| Security Anti-patterns | 3 | 5 | _ + _ + _ + _ + _ = __ | __ × 3 = __ |
| Maintainability Anti-patterns | 3 | 5 | _ + _ + _ + _ + _ = __ | __ × 3 = __ |
| **TOTAL** | | **46** | | **__ / 246** |

```
Score = (Total / 246) × 100 = ___%
```

## VEREDICTO

**RULE**: If any CRITICAL finding exists → Score = 0 and automatic NO-GO
**RULE**: If any scope or security anti-pattern detected → automatic phase failure

- [ ] Score ≥ 75 → Implementación aceptable, pasar a AUDIT_CODE
- [ ] Score < 75 → Revisar implementación
- [ ] Hallazgo CRITICAL → NO continuar
- [ ] Anti-pattern de scope o seguridad detectado → NO continuar

> ⚠️ IMPLEMENT no emite un gate GO/NO-GO formal, pero un hallazgo CRITICAL o un anti-pattern de scope o seguridad invalida el artefacto IMPLEMENT y debe corregirse antes de AUDIT_CODE.

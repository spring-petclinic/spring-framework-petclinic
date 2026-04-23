# Ciclo de Vida de Desarrollo de Aplicaciones con integración AECF

LAST_REVIEW: 2026-04-13
OWNER SEACHAD

---

## Índice

1. [Fundamentos metodológicos](#1-fundamentos-metodológicos)
2. [Modelo de ciclo de vida propuesto](#2-modelo-de-ciclo-de-vida-propuesto)
3. [Fase 1 - Inception y Discovery](#3-fase-1---inception-y-discovery)
4. [Fase 2 - Arquitectura y Diseño](#4-fase-2---arquitectura-y-diseño)
5. [Fase 3 - Desarrollo iterativo](#5-fase-3---desarrollo-iterativo)
6. [Fase 4 - Calidad y Testing](#6-fase-4---calidad-y-testing)
7. [Fase 5 - Seguridad y Compliance](#7-fase-5---seguridad-y-compliance)
8. [Fase 6 - Release Governance](#8-fase-6---release-governance)
9. [Fase 7 - Operaciones y Evolución](#9-fase-7---operaciones-y-evolución)
10. [Mapa resumen: skills por fase](#10-mapa-resumen-skills-por-fase)
11. [Cadenas de skills recomendadas](#11-cadenas-de-skills-recomendadas)
12. [Reglas de construcción para el skill](#12-reglas-de-construcción-para-el-skill)
13. [Referencias](#13-referencias)

---

## 1. Fundamentos metodológicos

Este modelo propone un ciclo de vida de desarrollo de aplicaciones inspirado en estándares de gestión y de ingeniería de software, con integración explícita de AECF como capa de gobernanza operativa.

Las metodologías aceptadas por el skill `aecf_application_lifecycle` son exactamente:

- `AGILE`
- `PMBOK`
- `PRINCE2`
- `SCRUM`
- `KANBAN`
- `ISO_12207`
- `HYBRID_PMBOK_SCRUM`

### 1.1 Mapeo de metodologías aceptadas

| Metodología aceptada | Referencia principal | Aportación al ciclo de vida |
|---|---|---|
| `AGILE` | Agile umbrella approach | Marco general iterativo e incremental que puede concretarse con Scrum, Kanban o un híbrido ligero |
| `PMBOK` | PMI PMBOK | Dominios de desempeño, gates de transición, gobierno del alcance y stakeholders |
| `PRINCE2` | PRINCE2 | Gobierno por etapas, control de tolerancias, products y management stages |
| `SCRUM` | Scrum Guide | Cadencia iterativa, sprint planning, review y retrospective |
| `KANBAN` | Kanban Method | Flujo continuo, gestión visual del trabajo, políticas explícitas y WIP |
| `ISO_12207` | ISO/IEC/IEEE 12207 | Procesos de ciclo de vida del software, verificación, validación y mantenimiento |
| `HYBRID_PMBOK_SCRUM` | PMBOK + Scrum | Gobierno formal con ejecución iterativa por incrementos |

### 1.2 Principios rectores

1. Cada fase tiene un objetivo claro, actividades principales, gate de salida y skills AECF recomendados.
2. La metodología concreta elegida debe mantener sus nombres de fases o checkpoints reconocibles.
3. AECF no sustituye la metodología: aporta contexto, auditoría, trazabilidad y gates operativos.
4. No se incluye una sección específica de aplicación a un proyecto concreto; la guía debe permanecer reutilizable.
5. En repos grandes o multi-equipo, el ciclo debe decidir si necesita `surfaces` de negocio, técnicas o mixtas antes de ejecutar skills repo-dependientes.
6. Cuando el trabajo dependa de patrones de stack, arquitectura o dominio, deben cargarse `domains` y `semantic_profiles` relevantes si existen.

---

## 2. Modelo de ciclo de vida propuesto

### 2.1 Diagrama general del ciclo

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CICLO DE VIDA DE APLICACIONES CON AECF                     │
└─────────────────────────────────────────────────────────────────────────────┘

 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────┐
 │  FASE 1      │ ──▶ │  FASE 2      │ ──▶ │  FASE 3      │ ──▶ │  FASE 4   │
 │  Inception   │     │  Arquitectura│     │  Desarrollo  │     │  Calidad  │
 │  Discovery   │     │  y Diseño    │     │  iterativo   │     │  Testing  │
 └──────────────┘     └──────────────┘     └──────────────┘     └────────────┘
		│                                          ▲                    │
		│                                          │                    ▼
		│                                     (bucle de entrega) ┌────────────┐
		│                                                        │  FASE 5   │
		│                                                        │ Seguridad │
		│                                                        │ Compliance│
		│                                                        └─────┬──────┘
		│                                                              │
		▼                                                              ▼
 ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────────────┐
 │  FASE 7      │ ◀── │  FASE 6      │ ◀── │  Gate: Release Readiness        │
 │ Operaciones  │     │  Release     │     │  (`aecf_release_readiness`)     │
 │ y Evolución  │     │ Governance   │     └──────────────────────────────────┘
 └──────┬───────┘     └──────────────┘
		│
		└─▶ Hotfix / deuda técnica / mejora continua
```

### 2.2 Relación entre fases y metodologías

| Fase propuesta | `PMBOK` | `PRINCE2` | `SCRUM` | `KANBAN` | `ISO_12207` |
|---|---|---|---|---|---|
| 1 - Inception y Discovery | Initiate | Starting Up a Project | Product framing | Service definition / replenishment inicial | Agreement / project planning |
| 2 - Arquitectura y Diseño | Plan | Initiating a Project | Backlog refinement técnico | Replenishment / design policies | Architecture and design |
| 3 - Desarrollo iterativo | Execute | Managing Product Delivery | Sprint execution | Active flow | Implementation |
| 4 - Calidad y Testing | Monitor and Control | Controlling a Stage | Definition of Done / verificación sprint | Flow review | Verification |
| 5 - Seguridad y Compliance | Monitor and Control | Stage controls and quality themes | Controles por sprint/release | Risk review continua | Validation |
| 6 - Release Governance | Close | Managing Stage Boundary / Closing a Project | Sprint review / release decision | Delivery | Delivery / transition |
| 7 - Operaciones y Evolución | Lessons learned | Closing a Project / follow-on actions | Retrospective | Continuous improvement | Operation / maintenance |

### 2.3 Contexto transversal: surfaces, domains y semantic profiles

Cuando la aplicación tiene espacios transversales de negocio o técnicos, el ciclo debe contemplar explícitamente el uso de `surfaces`:

1. `business_surface` para reglas funcionales, ownership y flujos de negocio.
2. `technical_surface` para arquitectura compartida, plataforma, integraciones e infraestructura.

El modelo recomendado está documentado en:

- [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md)
- [AECF_SURFACE_SELECTION_INTAKE.md](AECF_SURFACE_SELECTION_INTAKE.md)
- [AECF_SKILL_SURFACE_CONTRACT.md](AECF_SKILL_SURFACE_CONTRACT.md)
- [AECF_RUN_CONTEXT_CONTRACT.md](AECF_RUN_CONTEXT_CONTRACT.md)

Además, cuando el ciclo necesite conocimiento específico de stack o patrón arquitectónico, debe valorar el uso de `domains` y `semantic_profiles`:

1. `domains` para conocimiento reusable del stack o vertical técnica.
2. `semantic_profiles` para variantes concretas dentro de un dominio.

Regla práctica:

1. problema transversal de negocio o arquitectura -> resolver `surfaces`,
2. problema dependiente de stack o patrón técnico -> cargar `domains` y `semantic_profiles`,
3. ambas necesidades a la vez -> combinar contexto global + `surfaces` + `domain`/`semantic_profile` justificados.

---

## 3. Fase 1 - Inception y Discovery

### Objetivo
Entender el contexto del producto, el sistema actual, los riesgos iniciales y los criterios de valor antes de diseñar o implementar cambios.

### Actividades principales
- Identificar stakeholders y restricciones de negocio.
- Confirmar stack, contexto del repositorio y módulos críticos.
- Entender el comportamiento del código legado si ya existe.
- Decidir si hacen falta `surfaces` para separar espacios técnicos transversales y de negocio.
- Identificar riesgos de datos, dependencias y trazabilidad.
- Definir objetivos y métricas de impacto.

### Gate de salida
- [ ] Contexto del proyecto o del sistema disponible y coherente.
- [ ] Stack y alcance confirmados.
- [ ] Decisión explícita sobre uso de `surfaces` cuando el sistema es transversal o multi-equipo.
- [ ] Riesgos y hotspots conocidos.
- [ ] Métricas de impacto iniciales definidas.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_application_lifecycle` | Al decidir la metodología y el operating model del proyecto | Guía de ciclo de vida por metodología |
| `aecf_new_project` | Si la aplicación nace desde cero | Skeleton del proyecto + contexto inicial |
| `aecf_project_context_generator` | Si la aplicación ya existe | `AECF_PROJECT_CONTEXT.md` |
| `aecf_codebase_intelligence` | Si hace falta discovery estructurado del repositorio | Inventario estructurado del codebase |
| `aecf_document_legacy` | Si hay módulos críticos sin documentación | Documentación técnica del legado |
| `aecf_explain_behavior` | Si hay que entender flujos concretos antes de actuar | Explicación de comportamiento |
| `aecf_define_impact_metrics` | Si se quieren fijar KPIs de negocio o de ingeniería | Métricas de impacto |

Si el sistema es grande o transversal, esta fase debe referenciar también:

- `AECF_SURFACE_CONTEXT_MODEL.md` para decidir `business_surface` y `technical_surface`.
- `domains/<domain>/pack.md` y `semantic_profiles/<profile>.md` cuando el contexto de stack o patrón técnico cambie materialmente la estrategia.

---

## 4. Fase 2 - Arquitectura y Diseño

### Objetivo
Definir cómo se construirá o evolucionará la aplicación: arquitectura, dependencias, deuda técnica, calidad esperada y restricciones transversales.

### Actividades principales
- Revisar arquitectura, componentes y decisiones de diseño.
- Evaluar acoplamiento y presión de refactor.
- Determinar si el diseño afecta a varias `surfaces` o a una sola `primary_surface`.
- Auditar dependencias externas y riesgos de supply chain.
- Identificar deuda técnica que condiciona la entrega.
- Definir estrategia de datos si hay cambios relevantes de modelo o pipeline.

### Gate de salida
- [ ] Arquitectura y decisiones de diseño explicitadas.
- [ ] Uso de `surfaces` validado si el cambio atraviesa varias fronteras técnicas o de negocio.
- [ ] Dependencias críticas auditadas.
- [ ] Deuda técnica priorizada o aceptada.
- [ ] Riesgos de datos y calidad considerados.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_set_stack` | Si el stack debe fijarse o corregirse | Stack operativo normalizado |
| `aecf_coupling_assessment` | Antes de cambios estructurales o refactors complejos | Mapa de acoplamiento |
| `aecf_dependency_audit` | Antes de upgrades o integraciones críticas | Inventario de dependencias y riesgos |
| `aecf_tech_debt_assessment` | Si el backlog técnico condiciona el diseño | Backlog de deuda priorizado |
| `aecf_resolve_linting` | Si hay que fijar el perfil de calidad antes de planificar | Perfil de static analysis |
| `aecf_data_strategy` | Si la aplicación introduce modelo de datos o pipeline relevante | Estrategia de datos |

Si la arquitectura depende de conocimiento especializado de stack, esta fase debe indicar si conviene cargar un `domain` o un `semantic_profile` antes de producir el diseño final.

---

## 5. Fase 3 - Desarrollo iterativo

### Objetivo
Implementar incrementos de forma gobernada, con trazabilidad desde la necesidad hasta el cambio materializado.

### Actividades principales
- Planificar incrementos o work items según la metodología elegida.
- Implementar nuevas funcionalidades o refactors.
- Resolver incidencias críticas fuera del flujo ordinario cuando sea necesario.
- Mantener la trazabilidad entre prompt, plan, cambios y validación.

### Gate de salida
- [ ] El incremento queda implementado o preparado para auditoría.
- [ ] Se generó o actualizó la evidencia de diseño y decisión.
- [ ] No quedan bloqueantes funcionales obvios para pasar a calidad.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_new_feature` | Nuevas capacidades o cambios funcionales | Flujo completo de delivery gobernado |
| `aecf_refactor` | Mejora estructural del código | Plan y refactor gobernado |
| `aecf_hotfix` | Incidencias P1/P2 o correcciones urgentes | Hotfix con evidencia |
| `aecf_new_test_set` | Cuando el módulo carece de cobertura suficiente | Strategy + tests |
| `aecf_system_replayability_adaptive` | Si el cambio exige trazabilidad o replay | Diseño de replayabilidad |

---

## 6. Fase 4 - Calidad y Testing

### Objetivo
Garantizar que la aplicación cumple los contratos esperados y reduce el riesgo de regresión antes de avanzar hacia release.

### Actividades principales
- Diseñar o ampliar suites de tests.
- Verificar contratos funcionales y técnicos.
- Auditar estándares de código y reproducibilidad.
- Revisar cobertura y evidencia de calidad.

### Gate de salida
- [ ] Evidencia de tests suficiente para el alcance.
- [ ] Sin findings críticos de calidad abiertos.
- [ ] Contratos relevantes verificados.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_new_test_set` | Para cerrar gaps de cobertura | Tests implementados o planificados |
| `aecf_code_standards_audit` | Antes de merge o checkpoint de calidad | Informe de estándares |
| `aecf_system_replayability_adaptive` | Si la reproducibilidad es un requisito del sistema | Evaluación de replayabilidad |

---

## 7. Fase 5 - Seguridad y Compliance

### Objetivo
Comprobar que la aplicación satisface los controles de seguridad y cumplimiento aplicables antes del release o del siguiente gate significativo.

### Actividades principales
- Revisar seguridad técnica y gestión de secretos.
- Evaluar normativa aplicable por datos, resiliencia o IA.
- Auditar gobierno de datos o de modelos cuando aplique.
- Registrar riesgos abiertos y mitigaciones.

### Gate de salida
- [ ] Sin findings críticos de seguridad abiertos.
- [ ] Riesgos altos con mitigación o aceptación explícita.
- [ ] Controles regulatorios relevantes evaluados.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_security_review` | Control general de seguridad técnica | Informe de seguridad |
| `aecf_security_review_gdpr` | Si se procesan datos personales | Gap analysis GDPR |
| `aecf_security_review_dora` | Si el sistema cae en resiliencia operativa financiera | Evaluación DORA |
| `aecf_security_review_eu_ai_act` | Si la aplicación incorpora IA/ML | Clasificación y obligaciones AI Act |
| `aecf_data_governance_audit` | Si cambia el modelo o uso del dato | Informe de data governance |
| `aecf_ai_risk_assessment` | Si hay riesgos operativos o regulatorios por IA | Matriz de riesgo IA |
| `aecf_model_governance_audit` | Si el modelo o la inferencia requieren control formal | Scorecard de model governance |

---

## 8. Fase 6 - Release Governance

### Objetivo
Emitir una decisión formal sobre la preparación para release y comunicar el estado del incremento o del producto.

### Actividades principales
- Evaluar readiness de release.
- Consolidar evidencia de calidad, seguridad y documentación.
- Generar comunicación ejecutiva para stakeholders.

### Gate de salida
- [ ] `aecf_release_readiness` en estado GO o con bloqueo explícito.
- [ ] Estado comunicado a stakeholders relevantes.
- [ ] Riesgos residuales documentados.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_release_readiness` | Antes de cada release o cierre de stage | Scorecard GO/NO-GO |
| `aecf_executive_summary` | Para consolidar el estado a nivel directivo o de gestión | Resumen ejecutivo |

---

## 9. Fase 7 - Operaciones y Evolución

### Objetivo
Mantener la aplicación en producción, gestionar incidentes, controlar degradación técnica y preparar el siguiente ciclo de mejora.

### Actividades principales
- Gestionar incidencias y hotfixes.
- Repriorizar deuda técnica y dependencias.
- Medir productividad y madurez operativa.
- Preparar el siguiente ciclo o incremento.

### Gate de entrada al siguiente ciclo
- [ ] Deuda técnica revisada.
- [ ] Riesgos operativos relevantes identificados.
- [ ] Prioridades del siguiente ciclo acordadas.

### Skills AECF recomendados

| Skill | Cuándo usarlo | Artefacto esperado |
|---|---|---|
| `aecf_hotfix` | Incidencias críticas en producción | Hotfix documentado |
| `aecf_productivity` | Revisión de throughput y foco del equipo | KPIs de productividad |
| `aecf_tech_debt_assessment` | Antes del siguiente ciclo o release mayor | Backlog técnico actualizado |
| `aecf_dependency_audit` | Por alertas, upgrades o revisión periódica | Riesgos de dependencias |
| `aecf_maturity_assessment` | Evaluación del sistema o del proceso | Scorecard de madurez |
| `aecf_code_standards_audit` | Revisión acumulada fuera del sprint | Informe de estándares |

---

## 10. Mapa resumen: skills por fase

```text
╔══════════════════╦══════════════════════════════════════════════════╦══════════════════════╗
║ FASE             ║ AECF SKILLS                                      ║ FRECUENCIA           ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 1 - Inception    ║ application_lifecycle                            ║ Inicio del proyecto  ║
║                  ║ new_project                                      ║ o del ciclo          ║
║                  ║ project_context_generator                        ║                      ║
║                  ║ codebase_intelligence                            ║                      ║
║                  ║ document_legacy                                  ║                      ║
║                  ║ explain_behavior                                 ║                      ║
║                  ║ define_impact_metrics                            ║                      ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 2 - Arquitectura ║ set_stack                                        ║ Al diseñar o         ║
║                  ║ coupling_assessment                              ║ replantear           ║
║                  ║ dependency_audit                                 ║ arquitectura         ║
║                  ║ tech_debt_assessment                             ║                      ║
║                  ║ resolve_linting                                  ║                      ║
║                  ║ data_strategy                                    ║                      ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 3 - Desarrollo   ║ new_feature                                      ║ Por iteración,       ║
║                  ║ refactor                                         ║ sprint o flujo       ║
║                  ║ hotfix                                           ║ continuo             ║
║                  ║ new_test_set                                     ║                      ║
║                  ║ system_replayability_adaptive                    ║                      ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 4 - Calidad      ║ new_test_set                                     ║ Antes de merge o     ║
║                  ║ code_standards_audit                             ║ checkpoint           ║
║                  ║ system_replayability_adaptive                    ║                      ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 5 - Seguridad    ║ security_review                                  ║ Por release mayor o  ║
║                  ║ security_review_gdpr                             ║ cambio relevante     ║
║                  ║ security_review_dora                             ║                      ║
║                  ║ security_review_eu_ai_act                        ║                      ║
║                  ║ data_governance_audit                            ║                      ║
║                  ║ ai_risk_assessment                               ║                      ║
║                  ║ model_governance_audit                           ║                      ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 6 - Release      ║ release_readiness                                ║ Cada release o       ║
║                  ║ executive_summary                                ║ cierre de stage      ║
╠══════════════════╬══════════════════════════════════════════════════╬══════════════════════╣
║ 7 - Operaciones  ║ hotfix                                           ║ Continuo / periódico ║
║                  ║ productivity                                     ║                      ║
║                  ║ tech_debt_assessment                             ║                      ║
║                  ║ dependency_audit                                 ║                      ║
║                  ║ maturity_assessment                              ║                      ║
║                  ║ code_standards_audit                             ║                      ║
╚══════════════════╩══════════════════════════════════════════════════╩══════════════════════╝
```

---

## 11. Cadenas de skills recomendadas

### 11.1 Inicio de ciclo con aplicación existente

```text
aecf_application_lifecycle
	→ aecf_project_context_generator
		→ aecf_codebase_intelligence
			→ aecf_document_legacy
				→ aecf_define_impact_metrics
```

### 11.2 Nueva capacidad con gobernanza completa

```text
aecf_application_lifecycle
	→ aecf_new_feature
		→ aecf_new_test_set
			→ aecf_release_readiness
				→ aecf_executive_summary
```

### 11.3 Rediseño o refactor estructural

```text
aecf_coupling_assessment
	→ aecf_tech_debt_assessment
		→ aecf_refactor
			→ aecf_code_standards_audit
				→ aecf_release_readiness
```

### 11.4 Flujo pre-release con seguridad reforzada

```text
aecf_code_standards_audit
	→ aecf_new_test_set
		→ aecf_security_review
			→ aecf_release_readiness
				→ aecf_executive_summary
```

### 11.5 Operación y mejora continua

```text
aecf_productivity
	→ aecf_tech_debt_assessment
		→ aecf_dependency_audit
			→ aecf_maturity_assessment
```

---

## 12. Reglas de construcción para el skill

El skill `aecf_application_lifecycle` debe construir el documento final siguiendo estas reglas:

1. Debe tomar una única metodología aceptada como entrada obligatoria.
2. Debe reflejar la lógica de este documento: fundamentos, modelo de ciclo, fases, mapa resumen y cadenas recomendadas.
3. Debe adaptar los nombres de checkpoints o fases a la metodología concreta elegida.
4. Debe mantener el documento genérico y reusable.
5. No debe incluir una sección de aplicación a un proyecto actual, ni un bloque equivalente a una sección 12 específica de proyecto, salvo petición explícita del usuario.
6. Si el usuario aporta contexto de negocio o de sistema, ese contexto debe usarse solo para matizar prioridades, riesgos y skills recomendados, no para convertir la guía en un informe de estado de un proyecto concreto.
7. Debe mencionar el uso de `surfaces` cuando el sistema tenga espacios técnicos transversales o de negocio.
8. Debe mencionar `domains` y `semantic_profiles` cuando el contexto de stack o patrón arquitectónico haga falta para una metodología concreta.

---

## 13. Referencias

| Estándar o método | Referencia de base |
|---|---|
| PMBOK | PMI - A Guide to the Project Management Body of Knowledge |
| PRINCE2 | AXELOS / PeopleCert - PRINCE2 |
| Scrum | Scrum Guide |
| Kanban | Kanban Method |
| ISO/IEC/IEEE 12207 | Systems and software engineering - Software life cycle processes |

Guías AECF relacionadas:

- [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md)
- [AECF_SKILL_SURFACE_CONTRACT.md](AECF_SKILL_SURFACE_CONTRACT.md)
- [AECF_RUN_CONTEXT_CONTRACT.md](AECF_RUN_CONTEXT_CONTRACT.md)
- [START_HERE.md](START_HERE.md)
- [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md)

---

Documento guía genérico para AECF prompt-only.
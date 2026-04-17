# AECF Prompts — Consulting Playbook

LAST_REVIEW: 2026-03-25

---

> Guía de implantación para consultores que introducen AECF Prompts en proyectos cliente.

---

## 1. Pre-implantación

### 1.1 Assessment inicial

Antes de implantar AECF Prompts, evaluar:

| Criterio | Pregunta | Respuesta |
|---|---|---|
| Madurez del equipo | ¿El equipo hace code reviews? | |
| Tooling | ¿Qué LLM usa el equipo? | |
| Testing | ¿Hay tests automatizados? | |
| CI/CD | ¿Hay pipeline de deployment? | |
| Documentación | ¿Documentan decisiones técnicas? | |

### 1.2 Selección del skill inicial

Empezar siempre con un skill TIER 1 para la primera demostración:

| Situación del cliente | Skill recomendado |
|---|---|
| Código legacy sin documentar | `document_legacy` |
| Preocupaciones de seguridad | `security_review` |
| Código inconsistente | `code_standards_audit` |
| Necesitan entender algo | `explain_behavior` |

---

## 2. Sesión de implantación (4 horas)

### Hora 1: Preparación

1. Instalar `aecf_prompts/` en el proyecto del cliente
2. Crear `AECF_PROJECT_CONTEXT.md` **junto con el equipo**
3. Revisar `guides/QUICK_START.md` con el equipo
4. Si el equipo quiere conservar una UX parecida a `@aecf` sin componente, revisar también `guides/AECF_PROMPT_ONLY_COMMANDS.md`

### Hora 2: Demostración TIER 1

1. Elegir un módulo real del proyecto del cliente
2. Ejecutar el skill TIER 1 elegido en vivo
3. Mostrar cómo se forma el prompt: `use skill=... TOPIC=... prompt=...`
4. Mostrar cómo se pega la invocación + el prompt de fase en el LLM
5. Mostrar cómo el prompt instruye al LLM a cargar contexto y guardar la salida automáticamente
6. Si el cliente prefiere hablar en sintaxis `@aecf`, mostrar la equivalencia con `guides/AECF_PROMPT_ONLY_COMMANDS.md`

### Hora 3: Demostración TIER 3

1. Elegir una feature pequeña y real
2. Ejecutar las primeras 3 fases del flujo `new_feature`:
   - PLAN → AUDIT_PLAN → (FIX_PLAN si NO-GO)
3. Mostrar el flujo de gate GO/NO-GO
4. Mostrar cómo se aplica el checklist y se calcula el scoring

### Hora 4: Hands-on del equipo

1. Cada miembro del equipo ejecuta un skill TIER 1 con un módulo propio
2. Resolver dudas en vivo
3. Establecer acuerdos:
   - ¿Qué features pasan por AECF?
   - ¿Qué skills aplican?
   - ¿Quién hace las auditorías?
   - ¿Dónde se guardan los documentos en `.aecf/runtime/documentation/`?

---

## 3. Personalización por cliente

### 3.1 Umbrales de scoring

Ajustar en `scoring/SCORING_MODEL.md`:

| Perfil del cliente | Feature | Hotfix | Security |
|---|---|---|---|
| Startup / MVP | ≥ 60 | ≥ 55 | ≥ 75 |
| Empresa mediana | ≥ 75 | ≥ 70 | ≥ 90 |
| Enterprise / Regulado | ≥ 85 | ≥ 80 | ≥ 95 |

### 3.2 Categorías de checklist

- Los checklists incluyen las categorías estándar
- Si el cliente no tiene dependencias externas → ignorar "Dependency Outage Resilience"
- Si el cliente tiene requisitos regulatorios → añadir categoría "Compliance" con peso 3

### 3.3 Skills adicionales

Para clientes con necesidades específicas, el consultor puede crear skills personalizados:

1. Copiar un skill existente como base
2. Ajustar las fases y los prompts referenciados
3. Documentar el skill en `skills/`

---

## 3.4 Uso opcional de sintaxis tipo `@aecf`

Si el cliente ya conoce la UX del componente o quiere una sintaxis más recordable, la implantación puede adoptar el modo prompt-only documentado en `guides/AECF_PROMPT_ONLY_COMMANDS.md`.

Regla práctica:

1. La sintaxis `@aecf ...` en `aecf_prompts` no ejecuta comandos reales.
2. El LLM la interpreta como intención textual y la resuelve contra skills, prompts y artefactos de `aecf_prompts`.
3. Para equipos nuevos, enseñar primero `use skill=...`.
4. Para equipos que vienen del componente, enseñar además la tabla de equivalencias `@aecf`.

---

## 4. Seguimiento post-implantación

### Semana 1-2: Adopción inicial

- [ ] El equipo ejecuta al menos 1 skill TIER 1 de forma autónoma
- [ ] Los outputs se guardan en `.aecf/runtime/documentation/`
- [ ] `AECF_PROJECT_CONTEXT.md` existe en la raíz del proyecto

### Semana 3-4: Adopción de gates

- [ ] El equipo ejecuta al menos 1 skill TIER 3 completo
- [ ] Se aplican checklists en las auditorías
- [ ] Se calcula scoring (aunque sea manual)
- [ ] Se toma la decisión GO/NO-GO con evidencia

### Mes 2+: Madurez

- [ ] AECF se usa para todas las features nuevas
- [ ] Los scores se usan como métrica de calidad
- [ ] La documentación en `.aecf/runtime/documentation/` crece con cada feature
- [ ] El equipo identifica qué skills necesita crear

---

## 5. Métricas de éxito de la implantación

| Métrica | Objetivo Mes 1 | Objetivo Mes 3 |
|---|---|---|
| Skills ejecutados por semana | ≥ 2 | ≥ 5 |
| Score promedio (features) | ≥ 60 | ≥ 75 |
| % features con AECF | ≥ 30% | ≥ 70% |
| Defectos en producción | Baseline | -30% vs baseline |
| Documentos en `.aecf/runtime/documentation/` | ≥ 5 | ≥ 20 |

---

## 6. Escalación a componente automatizado

Cuando el cliente muestra madurez con AECF Prompts (Score ≥ 75 consistente, ≥ 70% de features con AECF), considerar la escalación al componente automatizado:

| Aspecto | AECF Prompts | Componente automatizado |
|---|---|---|
| Ejecución | Manual (copiar prompt) | Automática (VS Code extension) |
| Gates | Evaluación manual | Evaluación automática |
| Scoring | Cálculo manual | Cálculo automático |
| FIX loops | Decisión del usuario | Orquestados por el engine |
| Context management | Manual | Automático (ambients, budget) |
| State persistence | Carpetas de documentación | State store automático |

> La adopción de AECF Prompts es el mejor predictor de éxito con el componente automatizado.

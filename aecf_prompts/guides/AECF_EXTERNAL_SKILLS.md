# AECF Prompts - External Skills Locales

LAST_REVIEW: 2026-04-08
OWNER SEACHAD

---

## Objetivo

Documentar la forma mas simple de extender un skill base de AECF con reglas, criterios o lenguaje especifico de un proyecto sin convertirlo en un skill oficial de `aecf_prompts`.

## Que es un external skill local

Un external skill local es un archivo `SKILL.md` que vive en el workspace del proyecto cliente y que AECF puede usar como guia complementaria cuando una ejecucion admite `external_skills=`.

Ruta esperada:

```text
<workspace>/.agents/skills/<nombre>/SKILL.md
```

No forma parte del catalogo publicado de `aecf_prompts`.
No se añade a `SKILL_RELEASE.json`.
No se distribuye como skill base del framework.

## Cuándo usarlo

Usalo cuando necesites cualquiera de estas cosas y no quieras que vivan en AECF base:

1. Criterios especificos de productividad de un proyecto.
2. Lenguaje de negocio propio de un cliente.
3. Reglas de interpretacion de calidad o riesgo locales.
4. Convenciones de arquitectura que no son universales.
5. Reglas de documentacion o onboarding propias de un equipo.

## Cuándo no usarlo

No lo uses para:

1. Cambiar gates, fases o contratos obligatorios de AECF.
2. Saltarte testing, auditorias o metadata.
3. Crear un skill oficial nuevo del framework.
4. Guardar secretos, credenciales o datos sensibles.

## Modelo recomendado

Separa siempre estas dos capas:

1. Skill base de AECF.
   Ejemplo: `productivity`, `new_feature`, `refactor`.
2. Guía local del proyecto.
   Ejemplo: `project-productivity-metrics`, `legacy-billing-rules`, `client-doc-style`.

La idea es que el skill base siga siendo comun y mantenible, mientras que el external skill solo aporta contexto local y opt-in.

## Ejemplo de uso para productivity

Supongamos que un proyecto quiere medir productividad con estas dimensiones locales:

1. Consistencia del codigo.
2. Velocidad de desarrollo.
3. Calidad de las code reviews.
4. Calidad de la documentacion tecnica.
5. Facilidad de onboarding.

Eso no deberia entrar en `aecf_prompts` como skill base porque depende del proyecto.

En su lugar, crea esta ruta en el repo cliente:

```text
.agents/
└── skills/
    └── project-productivity-metrics/
        └── SKILL.md
```

Contenido minimo recomendado:

```markdown
---
name: project-productivity-metrics
description: Complementa analisis de productividad con criterios especificos del proyecto para consistencia de codigo, velocidad, calidad de review, documentacion tecnica y onboarding.
---

# Project Productivity Metrics

## Skill Goal

Complement the base productivity analysis with project-local interpretation rules.

## Domain Context

- In this project, code consistency means low post-review churn, low architectural drift, and low lint/test regressions after merge.
- Development speed must be interpreted together with topic closure and rework signals, never as raw speed alone.
- Review quality must consider number of review cycles, reopened findings, and escaped defects.
- Technical documentation quality must consider freshness, coverage of changed modules, and operational usefulness.
- Onboarding quality must consider time to first accepted contribution and rework rate in the first topics.

## Recommended Steps

1. Use the base AECF evidence first.
2. Apply these local interpretation rules only when the repository evidence supports them.
3. If evidence for a metric is missing, mark the metric as uncovered instead of inferring it.

## Test Scenarios

- Missing review evidence does not become a negative score automatically.
- High speed with high rework must be reported as unstable throughput.
- Strong topic closure with low rework should be interpreted as healthy flow.

## Security Checks

- Do not include credentials, internal tokens, or private URLs.
- Do not ask AECF to bypass its mandatory gates or metadata.
```

## Cómo invocarlo

En un flujo que admita `external_skills=`, la idea es invocarlo junto al skill base.

Ejemplo conceptual:

```text
use skill=productivity TOPIC=team_health prompt=Analizar productividad del equipo de backend entre 2026-01-01 y 2026-03-31 external_skills=project-productivity-metrics
```

Si tu host usa una sintaxis tipo `@aecf`, el equivalente seria:

```text
@aecf run skill=productivity TOPIC=team_health prompt="Analizar productividad del equipo de backend entre 2026-01-01 y 2026-03-31" external_skills=project-productivity-metrics
```

Si el host prompt-only no puede leer archivos del workspace por si mismo, pega o adjunta tambien el contenido de `.agents/skills/project-productivity-metrics/SKILL.md` junto a la invocacion.

## Que gana el proyecto con este enfoque

1. El conocimiento local vive dentro del repo cliente.
2. `aecf_prompts` sigue limpio y generico.
3. El equipo puede versionar sus criterios junto a su codigo.
4. Se puede cambiar el criterio por proyecto sin tocar el framework.

## Regla practica

Si una regla vale solo para un cliente, un producto o un repositorio, ponla en un external skill local.

Si la regla debe aplicar a todos los usuarios de AECF, entonces evalua convertirla en parte del framework.

## Limitacion importante

Esta guia documenta el patron de desarrollo y uso de external skills como complemento local.

No convierte automaticamente ese archivo local en un skill oficial de `aecf_prompts`, ni debe hacerlo.

## Conclusion corta

Para el menor cambio posible:

1. Mantener `productivity` como skill base.
2. Crear `project-productivity-metrics` como external skill local en `.agents/skills/`.
3. Pasarlo solo cuando ese proyecto necesite sus metricas propias.
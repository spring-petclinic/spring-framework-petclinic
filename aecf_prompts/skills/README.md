# README - skills

LAST_REVIEW: 2026-04-15

## Descripción objetivo
Esta carpeta agrupa activos y recursos de AECF para el ámbito "aecf_prompts/skills", con el objetivo de mantener una estructura trazable, reutilizable y consistente en el flujo de trabajo del proyecto.

## Responsabilidad dentro de AECF
Dentro de AECF, esta carpeta es responsable de centralizar artefactos de su dominio, facilitar mantenimiento/evolución por área funcional y preservar la separación de responsabilidades con el resto de módulos.

## Regla operativa
Esta carpeta es la superficie fuente prompt-only para el catalogo completo de skills.

- Edita aqui el catalogo completo de skills.
- Usa `aecf_prompts/skills/SKILL_RELEASE.json` para decidir que skills entran en el bundle cliente.
- Regenera las copias del componente y la copia embebida con `node aecf_test_participant/embed-prompts.js`.

El task de bundle publica solo el subconjunto permitido por `SKILL_RELEASE.json` segun el `bundle-mode` elegido.

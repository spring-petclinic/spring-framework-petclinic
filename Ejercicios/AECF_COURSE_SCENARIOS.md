# 10 Escenarios AECF para Curso con PetClinic

> Base: Spring Framework PetClinic — Spring 7, Java 17, Jakarta EE, 3 capas (Controller → Service → Repository), 3 implementaciones de persistencia intercambiables.

---

## Escenario 1 — `aecf_explain_behaviour`: Las 3 estrategias de persistencia y el cambio de perfil

**¿Por qué es interesante?**
Este proyecto incluye tres implementaciones completas del mismo contrato de repositorio: JPA pura con `EntityManager`, JDBC con `JdbcClient`, y Spring Data JPA. Cambiar de una a otra es solo pasar `-Dspring.profiles.active=jdbc`. Un desarrollador que llegue al código frío no entiende por qué existen tres versiones ni cómo funcionan los perfiles.

**¿Qué demuestra?**
- La capacidad de Claude para razonar sobre arquitectura multi-implementación
- Cómo leer XML de configuración y trazar el wiring de beans con perfil condicional
- Que Claude puede comparar implementaciones equivalentes y señalar diferencias de comportamiento

**¿Qué deberíamos ver?**
Claude debe identificar los tres paquetes (`jpa/`, `jdbc/`, `springdatajpa/`), leer `business-config.xml`, explicar cómo Spring activa los beans según perfil, y producir una tabla comparativa de los tres enfoques con sus trade-offs de rendimiento.

**Prompt AECF:**
```
@aecf run skill=aecf_explain_behaviour TOPIC=persistence_strategies prompt="Explica cómo funciona el sistema de repositorios de este proyecto. Hay tres implementaciones del mismo contrato (JPA, JDBC, Spring Data JPA) activadas por Spring profiles. ¿Por qué existen las tres, cómo se activa cada una y cuáles son sus trade-offs de rendimiento?"
```

---

## Escenario 2 — `aecf_new_feature`: Paginación en el listado de propietarios

**¿Por qué es interesante?**
`OwnerController.processFindForm()` devuelve TODOS los owners que coincidan con el apellido buscado. Si hay miles de registros, la consulta devuelve todo. Es un bug de rendimiento realista y la feature de paginación es clásica en aplicaciones Spring MVC.

**¿Qué demuestra?**
- Cómo Claude navega del controlador al repositorio para entender el flujo completo antes de proponer cambios
- Que debe modificar la capa de servicio, el repositorio y la vista JSP de forma coherente
- Gestión del estado de paginación en una petición GET stateless

**¿Qué deberíamos ver?**
Claude debe proponer cambios en `OwnerRepository` (añadir `Pageable`), `ClinicService`, `OwnerController`, y la vista `ownersList.jsp` para renderizar los controles de página. Debería también proponer un test de controlador.

**Prompt AECF:**
```
@aecf run skill=aecf_new_feature TOPIC=owner_pagination prompt="Añadir paginación al listado de búsqueda de owners en OwnerController.processFindForm(). Actualmente devuelve todos los resultados sin límite. Mostrar 5 resultados por página con controles de siguiente/anterior. Modificar OwnerRepository, ClinicService, OwnerController y la vista ownersList.jsp."
```

---

## Escenario 3 — `aecf_refactor`: Eliminar el acoplamiento de EAGER loading

**¿Por qué es interesante?**
`Pet.visits` está mapeado como `FetchType.EAGER` en `src/main/java/org/springframework/samples/petclinic/model/Pet.java`. Esa elección acopla el modelo a una estrategia de carga concreta y oculta si realmente se necesita materializar `visits` en todos los recorridos. Además, el código ya ofrece una vía alternativa para cargar visitas por separado en `ClinicServiceImpl.findVisitsByPetId(int)`, lo que hace verificable que existe margen para desacoplar esa relación.

**¿Qué demuestra?**
- Refactor guiado por evidencia: Claude debe partir del mapeo real en `Pet.java` y de los puntos de acceso a `pet.getVisits()` para justificar si conviene pasar a `LAZY`
- Razonamiento sobre side effects: cambiar EAGER a LAZY puede romper otros puntos de carga
- Búsqueda de todos los puntos de uso antes de modificar

**¿Qué deberíamos ver?**
Claude debe encontrar el `@OneToMany(fetch = FetchType.EAGER)` en `Pet.java`, rastrear todos los puntos donde se accede a `pet.getVisits()` fuera de contexto transaccional, identificar si esos accesos pueden sustituirse por carga explícita desde servicio o por una frontera transaccional correcta, y proponer el refactor sin introducir `LazyInitializationException`.

**Prompt AECF:**
```
@aecf run skill=aecf_refactor TOPIC=eager_loading_fix prompt="El modelo Pet tiene una relación OneToMany con Visit mapeada como FetchType.EAGER en Pet.java. Analizar todos los puntos de acceso a pet.getVisits(), comparar ese acoplamiento con la carga explícita de visitas disponible en ClinicServiceImpl.findVisitsByPetId(int), trazar el impacto de cambiar a LAZY y proponer el refactor correcto sin introducir LazyInitializationException."
```

---

## Escenario 4 — `aecf_document_legacy`: Documentar la configuración XML

**¿Por qué es interesante?**
`business-config.xml`, `mvc-core-config.xml`, `mvc-view-config.xml`, `datasource-config.xml` y `tools-config.xml` son configuración Spring estilo pre-Boot. Para un desarrollador moderno que solo conoce `@SpringBootApplication` y `application.yml`, este XML es opaco.

**¿Qué demuestra?**
- La capacidad de Claude para leer XML de configuración Spring (namespaces, beans, imports, perfiles)
- Generación de documentación técnica precisa desde fuentes primarias
- Traducción entre paradigmas (XML vs. Java Config vs. Boot autoconfiguration)

**¿Qué deberíamos ver?**
Claude debe producir un documento que explique qué hace cada archivo XML, qué beans registra, cómo se relacionan entre sí, y —opcionalmente— su equivalente en Spring Boot si se quisiera migrar. Conviene incluir `mvc-view-config.xml` junto con `mvc-core-config.xml`, porque ahí vive la resolución de vistas y la negociación de contenido de la capa MVC.

**Prompt AECF:**
```
@aecf run skill=aecf_document_legacy TOPIC=spring_xml_config prompt="Documentar los cinco archivos de configuración XML en src/main/resources/spring/ (business-config.xml, mvc-core-config.xml, mvc-view-config.xml, datasource-config.xml, tools-config.xml). Para cada uno: qué beans registra, cómo se relaciona con los demás, qué perfiles Spring activa, y su equivalente conceptual en Spring Boot. Explicar además por qué mvc-core-config.xml y mvc-view-config.xml están separados dentro de la configuración MVC."
```

---

## Escenario 5 — `aecf_new_test_set`: Cubrir el repositorio JDBC

**¿Por qué es interesante?**
`ClinicServiceJdbcTests` hereda de `AbstractClinicServiceTests` y se ejecuta con perfil `jdbc`, pero los tests son genéricos. Los detalles específicos de JDBC —como el `SimpleJdbcInsert`, el `RowMapper` personalizado o el manejo de tipos— no están probados de forma aislada.

**¿Qué demuestra?**
- Que Claude puede analizar cobertura de tests existentes y detectar gaps
- Generación de tests orientados a la implementación, no solo al contrato
- Uso correcto de bases de datos embebidas (H2) para tests de integración

**¿Qué deberíamos ver?**
Claude debe leer `JdbcOwnerRepositoryImpl`, identificar lógica específica no cubierta (ej: el extractor de ResultSet para owners con múltiples pets), y generar tests que verifiquen el comportamiento del mapeo de datos.

**Prompt AECF:**
```
@aecf run skill=aecf_new_test_set TOPIC=jdbc_repository_tests prompt="Analizar la cobertura de tests del repositorio JDBC (JdbcOwnerRepositoryImpl, JdbcPetRepositoryImpl). Los tests actuales en ClinicServiceJdbcTests solo cubren el contrato genérico. Identificar los gaps en lógica específica de JDBC: RowMapper, ResultSetExtractor para owners con múltiples pets, SimpleJdbcInsert, y manejo de tipos. Generar los tests de integración que faltan usando perfil jdbc con H2."
```

---

## Escenario 6 — `aecf_explain_behaviour`: El aspecto de monitorización y su punto ciego

**¿Por qué es interesante?**
`CallMonitoringAspect` usa AOP para contar llamadas y medir tiempos en repositorios. Pero hay un comentario en el código: los repositorios de Spring Data JPA son proxies de interfaz y el aspecto no los intercepta correctamente. Es un bug arquitectural con causa técnica profunda.

**¿Qué demuestra?**
- Razonamiento sobre AOP, proxies dinámicos y la jerarquía de proxies de Spring
- Capacidad de Claude para leer el comentario de advertencia, reproducir el problema conceptualmente y explicar por qué ocurre
- Proponer una solución (ej: AspectJ weaving, cambiar la estrategia de selección del advice, usar mecanismos específicos de Spring Data)

**¿Qué deberíamos ver?**
Claude debe leer `CallMonitoringAspect.java`, explicar el mecanismo de proxy de Spring Data JPA, y describir por qué el pointcut real `within(@org.springframework.stereotype.Repository *)` deja fuera a los proxies generados para los repositorios de Spring Data JPA, aunque sí funciona con las implementaciones JPA y JDBC anotadas directamente.

**Prompt AECF:**
```
@aecf run skill=aecf_explain_behaviour TOPIC=aop_monitoring_aspect prompt="CallMonitoringAspect usa AOP para monitorizar repositorios pero no funciona con Spring Data JPA. Explicar por qué el pointcut real within(@org.springframework.stereotype.Repository *) selecciona las clases concretas anotadas con @Repository pero deja fuera a los proxies de interfaz generados por Spring Data JPA, qué mecanismo de proxy los diferencia de los repositorios JPA y JDBC del proyecto, y qué opciones existen para solucionar ese punto ciego."
```

---

## Escenario 7 — `aecf_new_feature`: Endpoint REST para vets con OpenAPI

**¿Por qué es interesante?**
`VetController` ya expone una vista HTML en `GET /vets` y dos endpoints serializados separados en `GET /vets.json` y `GET /vets.xml`. Eso obliga a razonar sobre si conviene documentar la API tal como existe hoy o consolidarla primero hacia un endpoint REST único con `produces` según `Accept`. La feature es concreta, acotada y demuestra bien el razonamiento sobre capas.

**¿Qué demuestra?**
- Cómo Claude amplía un endpoint existente sin romper el comportamiento HTML
- Añadir dependencias Maven, configurar SpringDoc/OpenAPI, y anotar el controlador
- Que Claude distingue entre rutas HTML existentes y endpoints serializados dedicados, o decide refactorizarlos explícitamente hacia una API REST más coherente

**¿Qué deberíamos ver?**
Claude debe partir de los mappings reales de `VetController` (`/vets`, `/vets.json`, `/vets.xml`), decidir explícitamente una de estas dos rutas: documentar la API con esos paths tal como existen hoy, o introducir primero una consolidación hacia un endpoint REST con `produces` según `Accept` sin romper la vista HTML. Después debe añadir la dependencia de SpringDoc OpenAPI a `pom.xml`, crear un `VetRestController` (o refactorizar explícitamente los endpoints serializados existentes), añadir anotaciones `@Operation`/`@ApiResponse`, y verificar que el endpoint `/v3/api-docs` funciona.

**Prompt AECF:**
```
@aecf run skill=aecf_new_feature TOPIC=vet_rest_api prompt="Añadir documentación OpenAPI al área de veterinarios partiendo de los paths reales del repo. VetController hoy expone la vista HTML en GET /vets y los formatos serializados en GET /vets.json y GET /vets.xml; no asumir que ya existe negociación por Accept en /vets. Decide explícitamente si conviene documentar esos endpoints tal como están o hacer primero una consolidación hacia un endpoint REST único con produces según Accept sin romper la vista HTML. Después añade SpringDoc OpenAPI al pom.xml, anota el controlador o extrae un VetRestController con @Operation y @ApiResponse, y asegura que /v3/api-docs y swagger-ui están disponibles."
```

---

## Escenario 8 — `aecf_security_review`: Revisar la seguridad del controlador de propietarios

**¿Por qué es interesante?**
`OwnerController` recibe parámetros de formulario directamente en objetos de dominio. Aunque usa `@InitBinder` para bloquear el campo `id`, hay otras superficies de ataque: mass assignment de otros campos, ausencia de CSRF explícito, y una ruta `/oups` que lanza una excepción intencionada.

**¿Qué demuestra?**
- Análisis de seguridad sobre código real, no ejemplos artificiales
- Claude identificando mecanismos de protección existentes y sus gaps
- Propuestas concretas de mejora con su justificación técnica

**¿Qué deberíamos ver?**
Claude debe revisar `OwnerController`, `PetController`, `PetclinicInitializer`, identificar la ausencia de Spring Security, el `@InitBinder`, la validación con `@NotEmpty`/`@Digits`, y generar un informe con vulnerabilidades potenciales y recomendaciones priorizadas.

**Prompt AECF:**
```
@aecf run skill=aecf_security_review TOPIC=controller_security prompt="Revisar la seguridad de la capa web de PetClinic. Analizar OwnerController, PetController, VisitController y PetclinicInitializer. Superficie de ataque: binding directo de formularios a entidades de dominio, @InitBinder como única protección contra mass assignment, ausencia de Spring Security, ruta /oups expuesta, y validación con @NotEmpty/@Digits. Generar informe CVSS con recomendaciones priorizadas."
```

---

## Escenario 9 — `aecf_refactor`: Migrar configuración XML a Java Config

**¿Por qué es interesante?**
Todo el wiring de beans está en XML (`business-config.xml`, etc.). Es un refactor de modernización puro: convertir a `@Configuration` classes sin cambiar el comportamiento observable. Es exactamente el tipo de tarea que una IA puede hacer de forma sistemática si entiende bien la semántica del XML.

**¿Qué demuestra?**
- Que Claude puede transformar XML Spring a Java Config de forma mecánica pero correcta
- Manejo de casos no triviales: `<context:component-scan>`, `<aop:aspectj-autoproxy>`, `<jdbc:initialize-database>`, y los tres perfiles de persistencia
- Verificación de que los tests siguen pasando tras el refactor

**¿Qué deberíamos ver?**
Claude debe producir clases `@Configuration` equivalentes para cada XML, mantener los perfiles `@Profile("jpa")`, `@Profile("jdbc")` etc., y proponer cómo eliminar los XML del classpath de forma gradual y segura.

**Prompt AECF:**
```
@aecf run skill=aecf_refactor TOPIC=xml_to_java_config prompt="Migrar la configuración Spring de XML a Java Config. Empezar por business-config.xml: contiene EntityManagerFactory, TransactionManager, component-scan y tres perfiles (jpa, jdbc, spring-data-jpa). Producir clases @Configuration equivalentes conservando los @Profile, sin cambiar el comportamiento observable, y proponer una estrategia de migración gradual que no rompa los tests existentes."
```

---

## Escenario 10 — `aecf_new_feature`: Internacionalización completa con selector de locale

**¿Por qué es interesante?**
El proyecto tiene bundles de mensajes `messages.properties`, `messages_en.properties`, `messages_es.properties` y `messages_de.properties`, pero no hay ningún mecanismo en la UI para que el usuario cambie de idioma. Los mensajes de validación están parcialmente internacionalizados. Es un feature incompleto y real.

**¿Qué demuestra?**
- Análisis de una feature a medio implementar: Claude debe descubrir el estado actual antes de proponer qué falta
- Añadir un `LocaleChangeInterceptor` y un selector de idioma en la cabecera de la aplicación
- Entender cómo Spring MVC resuelve mensajes y cómo los mensajes de validación JSR-303 se localizan

**¿Qué deberíamos ver?**
Claude debe leer `mvc-core-config.xml` para ver si hay `LocaleResolver` configurado, revisar los ficheros de mensajes para detectar gaps entre idiomas, y proponer añadir el interceptor de cambio de locale + un selector en el layout JSP.

**Prompt AECF:**
```
@aecf run skill=aecf_new_feature TOPIC=i18n_locale_selector prompt="El proyecto tiene bundles de mensajes en src/main/resources/messages/ (`messages.properties`, `messages_en.properties`, `messages_es.properties`, `messages_de.properties`) pero no hay ningún mecanismo en la UI para cambiar de idioma. Analizar qué LocaleResolver y LocaleChangeInterceptor están configurados en mvc-core-config.xml, detectar gaps de cobertura entre los ficheros de mensajes, e implementar el selector de idioma completo: interceptor Spring MVC + widget en el layout JSP."
```

---

## Resumen de cobertura de skills AECF

| # | Escenario | Skill AECF | Tier | Complejidad |
|---|-----------|-----------|------|-------------|
| 1 | 3 estrategias de persistencia | `aecf_explain_behaviour` | TIER1 | Media |
| 2 | Paginación en owners | `aecf_new_feature` | TIER3 | Media |
| 3 | Refactor EAGER loading | `aecf_refactor` | TIER3 | Alta |
| 4 | Documentar XML config | `aecf_document_legacy` | TIER2 | Baja |
| 5 | Cobertura tests JDBC | `aecf_new_test_set` | TIER3 | Media |
| 6 | AOP y punto ciego | `aecf_explain_behaviour` | TIER1 | Alta |
| 7 | REST + OpenAPI | `aecf_new_feature` | TIER3 | Media |
| 8 | Security review | `aecf_security_review` | TIER1 | Media |
| 9 | XML → Java Config | `aecf_refactor` | TIER3 | Alta |
| 10 | i18n completa | `aecf_new_feature` | TIER3 | Media |

---

## Notas pedagógicas

- **Escenarios 1, 4, 6** son ideales para mostrar la capacidad de Claude de **leer y explicar** código que nadie documenta.
- **Escenarios 2, 7, 10** muestran **new_feature con Claude guiando el análisis previo** antes de escribir código.
- **Escenarios 3, 9** son los más exigentes: refactors donde **el riesgo de romper cosas es real** y Claude debe trazar impactos.
- **Escenario 5** es ideal para discutir **qué tests tienen valor real** vs. tests que solo suben el coverage.
- **Escenario 8** introduce el **rol de Claude como revisor de seguridad**, útil para mostrar sus límites y aciertos.

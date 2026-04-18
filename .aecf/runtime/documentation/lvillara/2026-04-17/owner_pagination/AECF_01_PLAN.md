# AECF_01 — Plan: Owner Pagination
## TOPIC: owner_pagination

---

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-17T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_new_feature TOPIC=owner_pagination prompt="Añadir paginación al listado de búsqueda de owners en OwnerController.processFindForm()..."` |
| Skill Executed | aecf_new_feature |
| Sequence Position | 1 of N |
| Total Prompts Executed | 1 |
| Phase | PHASE 1 — PLAN |

---

## 1. FEATURE DESCRIPTION

Añadir paginación al listado de búsqueda de owners en `OwnerController.processFindForm()`. Actualmente devuelve todos los resultados sin límite. Se requiere:

- **5 resultados por página** (PAGE_SIZE = 5, constante)
- **Controles de siguiente/anterior** en la vista
- Preservar el **comportamiento actual de redirección** cuando hay exactamente 1 resultado
- Soportar los **3 perfiles de persistencia** (jpa, jdbc, spring-data-jpa)

---

## 2. SCOPE

### Archivos a modificar

| Archivo | Tipo de cambio | Perfil |
|---------|---------------|--------|
| `src/main/java/.../repository/OwnerRepository.java` | Añadir 2 métodos de interfaz | todos |
| `src/main/java/.../repository/jpa/JpaOwnerRepositoryImpl.java` | Implementar los 2 métodos | jpa |
| `src/main/java/.../repository/jdbc/JdbcOwnerRepositoryImpl.java` | Implementar los 2 métodos | jdbc |
| `src/main/java/.../repository/springdatajpa/SpringDataOwnerRepository.java` | Declarar los 2 métodos con `@Query` | spring-data-jpa |
| `src/main/java/.../service/ClinicService.java` | Añadir 2 métodos de interfaz | todos |
| `src/main/java/.../service/ClinicServiceImpl.java` | Implementar los 2 métodos | todos |
| `src/main/java/.../web/OwnerController.java` | Modificar `processFindForm` | todos |
| `src/main/webapp/WEB-INF/jsp/owners/ownersList.jsp` | Añadir controles de paginación | todos |

### Archivos de test a modificar/crear

| Archivo | Tipo de cambio |
|---------|---------------|
| `src/test/java/.../service/AbstractClinicServiceTests.java` | Añadir tests de paginación |

---

## 3. DISEÑO TÉCNICO

### 3.1 Nuevos métodos en la capa de repositorio

**`OwnerRepository.java`** — Añadir:

```java
/**
 * Retrieve a page of Owners from the data store by last name.
 * @param lastName Value to search for (prefix match)
 * @param page 1-based page number
 * @param pageSize number of results per page
 * @return Collection of matching Owners for the requested page
 */
Collection<Owner> findByLastName(String lastName, int page, int pageSize);

/**
 * Count Owners whose last name starts with the given prefix.
 * @param lastName prefix to search
 * @return total count of matching Owners
 */
int countByLastName(String lastName);
```

### 3.2 Implementaciones por perfil

#### Perfil `jpa` — `JpaOwnerRepositoryImpl`

```java
public Collection<Owner> findByLastName(String lastName, int page, int pageSize) {
    Query query = this.em.createQuery(
        "SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets " +
        "WHERE owner.lastName LIKE :lastName ORDER BY owner.lastName, owner.id");
    query.setParameter("lastName", lastName + "%");
    query.setFirstResult((page - 1) * pageSize);
    query.setMaxResults(pageSize);
    return query.getResultList();
}

public int countByLastName(String lastName) {
    Query query = this.em.createQuery(
        "SELECT COUNT(DISTINCT owner) FROM Owner owner WHERE owner.lastName LIKE :lastName");
    query.setParameter("lastName", lastName + "%");
    return ((Long) query.getSingleResult()).intValue();
}
```

**Nota técnica JPA**: `setFirstResult`/`setMaxResults` sobre una query con `join fetch` genera una advertencia Hibernate `HHH90003004` cuando hay colecciones (`pets`) en el fetch. Hibernate aplica el paginado in-memory para garantizar la correctitud de la colección fetch. Para N pequeños (búsquedas de texto) en una demo pedagógica este trade-off es aceptable. La alternativa sería dos queries (count + IDs + reload), que queda documentada como mejora futura.

#### Perfil `jdbc` — `JdbcOwnerRepositoryImpl`

```java
public Collection<Owner> findByLastName(String lastName, int page, int pageSize) {
    int offset = (page - 1) * pageSize;
    List<Owner> owners = this.jdbcClient.sql("""
            SELECT id, first_name, last_name, address, city, telephone
            FROM owners
            WHERE last_name LIKE :lastName
            ORDER BY last_name, id
            LIMIT :limit OFFSET :offset
            """)
        .param("lastName", lastName + "%")
        .param("limit", pageSize)
        .param("offset", offset)
        .query(BeanPropertyRowMapper.newInstance(Owner.class))
        .list();
    loadOwnersPetsAndVisits(owners);
    return owners;
}

public int countByLastName(String lastName) {
    return this.jdbcClient.sql("""
            SELECT COUNT(*) FROM owners WHERE last_name LIKE :lastName
            """)
        .param("lastName", lastName + "%")
        .query(Integer.class)
        .single();
}
```

**Nota técnica JDBC**: `LIMIT`/`OFFSET` es sintaxis H2/MySQL/PostgreSQL compatible. La base de datos H2 (default) soporta esta sintaxis. Para HSQLDB se usaría `FETCH FIRST n ROWS ONLY` — fuera del scope actual (solo H2/MySQL/PostgreSQL en pom.xml DB profiles activos).

#### Perfil `spring-data-jpa` — `SpringDataOwnerRepository`

```java
@Query("SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets " +
       "WHERE owner.lastName LIKE :lastName% ORDER BY owner.lastName, owner.id")
Collection<Owner> findByLastName(@Param("lastName") String lastName, Pageable pageable);

@Query("SELECT COUNT(DISTINCT owner) FROM Owner owner WHERE owner.lastName LIKE :lastName%")
int countByLastName(@Param("lastName") String lastName);
```

**Nota técnica Spring Data JPA**: Spring Data admite `Pageable` como parámetro adicional en métodos `@Query`. El proxy aplica `setFirstResult`/`setMaxResults` automáticamente. La firma en `OwnerRepository` usa `int page, int pageSize` (para uniformidad con JDBC); `SpringDataOwnerRepository` sobreescribe el método con `Pageable` y la implementación de `ClinicServiceImpl` construye el `PageRequest` antes de llamar al repositorio Spring Data. Para no romper el contrato común, el overload con `Pageable` se declara en `SpringDataOwnerRepository` directamente y `ClinicServiceImpl` inyecta `OwnerRepository` pero hace un cast condicional si el perfil es Spring Data. **Alternativa más limpia**: añadir el método `findByLastName(String, int, int)` directamente en todos los repositorios incluyendo Spring Data, y que la impl Spring Data convierta internamente a `Pageable`. Esta es la opción elegida para mantener el contrato uniforme en `OwnerRepository`.

### 3.3 Nuevos métodos en la capa de servicio

**`ClinicService.java`** — Añadir:

```java
Collection<Owner> findOwnerByLastName(String lastName, int page, int pageSize);
int countOwnersByLastName(String lastName);
```

**`ClinicServiceImpl.java`** — Implementar:

```java
@Override
@Transactional(readOnly = true)
public Collection<Owner> findOwnerByLastName(String lastName, int page, int pageSize) {
    return ownerRepository.findByLastName(lastName, page, pageSize);
}

@Override
@Transactional(readOnly = true)
public int countOwnersByLastName(String lastName) {
    return ownerRepository.countByLastName(lastName);
}
```

### 3.4 Modificación de OwnerController

**Método `processFindForm`** — Lógica actualizada:

```
processFindForm(Owner owner, BindingResult result, @RequestParam(defaultValue="1") int page, Map model)
│
├── lastName = "" si null
├── totalCount = clinicService.countOwnersByLastName(lastName)
│
├── totalCount == 0 → rejectValue → return "owners/findOwners"
├── totalCount == 1 → findOwnerByLastName(lastName, 1, 1) → redirect:/owners/{id}
└── totalCount > 1 →
    │   pageOwners = findOwnerByLastName(lastName, page, PAGE_SIZE)
    │   totalPages = ceil(totalCount / PAGE_SIZE)
    │   model.put("selections", pageOwners)
    │   model.put("currentPage", page)
    │   model.put("totalPages", totalPages)
    │   model.put("totalItems", totalCount)
    │   model.put("lastName", owner.getLastName())
    └── return "owners/ownersList"
```

**Constante de clase**:
```java
private static final int PAGE_SIZE = 5;
```

**Parámetro de URL**: `?page=1`, `?page=2`, etc. Los links next/prev en la vista mantendrán el `lastName` del buscador.

### 3.5 Modificación de ownersList.jsp

Añadir debajo de la tabla:

```jsp
<c:if test="${totalPages > 1}">
  <nav aria-label="Owner search results navigation">
    <ul class="pagination justify-content-center">
      <li class="page-item <c:if test='${currentPage == 1}'>disabled</c:if>">
        <spring:url value="/owners" var="prevUrl">
          <spring:param name="lastName" value="${lastName}"/>
          <spring:param name="page" value="${currentPage - 1}"/>
        </spring:url>
        <a class="page-link" href="${fn:escapeXml(prevUrl)}">&laquo; Previous</a>
      </li>
      <li class="page-item disabled">
        <span class="page-link">Page ${currentPage} of ${totalPages} (${totalItems} results)</span>
      </li>
      <li class="page-item <c:if test='${currentPage == totalPages}'>disabled</c:if>">
        <spring:url value="/owners" var="nextUrl">
          <spring:param name="lastName" value="${lastName}"/>
          <spring:param name="page" value="${currentPage + 1}"/>
        </spring:url>
        <a class="page-link" href="${fn:escapeXml(nextUrl)}">Next &raquo;</a>
      </li>
    </ul>
  </nav>
</c:if>
```

---

## 4. ORDEN DE IMPLEMENTACIÓN

| Paso | Archivo | Acción |
|------|---------|--------|
| 1 | `OwnerRepository.java` | Añadir `findByLastName(String, int, int)` y `countByLastName(String)` |
| 2 | `JpaOwnerRepositoryImpl.java` | Implementar ambos métodos con JPQL + setFirstResult/setMaxResults |
| 3 | `JdbcOwnerRepositoryImpl.java` | Implementar ambos métodos con SQL LIMIT/OFFSET y COUNT(*) |
| 4 | `SpringDataOwnerRepository.java` | Declarar `findByLastName(String, int, int)` y `countByLastName(String)` con `@Query` + `@Modifying` y conversión interna a `PageRequest` |
| 5 | `ClinicService.java` | Añadir `findOwnerByLastName(String, int, int)` y `countOwnersByLastName(String)` |
| 6 | `ClinicServiceImpl.java` | Implementar ambos métodos delegando al repositorio |
| 7 | `OwnerController.java` | Modificar `processFindForm` — añadir `page` param, total count, pagination model attrs |
| 8 | `ownersList.jsp` | Añadir bloque de paginación Bootstrap |
| 9 | `AbstractClinicServiceTests.java` | Añadir tests para los 2 nuevos métodos de servicio |

---

## 5. PRESERVACIÓN DE COMPORTAMIENTO EXISTENTE

| Comportamiento | Estado | Descripción |
|----------------|--------|-------------|
| 0 resultados → error | ✅ Preservado | `countOwnersByLastName == 0` → `rejectValue` |
| 1 resultado → redirect | ✅ Preservado | `countOwnersByLastName == 1` → buscar page=1, pageSize=1 → redirect |
| >1 resultado → lista | ✅ Preservado | Ahora paginada |
| `/owners` sin lastName → busca "" | ✅ Preservado | `lastName == null` → `""` antes del conteo |
| Interfaz ClinicService no rompe | ✅ Preservado | Se añaden overloads, no se eliminan métodos existentes |

---

## 6. ANÁLISIS DE IMPACTO

### Impacto en tests existentes

- `AbstractClinicServiceTests.shouldFindOwnersByLastName()` — **NO AFECTADO**: llama a `findOwnerByLastName(String)` que permanece intacto.
- Los 3 perfiles pasan el mismo test suite — la nueva firma es adicional, no reemplaza.

### Impacto en el perfil Spring Data JPA

`SpringDataOwnerRepository` extiende `OwnerRepository` que declarará `findByLastName(String, int, int)` y `countByLastName(String)`. Spring Data JPA puede inferir queries por nombre de método, pero las firmas con `int, int` no siguen la convención de Spring Data para paginación (que usa `Pageable`). Por ello, **se requieren anotaciones `@Query` explícitas** en `SpringDataOwnerRepository` para estos dos métodos, y la implementación interna construye un `PageRequest` desde los parámetros `int`.

Implementación en `SpringDataOwnerRepository`:

```java
@Override
@Query("SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets " +
       "WHERE owner.lastName LIKE :lastName% ORDER BY owner.lastName, owner.id")
Collection<Owner> findByLastName(@Param("lastName") String lastName,
                                  @Param("page") int page,
                                  @Param("pageSize") int pageSize);
```

**Problema**: Spring Data JPA no puede usar `int page, int pageSize` como parámetros de paginación en JPQL — necesita `Pageable`. Se resuelve con una implementación default en la interfaz `OwnerRepository` que convierte `(page, pageSize)` llamando a la versión paginada interna, o con un `default` method en la interfaz.

**Solución adoptada**: Añadir un método `default` en `OwnerRepository` que construye la paginación, y que `SpringDataOwnerRepository` declare un método con `Pageable` diferente. Para no romper el contrato uniforme, `SpringDataOwnerRepository` implementa `findByLastName(String, int, int)` como método `default` heredado de `OwnerRepository` que internamente llama `findByLastNamePaged(lastName, PageRequest.of(page-1, pageSize))`.

**Implementación final resuelta**:

En `OwnerRepository`:
```java
Collection<Owner> findByLastName(String lastName, int page, int pageSize);
int countByLastName(String lastName);
```

En `SpringDataOwnerRepository`:
```java
// Método Spring Data nativo para paginación interna
@Query("SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets " +
       "WHERE owner.lastName LIKE :lastName% ORDER BY owner.lastName, owner.id")
Collection<Owner> findByLastNamePaged(@Param("lastName") String lastName, Pageable pageable);

@Query("SELECT COUNT(DISTINCT owner) FROM Owner owner WHERE owner.lastName LIKE :lastName%")
int countByLastName(@Param("lastName") String lastName);

// Implementación del contrato OwnerRepository con conversión interna
default Collection<Owner> findByLastName(String lastName, int page, int pageSize) {
    return findByLastNamePaged(lastName, PageRequest.of(page - 1, pageSize));
}
```

---

## 7. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Hibernate in-memory pagination warning (HHH90003004) con `join fetch` + setMaxResults | ALTA | BAJO | Documetar como expected; alternativa dos-query fuera de scope de feature didáctica |
| LIMIT/OFFSET no compatible con HSQLDB | MEDIA | BAJO | HSQLDB profile no está en el path de test activo (pom.xml: H2 default, MySQL, PostgreSQL) |
| `countByLastName` duplicado con `findByLastName` → 2 queries donde antes había 1 para case >1 | ALTA | BAJO | Trade-off de paginación estándar; documentado |
| Spring Data JPA `default` method en interfaz no reconocido por proxy | BAJA | ALTA | Verificar en test; alternativa: mover a `ClinicServiceImpl` con cast a `SpringDataOwnerRepository` si el default no funciona |

---

## 8. CRITERIOS DE ACEPTACIÓN

- [ ] Búsqueda que devuelve >5 resultados muestra solo los primeros 5 con controles de paginación
- [ ] Control "Previous" deshabilitado en página 1
- [ ] Control "Next" deshabilitado en la última página
- [ ] La URL `/owners?lastName=Davis&page=2` devuelve la página 2
- [ ] Búsqueda con 1 resultado redirige directamente al owner (comportamiento preservado)
- [ ] Búsqueda sin resultados muestra mensaje de error (comportamiento preservado)
- [ ] Tests pasan en los 3 profiles (jpa, spring-data-jpa, jdbc)
- [ ] Ningún test existente roto

---

## 9. OUT OF SCOPE

- Ordenación configurable por columna
- Tamaño de página configurable por el usuario
- Paginación de VetController o PetController
- HSQLDB compatibility para LIMIT/OFFSET
- Índice de páginas numéricas (1, 2, 3... N)
- Benchmarking del N+1 del profile JDBC con paginación

---

## Gate

PENDING AUDIT

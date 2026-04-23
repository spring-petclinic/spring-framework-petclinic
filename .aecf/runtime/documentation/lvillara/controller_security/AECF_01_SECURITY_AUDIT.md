# AECF Security Audit — Web Layer Controller Security

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-18T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_security_review TOPIC=controller_security` |
| Skill Executed | aecf_security_review |
| Sequence Position | 1 |
| Total Prompts Executed | 1 |

---

## WORKING_CONTEXT (Discovery)

| Field | Value |
|-------|-------|
| **Target Scope** | Web layer: OwnerController, PetController, VisitController, CrashController, PetclinicInitializer, PetValidator, VetRestController, mvc-core-config.xml |
| **Entry Points** | `PetclinicInitializer.java` — Servlet 3.0 bootstrap, `DispatcherServlet` mapped to `/` |
| **Discovered Paths** | See Sources below |
| **Auth Layer** | ABSENT — Spring Security not present |
| **CSRF Protection** | ABSENT |
| **Security Headers** | NOT configured in mvc-core-config.xml |
| **Exception Handling** | `SimpleMappingExceptionResolver` → `exception.jsp` |
| **Discovery Status** | ✅ GO |

**Sources**:
- [OwnerController.java](src/main/java/org/springframework/samples/petclinic/web/OwnerController.java)
- [PetController.java](src/main/java/org/springframework/samples/petclinic/web/PetController.java)
- [VisitController.java](src/main/java/org/springframework/samples/petclinic/web/VisitController.java)
- [CrashController.java](src/main/java/org/springframework/samples/petclinic/web/CrashController.java)
- [PetValidator.java](src/main/java/org/springframework/samples/petclinic/web/PetValidator.java)
- [VetRestController.java](src/main/java/org/springframework/samples/petclinic/web/VetRestController.java)
- [PetclinicInitializer.java](src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java)
- [mvc-core-config.xml](src/main/resources/spring/mvc-core-config.xml)

**Uncertainties**:
- JSP files not read — XSS risk via unescaped output not fully confirmed (assumed partial JSTL escaping)
- Runtime environment may add WAF or reverse-proxy security headers (unverifiable statically)

---

## Executive Summary

| Severity | Count | CVSS Range |
|----------|-------|------------|
| <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">CRITICAL</span> | **2** | 9.1 – 9.8 |
| <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span> | **3** | 6.5 – 7.5 |
| <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span> | **5** | 4.3 – 5.3 |
| <span style="background:#198754;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">LOW</span> | **2** | 2.1 – 3.1 |
| **Total** | **12** | |

> **VERDICT**: <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">NO-GO</span>
>
> 2 CRITICAL vulnerabilities block deployment. The application has zero authentication and zero authorization — every data mutation endpoint is publicly accessible without any credential check.

---

## 🗂️ Sections Analyzed — Navigation Index

| # | Section Analyzed | Findings | Link |
|---|-----------------|----------|------|
| 1 | OWASP A01: Broken Access Control | <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">CRITICAL</span> ×2, <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span> ×1 | [→ Findings](#owasp-a01-broken-access-control) |
| 2 | OWASP A03: Injection | 0 findings | — |
| 3 | OWASP A04: Insecure Design — Mass Assignment | <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span> ×1 | [→ Findings](#owasp-a04-insecure-design--mass-assignment) |
| 4 | OWASP A05: Security Misconfiguration | <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span> ×1, <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span> ×2 | [→ Findings](#owasp-a05-security-misconfiguration) |
| 5 | OWASP A07: Identification and Authentication Failures | <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">CRITICAL</span> ×1 (see A01) | — |
| 6 | OWASP A09: Security Logging & Monitoring Failures | <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span> ×1 | [→ Findings](#owasp-a09-security-logging--monitoring-failures) |
| 7 | Input Validation & Data Enumeration | <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span> ×1, <span style="background:#198754;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">LOW</span> ×2 | [→ Findings](#input-validation--data-enumeration) |
| 8 | Rate Limiting | <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span> ×1 | [→ Findings](#rate-limiting) |
| 9 | Secrets & Credentials | 0 findings | — |
| 10 | Dependency CVEs | INFO only — not in scope of this audit | — |

---

## Detailed Findings

### OWASP A01: Broken Access Control

---

#### [CRIT-001] Ausencia total de autenticación — Todos los endpoints accesibles sin credenciales

**Severity**: <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">CRITICAL</span>
**CVSS 3.1**: **9.8** (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
**OWASP**: A07: Identification and Authentication Failures / A01: Broken Access Control
**Rule**: SEC-AUTH-01

**Location**: All controllers — no authentication filter present in the application

| Endpoint | Method | Risk |
|----------|--------|------|
| `/owners/new` | POST | Create arbitrary owners |
| `/owners/{ownerId}/edit` | POST | Modify any owner |
| `/owners/{ownerId}/pets/new` | POST | Add pets to any owner |
| `/owners/{ownerId}/pets/{petId}/edit` | POST | Modify any pet |
| `/owners/{ownerId}/pets/{petId}/visits/new` | POST | Create visits for any pet |
| `/owners` | GET | Enumerate all owner records |
| `/api/vets` | GET | Expose full vet roster |

**Evidence**:
- [PetclinicInitializer.java:76-79](src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java#L76) — `getServletFilters()` returns only `CharacterEncodingFilter`. No `SecurityFilterChain` present.
- `pom.xml` — `spring-security-*` dependency absent (confirmed via project context).
- [mvc-core-config.xml](src/main/resources/spring/mvc-core-config.xml) — No `<security:*>` namespace elements.

**Impact**: Any unauthenticated user on the network can create, read, update, and delete all veterinary practice data.

🔧 **Execute**:
```
@aecf run skill=aecf_new_feature topic=controller_security prompt="Add Spring Security dependency and configure SecurityFilterChain with form-based authentication. Protect all /owners/** and /api/** endpoints. Permit GET /vets and GET / anonymously. File: pom.xml + PetclinicInitializer.java"
```

---

#### [CRIT-002] IDOR en PetController — Pet no validado contra ownerId del path

**Severity**: <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">CRITICAL</span>
**CVSS 3.1**: **9.1** (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N)
**OWASP**: A01: Broken Access Control
**Rule**: SEC-AUTHZ-01

**Location**:
- [PetController.java:93-97](src/main/java/org/springframework/samples/petclinic/web/PetController.java#L93) — `initUpdateForm`
- [PetController.java:99-109](src/main/java/org/springframework/samples/petclinic/web/PetController.java#L99) — `processUpdateForm`

**Vulnerable pattern**:
```java
// PetController.java:93-97
@GetMapping(value = "/pets/{petId}/edit")
public String initUpdateForm(@PathVariable("petId") int petId, ModelMap model) {
    Pet pet = this.clinicService.findPetById(petId);  // No ownership check
    model.put("pet", pet);
    return VIEWS_PETS_CREATE_OR_UPDATE_FORM;
}
```

**Exploit scenario**:
1. Attacker knows `petId=99` belongs to `ownerId=5`
2. Attacker requests `GET /owners/1/pets/99/edit`
3. `findOwner(ownerId=1)` loads owner 1 ✓ (no cross-check)
4. `findPetById(99)` loads pet 99 ✓ (no verification that pet 99 ∈ owner 1)
5. Attacker can view and edit pet 99 belonging to another owner

**Same pattern in VisitController**:
- [VisitController.java:70-75](src/main/java/org/springframework/samples/petclinic/web/VisitController.java#L70) — `loadPetWithVisit` loads any petId without owner context verification

🔧 **Execute**:
```
@aecf run skill=aecf_refactor topic=controller_security prompt="Add ownership verification in PetController.initUpdateForm (PetController.java:93) and processUpdateForm (PetController.java:99): verify pet.getOwner().getId() == ownerId from path variable. Same check in VisitController.loadPetWithVisit (VisitController.java:70)."
```

---

#### [HIGH-003] IDOR en VisitController — petId sin verificación de propiedad del owner

**Severity**: <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span>
**CVSS 3.1**: **7.5** (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N)
**OWASP**: A01: Broken Access Control
**Rule**: SEC-AUTHZ-01

**Location**: [VisitController.java:86-90](src/main/java/org/springframework/samples/petclinic/web/VisitController.java#L86)

```java
// VisitController.java:86-90
@GetMapping(value = "/owners/*/pets/{petId}/visits/new")
public String initNewVisitForm(@PathVariable("petId") int petId, Map<String, Object> model) {
    model.put("visits", this.clinicService.findVisitsByPetId(petId));
    return "pets/createOrUpdateVisitForm";
}
```

The wildcard `*` in the GET mapping makes ownerId completely unchecked. Combined with the `@ModelAttribute("visit")` loading any petId in `loadPetWithVisit`, any pet's visit history is accessible and new visits can be created via POST `/owners/1/pets/99/visits/new` for a pet belonging to owner 5.

🔧 **Execute**:
```
@aecf run skill=aecf_refactor topic=controller_security prompt="Replace wildcard * with {ownerId} in VisitController GET mapping (VisitController.java:86). Add ownership verification: pet loaded in loadPetWithVisit must belong to ownerId from path. Reject with 403 if not."
```

---

### OWASP A04: Insecure Design — Mass Assignment

---

#### [HIGH-001] Mass Assignment vía binding directo a entidades — Enfoque blacklist

**Severity**: <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span>
**CVSS 3.1**: **7.5** (AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N)
**OWASP**: A04: Insecure Design
**Rule**: SEC-INPUT-01

**Location**:
- [OwnerController.java:49-52](src/main/java/org/springframework/samples/petclinic/web/OwnerController.java#L49) — `setAllowedFields`
- [VisitController.java:45-48](src/main/java/org/springframework/samples/petclinic/web/VisitController.java#L45) — `setAllowedFields`
- [PetController.java:59-62](src/main/java/org/springframework/samples/petclinic/web/PetController.java#L59) — `initOwnerBinder`

**Pattern**:
```java
// OwnerController.java:49-52
@InitBinder
public void setAllowedFields(WebDataBinder dataBinder) {
    dataBinder.setDisallowedFields("id");  // blacklist — only 'id' blocked
}
```

Controllers bind HTTP form parameters directly to JPA domain entities (`Owner`, `Visit`) using a **blacklist** approach. Only the `id` field is disallowed. Any field added to the entity model in the future (e.g., `role`, `creditLimit`, `internalNotes`) would be automatically bindable from HTTP requests.

Spring's `WebDataBinder.setAllowedFields()` (allowlist) is the secure alternative — it requires explicitly declaring every field that may be bound, rejecting all others by default.

**Affected controllers and entities**:

| Controller | Entity | Blacklisted Only |
|------------|--------|------------------|
| `OwnerController` | `Owner` (firstName, lastName, address, city, telephone) | `id` |
| `VisitController` | `Visit` (date, description) | `id` |
| `PetController` | `Owner` (via `initOwnerBinder`) | `id` |

🔧 **Execute**:
```
@aecf run skill=aecf_refactor topic=controller_security prompt="Replace setDisallowedFields('id') with setAllowedFields(allowlist) in OwnerController.java:49, VisitController.java:45, and PetController.java:59. For Owner: allow firstName, lastName, address, city, telephone. For Visit: allow date, description. For Pet (PetValidator already in place): allow name, birthDate, type."
```

---

### OWASP A05: Security Misconfiguration

---

#### [HIGH-002] Ausencia de protección CSRF en endpoints de mutación de estado

**Severity**: <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span>
**CVSS 3.1**: **6.5** (AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N)
**OWASP**: A05: Security Misconfiguration / A01: Broken Access Control
**Rule**: SEC-CSRF-01 (MATRIX-PENDING → ✅ AUTO-APPLIED)

**Location**: All POST endpoints — no CSRF mechanism present

```java
// OwnerController.java:61-68
@PostMapping(value = "/owners/new")
public String processCreationForm(@Valid Owner owner, BindingResult result) {
    // No CSRF token checked — Spring Security CSRF filter absent
    this.clinicService.saveOwner(owner);
    return "redirect:/owners/" + owner.getId();
}
```

Spring Security provides CSRF protection by default when configured. Since Spring Security is absent, there is no CSRF filter in the `FilterChain`. An attacker can forge cross-origin POST requests that the browser will submit with the victim's session cookies (if sessions are ever introduced).

**Affected endpoints**: All 5 POST mutation endpoints (owners/new, owners/edit, pets/new, pets/edit, visits/new).

🔧 **Execute**:
```
@aecf run skill=aecf_new_feature topic=controller_security prompt="Enable CSRF protection. Primary path: add Spring Security with CSRF filter enabled (default behavior). Alternative without Spring Security: add custom CsrfFilter or Synchronizer Token Pattern in mvc-core-config.xml. Ensure JSP forms include the CSRF token hidden field."
```

---

#### [MED-001] Security HTTP headers ausentes — Sin CSP, X-Frame-Options, HSTS

**Severity**: <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span>
**CVSS 3.1**: **5.3** (AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)
**OWASP**: A05: Security Misconfiguration
**Rule**: SEC-CONF-02

**Location**: [mvc-core-config.xml](src/main/resources/spring/mvc-core-config.xml) — no header filter registered

Missing headers:

| Header | Risk if Absent |
|--------|----------------|
| `Content-Security-Policy` | XSS amplification, inline script execution |
| `X-Frame-Options: DENY` | Clickjacking |
| `X-Content-Type-Options: nosniff` | MIME sniffing attacks |
| `Strict-Transport-Security` | SSL stripping |
| `Referrer-Policy` | URL leakage in Referer header |

🔧 **Execute** (optional for MEDIUM):
```
@aecf run skill=aecf_refactor topic=controller_security prompt="Add security HTTP response headers to mvc-core-config.xml. Register a ShallowEtagHeaderFilter or custom OncePerRequestFilter that sets X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Content-Security-Policy: default-src 'self', Referrer-Policy: no-referrer. Alternatively, configure via Spring Security .headers() if Spring Security is added."
```

---

#### [MED-002] Ruta /oups (CrashController) accesible en producción — information disclosure

**Severity**: <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span>
**CVSS 3.1**: **5.3** (AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)
**OWASP**: A05: Security Misconfiguration
**Rule**: SEC-INFO-01 (MATRIX-PENDING → ✅ AUTO-APPLIED)

**Location**: [CrashController.java:33](src/main/java/org/springframework/samples/petclinic/web/CrashController.java#L33)

```java
@GetMapping(value = "/oups")
public String triggerException() {
    throw new RuntimeException("Expected: controller used to showcase what " +
        "happens when an exception is thrown");
}
```

This intentional crash endpoint is a demo/teaching artifact. It deliberately triggers an exception visible to any unauthenticated user. The `SimpleMappingExceptionResolver` maps it to `exception.jsp`, which may expose stack frames, internal class names, or application version information depending on its implementation.

**Risk**: In production, this endpoint:
1. Reveals the existence of error-handling infrastructure
2. May expose internal class names in the exception message
3. Creates a trivially exploitable denial-of-experience route

---

### OWASP A09: Security Logging & Monitoring Failures

---

#### [MED-004] Sin logging de eventos de seguridad

**Severity**: <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span>
**CVSS 3.1**: **4.3** (AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N)
**OWASP**: A09: Security Logging and Monitoring Failures
**Rule**: SEC-LOG-01

**Location**: All controllers — no security event logging present

No controller logs:
- Unauthorized access attempts
- Data mutation events (owner/pet/visit created/modified)
- Validation failures that may indicate attack probing
- Access to the `/oups` crash endpoint

The `CallMonitoringAspect` via JMX tracks invocation counts but does not produce security audit logs. Logback is configured (`logback.xml`) but no security-specific logger or appender is defined.

---

### Input Validation & Data Enumeration

---

#### [MED-003] Owner search con lastName vacío enumera todos los propietarios

**Severity**: <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span>
**CVSS 3.1**: **5.3** (AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)
**OWASP**: A01: Broken Access Control (data enumeration)
**Rule**: SEC-ENUM-01 (MATRIX-PENDING → ✅ AUTO-APPLIED)

**Location**: [OwnerController.java:86-112](src/main/java/org/springframework/samples/petclinic/web/OwnerController.java#L86)

```java
@GetMapping(value = "/owners")
public String processFindForm(Owner owner, BindingResult result, ...) {
    if (owner.getLastName() == null) {
        owner.setLastName("");  // Empty string → LIKE '%' → all owners returned
    }
    // ...
}
```

A request to `GET /owners` (no `lastName` parameter) returns all owners paginated. Combined with zero authentication, any unauthenticated user can enumerate the complete database of owner names, addresses, telephone numbers, and pets by iterating pages.

---

#### [LOW-001] PetValidator — Validación de tipo omitida en formulario de edición

**Severity**: <span style="background:#198754;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">LOW</span>
**CVSS 3.1**: **3.1** (AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N)
**OWASP**: A04: Insecure Design
**Rule**: SEC-INPUT-02

**Location**: [PetValidator.java:48-50](src/main/java/org/springframework/samples/petclinic/web/PetValidator.java#L48)

```java
// type validation
if (pet.isNew() && pet.getType() == null) {  // Only validated for new pets
    errors.rejectValue("type", REQUIRED, REQUIRED);
}
```

Pet type is only validated for new pets. On the edit form, a null pet type passes validation and may be persisted depending on database constraints. Low risk as `PetType` is a FK with a not-null constraint at DB level, but the gap creates an inconsistency.

---

#### [LOW-002] CharacterEncodingFilter con forceEncoding=true sin validación de Content-Type

**Severity**: <span style="background:#198754;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">LOW</span>
**CVSS 3.1**: **2.1** (AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N)
**OWASP**: A05: Security Misconfiguration (low impact)
**Rule**: Mapped to existing LOW context — NO_ADD_RULE

**Location**: [PetclinicInitializer.java:76-79](src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java#L76)

```java
CharacterEncodingFilter characterEncodingFilter = new CharacterEncodingFilter("UTF-8", true);
```

`forceEncoding=true` overrides any encoding declared in the request `Content-Type` header. In modern browsers and HTTP/2 stacks this is benign. Theoretical risk: a crafted request with a malicious encoding declaration is silently overridden rather than rejected, making charset confusion attacks impractical. No rule addition needed.

---

### Rate Limiting

---

#### [MED-005] Sin rate limiting en ningún endpoint

**Severity**: <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span>
**CVSS 3.1**: **5.3** (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N)
**OWASP**: A05: Security Misconfiguration
**Rule**: SEC-RATE-01

No rate limiting is configured at the application layer. Combined with the absence of authentication, the following abuse scenarios are trivial:
- Mass creation of owners/pets/visits via automated scripts
- Enumeration of all owners by scraping paginated results
- Flooding the `/oups` endpoint to fill logs

---

## Attack Vectors Summary

| Attack | Vector | Exploitability | Impact |
|--------|--------|---------------|--------|
| Unauthenticated data mutation | Network | Trivial (no credentials needed) | High — all data modifiable |
| IDOR pet/visit cross-owner | Network | Trivial (known numeric IDs) | High — any record readable/modifiable |
| CSRF-forced mutation | Browser XSS or external site | Requires victim interaction | High — all POST endpoints forgeable |
| Mass assignment future risk | Network | Low (no current dangerous fields) | Medium — latent risk on schema change |
| Owner data enumeration | Network | Trivial | Medium — full PII exposure |
| Demo endpoint abuse | Network | Trivial | Low — info disclosure |

---

## Analysis by OWASP Category

| OWASP Category | Status | Findings |
|----------------|--------|----------|
| A01: Broken Access Control | 🔴 FAIL | CRIT-001, CRIT-002, HIGH-003, MED-003 |
| A02: Cryptographic Failures | ✅ N/A | No crypto operations in scope |
| A03: Injection | ✅ PASS | No SQL/command injection detected in controllers (JPA/named params used) |
| A04: Insecure Design | 🟠 FAIL | HIGH-001 (mass assignment blacklist) |
| A05: Security Misconfiguration | 🔴 FAIL | HIGH-002 (CSRF), MED-001 (headers), MED-002 (/oups), MED-005 (rate limiting) |
| A06: Vulnerable Components | ⚠️ NOT AUDITED | Run `aecf_dependency_audit` for CVE scan |
| A07: Auth Failures | 🔴 FAIL | CRIT-001 |
| A08: Software & Data Integrity | 🟠 FAIL | HIGH-002 (CSRF — data integrity failures) |
| A09: Logging & Monitoring | 🟠 FAIL | MED-004 |
| A10: SSRF | ✅ PASS | No user-controlled URL fetch detected |

---

## Prioritized Mitigation Plan

### <span style="background:#dc3545;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">CRITICAL</span> — Block deployment immediately

| ID | Finding | Effort | Skill |
|----|---------|--------|-------|
| CRIT-001 | Add Spring Security + authentication | High (2-5 days) | `aecf_new_feature` |
| CRIT-002 | Add pet→owner ownership verification | Low (2h) | `aecf_refactor` |

### <span style="background:#fd7e14;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">HIGH</span> — Fix before next release or compensate with WAF

| ID | Finding | Effort | Skill |
|----|---------|--------|-------|
| HIGH-001 | Replace blacklist with allowlist in @InitBinder | Low (1h) | `aecf_refactor` |
| HIGH-002 | Enable CSRF protection | Medium (1 day, part of Spring Security) | `aecf_new_feature` |
| HIGH-003 | Fix wildcard in VisitController + ownership check | Low (2h) | `aecf_refactor` |

### <span style="background:#0d6efd;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">MEDIUM</span> — Fix in current or next sprint

| ID | Finding | Effort | Skill |
|----|---------|--------|-------|
| MED-001 | Add security HTTP headers | Low (2h) | `aecf_refactor` |
| MED-002 | Remove or gate `/oups` endpoint in production | Low (30min) | `aecf_refactor` |
| MED-003 | Require authentication before owner enumeration | Part of CRIT-001 | `aecf_new_feature` |
| MED-004 | Add security event logging | Low (2h) | `aecf_refactor` |
| MED-005 | Add rate limiting | Medium (1 day) | `aecf_new_feature` |

### <span style="background:#198754;color:#fff;padding:2px 8px;border-radius:4px;font-weight:bold;font-size:0.85em">LOW</span> — Backlog

| ID | Finding | Recommendation |
|----|---------|----------------|
| LOW-001 | PetValidator type gap on edit | Accept or fix with explicit type check on update |
| LOW-002 | CharacterEncodingFilter forceEncoding | Accept — theoretical risk, no practical exploit |

---

## Classification Decision Log — MATRIX-PENDING Findings

| Finding | Location | Proposed Rule ID | Provisional Severity | Decision | Rationale |
|---------|----------|-----------------|---------------------|----------|-----------|
| CSRF protection absent | All POST controllers | SEC-CSRF-01 | HIGH | ✅ AUTO-APPLIED | Repeatable pattern (all 5 POST endpoints), CVSS 6.5, leads to unauthorized data modification, not covered by existing rules |
| Demo route in production | [CrashController.java:33](src/main/java/org/springframework/samples/petclinic/web/CrashController.java#L33) | SEC-INFO-01 | MEDIUM | ✅ AUTO-APPLIED | Project-specific pattern, CVSS 5.3, information disclosure, distinct from existing SEC-CONF-01/02 |
| Owner enumeration via empty search | [OwnerController.java:90](src/main/java/org/springframework/samples/petclinic/web/OwnerController.java#L90) | SEC-ENUM-01 | MEDIUM | ✅ AUTO-APPLIED | Repeatable pattern (could affect other search endpoints), CVSS 5.3, data exposure, not in existing rules |
| CharacterEncodingFilter forceEncoding | [PetclinicInitializer.java:77](src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java#L77) | N/A | LOW | NO_ADD_RULE | Theoretical risk only, no practical exploit path in this context, no new rule warranted |
| PetValidator type gap on edit | [PetValidator.java:48](src/main/java/org/springframework/samples/petclinic/web/PetValidator.java#L48) | N/A | LOW | NO_ADD_RULE | Already covered by SEC-INPUT-02 (missing validation on non-critical field) |

**Summary**: 3 ADD_RULE (all ✅ AUTO-APPLIED to matrix v1.3), 2 NO_ADD_RULE

**Matrix version after this audit**: **v1.3** (bumped from template baseline v1 → v1.1 → v1.2 → v1.3)

---

## Security Settings Review

| Setting | Status | Finding |
|---------|--------|---------|
| Spring Security | ❌ ABSENT | CRIT-001 |
| CSRF filter | ❌ ABSENT | HIGH-002 |
| Security headers | ❌ NOT CONFIGURED | MED-001 |
| HTTPS enforcement | ⚠️ UNKNOWN | Cannot verify without runtime config |
| Session management | ⚠️ DEFAULT | No explicit session timeout configured |
| Exception handling | ✅ PRESENT | `SimpleMappingExceptionResolver` in mvc-core-config.xml |
| Input encoding | ✅ PRESENT | CharacterEncodingFilter UTF-8 |
| Bean Validation | ✅ PRESENT | `@Valid` + Hibernate Validator 9.1.0.Final on all forms |

---

## Secrets & Credentials

✅ No hardcoded secrets detected in controller layer.
- No API keys, tokens, or passwords in the audited files.
- DB credentials are externalized via Spring profiles in `datasource-config.xml`.

---

## Dependency Analysis (Scope: Informational Only)

Full CVE analysis not in scope for this skill execution. Notable observations:

| Library | Version | Action |
|---------|---------|--------|
| Hibernate ORM | 7.3.0.Final | Run `aecf_dependency_audit` |
| Jackson | 3.1.1 | Run `aecf_dependency_audit` |
| SpringDoc OpenAPI | 2.8.0 | Run `aecf_dependency_audit` |

🔧 **Recommended follow-up**:
```
@aecf run skill=aecf_dependency_audit topic=controller_security prompt="Audit all dependencies in pom.xml for known CVEs. Focus on Hibernate ORM 7.3.0.Final, Jackson 3.1.1, SpringDoc 2.8.0, and Spring Framework 7.0.6."
```

---

## VERDICT

> ## 🚫 NO-GO
>
> **Reason**: 2 CRITICAL vulnerabilities present.
>
> 1. **CRIT-001** — Zero authentication on all mutation endpoints (CVSS 9.8)
> 2. **CRIT-002** — IDOR: pet ownership not verified against URL ownerId (CVSS 9.1)
>
> **Minimum to achieve CONDITIONAL GO**:
> - Add authentication layer (Spring Security, any form)
> - Add pet→owner ownership verification in PetController and VisitController
>
> **Minimum to achieve GO**:
> - All CRITICAL resolved
> - All HIGH resolved or compensated
> - MEDIUM findings documented with residual risk acceptance

---

*Generated by `aecf_security_review` | TOPIC: controller_security | Prompt-only mode*
*Severity matrix bootstrapped at: `.aecf/runtime/documentation/AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md` (v1.3)*

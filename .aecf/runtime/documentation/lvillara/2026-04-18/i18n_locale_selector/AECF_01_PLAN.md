# AECF — Plan: i18n Locale Selector

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-18T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_new_feature TOPIC=i18n_locale_selector` |
| Skill Executed | aecf_new_feature |
| Sequence Position | 1 |
| Total Prompts Executed | 7 |

---

## Feature Description

Add a user-visible language selector to the PetClinic UI so visitors can switch between English, Spanish, and German. The application already has translated message bundles but no mechanism to change locale at runtime.

---

## Current State Analysis

### What exists

| Component | Status | Detail |
|-----------|--------|--------|
| `messageSource` | ✅ Configured | `ResourceBundleMessageSource`, basename `messages/messages` |
| `messages.properties` (default/EN) | ✅ 8 keys | `welcome`, `required`, `notFound`, `duplicate`, `nonNumeric`, `duplicateFormSubmission`, `typeMismatch.date`, `typeMismatch.birthDate` |
| `messages_en.properties` | ✅ Empty (fallback) | Intentionally empty; all lookups fall to default |
| `messages_es.properties` | ✅ 8 keys (complete) | Full Spanish translations |
| `messages_de.properties` | ✅ 8 keys (complete) | Full German translations |
| `LocaleResolver` | ❌ ABSENT | Default `AcceptHeaderLocaleResolver` active — reads browser Accept-Language, cannot be changed by user |
| `LocaleChangeInterceptor` | ❌ ABSENT | No `<mvc:interceptors>` block in `mvc-core-config.xml` |
| Language selector UI | ❌ ABSENT | No widget in `menu.tag`, `layout.tag`, or any JSP |

### Message Bundle Gap Analysis

| Key | messages.properties | messages_es | messages_de | messages_en |
|-----|---------------------|-------------|-------------|-------------|
| `welcome` | ✅ | ✅ | ✅ | (fallback) |
| `required` | ✅ | ✅ | ✅ | (fallback) |
| `notFound` | ✅ | ✅ | ✅ | (fallback) |
| `duplicate` | ✅ | ✅ | ✅ | (fallback) |
| `nonNumeric` | ✅ | ✅ | ✅ | (fallback) |
| `duplicateFormSubmission` | ✅ | ✅ | ✅ | (fallback) |
| `typeMismatch.date` | ✅ | ✅ | ✅ | (fallback) |
| `typeMismatch.birthDate` | ✅ | ✅ | ✅ | (fallback) |
| `lang.selector.label` | ❌ MISSING | ❌ | ❌ | ❌ |
| `lang.en` | ❌ MISSING | ❌ | ❌ | ❌ |
| `lang.es` | ❌ MISSING | ❌ | ❌ | ❌ |
| `lang.de` | ❌ MISSING | ❌ | ❌ | ❌ |

**Gap verdict**: Existing 8 keys are fully covered across all locales. The 4 new keys for the selector widget are absent from all files.

---

## Acceptance Criteria

1. **AC-1**: User can switch language by clicking EN / ES / DE links in the navbar.
2. **AC-2**: Selected locale persists in a session cookie (`PETCLINIC_LOCALE`) for the browser session.
3. **AC-3**: The welcome message renders in the selected language (uses `welcome` key from `messageSource`).
4. **AC-4**: Language switch works on any page (interceptor is global).
5. **AC-5**: No regression on existing 87 tests.

---

## Implementation Plan

### Step A: `mvc-core-config.xml` — Add LocaleResolver + LocaleChangeInterceptor

Add 3 declarations to `mvc-core-config.xml`:

**1. `CookieLocaleResolver`** (bean id must be exactly `localeResolver`):
```xml
<bean id="localeResolver"
      class="org.springframework.web.servlet.i18n.CookieLocaleResolver">
    <property name="defaultLocale" value="en"/>
    <property name="cookieName" value="PETCLINIC_LOCALE"/>
    <property name="cookieMaxAge" value="-1"/>
</bean>
```
- `CookieLocaleResolver` chosen over `SessionLocaleResolver`: cookie persists browser session; safer if session is invalidated.
- `defaultLocale=en`: falls back to English when no cookie present.
- `cookieMaxAge=-1`: session cookie (deleted when browser closes). Set to `86400` (24h) for persistent preference.

**2. `LocaleChangeInterceptor`**:
```xml
<bean id="localeChangeInterceptor"
      class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor">
    <property name="paramName" value="lang"/>
</bean>
```
- Intercepts any request with `?lang=XX` query parameter.
- Calls `LocaleResolver.setLocale()` before handler execution.

**3. `<mvc:interceptors>`**:
```xml
<mvc:interceptors>
    <ref bean="localeChangeInterceptor"/>
</mvc:interceptors>
```

### Step B: Message Bundles — Add Selector Keys

Add 4 keys to `messages.properties` (EN default):
```properties
lang.selector.label=Language
lang.en=English
lang.es=Spanish
lang.de=German
```

Add to `messages_es.properties`:
```properties
lang.selector.label=Idioma
lang.en=Inglés
lang.es=Español
lang.de=Alemán
```

Add to `messages_de.properties`:
```properties
lang.selector.label=Sprache
lang.en=Englisch
lang.es=Spanisch
lang.de=Deutsch
```

Leave `messages_en.properties` unchanged (intentionally falls back to default).

### Step C: `menu.tag` — Add Language Selector Widget

Add a language selector on the right side of the Bootstrap 5 navbar, inside the collapsible div, after the existing `<ul class="navbar-nav me-auto ...">` group.

```jsp
<%-- Language selector — links to current page with ?lang=XX intercepted by LocaleChangeInterceptor --%>
<ul class="navbar-nav ms-2">
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="langDropdown"
           role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <span class="fa fa-globe"></span>
            <fmt:message key="lang.selector.label"/>
        </a>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="langDropdown">
            <li>
                <a class="dropdown-item"
                   href="${pageContext.request.requestURI}?lang=en">
                    <fmt:message key="lang.en"/>
                </a>
            </li>
            <li>
                <a class="dropdown-item"
                   href="${pageContext.request.requestURI}?lang=es">
                    <fmt:message key="lang.es"/>
                </a>
            </li>
            <li>
                <a class="dropdown-item"
                   href="${pageContext.request.requestURI}?lang=de">
                    <fmt:message key="lang.de"/>
                </a>
            </li>
        </ul>
    </li>
</ul>
```

Requires adding `<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>` to `menu.tag`.

---

## Files to Modify

| File | Change Type |
|------|------------|
| `src/main/resources/spring/mvc-core-config.xml` | Add LocaleResolver + LocaleChangeInterceptor + mvc:interceptors |
| `src/main/resources/messages/messages.properties` | Add 4 lang.* keys |
| `src/main/resources/messages/messages_es.properties` | Add 4 lang.* keys |
| `src/main/resources/messages/messages_de.properties` | Add 4 lang.* keys |
| `src/main/webapp/WEB-INF/tags/menu.tag` | Add language selector dropdown |

## Files to Create

| File | Purpose |
|------|---------|
| `src/test/java/.../web/LocaleChangeInterceptorTests.java` | Verify interceptor + cookie behavior |

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| R1: Bean `localeResolver` must have exactly that id — Spring MVC looks it up by convention | LOW | Explicit `id="localeResolver"` in XML |
| R2: `LocaleChangeInterceptor` not registered globally → only works for some paths | LOW | `<mvc:interceptors>` without path restriction = all requests |
| R3: `?lang=` param conflicts with pagination `?page=` param | LOW | Different param names; no conflict |
| R4: JSP forward URLs include `requestURI` but lose query string | LOW | `requestURI` gives path only; `?lang=xx` replaces any existing lang param |
| R5: Existing tests with `standaloneSetup` may be affected if they use a locale-sensitive message | LOW | Standalonesetup bypasses interceptors; no impact |

---

_Document generated by `aecf_new_feature` | Phase 1/7 | TOPIC: i18n_locale_selector_

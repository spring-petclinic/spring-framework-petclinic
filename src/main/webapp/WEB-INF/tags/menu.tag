<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="petclinic" tagdir="/WEB-INF/tags" %>
<%@ attribute name="name" required="true" rtexprvalue="true"
              description="Name of the active menu: home, owners, vets or error" %>

<%--
  AECF_META: skill=aecf_new_feature topic=i18n_locale_selector run_time=2026-04-18T00:00:00Z
             generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
             last_modified_skill=aecf_new_feature last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
  Language selector dropdown added to the right side of the navbar.
  Links append ?lang=XX to the current request URI; LocaleChangeInterceptor handles the switch.
--%>

<nav class="navbar navbar-expand-lg navbar-dark" role="navigation">
    <div class="container-fluid">
        <a class="navbar-brand" href="<spring:url value="/" htmlEscape="true" />"><span></span></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#main-navbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="main-navbar">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">

                <petclinic:menuItem active="${name eq 'home'}" url="/" title="home page" glyph="fa-home">
                    <span>Home</span>
                </petclinic:menuItem>

                <petclinic:menuItem active="${name eq 'owners'}" url="/owners/find"
                                    title="find owners" glyph="fa-search">
                    <span>Find owners</span>
                </petclinic:menuItem>

                <petclinic:menuItem active="${name eq 'vets'}" url="/vets"
                                    title="veterinarians" glyph="fa-th-list">
                    <span>Veterinarians</span>
                </petclinic:menuItem>

                <petclinic:menuItem active="${name eq 'error'}" url="/oups"
                            title="trigger a RuntimeException to see how it is handled"
                            glyph="exclamation-triangle">
                    <span>Error</span>
                </petclinic:menuItem>

            </ul>

            <%-- Language selector: Bootstrap 5 dropdown on the right side of the navbar --%>
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

        </div>
    </div>
</nav>

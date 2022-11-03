<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="petclinic" tagdir="/WEB-INF/tags" %>
<%@ attribute name="name" required="true" rtexprvalue="true"
              description="Name of the active menu: home, owners, vets or error" %>

<nav class="navbar navbar-expand-lg navbar-dark" role="navigation">
    <div class="container-fluid">
        <a class="navbar-brand" href="<spring:url value="/" htmlEscape="true" />"><span></span></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#main-navbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="main-navbar" style>
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
        </div>
    </div>
</nav>

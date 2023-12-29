<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>

<%@ attribute name="active" required="true" rtexprvalue="true" %>
<%@ attribute name="url" required="true" rtexprvalue="true" %>
<%@ attribute name="title" required="false" rtexprvalue="true" %>
<%@ attribute name="glyph" required="false" rtexprvalue="true" %>

<li class="${active ? 'nav-item' : ''}">
    <a class="${active ? 'nav-link active' : 'nav-link'}" href="<spring:url value="${url}" htmlEscape="true" />"
       title="${fn:escapeXml(title)}">
        <span class="fa ${glyph}"></span>
        <jsp:doBody/>
    </a>
</li>

<%@ page session="false" trimDirectiveWhitespaces="true" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="petclinic" tagdir="/WEB-INF/tags" %>

<petclinic:layout pageName="owners">
    <h2 id="owners">Owners</h2>

    <table id="ownersTable" class="table table-striped" aria-describedby="owners">
        <thead>
        <tr>
            <th scope="col" style="width: 150px;">Name</th>
            <th scope="col" style="width: 200px;">Address</th>
            <th scope="col">City</th>
            <th scope="col" style="width: 120px">Telephone</th>
            <th scope="col">Pets</th>
        </tr>
        </thead>
        <tbody>
        <c:forEach items="${selections}" var="owner">
            <tr>
                <td>
                    <spring:url value="/owners/{ownerId}" var="ownerUrl">
                        <spring:param name="ownerId" value="${owner.id}"/>
                    </spring:url>
                    <a href="${fn:escapeXml(ownerUrl)}"><c:out value="${owner.firstName} ${owner.lastName}"/></a>
                </td>
                <td>
                    <c:out value="${owner.address}"/>
                </td>
                <td>
                    <c:out value="${owner.city}"/>
                </td>
                <td>
                    <c:out value="${owner.telephone}"/>
                </td>
                <td>
                    <c:forEach var="pet" items="${owner.pets}">
                        <c:out value="${pet.name} "/>
                    </c:forEach>
                </td>
            </tr>
        </c:forEach>
        </tbody>
    </table>

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
</petclinic:layout>

# Lab 1: In-App AI with RAG (Assistive AI)

**Theme:** AI answers questions inside the application  
**Duration:** ~7 hours  
**Prerequisites:** Completed Lab 0

---

## Overview

Lab 0 identified opportunities. Lab 1 builds the first AI feature: **natural-language Q&A grounded strictly in PetClinic data**.

This is **Assistive AI**—AI that augments understanding without replacing human judgment or changing workflows. You ask it questions; it retrieves and synthesizes answers from existing data. No hallucinations. No external knowledge. No automation.

### The Core Teaching Moment

> **"This is not automation—this is augmented understanding."**

RAG is fundamentally about *giving decision-makers better context*. A vet doesn't need a machine to make the diagnosis; they need fast access to the right information. This lab teaches that AI's first job is information retrieval and synthesis, not replacement of human judgment.

---

## Learning Objectives

By the end of this lab, you will:

1. **Understand how RAG systems work** — retrieve relevant context, synthesize answers, ground in source data
2. **Design retrieval for a specific domain** — index PetClinic entities (owners, pets, visits, clinical notes)
3. **Build confidence in augmentation** — learn why RAG is more powerful and safer than automation
4. **Know when RAG is the right pattern** — decision support yes, autonomous decision-making no
5. **Evaluate RAG quality** — accuracy of retrieval, relevance to questions, user trust in citations
6. **Implement end-to-end** — from index creation through UI integration to live Q&A

---

## Prerequisites

- ✅ Lab 0 completed (you understand the PetClinic domain and have the app running locally)
- Azure subscription with access to:
    - Microsoft Foundry / Azure OpenAI (for LLM inference)
  - Azure AI Search (for semantic search and indexing)
- Python 3.11+ installed for setup and indexing scripts
- Java 17+ and the Maven wrapper available if you want the app-native integration path
- Visual Studio Code or similar editor
- ~7 hours of focused time

> **Note:** If you don't have Azure resources, we'll provide a local vector database alternative (Chroma or Milvus) in the appendix.

---

## Time Estimate

**7 hours** total:
- 1.5 hours: Index setup and data preparation
- 2 hours: Azure AI Search configuration and retrieval testing
- 2 hours: RAG prompt engineering and confidence scoring
- 1 hour: UI integration and citations
- 0.5 hours: Verification and documentation

---

## What This Lab Proves

1. **AI can deliver value without changing workflows.** Staff don't need to learn new interaction patterns; Q&A fits naturally into existing apps.
2. **RAG fits naturally into legacy apps.** You don't refactor the backend; you layer AI on top.
3. **Citations ground trust.** Users trust AI more when they can click through to source records.
4. **Bounded confidence is a feature.** "I don't know" from AI is better than a confident hallucination.

---

## Key Activities

### Activity 1: Index PetClinic Data
- [ ] Extract entities (owners, pets, visits, clinical notes) from the database
- [ ] Chunk and structure data for semantic search
- [ ] Create Azure AI Search index with metadata (entity type, ID, date, clinical relevance)
- [ ] Verify indexing: Can you search by semantic similarity?

### Activity 2: Add Q&A to the UI
- [ ] Create an "Ask about a patient" widget in the PetClinic UI
- [ ] User types a natural-language question
- [ ] System retrieves relevant records (owners, pets, visits)
- [ ] LLM synthesizes a grounded answer with citations

### Activity 3: Enforce Retrieval Bounds
- [ ] Answers cite specific records (no standalone claims)
- [ ] System declines to answer if confidence is low
- [ ] Explain why an answer could not be provided

### Activity 4: Measure and Iterate
- [ ] Test with real questions from the clinic domain
- [ ] Measure accuracy: Does the answer match retrieved data?
- [ ] Measure relevance: Does the answer address the question?
- [ ] Gather user feedback: Do citations build trust?

---

## Step-by-Step Instructions

### Step 1: Set Up Azure Resources

#### 1.1 Create an Azure AI Search Service

1. Open the [Azure Portal](https://portal.azure.com).
2. Click **"Create a resource"** → search for **"Azure AI Search"**.
3. Fill in the form:
   - **Resource group:** Create new (e.g., `petclinic-ai`)
   - **Service name:** `petclinic-search` (must be globally unique)
   - **Region:** Choose your closest region
   - **Pricing tier:** Standard (sufficient for this lab)
4. Click **"Review + Create"** → **"Create"**.
5. Wait for deployment (2-3 minutes). When complete, click **"Go to resource"**.
6. In the left menu, open **Settings** → **Keys** and switch the service to **Role-based access control**. If you still have older clients that use keys, choose **Both** temporarily while you migrate them.
7. Record the **Service Endpoint URL**.
8. In **Access control (IAM)**, assign your local developer identity or dev group these roles:
    - **Search Service Contributor**
    - **Search Index Data Contributor**
    - For production query-only callers, prefer **Search Index Data Reader**
9. Sign in locally with `az login` or Visual Studio using that same Microsoft Entra ID account before you run the sample code.

> **Note:** Azure AI Search defaults to API keys, but Microsoft Learn now recommends RBAC for application access. New role assignments can take 5-10 minutes to propagate, so a fresh `401` or `403` immediately after setup often resolves after a short wait.

#### 1.2 Create a Microsoft Foundry model deployment

1. In the Azure Portal, search for **"Microsoft Foundry"** and click **"Create"**.
2. Fill in the form:
   - **Resource group:** Use the same group as AI Search
   - **Name:** `petclinic-foundry`
   - **Region:** Use a region with gpt-5.2 availability (e.g., East US 2)
3. Click **"Create"** and wait for deployment.
4. Go to the resource. In **Access control (IAM)**, assign the calling user, service principal, or managed identity the **Cognitive Services User** role at the Foundry resource scope.
5. For local development, use your signed-in Microsoft Entra ID identity (`az login` or Visual Studio). For Azure-hosted workloads, enable system-assigned or user-assigned managed identity for the app that will call the model.
6. Click **"Model deployments"** → **"Create new deployment"**. Select:
   - **Model name:** `gpt-5.2`
   - **Model version:** Latest available
   - **Deployment name:** `gpt-5.2`

7. Click **"Create"** and wait.
8. Record the:
    - **Endpoint**
    - **Deployment name**

> **Teaching Moment:** Microsoft Foundry model deployments let you use Azure-hosted GPT models while keeping clinic data inside your tenant boundary. That matters for patient privacy, auditability, and compliance.

> **Identity Note:** `Owner` or `Contributor` alone does **not** grant inference access on Foundry. The caller needs the **Cognitive Services User** role on the Foundry resource.

> **Production Note:** `DefaultAzureCredential` is the recommended local/dev starting point because it works with developer sign-in locally and managed identity in Azure. In production, prefer managed identity explicitly (or a constrained `ChainedTokenCredential`) and disable local auth only after every caller has migrated off keys.

---

### Step 2: Extract and Prepare PetClinic Data

#### 2.1 Create a Python Data Extraction Script

Prefer Python for one-time extraction and indexing tasks. It keeps the setup flow lightweight and matches current Azure SDK examples. Use Java as the app-native alternative when you want to reuse Spring repositories and keep the extraction logic inside the PetClinic codebase.

Install `sqlalchemy` plus the database driver that matches your local datasource, then create `labs/scripts/extract_petclinic_data.py`:

```python
from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, text

DATABASE_URL = os.environ["PETCLINIC_DB_URL"]
OUTPUT_PATH = Path(os.environ.get("PETCLINIC_DOCUMENT_PATH", "labs/data/petclinic-documents.json"))


def fetch_all(connection, sql: str) -> list[dict]:
    return [dict(row._mapping) for row in connection.execute(text(sql))]


def to_iso(value: date | datetime | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return datetime.combine(value, datetime.min.time(), tzinfo=timezone.utc).isoformat()


def build_owner_document(owner: dict, pets: list[dict]) -> dict:
    pet_lines = "\n".join(f"  - {pet['name']} ({pet['pet_type']})" for pet in pets) or "  - None recorded"
    return {
        "id": f"owner-{owner['id']}",
        "entityType": "owner",
        "entityId": str(owner["id"]),
        "text": (
            f"Owner: {owner['first_name']} {owner['last_name']}\n"
            f"Address: {owner['address']}, {owner['city']}\n"
            f"Telephone: {owner['telephone']}\n\n"
            f"Pets:\n{pet_lines}"
        ),
        "summary": f"Owner: {owner['first_name']} {owner['last_name']}",
        "createdDate": datetime.now(timezone.utc).isoformat(),
        "clinicalRelevance": "medium",
    }


def build_pet_document(pet: dict, owner: dict, visits: list[dict]) -> dict:
    visit_lines = "\n".join(
        f"  {visit['visit_date']}: {visit['description']}"
        for visit in visits[:10]
    ) or "  No visits recorded"
    return {
        "id": f"pet-{pet['id']}",
        "entityType": "pet",
        "entityId": str(pet["id"]),
        "text": (
            f"Pet: {pet['name']}\n"
            f"Type: {pet['pet_type']}\n"
            f"Birth Date: {pet['birth_date']}\n"
            f"Owner: {owner['first_name']} {owner['last_name']}\n\n"
            f"Recent Visits:\n{visit_lines}"
        ),
        "summary": f"Pet: {pet['name']} ({pet['pet_type']})",
        "createdDate": to_iso(pet.get("birth_date")),
        "clinicalRelevance": "high",
    }


def build_visit_document(visit: dict, pet: dict, owner: dict) -> dict:
    return {
        "id": f"visit-{visit['id']}",
        "entityType": "visit",
        "entityId": str(visit["id"]),
        "text": (
            f"Visit Date: {visit['visit_date']}\n"
            f"Pet: {pet['name']}\n"
            f"Owner: {owner['first_name']} {owner['last_name']}\n"
            f"Description: {visit['description']}"
        ),
        "summary": f"Visit {visit['visit_date']}: {pet['name']}",
        "createdDate": to_iso(visit.get("visit_date")),
        "clinicalRelevance": "high",
    }


engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    owners = fetch_all(
        connection,
        """
        SELECT id, first_name, last_name, address, city, telephone
        FROM owners
        ORDER BY id
        """,
    )
    pets = fetch_all(
        connection,
        """
        SELECT p.id, p.name, p.birth_date, p.owner_id, t.name AS pet_type
        FROM pets p
        JOIN types t ON t.id = p.type_id
        ORDER BY p.id
        """,
    )
    visits = fetch_all(
        connection,
        """
        SELECT id, pet_id, visit_date, description
        FROM visits
        ORDER BY pet_id, visit_date DESC
        """,
    )

owners_by_id = {owner["id"]: owner for owner in owners}
pets_by_owner = defaultdict(list)
visits_by_pet = defaultdict(list)

for pet in pets:
    pets_by_owner[pet["owner_id"]].append(pet)

for visit in visits:
    visits_by_pet[visit["pet_id"]].append(visit)

documents: list[dict] = []

for owner in owners:
    owner_pets = pets_by_owner[owner["id"]]
    documents.append(build_owner_document(owner, owner_pets))

    for pet in owner_pets:
        pet_visits = visits_by_pet[pet["id"]]
        documents.append(build_pet_document(pet, owner, pet_visits))
        for visit in pet_visits:
            documents.append(build_visit_document(visit, pet, owner))

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(json.dumps(documents, indent=2), encoding="utf-8")
print(f"Wrote {len(documents)} documents to {OUTPUT_PATH}")
```

#### 2.2 Keep Java as the App-Native Alternative

If you want extraction to live inside the Spring application boundary, implement the same document formatting in a Java `CommandLineRunner` or admin-only service that reuses `OwnerRepository`, `PetRepository`, and `VisitRepository`. Use Python for the lab's bootstrap path; use Java when the application itself owns the extraction lifecycle.

#### 2.3 Export Data to JSON

Set `PETCLINIC_DB_URL` to the same datasource your local app uses, then run the extraction:

```text
# Linux/Mac
export PETCLINIC_DB_URL="<sqlalchemy-connection-string>"
python labs/scripts/extract_petclinic_data.py

# Windows
set PETCLINIC_DB_URL=<sqlalchemy-connection-string>
python labs/scripts/extract_petclinic_data.py
```

Verify the output has a structure like:

```json
[
  {
    "id": "owner-1",
    "entityType": "owner",
    "entityId": "1",
    "text": "Owner: John Davis\nAddress: 123 Main St...",
    "summary": "Owner: John Davis",
    "createdDate": "2024-01-15T12:00:00Z",
    "clinicalRelevance": "medium"
  },
  {
    "id": "pet-1",
    "entityType": "pet",
    "entityId": "1",
    "text": "Pet: Bella\nType: Dog\nBreed: Rough Collie...",
    "summary": "Pet: Bella (Dog)",
    "createdDate": "2010-06-24T00:00:00Z",
    "clinicalRelevance": "high"
  }
]
```

> **Note:** Grouping documents at the pet + full-visit-history level (not paragraph level) preserves context and reduces hallucination.

---

### Step 3: Create and Populate the Azure AI Search Index

#### 3.1 Create a Python Search Bootstrap Script

For setup-time index creation and document loading, prefer a standalone Python bootstrap script that uses `DefaultAzureCredential`. This aligns with current Microsoft Learn guidance for Azure AI Search RBAC and keeps secrets out of the lab.

Create `labs/scripts/bootstrap_search_index.py`:

```python
import json
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
)

SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX_NAME", "petclinic-index")
DOCUMENT_PATH = Path(os.environ.get("PETCLINIC_DOCUMENT_PATH", "labs/data/petclinic-documents.json"))

credential = DefaultAzureCredential()

index_client = SearchIndexClient(
    endpoint=SEARCH_ENDPOINT,
    credential=credential,
    audience="https://search.azure.com",
)

search_client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=credential,
    audience="https://search.azure.com",
)

index = SearchIndex(
    name=INDEX_NAME,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="entityType", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="entityId", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchableField(name="text", type=SearchFieldDataType.String),
        SearchableField(name="summary", type=SearchFieldDataType.String),
        SimpleField(name="createdDate", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True),
        SimpleField(name="clinicalRelevance", type=SearchFieldDataType.String, filterable=True),
    ],
    semantic_search=SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="summary"),
                    content_fields=[SemanticField(field_name="text")],
                ),
            )
        ]
    ),
)


def ensure_index() -> None:
    index_client.create_or_update_index(index)
    print(f"✓ Index '{INDEX_NAME}' is ready.")


def load_documents() -> list[dict]:
    return json.loads(DOCUMENT_PATH.read_text(encoding="utf-8"))


def upload_documents(documents: list[dict]) -> None:
    results = search_client.upload_documents(documents=documents)
    succeeded = sum(1 for item in results if item.succeeded)
    print(f"✓ Indexed {succeeded} documents")


def test_queries() -> None:
    for query in [
        "What health issues has Bella had?",
        "Medications for dogs with allergies",
        "Visits in 2024",
    ]:
        print(f"\nQuery: {query}")
        results = search_client.search(
            search_text=query,
            query_type="semantic",
            semantic_configuration_name="default",
            top=3,
        )
        for result in results:
            score = result.get("@search.reranker_score") or result.get("@search.score") or 0
            print(f"  [{score:.2f}] {result['summary']}")


if __name__ == "__main__":
    ensure_index()
    documents = load_documents()
    upload_documents(documents)
    test_queries()
```

#### 3.2 Keep Java as the App-Native Alternative

If you decide the application should own index provisioning later, use the Java Azure SDK builders inside a Spring `CommandLineRunner`, admin endpoint, or deployment task:

```java
import com.azure.core.credential.TokenCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.search.documents.SearchClient;
import com.azure.search.documents.SearchClientBuilder;
import com.azure.search.documents.indexes.SearchIndexClient;
import com.azure.search.documents.indexes.SearchIndexClientBuilder;

TokenCredential credential = new DefaultAzureCredentialBuilder().build();

SearchIndexClient indexClient = new SearchIndexClientBuilder()
    .endpoint(System.getenv("AZURE_SEARCH_ENDPOINT"))
    .credential(credential)
    .buildClient();

SearchClient searchClient = new SearchClientBuilder()
    .endpoint(System.getenv("AZURE_SEARCH_ENDPOINT"))
    .indexName(System.getenv("AZURE_SEARCH_INDEX_NAME"))
    .credential(credential)
    .buildClient();
```

This keeps the lab aligned with the Java app while still using Python as the preferred setup path.

#### 3.3 Run the Index Initialization

Install the Azure SDK packages and run the bootstrap script:

```text
# Linux/Mac
python -m pip install azure-identity azure-search-documents
export AZURE_SEARCH_ENDPOINT="https://petclinic-search.search.windows.net"
export AZURE_SEARCH_INDEX_NAME="petclinic-index"
export PETCLINIC_DOCUMENT_PATH="labs/data/petclinic-documents.json"
# Optional when using a user-assigned managed identity:
export AZURE_CLIENT_ID="<managed-identity-client-id>"
python labs/scripts/bootstrap_search_index.py

# Windows
python -m pip install azure-identity azure-search-documents
set AZURE_SEARCH_ENDPOINT=https://petclinic-search.search.windows.net
set AZURE_SEARCH_INDEX_NAME=petclinic-index
set PETCLINIC_DOCUMENT_PATH=labs/data/petclinic-documents.json
REM Optional when using a user-assigned managed identity:
set AZURE_CLIENT_ID=<managed-identity-client-id>
python labs/scripts/bootstrap_search_index.py
```

> **Troubleshooting:** `DefaultAzureCredential` uses your signed-in developer tools locally and managed identity in Azure. If you see `401` or `403`, verify Azure AI Search is configured for RBAC (or **Both** during migration), your identity has **Search Service Contributor** and **Search Index Data Contributor**, and allow a few minutes for role propagation. For query-only production callers, reduce permissions to **Search Index Data Reader**.

You should see output like:

```
✓ Index 'petclinic-index' created successfully.
Loading documents from JSON...
✓ Indexed 42 documents

--- Testing Semantic Search ---
Query: What health issues has Bella had?
  [87%] Pet: Bella (Dog)
  [76%] Visit 2024-01-15: Ear infection
  [72%] Visit 2023-10-22: Ear infection
```

> **Teaching Moment:** This proves that semantic search understands *meaning*, not just keywords. The query mentions "health issues" but the index found "ear infection"—semantic alignment.

---

### Step 4: Implement RAG in the Java application

#### 4.1 Create a Java RAG service

Create `src/main/java/org/springframework/samples/petclinic/service/RagKernelService.java`:

```java
package org.springframework.samples.petclinic.service;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.semanticfunctions.KernelArguments;

@Service
public class RagKernelService {

    private final Kernel kernel;
    private final RagSearchService ragSearchService;

    public RagKernelService(Kernel kernel, RagSearchService ragSearchService) {
        this.kernel = kernel;
        this.ragSearchService = ragSearchService;
    }

    public RagResponse answerQuestion(String question) {
        List<RetrievalResult> retrievedDocs = ragSearchService.search(question, 5);

        double avgConfidence = retrievedDocs.stream()
            .mapToDouble(RetrievalResult::confidence)
            .average()
            .orElse(0.0d);

        if (avgConfidence < 0.5d) {
            return new RagResponse(
                question,
                "I don't have enough information to confidently answer this question. Please provide more context or check the clinical records directly.",
                avgConfidence,
                List.of(),
                retrievedDocs.size(),
                "Low retrieval confidence"
            );
        }

        String retrievedRecords = retrievedDocs.stream()
            .map(doc -> "[" + doc.entityType().toUpperCase() + "] " + doc.summary() + "\n" + doc.text())
            .collect(Collectors.joining("\n\n"));

        String answer = kernel.invokePromptAsync(
            """
            You are a veterinary assistant helping clinic staff answer questions about patient records.

            INSTRUCTIONS:
            1. Answer ONLY based on the provided clinical records below.
            2. If information is not in the records, say 'I don't have data on that.'
            3. Cite which record(s) support each claim.
            4. Be concise and clinical in tone.

            CLINICAL RECORDS:
            {{$retrieved_records}}

            QUESTION: {{$question}}

            ANSWER:
            """,
            KernelArguments.builder()
                .withVariable("question", question)
                .withVariable("retrieved_records", retrievedRecords)
                .build())
            .block()
            .getResult();

        return new RagResponse(
            question,
            answer,
            Math.min(1.0d, avgConfidence * (retrievedDocs.size() >= 2 ? 1.1d : 1.0d)),
            retrievedDocs.stream().map(Citation::from).toList(),
            retrievedDocs.size(),
            null
        );
    }

    public record RagResponse(
        String question,
        String answer,
        double confidence,
        List<Citation> citations,
        int retrievedCount,
        String declinedReason
    ) {}

    public record Citation(
        String entityType,
        String entityId,
        String summary,
        LocalDate createdDate,
        double confidence,
        String sourceUrl
    ) {
        static Citation from(RetrievalResult doc) {
            return new Citation(doc.entityType(), doc.entityId(), doc.summary(), doc.createdDate(), doc.confidence(), doc.sourceUrl());
        }
    }
}
```

This keeps the app-native path aligned with Spring MVC and Java 17 while still using Entra-based credentials for Foundry and Azure AI Search.

---

### Step 5: Add a Q&A Controller and UI

#### 5.1 Create a RAG API Controller

Create `src/main/java/org/springframework/samples/petclinic/web/RagController.java`:

```java
package org.springframework.samples.petclinic.web;

import org.springframework.http.ResponseEntity;
import org.springframework.samples.petclinic.service.RagKernelService;
import org.springframework.samples.petclinic.service.RagKernelService.RagResponse;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/rag")
public class RagController {

    private final RagKernelService ragService;

    public RagController(RagKernelService ragService) {
        this.ragService = ragService;
    }

    @PostMapping("/ask")
    public ResponseEntity<RagResponse> askQuestion(@RequestBody AskRequest request) {
        if (!StringUtils.hasText(request.question())) {
            return ResponseEntity.badRequest().build();
        }

        return ResponseEntity.ok(ragService.answerQuestion(request.question()));
    }

    public record AskRequest(String question) {}
}
```

#### 5.2 Add UI Components

Create `src/main/webapp/resources/js/rag-widget.js`:

```javascript
class RagWidget {
    constructor(elementId, apiEndpoint) {
        this.container = document.getElementById(elementId);
        this.apiEndpoint = apiEndpoint;
        this.isLoading = false;

        this.render();
        this.attachEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="rag-widget">
                <h3>Ask About a Patient</h3>
                <input 
                    type="text" 
                    id="ragQuestion" 
                    placeholder="e.g., 'What health issues has Bella had?'"
                    class="rag-input"
                />
                <button id="ragSubmit" class="rag-button">Ask</button>

                <div id="ragLoading" class="rag-loading" style="display:none;">
                    Searching clinical records...
                </div>

                <div id="ragResponse" class="rag-response" style="display:none;">
                    <div id="ragAnswer" class="rag-answer"></div>
                    <div id="ragConfidence" class="rag-confidence"></div>
                    <div id="ragCitations" class="rag-citations"></div>
                </div>

                <div id="ragError" class="rag-error" style="display:none;"></div>
            </div>
        `;
    }

    attachEventListeners() {
        const submitBtn = document.getElementById("ragSubmit");
        const questionInput = document.getElementById("ragQuestion");

        submitBtn.addEventListener("click", () => this.askQuestion());
        questionInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") this.askQuestion();
        });
    }

    async askQuestion() {
        const question = document.getElementById("ragQuestion").value;
        if (!question) return;

        this.setLoading(true);

        try {
            const response = await fetch(`${this.apiEndpoint}/ask`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question })
            });

            const data = await response.json();
            this.displayResponse(data);
        } catch (error) {
            this.displayError(error.message);
        } finally {
            this.setLoading(false);
        }
    }

    displayResponse(response) {
        const responseDiv = document.getElementById("ragResponse");
        const answerDiv = document.getElementById("ragAnswer");
        const confidenceDiv = document.getElementById("ragConfidence");
        const citationsDiv = document.getElementById("ragCitations");

        // Display answer
        answerDiv.innerHTML = `<strong>Answer:</strong> ${response.answer}`;

        // Display confidence
        const confidencePercent = (response.confidence * 100).toFixed(0);
        const confidenceClass = confidencePercent >= 80 ? "high" : confidencePercent >= 50 ? "medium" : "low";
        confidenceDiv.innerHTML = `
            <div class="rag-confidence ${confidenceClass}">
                Confidence: ${confidencePercent}%
            </div>
        `;

        // Display citations
        if (response.citations && response.citations.length > 0) {
            let citationsHtml = "<strong>Sources:</strong><ul>";
            response.citations.forEach(cite => {
                citationsHtml += `
                    <li>
                        <a href="${cite.sourceUrl}" target="_blank">
                            ${cite.summary} (${cite.createdDate.split('T')[0]})
                        </a>
                    </li>
                `;
            });
            citationsHtml += "</ul>";
            citationsDiv.innerHTML = citationsHtml;
        } else {
            citationsDiv.innerHTML = "";
        }

        responseDiv.style.display = "block";
        document.getElementById("ragError").style.display = "none";
    }

    displayError(message) {
        const errorDiv = document.getElementById("ragError");
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.style.display = "block";
        document.getElementById("ragResponse").style.display = "none";
    }

    setLoading(loading) {
        this.isLoading = loading;
        const loadingDiv = document.getElementById("ragLoading");
        loadingDiv.style.display = loading ? "block" : "none";
    }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    new RagWidget("rag-widget-container", "/api/rag");
});
```

Create `src/main/webapp/resources/css/rag-widget.css`:

```css
.rag-widget {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    background-color: #f9f9f9;
}

.rag-widget h3 {
    margin: 0 0 15px 0;
    color: #333;
    font-size: 18px;
}

.rag-input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    margin-bottom: 10px;
}

.rag-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
}

.rag-button:hover {
    background-color: #0056b3;
}

.rag-loading {
    color: #666;
    font-style: italic;
    margin: 10px 0;
}

.rag-response {
    margin-top: 20px;
    padding: 15px;
    background-color: white;
    border-left: 4px solid #28a745;
    border-radius: 4px;
}

.rag-answer {
    margin-bottom: 15px;
    line-height: 1.6;
    color: #333;
}

.rag-confidence {
    padding: 10px;
    border-radius: 4px;
    font-weight: bold;
    margin-bottom: 15px;
}

.rag-confidence.high {
    background-color: #d4edda;
    color: #155724;
}

.rag-confidence.medium {
    background-color: #fff3cd;
    color: #856404;
}

.rag-confidence.low {
    background-color: #f8d7da;
    color: #721c24;
}

.rag-citations ul {
    margin: 10px 0;
    padding-left: 20px;
}

.rag-citations li {
    margin: 5px 0;
}

.rag-citations a {
    color: #007bff;
    text-decoration: none;
}

.rag-citations a:hover {
    text-decoration: underline;
}

.rag-error {
    background-color: #f8d7da;
    color: #721c24;
    padding: 15px;
    border-radius: 4px;
    margin: 10px 0;
}
```

#### 5.3 Register the Widget in the PetClinic Layout

Update `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp` to include the RAG widget near the pet history table:

```jsp
<spring:url value="/resources/css/rag-widget.css" var="ragWidgetCss" />
<spring:url value="/resources/js/rag-widget.js" var="ragWidgetJs" />

<!-- Add after the pets/visits table -->
<section class="rag-widget-panel">
    <h2>Ask About a Patient</h2>
    <div id="rag-widget-container"></div>
</section>

<jsp:attribute name="customScript">
    <link rel="stylesheet" href="${fn:escapeXml(ragWidgetCss)}" />
    <script src="${fn:escapeXml(ragWidgetJs)}"></script>
</jsp:attribute>
```

Register the clients in `src/main/java/org/springframework/samples/petclinic/config/AiConfiguration.java`:

```java
package org.springframework.samples.petclinic.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.StringUtils;

import com.azure.ai.openai.OpenAIAsyncClient;
import com.azure.ai.openai.OpenAIClientBuilder;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.search.documents.SearchClient;
import com.azure.search.documents.SearchClientBuilder;
import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.aiservices.openai.chatcompletion.OpenAIChatCompletion;
import com.microsoft.semantickernel.services.chatcompletion.ChatCompletionService;

@Configuration
public class AiConfiguration {

    @Bean
    DefaultAzureCredential azureCredential(@Value("${azure.identity.client-id:}") String managedIdentityClientId) {
        DefaultAzureCredentialBuilder builder = new DefaultAzureCredentialBuilder();
        if (StringUtils.hasText(managedIdentityClientId)) {
            builder.managedIdentityClientId(managedIdentityClientId);
        }
        return builder.build();
    }

    @Bean
    SearchClient searchClient(DefaultAzureCredential credential,
                              @Value("${azure.search.endpoint}") String endpoint,
                              @Value("${azure.search.index-name}") String indexName) {
        return new SearchClientBuilder()
            .endpoint(endpoint)
            .indexName(indexName)
            .credential(credential)
            .buildClient();
    }

    @Bean
    Kernel kernel(DefaultAzureCredential credential,
                  @Value("${azure.openai.endpoint}") String endpoint,
                  @Value("${azure.openai.chat-deployment}") String deploymentName) {
        OpenAIAsyncClient client = new OpenAIClientBuilder()
            .endpoint(endpoint)
            .credential(credential)
            .buildAsyncClient();

        ChatCompletionService chatCompletion = OpenAIChatCompletion.builder()
            .withModelId(deploymentName)
            .withOpenAIAsyncClient(client)
            .build();

        return Kernel.builder()
            .withAIService(ChatCompletionService.class, chatCompletion)
            .build();
    }
}
```

> **Configuration Note:** Store only the Foundry endpoint, deployment name, Search endpoint/index name, and optional managed identity client ID. Do not store an Azure OpenAI API key as the primary path. The calling identity still needs the **Cognitive Services User** role on the Foundry resource.

---

### Step 6: Test End-to-End

#### 6.1 Run the Application

```bash
# Build
./mvnw clean package

# Run (Windows)
mvnw.cmd jetty:run-war

# Run (Linux/Mac)
./mvnw jetty:run-war
```

Navigate to `http://localhost:8080/` and look for the "Ask About a Patient" widget.

#### 6.2 Test with Real Questions

Try these questions:

1. **"What health issues has Bella had?"**
   - Expected: Returns Bella's visits with ear infection diagnoses
   - Verify: Citations link to specific visit records
   - Confidence: Should be >80%

2. **"Which pets has Dr. Smith treated?"**
   - Expected: Lists pets by a veterinarian
   - Verify: Multiple citations, good semantic match
   - Confidence: Should be >75%

3. **"What medications were prescribed for allergies?"**
   - Expected: Either returns relevant records OR declines with "I don't have..."
   - Verify: System shows confidence <50% → declining to answer
   - Confidence: Should reflect uncertainty

4. **"When will the moon turn blue?"**
   - Expected: Declines to answer (completely out of domain)
   - Verify: Retrieval confidence <30%, answer is "I don't have data on that"
   - Confidence: Low or declined reason shown

> **Teaching Moment:** Observe what happens when questions are:
> - **Well-grounded** (health issues for a specific pet) → high confidence, precise answers
> - **Vague** (which pets have issues) → medium confidence, multiple results
> - **Out of domain** (moon phases, weather) → declined with explanation

---

## Checkpoint 1: RAG Foundation ✓

Before moving forward, verify:

- [ ] Azure AI Search index is populated with 40+ documents
- [ ] Semantic search returns relevant results (test 3+ queries)
- [ ] RAG API returns grounded answers with citations
- [ ] Low-confidence questions trigger "I don't know" responses
- [ ] UI widget loads, accepts input, displays answers with citations
- [ ] Links to source records work correctly

**Verification Commands:**

```bash
# Check index status
curl -H "Authorization: Bearer <token>" \
  https://petclinic-search.search.windows.net/indexes/petclinic-index/stats?api-version=2023-11-01

# Test RAG endpoint
curl -X POST http://localhost:8080/api/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What health issues has Bella had?"}'
```

---

## Outputs from This Lab

### Output 1: Grounded Q&A Feature ✓

A deployed capability within PetClinic that:
- Accepts natural-language questions from veterinarians
- Retrieves relevant records via semantic search
- Synthesizes answers grounded in source data
- Cites sources for every claim
- Declines to answer when uncertain

### Output 2: Vector Index Schema ✓

Documentation of:
- **Indexed entities:** Owners, Pets, Visits, Clinical Notes
- **Embedding strategy:** Azure AI Search semantic search (BM25 + semantic ranking)
- **Metadata structure:** entity_type, entity_id, created_date, clinical_relevance
- **Retrieval logic:** Semantic similarity with 0.5+ confidence threshold

### Output 3: Confidence Assessment Framework ✓

Your system now defines:
- **High confidence (>80%):** Answer grounded in 2+ recent sources → display with green badge
- **Medium confidence (50-80%):** Answer grounded in 1-2 older sources → display with yellow badge
- **Low confidence (<50%):** Insufficient data → decline to answer with explanation

---

## Summary and What's Next

### Key Learnings

1. **RAG is fundamentally augmentation, not automation.** The vet remains in control; AI just surfaces relevant context faster.
2. **Grounding in data builds trust.** Citations transform AI from a "magic black box" to an auditable decision support tool.
3. **Bounded confidence is a feature.** "I don't know" is better than a confident hallucination.
4. **Indexing strategy matters.** Chunking at the document level (not paragraph) preserves context and reduces hallucination.

### What's Next: Lab 2

Lab 2 moves beyond Q&A (passive augmentation) to **action drafting** (active assistance).

AI will propose:
- Visit summaries
- Follow-up plans
- Owner messages

But humans **approve before execution**. This introduces the Human-in-the-Loop pattern, where every AI recommendation is logged, reviewable, and attributed.

---

## Reflection Questions

Before moving to Lab 2, reflect on these questions:

1. **What was the hardest part about implementing RAG in an existing system?**
   - Was it indexing? Prompt engineering? Integration?

2. **What types of questions does RAG handle well? Poorly?**
   - Questions grounded in structured data: ✓ (e.g., "visits in 2024")
   - Questions requiring inference: ✗ (e.g., "is the pet healthy?")

3. **If a user gets a wrong answer, how would you debug it?**
   - Check retrieval: Did the search find the right records?
   - Check grounding: Did the LLM stick to the retrieved data?
   - Check confidence: Why was the system confident in a wrong answer?

4. **Would you deploy this to production today? What's missing?**
   - Performance: How fast is Q&A under load?
   - Privacy: Are you logging questions securely?
   - Accuracy: Have you tested with veterinarians?
   - Compliance: Do your citations meet audit requirements?

---

## Troubleshooting

### "Index not found" error

**Problem:** Azure AI Search returns 404 when trying to search.

**Solution:**
```bash
# Verify index creation
curl -H "Authorization: Bearer <token>" \
  https://petclinic-search.search.windows.net/indexes?api-version=2023-11-01 | jq .

# If not listed, run initialization again
python labs/scripts/bootstrap_search_index.py
```

### Low retrieval confidence on all queries

**Problem:** Confidence scores are consistently <50%.

**Solution:**
1. Check document extraction: Are documents complete and meaningful?
   ```bash
   head -20 labs/data/petclinic-documents.json
   ```
2. Test Azure AI Search directly (avoid Semantic Kernel layer)
3. Verify semantic search is enabled on the index
4. Check that documents have at least 100 characters of content

### Timeout when retrieving large result sets

**Problem:** RAG service hangs when there are 1000+ documents.

**Solution:**
1. Reduce `topK` parameter (default 5 is reasonable)
2. Add filtering by `clinicalRelevance` to narrow results
3. Use pagination for batch operations
4. Set a timeout on search requests:
    ```java
    SearchOptions searchOptions = new SearchOptions().setTop(5);
    var results = CompletableFuture
         .supplyAsync(() -> searchClient.search(query, searchOptions, Context.NONE))
         .orTimeout(10, TimeUnit.SECONDS)
         .join();
    ```

### UI Widget Not Appearing

**Problem:** The "Ask About a Patient" widget doesn't show in the browser.

**Solution:**
1. Check browser console for JavaScript errors
2. Verify `rag-widget-container` div exists in your layout
3. Verify CSS and JS files are loaded (check Network tab)
4. Check that the API endpoint is correct (`/api/rag/ask`)

---

## Additional Resources

- [Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [RAG Patterns and Best Practices](https://aka.ms/rag-best-practices)
- [Spring PetClinic Architecture](https://github.com/spring-projects/spring-petclinic)

---

*Lab 1 written by CJ, Technical Writer*  
*Based on pedagogical framework by Toby and technical patterns by Josh*  
*Last updated: 2024*

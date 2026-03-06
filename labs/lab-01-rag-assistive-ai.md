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
  - Azure OpenAI (for LLM inference)
  - Azure AI Search (for semantic search and indexing)
- .NET 8+ SDK installed
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
6. In the left menu, click **"Keys"**. Copy the:
   - **Admin Key** (store securely)
   - **Service Endpoint URL**

> **Note:** You'll use these credentials in your application. Never commit them to git; use environment variables or Azure Key Vault.

#### 1.2 Create an Azure OpenAI Deployment

1. In the Azure Portal, search for **"Azure OpenAI"** and click **"Create"**.
2. Fill in the form:
   - **Resource group:** Use the same group as AI Search
   - **Name:** `petclinic-openai`
   - **Region:** Use a region with gpt-4 or gpt-3.5-turbo availability
   - **Pricing tier:** Standard
3. Click **"Create"** and wait for deployment.
4. Go to the resource. In the left menu, click **"Keys and Endpoint"**. Copy:
   - **Key 1** (store securely)
   - **Endpoint**
5. Click **"Model deployments"** → **"Create new deployment"**. Select:
   - **Model name:** `gpt-3.5-turbo`
   - **Model version:** Latest available
   - **Deployment name:** `gpt-35-turbo`
   - **Tokens per minute rate limit:** 10K (sufficient for testing)
6. Click **"Create"** and wait.

> **Teaching Moment:** Azure OpenAI gives you access to GPT models with your data staying in your tenant. This is critical for healthcare/clinic data where privacy and compliance matter.

---

### Step 2: Extract and Prepare PetClinic Data

#### 2.1 Create a Data Extraction Script

Create a new file `labs/scripts/extract-petclinic-data.cs` (or Java/Python equivalent):

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using PetClinic.Data;

public class DataExtractor
{
    private readonly IOwnerRepository _ownerRepo;
    private readonly IPetRepository _petRepo;
    private readonly IVisitRepository _visitRepo;

    public DataExtractor(IOwnerRepository ownerRepo, IPetRepository petRepo, IVisitRepository visitRepo)
    {
        _ownerRepo = ownerRepo;
        _petRepo = petRepo;
        _visitRepo = visitRepo;
    }

    public List<IndexedDocument> ExtractAllDocuments()
    {
        var documents = new List<IndexedDocument>();

        // Extract owner documents
        foreach (var owner in _ownerRepo.GetAll())
        {
            documents.Add(new IndexedDocument
            {
                Id = $"owner-{owner.Id}",
                EntityType = "owner",
                EntityId = owner.Id.ToString(),
                Text = FormatOwnerDocument(owner),
                Summary = $"Owner: {owner.FirstName} {owner.LastName}",
                CreatedDate = DateTime.UtcNow,
                ClinicalRelevance = "medium"
            });
        }

        // Extract pet + visit documents (grouped)
        foreach (var pet in _petRepo.GetAll())
        {
            var visits = _visitRepo.GetVisitsByPet(pet.Id);
            documents.Add(new IndexedDocument
            {
                Id = $"pet-{pet.Id}",
                EntityType = "pet",
                EntityId = pet.Id.ToString(),
                Text = FormatPetDocument(pet, visits),
                Summary = $"Pet: {pet.Name} ({pet.Type})",
                CreatedDate = pet.BirthDate,
                ClinicalRelevance = "high"
            });

            // Extract visit documents (granular)
            foreach (var visit in visits)
            {
                documents.Add(new IndexedDocument
                {
                    Id = $"visit-{visit.Id}",
                    EntityType = "visit",
                    EntityId = visit.Id.ToString(),
                    Text = FormatVisitDocument(visit),
                    Summary = $"Visit {visit.Date:yyyy-MM-dd}: {visit.Type}",
                    CreatedDate = visit.Date,
                    ClinicalRelevance = "high"
                });
            }
        }

        return documents;
    }

    private string FormatOwnerDocument(Owner owner)
    {
        return $@"
Owner: {owner.FirstName} {owner.LastName}
Address: {owner.Address}, {owner.City}, {owner.State}
Telephone: {owner.Telephone}
Email: {owner.Email ?? "Not provided"}

Pets:
{string.Join("\n", owner.Pets.Select(p => $"  - {p.Name} ({p.Type})"))}
";
    }

    private string FormatPetDocument(Pet pet, List<Visit> visits)
    {
        var visitSummary = string.Join("\n", visits
            .OrderByDescending(v => v.Date)
            .Take(10)
            .Select(v => $"  {v.Date:yyyy-MM-dd}: {v.Description}"));

        return $@"
Pet: {pet.Name}
Type: {pet.Type}
Breed: {pet.Breed}
Birth Date: {pet.BirthDate:yyyy-MM-dd}
Owner: {pet.Owner.FirstName} {pet.Owner.LastName}

Recent Visits:
{visitSummary}
";
    }

    private string FormatVisitDocument(Visit visit)
    {
        return $@"
Visit Date: {visit.Date:yyyy-MM-dd}
Pet: {visit.Pet.Name}
Owner: {visit.Pet.Owner.FirstName} {visit.Pet.Owner.LastName}
Veterinarian: {visit.Veterinarian.FirstName} {visit.Veterinarian.LastName}
Type: {visit.Type}
Description: {visit.Description}
";
    }
}

public class IndexedDocument
{
    public string Id { get; set; }
    public string EntityType { get; set; }
    public string EntityId { get; set; }
    public string Text { get; set; }
    public string Summary { get; set; }
    public DateTime CreatedDate { get; set; }
    public string ClinicalRelevance { get; set; }
}
```

#### 2.2 Export Data to JSON

Run the extraction and save to a JSON file:

```bash
dotnet run --project labs/scripts/DataExtractor.csproj > labs/data/petclinic-documents.json
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

#### 3.1 Create a Semantic Kernel RAG Service

Create `src/Services/RagService.cs`:

```csharp
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;

public class RagService
{
    private readonly SearchIndexClient _indexClient;
    private readonly SearchClient _searchClient;
    private readonly string _indexName = "petclinic-index";

    public RagService(string searchEndpoint, string adminKey)
    {
        var credential = new AzureKeyCredential(adminKey);
        _indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);
        _searchClient = _indexClient.GetSearchClient(_indexName);
    }

    // Create the index with semantic search configuration
    public async Task CreateIndexAsync()
    {
        var fieldBuilder = new FieldBuilder();
        var searchFields = fieldBuilder.Build(typeof(IndexedDocument));

        var index = new SearchIndex(_indexName)
        {
            Fields = new FieldCollection
            {
                new SearchField("id", SearchFieldDataType.String) { IsKey = true, IsRetrievable = true },
                new SearchField("entityType", SearchFieldDataType.String) { IsFilterable = true, IsRetrievable = true },
                new SearchField("entityId", SearchFieldDataType.String) { IsFilterable = true, IsRetrievable = true },
                new SearchField("text", SearchFieldDataType.String) { IsSearchable = true, IsRetrievable = true },
                new SearchField("summary", SearchFieldDataType.String) { IsSearchable = true, IsRetrievable = true },
                new SearchField("createdDate", SearchFieldDataType.DateTimeOffset) { IsFilterable = true, IsSortable = true },
                new SearchField("clinicalRelevance", SearchFieldDataType.String) { IsFilterable = true, IsRetrievable = true }
            },
            SemanticConfiguration = new SemanticConfiguration("default",
                new SemanticPrioritizedFields
                {
                    TitleField = new SemanticField { FieldName = "summary" },
                    ContentFields = new[] { new SemanticField { FieldName = "text" } }
                })
        };

        try
        {
            await _indexClient.CreateIndexAsync(index);
            Console.WriteLine($"✓ Index '{_indexName}' created successfully.");
        }
        catch (Azure.RequestFailedException ex) when (ex.Status == 409)
        {
            Console.WriteLine($"✓ Index '{_indexName}' already exists.");
        }
    }

    // Upload documents to the index
    public async Task IndexDocumentsAsync(List<IndexedDocument> documents)
    {
        var batch = IndexDocumentsBatch.Upload(documents);
        var result = await _searchClient.IndexDocumentsAsync(batch);
        Console.WriteLine($"✓ Indexed {result.Results.Count} documents");
    }

    // Semantic search with confidence scoring
    public async Task<List<RetrievalResult>> SearchAsync(string query, int topK = 5)
    {
        var searchOptions = new SearchOptions
        {
            Size = topK,
            IncludeTotalCount = true,
            QueryLanguage = QueryLanguage.EnUS,
            QueryType = SearchQueryType.Semantic,
            SemanticConfigurationName = "default"
        };

        var results = new List<RetrievalResult>();

        try
        {
            var response = await _searchClient.SearchAsync<IndexedDocument>(query, searchOptions);

            await foreach (var result in response.GetResultsAsync())
            {
                var confidence = (result.RerankerScore ?? result.Score ?? 0) * 100;
                results.Add(new RetrievalResult
                {
                    Id = result.Document.Id,
                    EntityType = result.Document.EntityType,
                    EntityId = result.Document.EntityId,
                    Text = result.Document.Text,
                    Summary = result.Document.Summary,
                    CreatedDate = result.Document.CreatedDate,
                    Confidence = Math.Min(100, confidence),
                    SourceUrl = $"/app/{result.Document.EntityType}s/{result.Document.EntityId}"
                });
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Search error: {ex.Message}");
        }

        return results;
    }
}

public class IndexedDocument
{
    public string Id { get; set; }
    public string EntityType { get; set; }
    public string EntityId { get; set; }
    public string Text { get; set; }
    public string Summary { get; set; }
    public DateTime CreatedDate { get; set; }
    public string ClinicalRelevance { get; set; }
}

public class RetrievalResult
{
    public string Id { get; set; }
    public string EntityType { get; set; }
    public string EntityId { get; set; }
    public string Text { get; set; }
    public string Summary { get; set; }
    public DateTime CreatedDate { get; set; }
    public double Confidence { get; set; }
    public string SourceUrl { get; set; }
}
```

#### 3.2 Initialize and Populate the Index

Create `labs/scripts/InitializeSearch.cs`:

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

public async static Task Main(string[] args)
{
    var searchEndpoint = Environment.GetEnvironmentVariable("AZURE_SEARCH_ENDPOINT")
        ?? throw new InvalidOperationException("AZURE_SEARCH_ENDPOINT not set");
    var adminKey = Environment.GetEnvironmentVariable("AZURE_SEARCH_ADMIN_KEY")
        ?? throw new InvalidOperationException("AZURE_SEARCH_ADMIN_KEY not set");

    var ragService = new RagService(searchEndpoint, adminKey);

    // Step 1: Create the index
    Console.WriteLine("Creating Azure AI Search index...");
    await ragService.CreateIndexAsync();

    // Step 2: Load documents from JSON
    Console.WriteLine("Loading documents from JSON...");
    var jsonPath = "labs/data/petclinic-documents.json";
    var json = await File.ReadAllTextAsync(jsonPath);
    var documents = JsonSerializer.Deserialize<List<IndexedDocument>>(json)
        ?? throw new InvalidOperationException("Failed to deserialize documents");

    // Step 3: Upload to index
    Console.WriteLine($"Uploading {documents.Count} documents to index...");
    await ragService.IndexDocumentsAsync(documents);

    Console.WriteLine("✓ Index initialization complete!");

    // Step 4: Test retrieval
    Console.WriteLine("\n--- Testing Semantic Search ---");
    var testQueries = new[]
    {
        "What health issues has Bella had?",
        "Medications for dogs with allergies",
        "Visits by Dr. Smith"
    };

    foreach (var query in testQueries)
    {
        Console.WriteLine($"\nQuery: {query}");
        var results = await ragService.SearchAsync(query, topK: 3);
        foreach (var result in results)
        {
            Console.WriteLine($"  [{result.Confidence:F0}%] {result.Summary}");
        }
    }
}
```

#### 3.3 Run the Index Initialization

Set environment variables and run the script:

```bash
# On Linux/Mac:
export AZURE_SEARCH_ENDPOINT="https://petclinic-search.search.windows.net"
export AZURE_SEARCH_ADMIN_KEY="your-admin-key-here"

# On Windows:
set AZURE_SEARCH_ENDPOINT=https://petclinic-search.search.windows.net
set AZURE_SEARCH_ADMIN_KEY=your-admin-key-here

dotnet run --project labs/scripts/InitializeSearch.csproj
```

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

### Step 4: Implement RAG with Semantic Kernel

#### 4.1 Create a RAG Kernel Service

Create `src/Services/RagKernelService.cs`:

```csharp
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public class RagKernelService
{
    private readonly Kernel _kernel;
    private readonly RagService _ragService;
    private readonly IChatCompletionService _chatCompletion;

    public RagKernelService(Kernel kernel, RagService ragService)
    {
        _kernel = kernel;
        _ragService = ragService;
        _chatCompletion = kernel.GetRequiredService<IChatCompletionService>();
    }

    public async Task<RagResponse> AnswerQuestionAsync(string question)
    {
        // Step 1: Retrieve relevant documents
        var retrievedDocs = await _ragService.SearchAsync(question, topK: 5);

        // Step 2: Check confidence threshold
        var avgConfidence = retrievedDocs.Any() ? retrievedDocs.Average(d => d.Confidence) : 0;
        if (avgConfidence < 50)
        {
            return new RagResponse
            {
                Question = question,
                Answer = "I don't have enough information to confidently answer this question. Please provide more context or check the clinical records directly.",
                Confidence = avgConfidence,
                Citations = new List<Citation>(),
                DeclinedReason = "Low retrieval confidence"
            };
        }

        // Step 3: Build prompt with retrieved context
        var contextBuilder = new StringBuilder();
        contextBuilder.AppendLine("Based on the following clinical records:\n");
        foreach (var doc in retrievedDocs)
        {
            contextBuilder.AppendLine($"[{doc.EntityType.ToUpper()}] {doc.Summary}");
            contextBuilder.AppendLine(doc.Text);
            contextBuilder.AppendLine();
        }

        var prompt = $@"You are a veterinary assistant helping clinic staff answer questions about patient records.

INSTRUCTIONS:
1. Answer ONLY based on the provided clinical records below.
2. If information is not in the records, say 'I don't have data on that.'
3. Cite which record(s) support each claim.
4. Be concise and clinical in tone.

CLINICAL RECORDS:
{contextBuilder}

QUESTION: {question}

ANSWER:";

        // Step 4: Generate answer with LLM
        var chatHistory = new ChatHistory();
        chatHistory.AddUserMessage(prompt);

        var result = await _chatCompletion.GetChatMessageContentAsync(chatHistory);
        var answer = result.Content ?? "";

        // Step 5: Build citation references
        var citations = BuildCitations(retrievedDocs);

        // Step 6: Calculate composite confidence
        var compositeConfidence = CalculateConfidence(avgConfidence, answer, citations);

        return new RagResponse
        {
            Question = question,
            Answer = answer,
            Confidence = compositeConfidence,
            Citations = citations,
            RetrievedCount = retrievedDocs.Count
        };
    }

    private List<Citation> BuildCitations(List<RetrievalResult> docs)
    {
        return docs.Select(doc => new Citation
        {
            EntityType = doc.EntityType,
            EntityId = doc.EntityId,
            Summary = doc.Summary,
            CreatedDate = doc.CreatedDate,
            Confidence = doc.Confidence,
            SourceUrl = doc.SourceUrl
        }).ToList();
    }

    private double CalculateConfidence(double retrievalConfidence, string answer, List<Citation> citations)
    {
        // Adjust confidence based on answer characteristics
        var baseConfidence = retrievalConfidence / 100.0;

        // Penalize if answer contains "unclear" or "contradictory"
        if (answer.Contains("unclear", System.StringComparison.OrdinalIgnoreCase) ||
            answer.Contains("contradictory", System.StringComparison.OrdinalIgnoreCase))
        {
            baseConfidence *= 0.8;
        }

        // Boost if multiple citations support the answer
        if (citations.Count >= 2)
        {
            baseConfidence = Math.Min(1.0, baseConfidence * 1.1);
        }

        return baseConfidence;
    }
}

public class RagResponse
{
    public string Question { get; set; }
    public string Answer { get; set; }
    public double Confidence { get; set; } // 0.0-1.0
    public List<Citation> Citations { get; set; }
    public int RetrievedCount { get; set; }
    public string DeclinedReason { get; set; }
}

public class Citation
{
    public string EntityType { get; set; }
    public string EntityId { get; set; }
    public string Summary { get; set; }
    public DateTime CreatedDate { get; set; }
    public double Confidence { get; set; }
    public string SourceUrl { get; set; }
}
```

---

### Step 5: Add a Q&A Controller and UI

#### 5.1 Create a RAG API Controller

Create `src/Controllers/RagController.cs`:

```csharp
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

[ApiController]
[Route("api/[controller]")]
public class RagController : ControllerBase
{
    private readonly RagKernelService _ragService;

    public RagController(RagKernelService ragService)
    {
        _ragService = ragService;
    }

    [HttpPost("ask")]
    public async Task<IActionResult> AskQuestion([FromBody] AskRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Question))
            return BadRequest("Question cannot be empty");

        var response = await _ragService.AnswerQuestionAsync(request.Question);
        return Ok(response);
    }
}

public class AskRequest
{
    public string Question { get; set; }
}
```

#### 5.2 Add UI Components

Create `src/wwwroot/js/rag-widget.js`:

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

Create `src/wwwroot/css/rag-widget.css`:

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

Update `src/Views/Shared/_Layout.cshtml` to include the RAG widget:

```html
<!-- Add to the body of your layout, where you want the Q&A widget to appear -->

<link rel="stylesheet" href="~/css/rag-widget.css" />

<!-- Somewhere in the main content area -->
<div id="rag-widget-container"></div>

<script src="~/js/rag-widget.js"></script>
```

Register the services in `Program.cs`:

```csharp
// Add to your dependency injection configuration
services.AddScoped<RagService>();
services.AddScoped<RagKernelService>();

// Configure Semantic Kernel
var semanticKernelBuilder = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(
        deploymentName: "gpt-35-turbo",
        endpoint: new Uri(configuration["AzureOpenAI:Endpoint"]),
        apiKey: configuration["AzureOpenAI:ApiKey"]
    );

services.AddSingleton(sp => semanticKernelBuilder.Build());
```

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
dotnet run --project labs/scripts/InitializeSearch.csproj
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
   ```csharp
   var searchOptions = new SearchOptions { Size = 5 };
   using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
   var results = await _searchClient.SearchAsync<IndexedDocument>(query, searchOptions, cts.Token);
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

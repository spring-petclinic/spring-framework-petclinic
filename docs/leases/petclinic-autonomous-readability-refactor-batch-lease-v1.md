# PetClinic Autonomous Readability Refactor Batch Lease v1

This lease defines the governed workflow for autonomous, low-to-medium-risk
readability refactoring in the owned Spring PetClinic repository.

It is intentionally split into authority phases. A refactor batch lease may
create local commits, but it must not publish, open or update a PR, merge,
release, deploy, or interact with upstream unless a later phase explicitly
authorizes that action.

## Lease Identity

```yaml
leaseName: petclinic-autonomous-readability-refactor-batch-lease-v1
repository: C:\dev\spring-framework-petclinic
defaultBranchPattern: threshold-governed-refactor-demo*
requiredInitialWorktree: clean
```

## Purpose

Continue PetClinic refactoring autonomously over a bounded candidate pool.
The lease is designed for mechanical readability work only:

- private helper extraction
- duplicate literal constant extraction
- redundant local variable simplification
- small controller branch readability decomposition
- validator and formatter readability cleanup

The lease does not authorize behavior changes or public claims about readiness,
correctness, security, or compliance.

## Authority Levels

```yaml
allowedRiskClasses:
  - R0_READ_ONLY
  - R1_READOUT
  - R2_REVERSIBLE_LOCAL_MUTATION
  - R3_LOCAL_COMMIT

notAuthorizedByThisLease:
  - R4_OWNED_REPO_BRANCH_PUSH
  - R4_OWNED_REPO_DRAFT_PR_CREATE_OR_UPDATE
  - R4_CI_STABILIZATION
  - R5_PR_MERGE
  - release
  - deploy
```

## Batch Budget

```yaml
maxCandidatesThisRun: 10
maxCommitsThisRun: 10
maxFilesPerCandidate: 1
maxChangedLinesPerCandidate: 80
maxNewPrivateMethodsPerCandidate: 2
maxRepairAttemptsPerCandidate: 1
fullMavenTestRequiredPerCandidate: true
requireCleanWorktreeBeforeEachCandidate: true
requireCleanWorktreeAfterEachCommit: true
stopOnUnexpectedChangedPath: true
```

## Allowed Paths

```yaml
allowedPaths:
  - src/main/java/org/springframework/samples/petclinic/web/**/*.java
  - src/main/java/org/springframework/samples/petclinic/service/**/*.java
  - src/main/java/org/springframework/samples/petclinic/model/**/*.java
  - src/main/java/org/springframework/samples/petclinic/util/**/*.java

forbiddenPaths:
  - pom.xml
  - src/test/**
  - src/main/resources/**
  - src/main/webapp/**
  - .github/**
  - target/**
  - hidden/config files
```

The default starting scope should be `web` and `service`. `model` and `util`
may be admitted only when the candidate is mechanically local and covered by the
same validation protocol.

## Candidate Classes

### 1. Private Helper Extraction For Readability

Allowed when all conditions hold:

- same class only
- helper method is private
- at most two new private methods
- extracted code is contiguous or logically identical to an existing local block
- no public API change
- no request mapping change
- no validation annotation change
- no repository call change
- no persistence behavior change
- no returned view name or model attribute name change

### 2. Duplicate Literal Constant Extraction

Allowed when all conditions hold:

- same class only
- new constant is `private static final String`
- literal is repeated in the same file
- literal represents a view name, redirect, model key, route path, validation
  field, or validation code
- replacement preserves the exact string value
- at most two constants per candidate

### 3. Redundant Local Variable Simplification

Allowed when all conditions hold:

- local variable is assigned exactly once
- initializer is side-effect free or already required immediately
- simplification does not reduce readability
- no behavior change

### 4. Controller Branch Readability Decomposition

Allowed when all conditions hold:

- only splits existing branch bodies into private methods
- returned view names and redirects are identical strings or constants
- model keys are identical
- BindingResult behavior is identical
- branch order is unchanged
- no request mapping, HTTP method, validation, repository, or persistence change

### 5. Validator Or Formatter Readability Cleanup

Allowed when all conditions hold:

- same class only
- no supported type change
- no validation field/code/message change
- no parse/print semantics change
- no exception message change unless explicitly authorized

### 6. Micro-Format Cleanup

Allowed only inside a method already admitted for one of the candidate classes
above. Broad file formatting is not authorized.

## Explicitly Forbidden Changes

```yaml
forbiddenChanges:
  - request mapping path changes
  - HTTP method changes
  - validation annotation semantic changes
  - repository query semantic changes
  - persistence behavior changes
  - transaction behavior changes unless separately authorized
  - cache annotation changes
  - returned view name changes
  - model attribute name changes
  - dependency or plugin updates
  - pom.xml edits
  - test edits
  - resource edits
  - broad formatting
  - feature work
```

## Discovery Protocol

Before each candidate:

```powershell
git status -sb
git rev-parse HEAD
git branch --show-current
git diff --name-only
```

Required:

- worktree is clean
- branch matches the lease invocation
- changed path list is empty

Discovery must scan only allowed paths. Exclude candidates already committed in
the current branch lineage unless the new candidate is a strictly local
continuation in a different method.

## Scoring

```yaml
positive:
  singleFile: 30
  noBehaviorChangeExpected: 30
  fullMavenTestAvailable: 20
  existingControllerOrServiceCoverage: 10
  privateHelperImprovesReadability: 15
  duplicateLiteralConstantRemovesRepetition: 10
  redundantLocalVariableSimplification: 12
  diffUnder40ChangedLines: 10
  diff40To80ChangedLines: 5
  noPublicSignatureChange: 10

negative:
  controllerBranchDecomposition: -10
  helperNameRequiresSemanticJudgment: -10
  changesMoreThanOneBranch: -15
  extractionCrossesNonContiguousLogic: -20

reject:
  - changes public method signature
  - changes request mapping, view, model, validation, repository, or persistence behavior
  - requires test changes
  - requires pom.xml or dependency changes
  - requires upstream, push, PR, merge, release, or deploy
```

Admission threshold:

```yaml
minimumScore: 75
```

## Tie-Break Rules

Apply in order:

1. Prefer smaller diff.
2. Prefer one private helper over two.
3. Prefer already covered controller or service methods.
4. Prefer `OwnerController` over `PetController` over `VisitController` over
   `VetController` over `PetValidator` over `PetTypeFormatter` over service.
5. Prefer lexical file path.
6. Prefer lexical method name.
7. Stop with an ambiguity packet if still indistinguishable.

## Candidate Packet

For every admitted candidate, record:

```yaml
candidateId: <stable id>
candidateClass: <class from this lease>
baseHead: <git rev-parse HEAD>
allowedFile: <single file>
beforeSha256: <file hash>
expectedDiffSummary: <short summary>
score: <numeric score>
tieBreakReason: <deterministic reason>
behaviorPreservation: <mechanical argument>
validationCommands:
  - git diff --name-only
  - git diff --check
  - $env:JAVA_HOME='C:\Program Files\Java\jdk-17'; .\mvnw.cmd test
revertStrategy: exact restore of admitted file before commit
nonClaims:
  - no push
  - no PR
  - no upstream interaction
  - no merge
  - no release
  - no deploy
  - no readiness/correctness/security/compliance claim
```

## Patch Protocol

Rules:

- edit only the admitted file
- stay within changed-line and helper-method budgets
- preserve all forbidden behavior-change checks
- use repository style
- avoid unrelated formatting

## Validation Protocol

Run after every candidate patch:

```powershell
git diff --name-only
git diff --check
$env:JAVA_HOME='C:\Program Files\Java\jdk-17'; .\mvnw.cmd test
```

Required:

- changed paths contain only the admitted file
- `git diff --check` passes
- full Maven test passes

## Failure And Repair Protocol

If validation fails:

1. Determine whether the failure is clearly caused by the current candidate.
2. If yes, perform at most one bounded repair inside the admitted file.
3. Rerun `git diff --check` and full Maven test.
4. If still failing, exact-revert the admitted file.
5. Require clean worktree after revert.
6. Stop with a failure receipt.

If the failure requires forbidden files, upstream interaction, dependency
changes, test changes, force push, merge, release, or deploy, stop without
repair.

## Commit Protocol

After successful validation:

```powershell
Get-FileHash -Algorithm SHA256 <admitted-file>
git add <admitted-file>
git commit -m "Refactor PetClinic <short candidate summary>"
git status -sb
git log -1 --oneline
git rev-parse HEAD
```

Required:

- only admitted file staged
- exactly one local commit per successful candidate
- worktree clean after commit

## Batch Continuation

Continue to the next candidate only when:

- budget remains
- worktree is clean
- previous commit succeeded
- another candidate reaches the admission threshold

Stop with `ready_no_candidates` when no candidate qualifies.

## Terminal Receipt

At batch end, report:

```yaml
processedCandidates: []
commitsCreated: []
finalHead: <sha>
finalGitStatus: <status>
testsRun: <commands and results>
stoppedReason: <reason>
remainingLikelyCandidates: []
nonClaims:
  - no push
  - no PR
  - no upstream interaction
  - no fetch/pull
  - no pom.xml/dependency change
  - no src/test change
  - no request mapping/view/model/validation/repository/persistence behavior change
  - no merge/release/deploy
  - no public readiness/correctness/security/compliance claim
```

## Downstream Authority Phases

The following leases must be separate invocations.

### Owned Branch Publish And Draft PR Lease

Purpose:

- run final `git diff --check`
- run full Maven test
- push the current branch to owned origin
- create or update a draft PR in the owned repository only

Not allowed:

- upstream interaction
- force push
- ready-for-review
- reviewer request
- merge
- release
- deploy

### Draft PR CI Stabilization Lease

Purpose:

- inspect existing owned draft PR
- read CI status
- if green, stop
- if pending, stop
- if failing, perform at most bounded branch-local repairs inside allowed paths

Not allowed:

- new feature work
- broad refactoring
- dependency or test changes
- ready-for-review
- reviewer request
- merge
- release
- deploy

### Owned Repo PR Merge Lease

Purpose:

- merge exactly one owned-repository PR using the authorized merge method

Preconditions:

- worktree clean
- PR open
- PR not draft
- PR head matches required SHA
- PR targets owned repository, not third-party upstream
- no conflicts
- all required checks pass
- full local Maven test passes

Not allowed:

- branch protection bypass
- force push
- code changes
- tag creation
- release
- deploy
- upstream interaction

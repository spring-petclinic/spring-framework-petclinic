# PetClinic Autonomous Readability Refactor Batch Invocation Template

Use this template to start a governed autonomous refactor batch from the current
repository state.

```yaml
startLease: petclinic-autonomous-readability-refactor-batch-lease-v1

repository: C:\dev\spring-framework-petclinic
branch: <current branch>
startHead: <git rev-parse HEAD>
initialWorktree: clean

budget:
  maxCandidatesThisRun: 10
  maxCommitsThisRun: 10
  maxFilesPerCandidate: 1
  maxChangedLinesPerCandidate: 80
  maxNewPrivateMethodsPerCandidate: 2
  maxRepairAttemptsPerCandidate: 1

scope:
  primaryAllowedPaths:
    - src/main/java/org/springframework/samples/petclinic/web/**/*.java
    - src/main/java/org/springframework/samples/petclinic/service/**/*.java
  optionalAllowedPaths:
    - src/main/java/org/springframework/samples/petclinic/model/**/*.java
    - src/main/java/org/springframework/samples/petclinic/util/**/*.java
    - src/main/java/org/springframework/samples/petclinic/repository/**/*.java
  repositoryScopeRules:
    - readability-only changes
    - no repository interface signature changes
    - no SQL/HQL/JPQL string changes
    - no query parameter name, value, or order changes
    - no row mapper, result extractor, association, or persistence behavior changes
    - no transaction or cache annotation changes
    - no exception type or exception message changes

validation:
  fullMavenTestRequiredPerCandidate: true
  commands:
    - git diff --name-only
    - git diff --check
    - $env:JAVA_HOME='C:\Program Files\Java\jdk-17'; .\mvnw.cmd test

authorization:
  allowed:
    - inspect repository state
    - discover and rank candidates
    - admit one candidate at a time
    - edit only the admitted file
    - exact-revert current candidate on validation failure
    - one bounded repair attempt per candidate
    - one local commit per successful candidate
    - continue until budget exhausted or no candidate qualifies
  forbidden:
    - push
    - PR creation or update
    - upstream interaction
    - fetch or pull
    - force push
    - merge
    - release
    - deploy
    - pom.xml or dependency changes
    - src/test changes
    - src/main/resources changes
    - src/main/webapp changes
    - request mapping/view/model/validation/repository/persistence behavior changes
    - SQL/HQL/JPQL changes
    - repository interface changes

stopConditions:
  - branch mismatch
  - start HEAD mismatch
  - dirty worktree before candidate
  - unexpected changed path
  - no candidate score >= 75
  - ambiguity after tie-breaks
  - behavior preservation cannot be argued mechanically
  - changed-line or helper-method budget exceeded
  - git diff --check fails
  - Maven test fails after one bounded repair
  - exact revert fails
  - commit fails
  - worktree not clean after commit
  - maxCandidatesThisRun reached
  - maxCommitsThisRun reached

finalReport:
  include:
    - processed candidates
    - rejected candidate summary
    - commits created
    - final HEAD
    - final git status
    - tests run and results
    - stopped reason
    - remaining likely candidates
    - explicit non-claims
```

Example invocation:

```text
Start lease petclinic-autonomous-readability-refactor-batch-lease-v1.

Repository: C:\dev\spring-framework-petclinic
Branch: threshold-governed-refactor-demo-3
Start HEAD: <current HEAD>
Initial worktree: clean

Run autonomously until budget exhaustion or ready_no_candidates.
Do not push, open or update PRs, merge, release, deploy, fetch, pull, or
interact with upstream.
```

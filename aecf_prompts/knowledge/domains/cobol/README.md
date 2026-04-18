# COBOL Domain

## What is this domain?

The **COBOL** domain covers legacy mainframe development and modernization using COBOL. It provides rules for safely evolving batch programs, CICS online transactions, copybook contracts, and JCL job control — preserving business-critical flows while enabling incremental modernization.

## Capabilities

- **Legacy preservation** of copybook contracts, JCL scheduling, and transaction boundaries.
- **Modernization strategies** favoring strangler-fig and adapter patterns around stable legacy seams.
- **Integration guidance** for exposing legacy capabilities to modern service layers.
- **Batch validation** covering dataset naming, side effects, and scheduling implications.
- **Regression evidence** requirements around financial, operational, and compliance-critical flows.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `cobol_batch_mainframe` | Batch COBOL programs — JCL, VSAM/QSAM datasets, copybooks, abend handling. |
| `cobol_cics_online` | CICS online transaction programs — BMS maps, COMMAREA, transaction routing, pseudo-conversational design. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=refactor stack=cobol
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=create_tests stack=cobol/cobol_batch_mainframe
```

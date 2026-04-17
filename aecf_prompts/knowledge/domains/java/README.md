# Java Domain

## What is this domain?

The **Java** domain covers Java application development across Spring Boot services, server-driven ZKoss UIs, JPA/Hibernate persistence, Maven-governed builds, Lombok-heavy models, compatibility across Java LTS baselines, modernization programs, and cloud workloads (AWS/Azure). It provides rules for build tool alignment (Maven/Gradle), constructor injection, explicit compatibility envelopes, migration seams, and test coverage with JUnit 5.

## Capabilities

- **Build system respect** preserving existing Maven or Gradle conventions without introducing migrations.
- **Maven lifecycle guidance** for plugin ownership, dependency convergence, compiler targets, and test-phase separation.
- **Architecture guidance** keeping business logic out of controllers and DTOs, with clean DI patterns.
- **UI guidance** for ZUL pages, composers or view models, and explicit desktop or session scope management in ZKoss applications.
- **Testing rules** using JUnit 5 with integration tests for wiring/persistence and local test doubles.
- **Dependency management** respecting existing Java version and plugin conventions.
- **Compatibility guidance** for mixed Java 8, 11, and newer LTS estates.
- **Modernization guidance** for phased extraction and API-first migration work.
- **Common pitfall detection** for static mutable state, incompatible dependency versions, and blurred API boundaries.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `spring_boot_service` | Spring Boot services — auto-configuration, REST controllers, actuator, profiles. |
| `zkoss` | ZKoss server-driven UI — ZUL pages, composers/view models, event flows, desktop/session scope. |
| `maven` | Maven lifecycle and tooling — parent/module structure, dependency management, compiler settings, surefire/failsafe. |
| `lombok` | Lombok-heavy models — generated constructors/accessors, builder semantics, equality and mutability review. |
| `lts_compatibility` | Multi-LTS Java support — runtime floor, compiler target, dependency and CI compatibility matrix. |
| `modernization` | Incremental modernization — extraction seams, compatibility-safe migration, API-first evolution. |
| `java_aws_workload` | Java on AWS — Lambda, SDK v2, DynamoDB, SQS/SNS, CDK/SAM deployment. |
| `java_azure_workload` | Java on Azure — Azure Functions, SDK, Cosmos DB, Service Bus, Bicep/ARM deployment. |
| `jpa_persistence` | JPA/Hibernate persistence — entity design, repository patterns, transactions, migrations. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=java
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=java/spring_boot_service
@aecf run skill=refactor stack=java/zkoss
@aecf run skill=refactor stack=java/maven
@aecf run skill=refactor stack=java/lombok
```

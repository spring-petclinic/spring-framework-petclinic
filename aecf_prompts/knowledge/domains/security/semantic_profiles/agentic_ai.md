---
profile_id: agentic_ai
title: OWASP Agentic AI Skills Top 10 (AST10) — Security for AI Agent Skills
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
regulation_reference_date: 2026-03-16
max_staleness_months: 6
profile_type: security_framework
stack_nodes:
  - security
requires: []
precedence: 80
fallback_mode: warn_continue
compatibility:
  - python
  - java
  - dotnet
  - node
  - go
  - rust
  - react
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - file=SKILL.md
  - file=skill.json
  - file=manifest.json
  - keyword=mcp
  - keyword=agent
  - keyword=agentic
  - path=skills/
  - path=agents/
  - dependency=langchain
  - dependency=autogen
  - dependency=crewai
  - dependency=semantic-kernel
  - dependency=openai-agents
max_lines_per_section: 8
tags:
  - owasp
  - agentic-ai
  - agent-security
  - supply-chain
  - skills
  - mcp
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## FRAMEWORK SCOPE

OWASP Agentic AI Skills Top 10 (AST10, 2026 Edition — project proposal stage). Applies to any system that builds, distributes, consumes, or orchestrates AI agent skills — including MCP servers/tools, agent frameworks, skill registries, and VS Code extensions with agent capabilities.

**Reference status**: AST10 is currently in OWASP Incubator phase (Q2 2026). The 10 risk categories are defined but detailed writeups are in progress. This profile provides code-level detection guidance based on the published risk taxonomy. The `max_staleness_months` field ensures a review is triggered as the project matures.

## WHEN THIS PROFILE ACTIVATES

This profile is injected into `security_review` and `ai_risk_assessment` contexts when the target workspace shows evidence of being an agentic AI project:

- Contains `SKILL.md`, `skill.json`, or agent manifest files
- Has dependencies on agent frameworks (LangChain, AutoGen, CrewAI, Semantic Kernel, OpenAI Agents SDK)
- Contains MCP server/tool definitions
- Has `agents/` or `skills/` directories with behavioral definitions

When activated, findings from this profile are reported **alongside** standard OWASP Top 10 (2021) findings, not instead of them.

## CODE-LEVEL AUDIT CHECKLIST

### AST01 — Malicious Skills
- Check for skills or plugins loaded from untrusted registries without integrity verification.
- Look for `eval()`, `exec()`, `subprocess.call()`, `child_process.exec()` in skill handlers that process external input.
- Verify skill loading paths do not allow directory traversal or arbitrary file inclusion.
- Check for cryptographic signature verification on skill packages before installation.

### AST02 — Supply Chain Compromise
- Verify dependency pinning: exact versions or hashes, not ranges or `latest`.
- Check for typosquatting indicators in package names (similar names to popular packages).
- Verify skill/tool sources are from known, trusted registries.
- Look for integrity checks (checksums, signatures) on downloaded skills or tools.
- Check CI/CD pipelines for dependency confusion vulnerabilities.

### AST03 — Over-Privileged Skills
- Verify skills declare minimum required permissions (file access, network, system).
- Check for skills with unrestricted file system access (read/write to arbitrary paths).
- Look for skills with network access not justified by their declared purpose.
- Verify skill permission boundaries are enforced at runtime, not just declared.
- Check for privilege escalation paths where skills can grant themselves additional permissions.

### AST04 — Insecure Skill Metadata
- Validate skill metadata files (YAML frontmatter, JSON manifests) against expected schemas.
- Check for injection vectors in metadata fields that are rendered or executed.
- Verify metadata does not contain embedded scripts, URIs to malicious resources, or template injection patterns.
- Look for metadata fields that control execution flow without validation.

### AST05 — Prompt Injection via Skills
- Check for user input flowing into skill prompts without sanitization.
- Look for skills that concatenate untrusted content into system prompts or tool descriptions.
- Verify skills validate and constrain output before passing to downstream tools.
- Check for indirect prompt injection vectors (data from external sources injected into agent context).
- Look for skills that override safety guardrails or system instructions.

### AST06 — Weak Skill Isolation
- Verify skills run in sandboxed environments (containers, VMs, restricted processes).
- Check for shared state between skills that could enable cross-skill data leakage.
- Look for skills with access to other skills' resources, credentials, or outputs without authorization.
- Verify skill execution environments have resource limits (CPU, memory, time, network).
- Check for skills that can modify the agent runtime or other skills' behavior.

### AST07 — Update and Version Drift
- Check for skills or tools pinned to mutable references (branch names, `latest` tags).
- Verify update mechanisms use integrity verification (hashes, signatures).
- Look for auto-update mechanisms that could introduce compromised versions.
- Check for dependency lock files (`package-lock.json`, `poetry.lock`, `Cargo.lock`) and verify they are committed and used.

### AST08 — Insufficient Skill Scanning
- Check whether skill packages undergo security scanning before deployment.
- Look for static analysis integration in skill development workflows.
- Verify secrets scanning covers skill configuration and metadata files.
- Check for runtime behavior monitoring of deployed skills.

### AST09 — Lack of Skill Governance
- Verify a skill inventory exists listing all active skills with owners, versions, and risk classifications.
- Check for skill lifecycle management (approval, review, deprecation processes).
- Look for audit logging of skill invocations and actions.
- Verify skill access is governed by role-based controls.
- Check for incident response procedures specific to compromised skills.

### AST10 — Cross-Platform Skill Reuse Risks
- Check for skills reused across platforms without platform-specific security adaptation.
- Verify platform-specific permission models are respected when porting skills.
- Look for universal skill format adoption that normalizes security metadata.
- Check for platform-specific sandboxing and isolation requirements.

## SEVERITY MAPPING

| AST Risk | Violation Type | Default Severity | Rationale |
|----------|---------------|-----------------|-----------|
| AST01 | Skill loading from untrusted source without verification | CRITICAL | Direct malware vector |
| AST01 | eval/exec in skill handlers processing external input | CRITICAL | Code injection |
| AST02 | Dependencies without pinning or integrity checks | HIGH | Supply chain compromise |
| AST02 | Typosquatting indicators in package names | HIGH | Supply chain attack |
| AST03 | Skill with unrestricted file system or network access | HIGH | Over-privilege |
| AST03 | No permission declaration in skill manifest | MEDIUM | Missing least-privilege |
| AST04 | Unvalidated metadata controlling execution flow | HIGH | Metadata injection |
| AST04 | Template injection in metadata fields | MEDIUM | Injection vector |
| AST05 | Unsanitized user input in skill prompts | CRITICAL | Prompt injection |
| AST05 | Skills overriding safety guardrails | CRITICAL | Guardrail bypass |
| AST06 | No sandboxing for skill execution | HIGH | Isolation failure |
| AST06 | Shared mutable state between skills | MEDIUM | Cross-skill leakage |
| AST07 | Mutable version references (latest, branch) | MEDIUM | Update drift |
| AST07 | Auto-update without integrity verification | HIGH | Compromised updates |
| AST08 | No security scanning for skill packages | MEDIUM | Insufficient scanning |
| AST09 | No skill inventory or governance | LOW | Governance gap |
| AST09 | No audit logging of skill invocations | MEDIUM | Accountability gap |
| AST10 | Cross-platform reuse without security adaptation | MEDIUM | Platform mismatch |

## DETECTION PATTERNS

### Python Agent Frameworks
```
# Dangerous patterns to flag
eval(skill_input)
exec(tool_output)
subprocess.call(agent_command, shell=True)
importlib.import_module(untrusted_module_name)
os.system(f"...")  # with agent-provided arguments
```

### Node.js Agent Frameworks
```
// Dangerous patterns to flag
require(dynamic_skill_path)
child_process.exec(agent_command)
vm.runInNewContext(untrusted_code)
Function(tool_output)()
```

### MCP Server Patterns
```
# Check for proper input validation in MCP tool handlers
# Flag tools without input schema validation
# Flag tools with unrestricted resource access
# Verify transport security (stdio vs SSE vs HTTP)
```

## RELATIONSHIP TO EXISTING AECF SKILLS

| AECF Skill | AST10 Overlap | Enhanced Guidance |
|-----------|---------------|-------------------|
| `security_review` | AST01, AST05 (partial via OWASP A03 Injection) | Full AST01-AST10 coverage when agentic context detected |
| `ai_risk_assessment` | AST03, AST06, AST09 (partial via operational risk) | Agentic-specific risk dimensions |
| `dependency_audit` | AST02, AST07 (supply chain, version drift) | Skill-specific supply chain risks |
| `data_governance_audit` | AST06 (data isolation) | Cross-skill data leakage |

## SCOPE LIMITATIONS

This profile covers CODE-LEVEL security patterns. The following require organizational verification:

- Skill marketplace/registry trust policies
- Organizational skill approval workflows
- Incident response procedures for compromised skills
- Staff training on agentic AI security
- Contractual agreements with skill providers

# Fine-Grained Tool Access Control

This is one of the most important ideas in production AI.

A model should not get blanket access to every system just because a tool exists.

## Access control model

Think in three layers.

### 1. Identity
Who is asking?

Examples:
- end user
- service account
- internal admin
- automation job

### 2. Authorization
What tools can that identity use?

Examples:
- analyst can use read-only SQL
- release engineer can read deployment notes
- nobody gets unrestricted shell access

### 3. Constraint
What subset of the tool can they use?

Examples:
- SQL only against allowlisted tables
- file reads only under approved directories
- ticket creation only for approved projects

## Example policy table

| Role | Tool | Allowed | Constraints |
|---|---|---:|---|
| analyst | query_readonly_sql | yes | select only, allowlisted tables |
| engineer | read_repo_file | yes | approved repos and paths |
| admin | create_ticket | yes | project allowlist |
| everyone | execute_shell | no | blocked |

## Good policy habits

- default deny
- separate read from write tools
- log all denied calls too
- validate arguments before execution
- keep tools small and narrow

## What to say in interviews

> I treated tool access like API security rather than prompt engineering. I separated identity, authorization, and argument constraints so the model only had least-privilege access to approved capabilities.

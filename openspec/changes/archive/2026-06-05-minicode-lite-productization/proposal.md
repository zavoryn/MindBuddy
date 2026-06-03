## Why

`mindbuddy` now has a strong runtime kernel, session replay, and checkpoint/rewind
surfaces, but it still feels like an advanced local runtime rather than a
lightweight Claude Code-style product. The next step is to turn the current
kernel into a coherent product surface by finishing the missing P1-P3 layers:
instruction governance, first-class delegation, extensibility, and release-grade
operator ergonomics.

## What Changes

- Add explicit instruction and policy layers so users can inspect which global,
  user, project, and machine-managed guidance was active in a turn.
- Turn hooks into first-class workflows with inspectable registration, lifecycle,
  async execution outcomes, and operator-facing UX in CLI/TUI/session artifacts.
- Productize delegated/background execution so subagents and long-running helper
  tasks are bounded, inspectable, replayable, and recoverable.
- Introduce a lightweight extension packaging model for local plugins/skills so
  `mindbuddy` can share reusable commands and workflows without needing a heavy
  marketplace.
- Expand runtime evaluation and operator diagnostics into a release-readiness
  surface that can compare profiles, validate provider fallback behavior, and
  explain degraded states clearly.

## Capabilities

### New Capabilities

- `instruction-policy-layers`: Explicit instruction precedence, inspection, and
  managed policy loading for runtime turns and session artifacts.
- `first-class-hook-workflows`: Hook registration, visibility, async completion,
  and operator workflows that feel like a product surface instead of an internal
  API.
- `delegated-background-runtime`: Product-grade background and subagent
  execution with inspectable status, isolated outputs, and replayable summaries.
- `extension-packaging`: Lightweight local plugin/skill packaging, discovery,
  enablement, and shareable install flows.
- `product-readiness-evaluation`: Release-facing evaluation, provider-fallback
  diagnostics, and runtime health reporting that make `mindbuddy-lite` operable.

### Modified Capabilities

- None.

## Impact

- Affected code:
  - `D:/Desktop/mindbuddy/mindbuddy/prompt.py`
  - `D:/Desktop/mindbuddy/mindbuddy/prompt_pipeline.py`
  - `D:/Desktop/mindbuddy/mindbuddy/config.py`
  - `D:/Desktop/mindbuddy/mindbuddy/hooks.py`
  - `D:/Desktop/mindbuddy/mindbuddy/background_tasks.py`
  - `D:/Desktop/mindbuddy/mindbuddy/agent_loop.py`
  - `D:/Desktop/mindbuddy/mindbuddy/session.py`
  - `D:/Desktop/mindbuddy/mindbuddy/cli_commands.py`
  - `D:/Desktop/mindbuddy/mindbuddy/tui/`
  - `D:/Desktop/mindbuddy/mindbuddy/runtime_profile_eval.py`
- New OpenSpec capability specs under
  `D:/Desktop/mindbuddy/openspec/changes/mindbuddy-lite-productization/specs/`
- New product-facing docs and build plans in `D:/Desktop/mindbuddy/docs/superpowers/`

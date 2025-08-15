# RuneLite Plugin Spec: Screen Region Capture and Input Dispatch

## Objective
Provide a RuneLite plugin that:
- Captures pixel-accurate screen regions from the OSRS game frame.
- Dispatches user-like input events (mouse/keyboard) to the client window.
- Exposes a narrow, auditable interface for the AI agent to request captures and send inputs.

This document specifies behaviors, interfaces, and constraints sufficient for implementation without guesswork.

## Constraints & Compliance
- Must respect OSRS/Jagex Terms of Service and RuneLite plugin ecosystem rules.
- Input dispatch must mimic human interaction and remain rate-limited and bounded by configured policies.
- No memory reading or game client code injection; rely on RuneLite APIs, overlays, and OS-level input primitives.
- All capture and input requests must be logged with timestamps and caller metadata for auditing.

## High-Level Architecture
- Plugin module: `ai-agent-tools`
- Components:
  1. CaptureService: produces `BufferedImage` for requested regions; supports coordinate systems and scaling.
  2. InputService: schedules and dispatches bounded mouse and keyboard events via OS (e.g., `java.awt.Robot`) guarded by safety policies.
  3. PolicyGuard: validates every input request against cooldowns, jitter, randomness, region bounds, and focus checks.
  4. IPC Layer (optional, behind a feature flag): JSON-over-stdin/stdout or local WebSocket for requests from an external controller. Disabled by default.
  5. AuditLogger: structured JSONL logs saved under `%AppData%/RuneLite/ai-agent-tools/logs`.

## Coordinate Spaces
- GameSpace (logical): RuneLite client area coordinates (origin at top-left of the game viewport).
- ScreenSpace (physical): OS screen coordinates from the top-left of the primary display.
- Conversion: `Client.getRealDimensions()` and window bounds translate GameSpace <-> ScreenSpace.

## CaptureService
- Inputs:
  - region: `{ x, y, width, height, space: 'GameSpace' | 'ScreenSpace' }`
  - format: `PNG` | `RAW` (default `PNG`)
  - downscale: optional integer factor ≥ 1 (default 1)
- Behavior:
  - Validate region lies within current client viewport; if `GameSpace`, convert to `ScreenSpace`.
  - Use RuneLite image hooks or Swing snapshot; fallback to `Robot.createScreenCapture` for ScreenSpace.
  - Apply downscale if requested using high-quality interpolation.
  - Return bytes and metadata: `{ width, height, space, ts, capture_ms }`.
- Performance targets: 128×128 ≤ 8 ms; full viewport ≤ 25 ms.

## InputService
- Mouse API:
  - move: `{ x, y, space }` → smooth path with micro-jitter, 80–220 ms depending on distance.
  - click: `{ button: 'LEFT'|'RIGHT', delay_ms? }` → press+release, down-time 60–140 ms.
  - moveAndClick: `{ x, y, space, button }`.
- Keyboard API:
  - typeText: `{ text, per_char_delay_ms_range: [60,140] }` (ASCII only unless whitelisted).
  - keyCombo: `{ keys: ['CTRL','C'], order: 'down-then-up' }` (safe subset).
- Safety policies (PolicyGuard):
  - ≤ 6 clicks/sec, ≤ 10 key presses/sec; minimum inter-action delay with randomness.
  - Inputs only when RuneLite window focused and visible.
  - Clicks constrained to viewport (except whitelisted UI chrome).

## IPC Interface (optional)
- Disabled by default; enable via config `enableIpc=true`.
- Transport: local WebSocket `ws://127.0.0.1:17877` or named pipe; JSON messages.
- Requests:
  - capture: `{ kind:'capture', region, format?, downscale? }`
  - input: `{ kind:'input', mouse?|keyboard? }`
- Responses:
  - success: `{ ok:true, id, data? }`
  - error: `{ ok:false, id, code, message }`
- Authentication: shared secret `ipcAuthToken`; reject on mismatch.

## Plugin Configuration
- `enableIpc` (default: false)
- `ipcAuthToken` (default: empty → disabled)
- `maxClicksPerSecond` (default: 5)
- `maxKeysPerSecond` (default: 8)
- `minInterActionDelayMs` (default: 120)
- `captureDownscaleMax` (default: 4)
- `logDirectory` (default: `%AppData%/RuneLite/ai-agent-tools/logs`)

## Auditing & Telemetry
- JSONL per session: `{ ts, event, requestId, kind, payloadHash, durationMs, result, error? }`.
- Rotate at 50 MB; retain 7 days.
- Overlay metrics panel shows recent rates and last action.

## Example Flows
1) Capture minimap:
   `{ kind:'capture', region:{ x:568, y:9, width:152, height:152, space:'GameSpace' }, format:'PNG', downscale:1 }`.
2) Inventory click:
   `{ kind:'input', mouse:{ moveAndClick:{ x:620, y:345, space:'GameSpace', button:'LEFT' } } }`.

## Implementation Notes
- `@PluginDescriptor(name = 'AI Agent Tools')`; inject `Client`, `ClientThread`, `ConfigManager`.
- Prefer RuneLite image hooks; Swing snapshot else; `Robot` as fallback.
- `Robot` on a dedicated thread with smoothing; no input when minimized/unfocused.
- Surface structured errors and log all failures.

## Security & Ethics
- IPC disabled by default; input rate-limited.
- Warn about ToS; intended for research/QA in controlled environments.

## Acceptance (this step)
- File exists at `docs/RUNELITE_PLUGIN_SPEC.md` with implementable detail; no TODOs.



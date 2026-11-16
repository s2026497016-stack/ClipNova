# ClipNova Product Specification

## Product goal

Build one reliable video-creation workspace that takes a creator from source media to reviewed, platform-ready short clips. The product takes inspiration from five categories of competitor workflow without copying their proprietary code, logos, copy, or exact visual designs.

## Reference strengths

| Reference product | Workflow to learn from |
|---|---|
| OpusClip | Long-form repurposing, highlight suggestions, captions, reframing, hooks |
| StreamLadder | Stream URL workflows, fast clipping, vertical layouts |
| Eklipse | Gaming-oriented highlight discovery and event-based moments |
| Vizard | Long recordings, editing, collaboration/workspace patterns |
| Spikes Studio | Automated clip generation, caption styling, creator publishing flow |

## Core modules

### 1. Home dashboard
- Recent projects and processing status
- New project actions: upload, paste supported URL, connect a live source
- Recent clips, storage usage, and clear next steps

### 2. Media intake
- Local file upload with progress and resumable/chunked transfer
- Supported source URL validation
- Source metadata, duration, thumbnail, and ownership/permission reminder
- Clear errors when a provider blocks access or a stream is unavailable

### 3. AI highlight engine
- Speech/transcript-based highlight candidates
- Scene, audio-energy, and context signals
- Gaming-event detection as a separate capability where game-specific signals/models exist
- Candidate scores with explanations and editable in/out points
- Never claim game events are detected when only generic audio analysis is available

### 4. Live clipping
- Provider-aware live source connection
- Rolling recording buffer and bounded processing queue
- Near-live candidate generation with clear latency/status indicators
- Recovery from stream disconnects and safe shutdown
- Respect platform terms, access controls, and creator permissions

### 5. Clip editor
- Timeline trim and preview
- 9:16, 1:1, and 16:9 canvases
- Smart subject framing with manual position/zoom override
- Caption text, timing, font, color, emphasis, and safe-area controls
- Hook/title editing and clip regeneration without losing the source

### 6. Workspace and library
- Projects, sources, clips, exports, and activity history
- Search, filters, and reusable caption presets
- Per-user data isolation for hosted deployments
- Storage controls and deletion tools

### 7. Export and publishing
- MP4 export with selectable resolution and aspect ratio
- Platform presets for Shorts, Reels, and TikTok
- Download first; social account connection and publishing only when the provider API supports it
- Review/approval step before scheduled or automatic publishing

## Non-functional requirements

- Secrets stay in environment variables or a secure settings store, never committed.
- Long-running work uses bounded queues and visible job states.
- Upload, render, and live-recording failures are recoverable and explain themselves.
- Tests cover permissions, job lifecycle, source validation, media cleanup, and exports.
- All user-visible controls must work; unavailable integrations must be marked as planned or disabled.

## Delivery order

1. Import and audit the existing licensed codebase; preserve its license notices.
2. Rebrand product identifiers, environment variables, docs, UI copy, and links.
3. Verify the baseline app and its existing tests before changing core media logic.
4. Improve dashboard and project workflow.
5. Add/verify import, clip review, captions, reframing, and export.
6. Strengthen live workflows and gaming-specific detection.
7. Add publishing integrations and end-to-end regression coverage.

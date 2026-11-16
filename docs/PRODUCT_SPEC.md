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

## Current implementation status

- [x] Imported the 89-file application foundation, including backend, web UI, tests, fonts, demo media and deployment assets.
- [x] Preserved the upstream MIT license file and its copyright notice.
- [x] Rebranded the main app pages, email templates, logos, configuration names, deployment files and repository links as ClipNova.
- [x] Removed the upstream maker's Instagram promotion and replaced the repository link with the ClipNova repository.
- [x] Added a GitHub Actions workflow to run the isolated regression suite.
- [ ] Confirm the first CI run passes; fix any regressions introduced during import/rebranding.
- [ ] Review the user's demo video and map its exact interface and interactions into the product.
 
## Delivery order

1. **Foundation:** import, rebrand and run regression tests.
2. **Core workflow:** polish dashboard, media intake, clip review and project library.
3. **Editing:** timeline controls, reframing, captions, title/hook editing and export.
4. **Livestream:** verify provider connections, rolling capture, queue stability and latency.
5. **Gaming:** add game-aware event detection where a suitable event signal/model exists.
6. **Publishing:** validate provider integrations, review/approval and scheduled publishing.
7. **Release:** end-to-end tests, deployment, backups, security review and user documentation.

The source import and rebrand are committed. The first automated test run is in progress; features are not marked complete until their real workflows have been verified.

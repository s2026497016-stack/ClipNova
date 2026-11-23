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

## Verified implementation status

### Working in the imported application
- [x] Local video upload, chunked uploads, source URL intake and media metadata.
- [x] Transcript/audio-based highlight selection, with an AI provider configured or a loudness-based fallback.
- [x] Vertical MP4 rendering with animated word captions, hook text, caption styles, background/zoom/centre-crop layouts and experimental smart face framing.
- [x] Clip review, manual in/out adjustments, title/hook edits and re-rendering.
- [x] Supported YouTube, Twitch and Kick source workflows, including rolling live-stream capture where the provider permits access.
- [x] Project/creator history, accounts, storage controls, job queues and supported social-account publishing flows.
- [x] Upstream MIT license and required copyright notice retained.
- [x] ClipNova branding applied to app pages, emails, logo assets, configuration, deployment templates and repository links.
- [x] GitHub Actions regression workflow added. The latest run completed successfully, including dependency installation and `python tests/run.py`.

### Known gaps — do not describe these as finished
- [ ] Gaming event recognition is not computer vision: current highlight selection uses transcript, audio loudness and available live-chat signals. It does not reliably identify kills, wins, headshots or game HUD events from pixels.
- [x] Selected clips now receive optional visual-activity evidence (sampled motion, edge density and scene changes), saved with clip metadata and refreshed when a clip is re-rendered. This is descriptive visual evidence only; it does not recognize specific game events or change AI clip ranking.
- [x] The clip editor now includes an interactive trim timeline with IN/OUT range controls, synchronized numeric fields, and a playhead that scrubs the rendered preview.
- [ ] The editor is not yet a full multi-track nonlinear editor: independent movable audio/video/caption clips, keyframes, transitions, and layered compositing are still planned.
- [ ] Smart face tracking now samples and smooths a dominant face position over time, but needs real-footage quality testing; it does not yet track identity through occlusion or support multiple people. Automatic speaker-aware reframing is not implemented.
- [ ] Cloud-hosted projects and cross-device sync require a configured deployment/storage architecture; local data is not automatically synced between devices.
- [ ] Live clipping latency and provider reliability still need real stream tests with authorized channels.
- [ ] Social publishing needs valid provider credentials and must be tested against each platform's current API permissions.
- [ ] Review the user's demo video and map its exact interface and interactions into the product; the video has not yet been accessible to inspect.

The imported foundation is automated-test green, but a successful regression suite is not the same as full production acceptance. Each known gap must be implemented and tested before being marked complete.

## Delivery order

1. **Foundation:** import, rebrand and run regression tests.
2. **Core workflow:** polish dashboard, media intake, clip review and project library.
3. **Editing:** timeline controls, reframing, captions, title/hook editing and export.
4. **Livestream:** verify provider connections, rolling capture, queue stability and latency.
5. **Gaming:** add game-aware event detection where a suitable event signal/model exists.
6. **Publishing:** validate provider integrations, review/approval and scheduled publishing.
7. **Release:** end-to-end tests, deployment, backups, security review and user documentation.

The source import and rebrand are committed. The first automated test run is in progress; features are not marked complete until their real workflows have been verified.


## Smart face framing update

The layout selector now includes **Smart face framing**. For landscape footage, ClipNova samples up to 25 frames across each selected clip with OpenCV's bundled frontal-face detector. It smooths the detected horizontal face positions and generates a time-based FFmpeg crop expression, so the 9:16 window can move as the person moves. If no face is found, the video is portrait/square, or detection cannot run, rendering safely falls back to the existing centre crop. This is single-dominant-face tracking; identity persistence through occlusion and multi-person selection still need a dedicated tracker and real-footage validation.

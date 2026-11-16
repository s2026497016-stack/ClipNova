# ClipNova

ClipNova turns long videos and live streams into short-form clips. It is built on an open-source video processing foundation and is being developed into a unified creator workspace.

## Current capabilities inherited from the application foundation

- Upload and process local video files.
- Generate candidate moments using speech transcription and AI-assisted analysis.
- Render vertical clips with captions and configurable styles.
- Record supported livestream sources into a rolling buffer and process highlights.
- Organize creators, channels, projects and clip history.
- Manage accounts, settings, storage and processing jobs.
- Connect supported social publishing providers where credentials and platform APIs are configured.

## Product direction

ClipNova is being developed with workflow inspiration from OpusClip, StreamLadder, Eklipse, Vizard and Spikes Studio: long-form repurposing, livestream workflows, gaming highlight discovery, a hands-on editor, captions, reframing and creator publishing.

The product will use original ClipNova branding and implementation. It will not copy competitors' proprietary source code, logos or exact visual designs.

## Run locally

Requirements: Python 3.11+, FFmpeg, and the dependencies in `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m studio
```

Open the local address printed by the application. Configure an AI provider and key in the app settings to enable AI-assisted moment selection and text generation. Without a configured provider, only the fallback capabilities supported by the app are available.

## Configuration

Copy `.env.example` to `.env`. Keep secrets in `.env`; never commit API keys, tokens, passwords, or private media.

See [DEPLOY.md](DEPLOY.md) for deployment and provider setup.

## License and attribution

ClipNova retains the upstream MIT license and required copyright notice for the reused application foundation. See [LICENSE](LICENSE). This project is an independent derivative; ClipNova branding and new work are maintained separately.

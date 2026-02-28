# Context Guard 🛡️

**Stop wasting tokens.** Audit your project for AI context waste.

Most AI coding agents (Claude Code, OpenClaw, Cursor) charge by the token. Context Guard scans your local project and finds the "bloat" (logs, binary assets, 10k-line lockfiles) that are eating your context window and your budget.

◈ **Live Auditor:** [https://context-guard-six.vercel.app](https://context-guard-six.vercel.app)
◈ **Designed by Human // Delivered by Tank.**

## Quick Start (Pro Plan)

If you have purchased the Full Access plan, you can run the scanner instantly:

```bash
curl -sSL https://context-guard-six.vercel.app/install.sh | bash
```

## Features

- **Token Audit:** Precise token counting using `tiktoken`.
- **Bloat Detector:** Find log files and binary assets killing your context window.
- **Cost Forecast:** Real-time pricing estimates for GPT-4, Claude 3, and Gemini.
- **Automated Ignore:** Generate custom `.contextignore` files to keep sessions lean.

## Technical Details

The core engine is written in Python and uses the `cl100k_base` encoding, making it compatible with the latest OpenAI and Anthropic models.

---
© 2026 Context Guard Labs. Powered by [OpenClaw](https://openclaw.ai).

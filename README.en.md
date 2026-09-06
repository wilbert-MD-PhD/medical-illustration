# Medical Illustration

An evidence-aware workflow for medical education illustrations, comics and infographics: plan the page, verify references, preserve approved anatomy, add editable lettering, and record review and delivery checks.

The Skill instructions are primarily in Chinese, with English discovery metadata. This English page is an installation overview; it does not represent a separately validated English workflow.

[中文首页](README.md) · [Releases](https://github.com/wilbert-MD-PhD/medical-illustration/releases) · [Validation scope](docs/validation.md)

## What you get

- Workflows for complete projects, single pages, revision, lettering, and delivery.
- Evidence, anatomy-reference, prompt, lettering, and review templates.
- A non-destructive Python project initializer.
- An editable SVG lettering example, a blank base, and a PDF review copy.

Image models, vector software, medical atlases, and human reviewers are supplied by the user's environment. Medical approval is specific to each work and reviewer; it is never included with an installation.

## Install

Paste these two lines into Codex:

```text
Use $skill-installer to install this Skill into my personal skills directory and verify the installation:
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0-rc.5/plugins/medical-illustration/skills/medical-illustration
```

Follow the [first-run environment checks](plugins/medical-illustration/skills/medical-illustration/references/first-run.md) to verify image generation, Chinese lettering and PDF export. Use `$medical-illustration` on your next turn; restart Codex if the skill list has not refreshed. This local installation route requires a desktop, CLI or IDE environment with local file and GitHub access. [Shareable installation guide](INSTALL.md).

Or download the [standalone Skill ZIP](https://github.com/wilbert-MD-PhD/medical-illustration/releases/download/v1.0.0-rc.5/medical-illustration-1.0.0-rc.5.zip) and copy its `medical-illustration/` folder to `~/.agents/skills/` (Windows: `%USERPROFILE%\.agents\skills\`). For project scope, use `<project>/.agents/skills/`.

Repository source archives contain the Marketplace layout: copy only the complete Skill directory at `plugins/medical-illustration/skills/medical-illustration/`. Restart Codex if it does not appear.

For a CLI with plugin support:

```bash
codex plugin marketplace add wilbert-MD-PhD/medical-illustration
codex plugin add medical-illustration@medical-illustration-marketplace
```

Choose one installation route to avoid duplicate skills. The old `v1.0.0-rc.2` tag lacks Skill source, and its uploaded ZIP has incorrectly marked Unicode filenames. Use `rc.3` or later.

## Try it

```text
Use $medical-illustration to plan a one-page medical education illustration.
Create a page brief, risk classification, and structured prompt.
Keep this as a draft; do not generate an image yet.
```

See the [two-page TFCC comic showcase](docs/showcase/tfcc/README.md), including blank bases and a lettered PDF review copy, and [installation details](plugins/medical-illustration/skills/medical-illustration/references/dependencies-installation.md).

## License

By wilbert. Content, templates and examples: CC BY-NC-SA 4.0. Executable code: MIT. Original works created using the workflow are not automatically relicensed; copied templates and third-party assets keep their own terms. See [license scope](LICENSE.md) and [NOTICE](plugins/medical-illustration/skills/medical-illustration/NOTICE.md).

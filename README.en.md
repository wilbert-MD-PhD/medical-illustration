# Medical Illustration

An evidence-aware workflow for medical education illustrations, comics and infographics: plan the page, verify references, preserve approved anatomy, add editable lettering, and record review and delivery checks.

The Skill instructions are primarily in Chinese, with English discovery metadata. This English page is an installation overview; it does not represent a separately validated English workflow.

[Install](#install) · [See the output](#see-the-output) · [Try it](#try-it) · [中文首页](README.md) · [Releases](https://github.com/wilbert-MD-PhD/medical-illustration/releases) · [Validation scope](docs/validation.md)

## What you get

- Workflows for complete projects, single pages, revision, lettering, and delivery.
- Evidence, anatomy-reference, prompt, lettering, and review templates.
- A non-destructive Python project initializer.
- An editable SVG lettering example, a blank base, and a PDF review copy.

Image models, vector software, medical atlases, and human reviewers are supplied by the user's environment. Medical approval is specific to each work and reviewer; it is never included with an installation.

## See the output

**A two-page TFCC education comic, from blank artwork to a lettered PDF review copy.** The following two pages show scene-based storytelling, character continuity, and Chinese lettering.

| Page 1 · Injury scene | Page 2 · Everyday movements |
|:---:|:---:|
| [![Page 1 with lettering](docs/showcase/tfcc/page-1.jpg)](docs/showcase/tfcc/page-1.jpg) | [![Page 2 with lettering](docs/showcase/tfcc/page-2.jpg)](docs/showcase/tfcc/page-2.jpg) |

[**View the two-page PDF**](docs/showcase/tfcc/review.pdf) · [Page 1 blank artwork](docs/showcase/tfcc/base-1.png) · [Page 2 blank artwork](docs/showcase/tfcc/base-2.png) · [Example notes](docs/showcase/tfcc/README.md)

<details>
<summary>Compare the two blank pages</summary>

| Page 1 · Blank artwork | Page 2 · Blank artwork |
|:---:|:---:|
| [![Page 1 blank artwork](docs/showcase/tfcc/base-1.png)](docs/showcase/tfcc/base-1.png) | [![Page 2 blank artwork](docs/showcase/tfcc/base-2.png)](docs/showcase/tfcc/base-2.png) |

</details>

This example remains a review copy and demonstrates the production output.

## Install

**Paste the following into Codex to install the Skill and check your production environment:**

```text
Use $skill-installer to install this Skill into my personal skills directory, preserving existing edits.
Then follow references/first-run.md to check image generation, Chinese lettering and PDF export,
and install any free dependencies needed for the task:
https://github.com/wilbert-MD-PhD/medical-illustration/tree/v1.0.0-rc.5/plugins/medical-illustration/skills/medical-illustration
```

Requires a Codex desktop, CLI or IDE environment with local file and GitHub access. Use `$medical-illustration` on your next turn; restart Codex if it does not appear. Image generation access depends on your account and available tools.

[**Share the installation and usage guide**](INSTALL.md) · [First-run checks](plugins/medical-illustration/skills/medical-illustration/references/first-run.md)

<details>
<summary>Other installation options: ZIP / Marketplace</summary>

Or download the [standalone Skill ZIP](https://github.com/wilbert-MD-PhD/medical-illustration/releases/download/v1.0.0-rc.5/medical-illustration-1.0.0-rc.5.zip) and copy its `medical-illustration/` folder to `~/.agents/skills/` (Windows: `%USERPROFILE%\.agents\skills\`). For project scope, use `<project>/.agents/skills/`.

Repository source archives contain the Marketplace layout: copy only the complete Skill directory at `plugins/medical-illustration/skills/medical-illustration/`. Restart Codex if it does not appear.

For a CLI with plugin support:

```bash
codex plugin marketplace add wilbert-MD-PhD/medical-illustration
codex plugin add medical-illustration@medical-illustration-marketplace
```

Choose one installation route to avoid duplicate skills. The old `v1.0.0-rc.2` tag lacks Skill source, and its uploaded ZIP has incorrectly marked Unicode filenames. Use `rc.5` or later.

</details>

## Try it

Replace the bracketed fields with your topic, audience, and page count.

```text
Use $medical-illustration to create a [page count]-page medical education comic
about [topic] for [audience]. Verify the evidence and plan characters and storyboards,
then follow the applicable review steps to produce blank artwork, editable Chinese
lettering, and a PDF review copy. Keep unreviewed medical content marked as pending review.
```

See the [two-page TFCC comic showcase](docs/showcase/tfcc/README.md), including blank bases and a lettered PDF review copy, and [installation details](plugins/medical-illustration/skills/medical-illustration/references/dependencies-installation.md).

## License

By wilbert. Content, templates and examples: CC BY-NC-SA 4.0. Executable code: MIT. Original works created using the workflow are not automatically relicensed; copied templates and third-party assets keep their own terms. See [license scope](LICENSE.md) and [NOTICE](plugins/medical-illustration/skills/medical-illustration/NOTICE.md).

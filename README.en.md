# Medical Illustration

**Turn medical knowledge into readable stories and clear illustrations of anatomy and mechanisms.**

Medical Illustration is a Skill for use in Codex. Describe your topic, audience and intended use. It helps you find medical references, write a script, design and generate artwork, then add editable text and check the result.

[![Validation](https://github.com/wilbert-MD-PhD/medical-illustration/actions/workflows/validate.yml/badge.svg)](https://github.com/wilbert-MD-PhD/medical-illustration/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/wilbert-MD-PhD/medical-illustration?include_prereleases)](https://github.com/wilbert-MD-PhD/medical-illustration/releases)

[中文](README.md) · [Installation](INSTALL.md#english-installation) · [Releases](https://github.com/wilbert-MD-PhD/medical-illustration/releases)

## What you can make

| Your project | How the Skill helps |
|---|---|
| Educational comics for patients and the public | Explain a medical question through everyday situations, dialogue and connected scenes |
| Medical illustrations for teaching and patient education | Use real references to show anatomical layers, injury locations and repair processes with clear labels |
| Research schematics involving medical structures | Organize structures and mechanisms around your claims and evidence, distinguishing established relationships from hypotheses |

Choose your characters, visual style, length and output format. Text, bubbles, medical labels and added arrows stay editable, making it easier to revise wording, move annotations and correct individual areas. Deliverables can include a Markdown script, color artwork, editable layout files and a PDF.

## See the results

<!-- wrist-showcase:start -->
### Eight carpal bones, explained through a story

A doctor and Axuan start with eight counters on a table, then explore the two carpal rows, different viewpoints and the joints between bones. This six-page Chinese *Wrist and carpal joints* example, v1.1, connects everyday dialogue with anatomy supported by traceable references.

| Introducing the structures | Changing the viewpoint | Locating joint interfaces |
|---|---|---|
| [![Page 1](docs/showcase/wrist/pages/page-1.jpg)](docs/showcase/wrist/pages/page-1.jpg) | [![Page 3](docs/showcase/wrist/pages/page-3.jpg)](docs/showcase/wrist/pages/page-3.jpg) | [![Page 5](docs/showcase/wrist/pages/page-5.jpg)](docs/showcase/wrist/pages/page-5.jpg) |

[Light six-page preview (0.96 MB)](docs/showcase/wrist/preview-light.pdf) · [Full PDF (30.05 MB)](docs/showcase/wrist/review.pdf) · [Illustration-to-reference comparison](docs/showcase/wrist/README.en.md) · [Credits and licenses](docs/showcase/wrist/CREDITS.md)


<!-- wrist-showcase:end -->

### What happens under an adhesive bandage?

Xiaoman cuts her finger while folding a paper airplane. Once the bandage is on, what happens underneath? The comic starts with a small everyday accident and takes readers through clotting, cleanup and skin repair.

[![What happens under an adhesive bandage?](docs/showcase/bandage/comic-v1.4.jpg)](docs/showcase/bandage/review-v1.4.pdf)

[Read the PDF](docs/showcase/bandage/review-v1.4.pdf) · [Chinese script](docs/showcase/bandage/script.md) · [How it was made](docs/showcase/bandage/README.en.md)

### A story about wrist pain

The TFCC (triangular fibrocartilage complex) comic brings everyday movement, character dialogue and wrist anatomy into one story. These two pages show another visual style and an example of Chinese lettering.

| Page 1 | Page 2 |
|---|---|
| [![Page 1](docs/showcase/tfcc/page-1.jpg)](docs/showcase/tfcc/page-1.jpg) | [![Page 2](docs/showcase/tfcc/page-2.jpg)](docs/showcase/tfcc/page-2.jpg) |

[Read the two-page PDF](docs/showcase/tfcc/review.pdf) · [Example notes](docs/showcase/tfcc/README.md)

## Every anatomical illustration has specific references

**The Skill requires every structure used to explain anatomy to have credible evidence matching its body region, viewpoint and anatomical layer.** Production starts by verifying and inspecting atlases, textbooks, original research or traceable models. Records state which relationships each source supports, whether it was supplied to generation, and how the result was checked. Suitable existing references and artwork can be reused with their provenance intact.

The doctor comic contains **five anatomical images in six placements**. The expanded comparisons below cover the whole hand, both sides of the wrist and the articular disc, with specific plates, textbook pages and original inputs.

| Final image | Atlas and textbook attachments | Purpose and additional input |
|---|---|---|
| B01 / page 1: palmar hand | Gray219; *Wrist and Hand*, Fig.4.18, printed p.52 | Bone groups and adjacency; BodyParts3D M01 supplies right-hand geometry. The textbook supports wrist relationships only |
| B02 / page 2: carpal rows | Gray219; Fig.4.18, p.52 | Row relationships and palmar overlap; BodyParts3D M02 provides the palmar projection |
| B03 / page 3 upper: dorsal wrist | Gray220; Fig.4.18, p.52 | Dorsal appearance and occlusion; BodyParts3D M03 provides the dorsal view |
| B04 / page 3 lower: triquetrum and pisiform | Fig.4.18; Fig.4.19a, p.53 | Palmar-ulnar relationships; BodyParts3D M04 supplies the viewpoint. Both textbook figures share one source |
| B05 / pages 4–5: joint interfaces | Gray336; Fig.4.19a, p.53 | Radius, proximal carpal row and ulnar-side disc; M06 is an interpretive scaffold, while B02 was a color reference only |

### Whole hand: phalanges, metacarpals and carpals

[![Whole-hand artwork, right-hand model and Gray219 reference](docs/showcase/wrist/comparisons/hand.png)](docs/showcase/wrist/comparisons/hand.png)

Gray219 shows the hand's bone groups and adjacency. The model supplies the chosen right-hand camera; the atlas retains its original orientation. Fig.4.18 contributes wrist relationships rather than evidence for every detail of the whole hand.

### Carpal rows: grouping, adjacency and palmar overlap

[![B02 artwork, M02 projection and Gray219 carpal detail](docs/showcase/wrist/comparisons/rows.png)](docs/showcase/wrist/comparisons/rows.png)

The comparison focuses on carpal adjacency and palmar overlap of the pisiform. Teaching colors and numbers were added during production; the original atlas retains its bone labels.

### Dorsal view: checking visible anatomy from another angle

[![B03 artwork, M03 projection and textbook Fig.4.18a](docs/showcase/wrist/comparisons/dorsal.png)](docs/showcase/wrist/comparisons/dorsal.png)

Fig.4.18a shows the dorsal wrist, including ligaments and their bony background. Gray220 was also attached to the original generation request. These references support appearance and occlusion checks; the model sets the illustration's viewpoint.

### Triquetrum and pisiform: palmar-ulnar relationships

[![B04 artwork, M04 projection and textbook Fig.4.18b](docs/showcase/wrist/comparisons/pisiform.png)](docs/showcase/wrist/comparisons/pisiform.png)

Fig.4.18b adds palmar context and Fig.4.19a adds ulnar-side soft-tissue context. The textbook includes ligament occlusion and different viewpoints. Compare the artwork directly with its matching model view, and use the textbook to check structural relationships.

### Joint surfaces and articular disc: bone and soft tissue

[![B05 artwork, M06 scaffold and Gray336 coronal relationships](docs/showcase/wrist/comparisons/interfaces.png)](docs/showcase/wrist/comparisons/interfaces.png)

Gray336 shows coronal wrist relationships. Fig.4.19a labels the articular disk **AD**. They support spatial checks of the radius, proximal carpal row and ulnar-side disc. M06 is a teaching scaffold; joint annotations added afterward require their own checks.

### Original atlas plates, textbook pages and captions

| Gray219: palmar hand | Gray220: dorsal hand | Gray336: coronal wrist |
|---|---|---|
| [<img src="docs/showcase/wrist/references/gray219.jpg" height="260" alt="Complete Gray219 plate">](docs/showcase/wrist/references/gray219.jpg) | [<img src="docs/showcase/wrist/references/gray220.jpg" height="260" alt="Complete Gray220 plate">](docs/showcase/wrist/references/gray220.jpg) | [<img src="docs/showcase/wrist/references/gray336.png" height="260" alt="Complete Gray336 plate">](docs/showcase/wrist/references/gray336.png) |
| [Original source](https://commons.wikimedia.org/wiki/File:Gray219.png) | [Original source](https://commons.wikimedia.org/wiki/File:Gray220.png) | [Original source](https://commons.wikimedia.org/wiki/File:Gray336.png) |

| Printed p.52: Fig.4.18 | Printed p.53: Fig.4.19a |
|---|---|
| [<img src="docs/showcase/wrist/references/springer-p52.png" width="330" alt="Textbook p.52 with dorsal and palmar wrist figures and caption">](docs/showcase/wrist/references/springer-p52.png) | [<img src="docs/showcase/wrist/references/springer-p53.png" width="330" alt="Textbook p.53 with ulnar-side schematic and caption">](docs/showcase/wrist/references/springer-p53.png) |
| a: dorsal; b: palmar. Bony background supports viewpoint checks. [Original caption](https://www.ncbi.nlm.nih.gov/books/NBK570159/figure/ch4.Fig18/) | a: ulnar-side schematic, including the articular disk AD. MRI panels are not this example's bone-shape template. [Original caption](https://www.ncbi.nlm.nih.gov/books/NBK570159/figure/ch4.Fig19/) |

The Gray plates come from Henry Gray's *Anatomy of the Human Body* (1918). The textbook chapter is Omid Khalilzadeh, Clarissa Canella and Laura M. Fayad, *Wrist and Hand*, in *Musculoskeletal Diseases 2021–2024: Diagnostic Imaging* (Springer, 2021), DOI [10.1007/978-3-030-71281-5_4](https://doi.org/10.1007/978-3-030-71281-5_4). The [NCBI open chapter](https://www.ncbi.nlm.nih.gov/books/NBK570159/) provides the text and captions. Geometric inputs came from right-hand and distal-forearm components in [BodyParts3D / DBCLS](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html), version 4.0, simplified-99 meshes.

**These references have documented uses.** Atlas images and complete textbook pages were attached to the original anatomical-artwork requests. The doctor adaptation reuses the images and their provenance. These five comparison boards are display layouts: [crop records](docs/showcase/wrist/comparisons/crop-map.json) preserve coordinates and hashes, while the [input map](docs/showcase/wrist/reference-map.json) records original attachments and prompts. Multiple figures from one source do not count as independent evidence. Page 5's [photographic movement references](docs/showcase/wrist/README.en.md#detail-comparisons-and-motion-references) are recorded separately; page 6 uses teaching props.

[Five-page comparison PDF (18.18 MB)](docs/showcase/wrist/comparisons/reference-details.pdf) · [Detailed correspondence and checks](docs/showcase/wrist/README.en.md) · [Sources and asset-specific licenses](docs/showcase/wrist/CREDITS.md). **Production is complete; human medical review is pending.** Source traceability and medical sign-off are recorded separately.

## Get started

Follow the [installation guide](INSTALL.md#english-installation), then give Codex a request such as:

```text
Use $medical-illustration to create a one-page comic about wound healing for readers without a medical background.
Start with an everyday story, use bright, clear artwork and natural dialogue.
Find and use trusted medical references. Deliver a Markdown script, editable layout files and a PDF.
```

For research figures, provide your claims, papers, structural relationships and target layout. You can also supply an existing script or image for further production, lettering or revision.

This is a production workflow Skill. It needs image-generation tools, available fonts and a vector/PDF editing environment. Supported outputs depend on those tools; Illustrator files require the corresponding software. See the [installation guide](INSTALL.md#english-installation) for setup.

## Checks and review status

The workflow includes comparing structures against references, checking lettering and continuity, and keeping source and revision records. The comics demonstrate production results; human medical sign-off is still pending, as recorded in each example. [Validation scope](docs/validation.md)

## Licenses and feedback

Author: **wilbert**. Content, templates and examples use **CC BY-NC-SA 4.0**; executable code and CI use **MIT**. Third-party reference figures retain their own licenses; see the [wrist showcase credits](docs/showcase/wrist/CREDITS.md) and each example's source page. Independently created work does not automatically inherit the Skill's licenses. Copied templates and third-party materials remain subject to their applicable terms.

[License scope](LICENSE.md) · [Third-party notices](plugins/medical-illustration/skills/medical-illustration/NOTICE.md) · [Issues](https://github.com/wilbert-MD-PhD/medical-illustration/issues) · [Maintenance](docs/maintaining.md)

# Wrist and carpal joints · Doctor showcase v1.1

A six-page Chinese comic in which a doctor and Axuan explain wrist bones and joints. It serves as the Skill's anatomy-reference example: all five anatomical images map to specific atlas plates, textbook figures, geometric scaffolds and actual generation attachments. The records below state each source's scope and provide visual comparisons; dialogue, labels and joint annotations retain editable layouts.

[Light six-page raster preview (0.96 MB)](preview-light.pdf) · [Full PDF (30.05 MB)](review.pdf) · [Chinese detailed comparison](README.md) · [Credits and licenses](CREDITS.md) · [Actual reference map](reference-map.json) · [Preservation checks](preservation-check.json)

| Page 1 | Page 3 | Page 5 |
|---|---|---|
| ![Page 1](pages/page-1.jpg) | ![Page 3](pages/page-3.jpg) | ![Page 5](pages/page-5.jpg) |

## What was supplied to generation?

This table reflects the original anatomical-artwork invocation records, not a bibliography added afterward. M01–M04 are projections of right-sided BodyParts3D meshes. M06 is an interpretive coronal line drawing, not a photograph or a direct section of the original model.

| Artwork and final page | Geometric input | Independent images actually attached | Supported relationship |
|---|---|---|---|
| B01 / page 1 | [M01](scaffolds/M01.png) | [Gray219](references/gray219.jpg), [textbook p.52 / Fig.4.18](references/springer-p52.png) | Hand bone groups and adjacency. The textbook figure supports wrist relationships, not every detail of the whole hand. |
| B02 / page 2 | [M02](scaffolds/M02.png) | [Gray219](references/gray219.jpg), [p.52 / Fig.4.18](references/springer-p52.png) | Carpal rows and palmar overlap, including the pisiform. |
| B03 / page 3 upper | [M03](scaffolds/M03.png) | [Gray220](references/gray220.jpg), [p.52 / Fig.4.18](references/springer-p52.png) | Dorsal shape and overlap. Conflicting website descriptions do not establish the viewpoint. |
| B04 / page 3 lower | [M04](scaffolds/M04.png) | [p.52 / Fig.4.18](references/springer-p52.png), [p.53 / Fig.4.19a](references/springer-p53.png) | Palmar-ulnar relationship of the triquetrum and pisiform. These textbook figures share one source; the independent geometric source is BodyParts3D. |
| B05 / pages 4–5 | [M06](scaffolds/M06.png) | [Gray336](references/gray336.png), [p.53 / Fig.4.19a](references/springer-p53.png) | Radius, proximal carpal row, ulnar-side articular disc and joint interfaces. B02 was also attached for illustration color/style only. |

The textbook is Khalilzadeh O, Canella C, Fayad LM. *Wrist and Hand* (2021), DOI [10.1007/978-3-030-71281-5_4](https://doi.org/10.1007/978-3-030-71281-5_4). Printed pages 52 and 53 are pages 12 and 13 of the local chapter PDF. Complete rendered book pages were attached; the relevant anatomical correspondence is with the stated schematic panels, not unrelated MRI/pathology panels. See [original chapter and captions](https://www.ncbi.nlm.nih.gov/books/NBK570159/).

The final right-sided camera is set by the model; atlas views were not mirrored to manufacture a visual match. The stated 140° refers to the difference between two model camera viewpoints, not a clinical range-of-motion instruction. Page 6 uses counting props and dialogue, not newly generated anatomy.

## Compare the actual inputs and output

| Asset | Geometric scaffold | Generated anatomical artwork |
|---|---|---|
| B01 | <img src="scaffolds/M01.png" width="200" alt="M01"> | <img src="artwork/B01.png" width="200" alt="B01"> |
| B02 | <img src="scaffolds/M02.png" width="200" alt="M02"> | <img src="artwork/B02.png" width="200" alt="B02"> |
| B03 | <img src="scaffolds/M03.png" width="200" alt="M03"> | <img src="artwork/B03.png" width="200" alt="B03"> |
| B04 | <img src="scaffolds/M04.png" width="200" alt="M04"> | <img src="artwork/B04.png" width="200" alt="B04"> |
| B05 | <img src="scaffolds/M06.png" width="200" alt="M06"> | <img src="artwork/B05.png" width="200" alt="B05"> |

The [Chinese comparison page](README.md) displays the independent atlas and textbook images alongside these relationships. Source images, mesh-derived illustrations and their appearances in the PDF retain the asset-specific terms in [CREDITS](CREDITS.md), rather than the repository's general noncommercial content license.

## Detail comparisons and motion references

Five display boards show [the whole hand](comparisons/hand.png), [the dorsal wrist](comparisons/dorsal.png), [the two rows](comparisons/rows.png), [triquetrum/pisiform](comparisons/pisiform.png) and [radial articulation/articular disc](comparisons/interfaces.png). See the [Chinese annotated comparison](README.md#结构局部对照), [five-page PDF boards, 18.18 MB](comparisons/reference-details.pdf) and [crop coordinates](comparisons/crop-map.json). These crops do not replace the original attachment records. Source orientations remain unchanged; different viewpoints are stated explicitly.

Page 5 introduces wrist-bending and palm-turning demonstrations using two actual photographic generation attachments: [Delva et al. 2020, Fig.1](references/motion-delva-fig1.jpg) and [Zhang et al. 2024, Fig.1](references/motion-zhang-fig1.jpg). They constrain visible poses and do not supply character identities. Attribution is recorded in [CREDITS](CREDITS.md).

## Scope and verification

Version 1.1 revises five character scenes and retains the final close-up. Axuan remains: the user confirmed that she is not among the private assets to exclude. Dialogue order, gestures, props and external anatomical labels were revised. Five original anatomy images remain in six placements, with matching decoded pixels and placement bounds. Page 3 and complete medical regions are no longer claimed to be pixel-identical because their external annotations changed.

The native Illustrator file has 88 editable text objects, including 13 area-text frames: 11 complete dialogue blocks, the opening title and one two-line medical description. Character images and locked anatomical images are separate layers; all 12 images are embedded. The native output was reopened and checked, then closed. It is delivered separately in the project. The full reading PDF retains vector text; the lightweight PDF is a raster preview.

**Human medical review remains pending.** Source traceability and preservation checks are distinct from clinical approval. Local preparation does not mean a GitHub push or Release has occurred.

## VOC Data – IIIF Manifests with Transcriptions

This repository contains a Jupyter notebook and a dataset of IIIF manifests from the NL-HaNA VOC Archives, augmented with page-level transcription text. The notebook downloads transcription TXT files and corresponding IIIF JSON manifests, merges the text into each manifest's canvases, and saves per-document outputs as well as a combined manifest.

### Contents
- `VOC_Data_Downloader.ipynb`: Batch processor that downloads, merges, and exports manifests.
- `merged_manifests/`: Output directory containing:
  - `merged_*.json`: One IIIF Manifest per document with an added `text` field per canvas.
  - `combined_all_manifests.json`: A single IIIF Manifest aggregating all canvases from successful merges.

### Data source and license
- Manifests: `https://data.globalise.huygens.knaw.nl/manifests/inventories/{id}.json`
- Images: IIIF Image API services referenced within each canvas
- Rights: `https://creativecommons.org/publicdomain/mark/1.0/` (as present in manifests)

### Notebook overview
The notebook performs these steps:
1. Read a `.tab` file listing transcription TXT URLs (one per line).
2. For each URL:
   - Download the TXT file; infer the document identifier (e.g., `1111`) from the filename.
   - Construct the corresponding IIIF manifest URL via a template.
   - Parse the TXT into sections keyed by canvas label IDs (e.g., `NL-HaNA_1.04.02_1111_0001`).
   - Merge the matched text into the manifest by setting a `text` field on each canvas.
   - Save as `merged_{id}.json` under `merged_manifests/`.
3. Create `combined_all_manifests.json` that concatenates all canvases from the successfully processed manifests.
4. Zip the `merged_manifests/` folder for convenience.

### Output schema (IIIF Presentation 3 with additions)
Each `merged_*.json` is an IIIF Manifest with a non-standard addition: a `text` field on each canvas. Key fields:
- Manifest
  - `@context`: `http://iiif.io/api/presentation/3/context.json`
  - `id`, `type`: `Manifest`
  - `label`, `metadata`, `rights`
  - `items`: Array of canvases
- Canvas (per page)
  - `id`, `type`: `Canvas`
  - `label.en[0]`: Canvas identifier, e.g., `NL-HaNA_1.04.02_1111_0001`
  - `height`, `width`
  - `items[0].items[0].body`: IIIF Image resource
  - `text`: String of merged transcription for this canvas (may be empty if no match)

Example (truncated):
```json
{
  "type": "Manifest",
  "label": {"en": ["Inventory 1111"]},
  "items": [
    {
      "type": "Canvas",
      "label": {"en": ["NL-HaNA_1.04.02_1111_0001"]},
      "items": [
        {
          "type": "AnnotationPage",
          "items": [
            {"type": "Annotation", "motivation": "painting", "body": {"type": "Image", "format": "image/jpeg"}}
          ]
        }
      ],
      "text": "... merged transcription text ..."
    }
  ]
}
```

`combined_all_manifests.json` is also a `Manifest` whose `items` array is the concatenation of the `items` from all successful `merged_*.json` files. Its `label` and `metadata` summarize the collection.

### How to run
1. Ensure you have a `.tab` file containing TXT download URLs (one per line). Example referenced in the notebook: `globalise_transcriptions_v2_txt.tab`.
2. Open `VOC_Data_Downloader.ipynb` in Jupyter and run all cells, or call `main(...)` from within the notebook:

```python
main('globalise_transcriptions_v2_txt.tab')
```

Default concurrency is 15 workers; adjust via `max_workers` if needed:

```python
main('globalise_transcriptions_v2_txt.tab', max_workers=20)
```

Outputs will be written to:
- `merged_manifests/` (individual manifests and `combined_all_manifests.json`)
- `merged_manifests.zip`

### Environment requirements
The notebook depends on standard Python 3 libraries plus `requests`. Minimal setup:

```bash
pip install requests
```

Recommended: Run inside a virtual environment. The notebook uses network access to fetch TXT and JSON files.

### Notes and caveats
- Canvas `text` is added locally and is not part of the IIIF Presentation 3 standard; downstream tools should treat it as a custom extension.
- TXT-to-canvas matching relies on labels like `NL-HaNA_1.04.02_{id}_{page}`; if labels or TXT formatting differ, some canvases may have empty `text`.
- `combined_all_manifests.json` may be large; use streaming parsers for programmatic consumption.

### Citation
If you use this data, please credit the NL-HaNA VOC Archives and the GLOBALISE project data services. Include a link to the manifest endpoints and the public domain mark indicated in the manifests.



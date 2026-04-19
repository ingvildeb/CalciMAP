# CalciMAP

Project-specific analysis and workflow scripts for the CalciMAP dataset.

This repository is made available primarily for documentation, transparency, and provenance. It shows how the CalciMAP image-processing and validation workflow was organized in practice, but it is not intended to be a general-purpose or plug-and-play software package.

## What this repository is

CalciMAP contains stepwise scripts used to process, prepare, align, and technically validate brain section image data from the CalciMAP project.

The repository documents:

- how raw microscopy exports were renamed and organized
- how image thumbnails and Nutil transform files were prepared
- how section images were prepared for QuickNII / atlas anchoring
- how DeepSlice-based and manual anchoring steps were combined
- how technical validation datasets were assembled and analyzed
- how project metadata were reshaped for reporting and sharing

## What this repository is not

This repository should not be read as a polished software package for outside users.

In particular:

- many scripts contain hard-coded local paths
- scripts often assume access to specific metadata spreadsheets and folder layouts
- the numbered scripts are meant to be run in a project-specific sequence
- external desktop tools are part of the workflow
- some scripts are historical records of what was run and may require adaptation before reuse

If you want reusable helper functions for similar projects, see the sibling repository `brain_section_scripts`, which is included here as a submodule and is also available separately:

- <https://github.com/ingvildeb/brain_section_scripts>

## Best-practice way to read this repo

The best way to use this repository is as a worked example or project record.

It may be useful if you want to understand:

- how a large serial-section imaging workflow was broken into manageable scripted steps
- how `brain_section_scripts` was used in a real project
- what intermediate processing stages existed between raw TIFF export and atlas-based analysis
- how technical validation and quality-control analyses were organized

It is less useful if you are looking for a package that can be installed and run unchanged on a new dataset.

## Relationship to `brain_section_scripts`

This repository depends heavily on `brain_section_scripts`, which is included here under [brain_section_scripts](C:/Users/Ingvild/GitHub/CalciMAP/brain_section_scripts) as a git submodule.

Several CalciMAP scripts explicitly import helper modules from that sibling repo, especially for:

- file renaming
- Nutil file creation
- QuickNII / VisuAlign JSON handling
- transform-file validation
- Nutil output checking

In practice, CalciMAP is the project-specific workflow layer, while `brain_section_scripts` contains more reusable utility code.

## Repository structure

### `0_miscellaneous/`

Supporting and one-off project scripts for metadata handling, project summaries, naming fixes, and utility tasks.

Examples include scripts for:

- estimating dataset file sizes
- extracting immunostaining metadata
- checking file consistency
- renaming adult mouse and rat datasets
- generating metadata tables for openMINDS-style sharing

This folder is best thought of as project support code rather than a linear workflow.

### `1_preprocessing_images/`

Sequential preprocessing steps for turning raw microscopy exports into consistently named, transformed, and reviewed image sets.

This folder includes scripts for:

- setting up folder structure
- renaming raw TIFFs
- creating initial thumbnails
- generating Nutil transform sheets
- creating transformed TIFFs
- moving files for Photoshop-based manual correction
- running Photoshop edits
- generating final thumbnails and tiled overviews

This stage is where CalciMAP most directly uses `brain_section_scripts` for renaming, Nutil setup, and output checks.

### `2_anchoring_images/`

Scripts for preparing images for atlas anchoring and managing alignment files.

This folder includes steps for:

- resizing thumbnails for QuickNII
- copying files into an anchoring workspace
- generating QuickNII JSON files
- running DeepSlice
- inserting or combining anchoring information
- splitting alignments by stain
- moving finalized alignment data
- checking alignment-data consistency

This stage reflects a practical anchoring workflow built around QuickNII, DeepSlice, and project-specific file organization.

### `3_technical_validation/`

Scripts and outputs related to technical validation analyses.

This area includes:

- preparing segmentation folders
- creating Nutil quantifier files
- removing markerless slices (avoids errors with VisuAlign export)
- extracting pooled raw region data
- plotting validated pooled data
- analyzing technical variability
- composing technical-variability figures

The subfolder `technical_variability_analysis/` also contains metadata files and generated outputs, which makes this repository useful as a record of both code and analysis products.

### `brain_section_scripts/`

The included helper repository used by many of the CalciMAP scripts. This contains reusable utilities that are documented separately in that repo.

## External tools and assumptions

The scripts in this repository assume a Windows-based workflow and depend on a wider processing environment, not just Python.

Depending on the script, the workflow may require:

- `pandas`, `numpy`, `Pillow`, `matplotlib`, and related libraries
- `brain_section_scripts`
- Nutil
- QuickNII
- DeepSlice
- Adobe Photoshop
- Excel metadata spreadsheets stored in project-specific locations

Because of these assumptions, most scripts will not run out of the box in a different environment without editing paths and sometimes adjusting logic.

## How users should approach reuse

If you are browsing this repository for your own project, the safest assumption is that the code is illustrative rather than immediately reusable.

The most realistic reuse pattern is:

1. Read the folder structure to understand the order of operations.
2. Identify the step closest to your own use case.
3. Move shared logic into a utility repo such as `brain_section_scripts` if needed.
4. Adapt paths, metadata inputs, and naming assumptions for your own project.
5. Test each step on a small subset of data before scaling up.

For most users, direct reuse of the exact scripts here will require modification.


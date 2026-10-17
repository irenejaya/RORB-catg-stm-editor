# RORB catg/stm Editor

A QGIS plugin for viewing and editing RORB catchment (`.catg`) and storm
(`.stm`) files in structured tables instead of editing raw text.

## Features

- Edit CATG nodes, reaches, storages, and routing data.
- Create or edit STM storm parameters, bursts, pluviographs, and hydrograph stations.
- Filter and search data, batch-edit CATG print flags, and export node or reach tables to CSV.
- Save files while preserving their original formatting and, for STM files, encoding.

## Installation

Requires QGIS 3.40 or later. Install the plugin ZIP through
**Plugins → Manage and Install Plugins → Install from ZIP**.

For manual installation, copy that folder into `python/plugins` in your active
QGIS profile, restart QGIS, then enable **RORB catg/stm Editor** under
**Plugins → Manage and Install Plugins → Installed**.

## Use

Open **RORB CATG Editor** or **RORB STM Editor** from the plugin toolbar or the
QGIS **Plugins** menu. Open a file to edit it, or choose **New STM** to create a
storm file. Use **Save** or **Save As** to write your changes.

See [LICENSE](LICENSE) for license information. Report issues on the
[GitHub issue tracker](https://github.com/irenejaya/RORB-catg-stm-editor/issues).

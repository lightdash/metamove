# YAML Meta/Tags to Config Transformer

## 🚀 Quick Start (Mac)

1. Download the latest binary from [GitHub Releases](https://github.com/lightdash/metamove/releases)
2. Make it executable:
   ```bash
   chmod +x metamove
   ```
3. Run it:
   ```bash
   ./metamove --help
   ```
   Or move it to your PATH for global use:
   ```bash
   sudo mv metamove /usr/local/bin/
   ```

---

## 🖥️ Other Platforms (Windows/Linux/Mac)

### Option 1: Install with pipx (recommended)
If you have Python 3.8–3.13:
```bash
pip install pipx  # if you don't have it
pipx install metamove
metamove --help
```

### Option 2: Install with pip
```bash
pip install metamove
metamove --help
```

### Option 3: Clone and run with Poetry
```bash
git clone https://github.com/lightdash/metamove.git
cd metamove
poetry install
poetry run metamove --help
```

---

## What It Does

This script (`main.py`) transforms your YAML files by moving `meta` and `tags` properties under a `config` block, following dbt-style conventions. It preserves comments, whitespace, and the order of fields as much as possible.

## How It Modifies Your YAML

- For every dictionary (including nested ones), if `meta` or `tags` are present, they are moved under a `config` key.
- If a `config` block already exists, `meta` and `tags` are merged into it.
- The script preserves YAML comments and whitespace using `ruamel.yaml`.
- The placement of the new `config` block follows these rules:
  - If `config` already exists, it is used and updated in place.
  - If not, `config` is inserted where `meta` or `tags` were, or at the end if neither is found.

### Example

**Before:**
```yaml
models:
  - name: my_model
    meta:
      owner: "Data Team"
    tags: ["core", "customer"]
    columns:
      - name: id
        meta:
          is_primary_key: true
        tags: ["identifier"]
```

**After:**
```yaml
models:
  - name: my_model
    config:
      meta:
        owner: "Data Team"
      tags: ["core", "customer"]
    columns:
      - name: id
        config:
          meta:
            is_primary_key: true
          tags: ["identifier"]
```

## Edge Cases Covered

- `meta` and `tags` at any nesting level (including inside `columns`)
- Existing `config` blocks (merges new values in)
- `meta` and `tags` as any YAML type (dict, list, scalar)
- Preserves YAML comments and whitespace formatting
- Placement of `config` block follows dbt precedence rules
- No information is lost: all fields and values are preserved
- Merging of lists (e.g., tags) and dicts (e.g., meta)

## Edge Cases Not Covered

- If your YAML uses advanced anchors/aliases, these are not guaranteed to be preserved
- If you have custom logic for merging (e.g., deduplication of tags), only a set-union is performed for lists
- The script does not validate dbt-specific schema or field requirements
- If you have comments inside folded blocks, their placement may not be exact after transformation

## How Merging Works

- **Dictionaries:** If both the existing `config` and the moved `meta`/`tags` are dicts, they are merged shallowly (keys from the moved value overwrite existing ones).
- **Lists:** If both are lists (e.g., tags), a set-union is performed (duplicates removed, order not guaranteed).
- **Other types:** The moved value overwrites the existing value in `config`.

## Usage

Run the script from the command line:

```bash
python main.py
```

By default, it will read `demo.yml` and write the transformed output to `demo_updated.yml`. You can modify the script to use your own input/output files.

## Testing

A comprehensive test suite is provided in `test_main.py` and can be run with:

```bash
poetry install
poetry run pytest
``` 
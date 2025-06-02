# MetaMove: Automate Your dbt 1.10 Migration

> ⚠️ **dbt 1.10 Deprecation Notice**: Starting with dbt 1.10, `meta` and `tags` properties must be moved under a `config` block. This tool automates that migration for you.

## 🎯 What This Does For You

If you're using dbt (Core or Cloud) and upgrading to version 1.10, you'll start seeing deprecation warnings for your YAML files. This is because dbt is changing how `meta` and `tags` should be structured in your project files.

Instead of manually updating hundreds of YAML files, MetaMove does it automatically while preserving your comments and formatting.

### Before & After Example

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

## 🚀 Quick Start

### For Mac Users
1. Download the latest binary from [GitHub Releases](https://github.com/lightdash/metamove/releases)
2. Make it executable:
   ```bash
   chmod +x metamove
   ```
3. Run it:
   ```bash
   ./metamove --help
   ```

### For Everyone Else
The easiest way to install is with pipx:
```bash
pip install pipx  # if you don't have it
pipx install metamove
metamove --help
```

## 📋 Usage Examples

### Basic Usage
Transform a single YAML file:
```bash
metamove models/my_model.yml
```

Transform multiple files:
```bash
metamove models/*.yml models/schema/*.yml
```

### Output Options
Transform files and save to a specific directory:
```bash
metamove models/*.yml -o transformed_models
```

Transform files in place (modify original files):
```bash
metamove models/*.yml -i
```

### Working with dbt Projects
Transform all YAML files in your dbt project:
```bash
metamove models/*.yml seeds/*.yml snapshots/*.yml
```

Transform specific model directories:
```bash
metamove models/marts/*.yml models/staging/*.yml
```

### Best Practices
1. Always backup your files before running transformations
2. Use `-o` to test changes in a separate directory first
3. Once verified, use `-i` to update files in place

## 💡 Why Use This?

- **Save Hours**: No more manual file editing
- **Zero Risk**: Preserves all your comments and formatting
- **Complete**: Handles all your YAML files, including nested structures
- **Smart**: Intelligently merges existing config blocks
- **Safe**: Creates backups before making changes

## 🔧 Technical Details

The tool handles:
- `meta` and `tags` at any nesting level (including inside `columns`)
- Existing `config` blocks (merges new values in)
- All YAML types (dict, list, scalar)
- YAML comments and whitespace formatting
- Proper placement following dbt precedence rules

## 📚 Learn More

- [dbt 1.10 Release Notes](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-v1.10)
- [dbt Configuration Guide](https://docs.getdbt.com/reference/define-configs)
- [GitHub Issue #11651](https://github.com/dbt-labs/dbt-core/issues/11651)

## 🤝 Contributing

Found a bug or have an idea? [Open an issue](https://github.com/lightdash/metamove/issues) or submit a pull request! 
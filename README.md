# MetaMove: Automate Your dbt 1.10 Migration

> ✅ **dbt 1.10 Change**: Starting with dbt 1.10, `meta` and `tags` properties must be moved under a `config` block. This tool automates that migration for you.

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

The easiest way to install is with pipx:
```bash
pip install pipx  # if you don't have it
pipx install metamove
metamove --help
```

## 📋 Usage Examples

### Basic Usage
Transform a single YAML file into a new directory `transformed`:
```bash
metamove models/my_model.yml # saves to ./transformed/
```

Transform multiple files into `transformed`:
```bash
metamove models/* models/schema/*
```

### Output Options
By default, transformed files are saved to a `transformed` directory in your current location so your original files aren't modified:
```bash
metamove models/*  # saves to ./transformed/
```

Instead you can transform files and save to a specific directory:
```bash
metamove models/* -o transformed_models
```

Once you're feeling confident, transform files in place (modify original files):
```bash
metamove models/* -i
```

### Working with dbt Projects
The tool automatically processes only `.yml` and `.yaml` files, so you can use simple wildcards:
```bash
# Transform all YAML files in your dbt project
metamove models/* seeds/* snapshots/*

# Transform all YAML files in nested directories
metamove models/**/*

# Transform specific model directories
metamove models/marts/* models/staging/*
```

### Best Practices
1. Always backup your files before running transformations
2. Use the default output directory first to test changes
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

## 🍎 Mac Binary (Coming Soon)

> Note: The Mac binary is currently being signed and will be available soon. For now, please use the pipx installation method above.

Once available, Mac users will be able to:
1. Download the latest binary from [GitHub Releases](https://github.com/lightdash/metamove/releases)
2. Make it executable:
   ```bash
   chmod +x metamove
   ```
3. Run it:
   ```bash
   ./metamove --help
   ``` 
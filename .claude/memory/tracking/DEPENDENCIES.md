# DEPENDENCIES.md - Dependency Management & Conflict Resolution

**Project**: AI-Driven Tax and Portfolio Reconciliation System
**Last Updated**: 2025-11-15
**Dependency Manager**: Poetry
**Python Version**: 3.14.0

---

## 📋 Overview

This document tracks dependency management decisions, version constraints, known conflicts, and resolution strategies for the AiFinIntern project. It serves as a troubleshooting guide for Poetry dependency resolution issues.

---

## 🎯 Purpose

- **Track dependency conflicts** and their resolutions
- **Document version constraints** and the reasons behind them
- **Maintain compatibility matrix** for critical packages
- **Provide troubleshooting guide** for Poetry errors
- **Record dependency upgrade paths** and migration notes

---

## ⚠️ Known Dependency Conflicts & Resolutions

### [CONFLICT-001] PyArrow vs Datasets Version Mismatch

**Date Identified**: 2025-11-15
**Status**: ✅ RESOLVED
**Severity**: HIGH (Blocking installation)

#### Problem Description

```
Because no versions of datasets match >3.1.0,<3.2.0 || >3.2.0,<3.3.0 || ...
and datasets (3.1.0) depends on pyarrow (>=15.0.0),
datasets (>=3.1.0,<4.0.0) requires pyarrow (>=15.0.0).

So, because aifinintern depends on both pyarrow (^14.0.1) and datasets (^3.1.0),
version solving failed.
```

#### Root Cause

- **datasets** package (^3.1.0) requires **pyarrow >= 15.0.0**
- **pyproject.toml** specified **pyarrow = "^14.0.1"**
- Poetry cannot find a compatible version that satisfies both constraints

#### Resolution

**Action**: Upgrade pyarrow constraint from `^14.0.1` to `^15.0.0`

```toml
# Before
pyarrow = "^14.0.1"

# After
pyarrow = "^15.0.0"
```

**Rationale**:
- PyArrow 15.0.0 is stable and well-tested
- Hugging Face datasets library requires modern PyArrow for Arrow format support
- No breaking changes affecting our use case between 14.x and 15.x

**Related Packages**:
- `datasets ^3.1.0` - Requires pyarrow >= 15.0.0
- `polars ^0.19.19` - Compatible with pyarrow 15.x
- `pandas ^2.1.4` - Compatible with pyarrow 15.x

**Testing Required**:
- [x] Poetry install succeeds
- [ ] Data loading from Arrow format works
- [ ] Polars DataFrame conversions work
- [ ] Hugging Face datasets load correctly

**References**:
- [PyArrow 15.0.0 Release Notes](https://arrow.apache.org/release/15.0.0.html)
- [Datasets Library Requirements](https://github.com/huggingface/datasets)

---

### [CONFLICT-002] Sentry-SDK vs Wandb Version Mismatch

**Date Identified**: 2025-11-15
**Status**: ✅ RESOLVED
**Severity**: HIGH (Blocking installation)

#### Problem Description

```
Because no versions of wandb match >0.18.7,<0.19.0
and wandb (0.18.7) depends on sentry-sdk (>=2.0.0),
wandb (>=0.18.7,<0.19.0) requires sentry-sdk (>=2.0.0).

Thus, wandb (>=0.18.7,<0.19.0) is incompatible with sentry-sdk[fastapi] (>=1.39.2,<2.0.0).
So, because aifinintern depends on both wandb (^0.18.7) and sentry-sdk[fastapi] (^1.39.2),
version solving failed.
```

#### Root Cause

- **wandb** package (^0.18.7) requires **sentry-sdk >= 2.0.0**
- **pyproject.toml** specified **sentry-sdk[fastapi] = "^1.39.2"** (which is <2.0.0)
- Poetry cannot find a compatible version that satisfies both constraints

#### Resolution

**Action**: Upgrade sentry-sdk constraint from `^1.39.2` to `^2.0.0`

```toml
# Before
sentry-sdk = {version = "^1.39.2", extras = ["fastapi"]}

# After
sentry-sdk = {version = "^2.0.0", extras = ["fastapi"]}
```

**Rationale**:
- Sentry-SDK 2.0.0+ is required by wandb for telemetry and error tracking
- Sentry-SDK 2.0.0 is stable with FastAPI integration support
- Breaking changes in 2.0.0 are minimal and don't affect our error monitoring use case

**Related Packages**:
- `wandb ^0.18.7` - Requires sentry-sdk >= 2.0.0 for integration
- `fastapi ^0.108.0` - Compatible with sentry-sdk 2.x

**Testing Required**:
- [x] Poetry install succeeds
- [ ] Sentry error tracking works with FastAPI
- [ ] Wandb experiment tracking initializes correctly
- [ ] Error logging and monitoring functional

**References**:
- [Sentry-SDK 2.0.0 Release Notes](https://github.com/getsentry/sentry-python/releases/tag/2.0.0)
- [Wandb Requirements](https://github.com/wandb/wandb)

---

## 📦 Critical Package Version Constraints

### Data Processing Stack

| Package | Version Constraint | Reason | Dependencies |
|---------|-------------------|---------|--------------|
| **pyarrow** | `^15.0.0` | Required by datasets >=3.1.0, Arrow format support | datasets, polars, pandas |
| **pandas** | `^2.1.4` | Stable release with Arrow backend support | pyarrow, numpy |
| **numpy** | `^1.26.2` | Compatible with PyTorch 2.6.0+ and pandas 2.1+ | pandas, scipy, torch |
| **polars** | `^0.19.19` | Fast DataFrame library with Arrow backend | pyarrow |

### Machine Learning Stack

| Package | Version Constraint | Reason | Dependencies |
|---------|-------------------|---------|--------------|
| **torch** | `>=2.6.0` | CUDA 13.0 support for RTX 5090 | torchvision, torchaudio |
| **torchvision** | `>=0.21.0` | Compatible with torch 2.6.0+ | torch |
| **tensorflow** | `^2.18.0` | Latest stable with CUDA 13.0 support | - |
| **transformers** | `^4.46.3` | Latest Hugging Face models | datasets, tokenizers |
| **datasets** | `^3.1.0` | Hugging Face datasets library | pyarrow >=15.0.0 |

### Database & Storage

| Package | Version Constraint | Reason | Dependencies |
|---------|-------------------|---------|--------------|
| **sqlalchemy** | `^2.0.25` | Latest stable ORM with async support | asyncpg, psycopg2-binary |
| **asyncpg** | `^0.29.0` | PostgreSQL async driver | - |
| **redis** | `^5.0.1` | Latest stable Redis client | hiredis |

### Monitoring & Logging

| Package | Version Constraint | Reason | Dependencies |
|---------|-------------------|---------|--------------|
| **sentry-sdk** | `^2.0.0` | Required by wandb >=0.18.7, FastAPI error tracking | wandb, fastapi |
| **wandb** | `^0.18.7` | Experiment tracking and ML monitoring | sentry-sdk >=2.0.0 |

---

## 🔄 Dependency Upgrade History

### 2025-11-15: Migrate pyproject.toml to PEP 621 Standard

**Trigger**: Poetry deprecation warnings for [tool.poetry] metadata fields
**Impact**: LOW - No functional changes, only configuration format migration
**Migration Steps**:
1. Created [project] section with all metadata (name, version, description, etc.)
2. Converted [tool.poetry.extras] → [project.optional-dependencies]
3. Converted [tool.poetry.scripts] → [project.scripts]
4. Added dynamic = ["dependencies"] to indicate Poetry manages dependencies
5. Removed deprecated [tool.poetry] metadata section
6. Removed License classifier (now specified in [project.license])
7. Kept [tool.poetry.dependencies] for Poetry-specific features (sources, extras)

**Rollback Plan**: Revert to previous commit if Poetry compatibility issues arise

**Changed Files**:
- `pyproject.toml` - Migrated to PEP 621 [project] format

**Testing Checklist**:
- [x] Poetry check passes with no warnings
- [ ] Poetry install works correctly
- [ ] All dependencies resolve properly
- [ ] Project metadata is correct

**References**:
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Poetry PEP 621 Support](https://python-poetry.org/docs/pyproject/#poetry-and-pep-621)

---

### 2025-11-15: Sentry-SDK 1.39.2 → 2.0.0

**Trigger**: Poetry dependency resolution failure with wandb ^0.18.7
**Impact**: LOW - No breaking changes for error monitoring use case
**Migration Steps**: None required (automatic upgrade)
**Rollback Plan**: Downgrade wandb to <0.18.7 if issues arise

**Changed Files**:
- `pyproject.toml` - Updated sentry-sdk version constraint

**Testing Checklist**:
- [x] Poetry install succeeds
- [ ] Sentry error tracking works
- [ ] Wandb integration functional
- [ ] FastAPI error monitoring works

---

### 2025-11-15: PyArrow 14.0.1 → 15.0.0

**Trigger**: Poetry dependency resolution failure with datasets ^3.1.0
**Impact**: LOW - No breaking changes for our use case
**Migration Steps**: None required (automatic upgrade)
**Rollback Plan**: Downgrade datasets to <3.1.0 if issues arise

**Changed Files**:
- `pyproject.toml` - Updated pyarrow version constraint

**Testing Checklist**:
- [x] Poetry install succeeds
- [ ] Unit tests pass
- [ ] Data loading tests pass
- [ ] Integration tests pass

---

## 🛠️ Troubleshooting Guide

### Poetry Install Fails with "version solving failed"

**Symptoms**:
```
Because <package-a> depends on <package-b> (version-constraint)
and <package-c> depends on <package-b> (conflicting-constraint),
version solving failed.
```

**Diagnosis Steps**:

1. **Identify conflicting packages**:
   ```bash
   poetry show <package-name>
   poetry show <package-name> --tree
   ```

2. **Check dependency requirements**:
   ```bash
   poetry show <package-name> --latest
   ```

3. **Analyze dependency tree**:
   ```bash
   poetry show --tree | grep <package-name>
   ```

**Resolution Strategies**:

1. **Upgrade to compatible version**:
   - Update version constraint in `pyproject.toml`
   - Ensure no breaking changes in release notes
   - Test thoroughly before committing

2. **Downgrade to compatible version**:
   - Only if upgrade breaks functionality
   - Document reason in this file
   - Create TODO to upgrade in future

3. **Use version ranges**:
   ```toml
   # Instead of pinning to specific version
   package = "^1.2.3"

   # Use range if conflicts exist
   package = ">=1.2.0,<2.0.0"
   ```

4. **Check for alternative packages**:
   - Look for maintained forks
   - Consider replacing deprecated packages

### Poetry Lock File Conflicts

**Symptoms**:
- Merge conflicts in `poetry.lock`
- Inconsistent lock file after pull

**Resolution**:
```bash
# Delete lock file and regenerate
rm poetry.lock
poetry lock --no-update

# Or update all dependencies
poetry update
```

### CUDA/GPU Package Conflicts

**Symptoms**:
- PyTorch CUDA version mismatch
- Conflicting CUDA runtime versions

**Resolution**:
1. **Verify CUDA version**:
   ```bash
   nvidia-smi  # Check driver CUDA version
   nvcc --version  # Check toolkit CUDA version
   ```

2. **Install PyTorch for specific CUDA version**:
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
   ```

3. **Check GPU compatibility**:
   - RTX 5090 requires CUDA 13.0+
   - Update `nvidia-cuda-runtime-cu12` if needed

---

## 📊 Compatibility Matrix

### Python Version Compatibility

| Package Category | Python 3.14 | Python 3.13 | Python 3.12 |
|-----------------|-------------|-------------|-------------|
| Core Trading | ✅ | ✅ | ✅ |
| Data Processing | ✅ | ✅ | ✅ |
| ML Frameworks | ✅ | ✅ | ✅ |
| Database | ✅ | ✅ | ✅ |
| Web Framework | ✅ | ✅ | ✅ |

### CUDA Version Compatibility

| GPU | CUDA Version | PyTorch | TensorFlow | cuDNN |
|-----|-------------|---------|------------|-------|
| RTX 5090 | 13.0 | 2.6.0+ | 2.18.0+ | 8.9+ |
| RTX 4090 | 12.x | 2.1.0+ | 2.15.0+ | 8.6+ |
| RTX 3090 | 11.x | 1.13.0+ | 2.10.0+ | 8.2+ |

---

## 🔍 Dependency Analysis Commands

### Show Installed Versions
```bash
poetry show
poetry show --tree
poetry show --latest
```

### Check Specific Package
```bash
poetry show <package-name>
poetry show <package-name> --tree
poetry show <package-name> --latest
```

### Update Dependencies
```bash
# Update all to latest compatible versions
poetry update

# Update specific package
poetry update <package-name>

# Update within constraint only (no major version bumps)
poetry update --dry-run
```

### Lock File Management
```bash
# Regenerate lock file without updating versions
poetry lock --no-update

# Update lock file with latest versions
poetry lock

# Check lock file validity
poetry check
```

### Dependency Export
```bash
# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt

# Export without hashes (for faster installs)
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

---

## 📝 Best Practices

### Version Constraint Guidelines

1. **Use caret (^) for most packages**:
   ```toml
   package = "^1.2.3"  # Allows 1.2.3 to <2.0.0
   ```

2. **Use tilde (~) for patch updates only**:
   ```toml
   package = "~1.2.3"  # Allows 1.2.3 to <1.3.0
   ```

3. **Pin exact versions for critical packages**:
   ```toml
   package = "1.2.3"  # Exactly 1.2.3
   ```

4. **Use >= for minimum version requirements**:
   ```toml
   package = ">=1.2.3"  # 1.2.3 or higher
   ```

### Dependency Update Strategy

1. **Regular Updates** (Monthly):
   - Security patches
   - Minor version updates
   - Bug fixes

2. **Major Updates** (Quarterly):
   - Major version bumps
   - Framework upgrades
   - Breaking changes

3. **Before Each Update**:
   - Review release notes
   - Check for breaking changes
   - Run full test suite
   - Update this document

### Testing After Dependency Changes

1. **Unit Tests**: `pytest tests/unit/`
2. **Integration Tests**: `pytest tests/integration/`
3. **GPU Tests**: `pytest tests/ -m gpu`
4. **Coverage Check**: `pytest --cov=components --cov-report=term-missing`

---

## 🚨 Critical Dependencies (Do Not Downgrade)

| Package | Minimum Version | Reason |
|---------|----------------|---------|
| **pyarrow** | 15.0.0 | Required by datasets library |
| **sentry-sdk** | 2.0.0 | Required by wandb >=0.18.7 |
| **torch** | 2.6.0 | CUDA 13.0 support for RTX 5090 |
| **tensorflow** | 2.18.0 | CUDA 13.0 compatibility |
| **python** | 3.14.0 | Project baseline |

---

## 📚 External Resources

### Documentation
- [Poetry Dependency Specification](https://python-poetry.org/docs/dependency-specification/)
- [PyPI Package Index](https://pypi.org/)
- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/)

### Tools
- [Poetry Documentation](https://python-poetry.org/docs/)
- [pip-tools](https://github.com/jazzband/pip-tools)
- [pipdeptree](https://github.com/tox-dev/pipdeptree)

---

## 📧 Reporting New Conflicts

When encountering a new dependency conflict:

1. **Document the error** in this file under "Known Dependency Conflicts"
2. **Research the issue**: Check package release notes and issue trackers
3. **Test resolution**: Verify fix in clean environment
4. **Update compatibility matrix** if affected
5. **Run full test suite** before committing
6. **Update CHANGES.md** with the fix

---

## 📊 Dependency Statistics

**Last Full Update**: 2025-11-15
**Total Dependencies**: 100+
**Direct Dependencies**: 80+
**Dev Dependencies**: 20+
**Known Conflicts**: 2 (all resolved)
**Python Version**: 3.14.0
**Poetry Version**: Latest stable

---

**Document Version**: 1.1
**Next Review**: 2025-11-22
**Maintained By**: Project Team

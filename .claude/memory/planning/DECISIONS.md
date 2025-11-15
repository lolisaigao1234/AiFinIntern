# Decision Log

**Project**: AI-Driven Tax and Portfolio Reconciliation System
**Last Updated**: 2025-11-15
**Documentation Home**: [CLAUDE.md](../../../CLAUDE.md)
**Location**: `.claude/memory/planning/DECISIONS.md`

---

## Overview

This document tracks all major architectural and technical decisions made during the project lifecycle. Each decision follows a structured format to capture the context, options considered, rationale, and consequences.

**Related Documentation**:
- [CLAUDE.md](../../../CLAUDE.md) - Main project overview and index
- [CHANGES.md](../tracking/CHANGES.md) - Implementation change log
- [RISKS.md](./RISKS.md) - Risk register
- [ROADMAP.md](./ROADMAP.md) - Project phases and milestones

---

## Decision Template

```markdown
### [DECISION-XXX] - Decision Title
**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Rejected | Superseded
**Decider**: [Name/Role]

#### Context
[What is the situation and problem statement?]

#### Options Considered
1. Option A - [brief description]
2. Option B - [brief description]
3. Option C - [brief description]

#### Decision
[What option was chosen and why?]

#### Consequences
**Positive**:
- [Benefit 1]
- [Benefit 2]

**Negative**:
- [Risk/Trade-off 1]
- [Risk/Trade-off 2]

#### Implementation Notes
[Any specific guidance for implementing this decision]
```

---

## Decisions

### [DECISION-007] - Restructure Project Documentation into .claude/memory Directory
**Date**: 2025-11-15
**Status**: Accepted ✅
**Decider**: Project Team

#### Context
The project root directory had become cluttered with numerous markdown documentation files (CLAUDE.md, DECISIONS.md, CHANGES.md, RISKS.md, ROADMAP.md, TESTING.md, ARCHITECTURE.md, AGENTS.md) plus the docs/ directory and Code/ sample directory. This made the project structure messy and difficult to navigate.

#### Options Considered
1. **Keep current structure** - Leave all files in root directory
2. **Move to docs/** - Put all markdown files in docs/ directory
3. **Create .claude/memory/** - Create a dedicated .claude/ directory with organized subdirectories
4. **Move to hidden .project/** - Use a different hidden directory name

#### Decision
Restructure all project documentation into `.claude/memory/` directory with the following organization:
- `.claude/memory/planning/` - Strategic planning documents (ROADMAP, DECISIONS, RISKS)
- `.claude/memory/tracking/` - Progress tracking (CHANGES, TESTING)
- `.claude/memory/architecture/` - Technical architecture (ARCHITECTURE, AGENTS)
- `.claude/memory/research/` - Research documentation organized by topic
- `.claude/memory/guides/` - Installation and setup guides
- `.claude/samples/` - Sample code and testbeds

Keep only README.md and CLAUDE.md (as index) in the root directory.

#### Consequences
**Positive**:
- Clean, organized project structure
- Clear separation of documentation by purpose
- Better discoverability of related documents
- Cleaner main directory (only README.md, CLAUDE.md, and config files)
- Easier to navigate and maintain documentation
- Follows convention of using hidden directories for tooling-specific files
- Sample code separated from documentation

**Negative**:
- Existing links and references need to be updated
- Slightly longer paths to documentation files
- May require updating CI/CD scripts if they reference old paths
- Users need to learn new structure

#### Implementation Notes
- Update all cross-references in documentation files to use relative paths
- Update CLAUDE.md to serve as main documentation index with new paths
- Ensure git history is preserved during file moves
- Update README.md if it references any moved files
- Create a migration note in CHANGES.md

**Migration Checklist**:
- [x] Create .claude/memory directory structure
- [x] Move planning documents (ROADMAP, DECISIONS, RISKS)
- [x] Move tracking documents (CHANGES, TESTING)
- [x] Move architecture documents (ARCHITECTURE, AGENTS)
- [x] Move research documentation
- [x] Move setup guides
- [x] Move sample code to .claude/samples/
- [x] Update CLAUDE.md with new structure and paths
- [x] Update cross-references in all moved documents
- [x] Remove empty docs/ and Code/ directories
- [x] Update this DECISIONS.md file
- [ ] Update CHANGES.md with migration entry
- [ ] Commit and push changes

---

### [DECISION-001] - CLAUDE.md as Main Memory File
**Date**: 2025-11-15
**Status**: Superseded (by split documentation structure)
**Decider**: Project Team

#### Context
Need a centralized documentation system to track all decisions, changes, and project evolution for the AI trading bot.

#### Options Considered
1. Multiple separate documentation files
2. Wiki-based documentation
3. Single CLAUDE.md memory file

#### Decision
Use CLAUDE.md as the single source of truth for project memory, decisions, and architecture.

#### Consequences
**Positive**:
- Single file for quick reference
- Easy to track project evolution
- Clear audit trail
- Better version control

**Negative**:
- File may become large over time
- Need discipline to keep updated
- May need to split later if too large

#### Implementation Notes
- Update CLAUDE.md for every significant change
- Include reasoning, expected outcomes, and risks
- Review and refactor structure as needed

**Note**: This decision was later superseded by splitting CLAUDE.md into focused documentation files (DECISIONS.md, CHANGES.md, RISKS.md, ROADMAP.md, TESTING.md) while keeping CLAUDE.md as the main index.

---

### [DECISION-002] - ML Fine-Tuning Over Training From Scratch
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need to decide whether to train ML models from scratch or fine-tune existing pre-trained models for trading signal generation and financial analysis.

#### Options Considered
1. Train models from scratch - Full control but resource intensive
2. Fine-tune pre-trained models - Leverage existing research, faster development
3. Hybrid approach - Mix of both strategies

#### Decision
Focus on **fine-tuning pre-trained models** from Hugging Face and other open-source platforms rather than training from scratch.

#### Consequences
**Positive**:
- Significantly reduced training time and computational costs
- Leverage state-of-the-art architectures from research community
- Better performance with limited financial data (transfer learning)
- Access to specialized financial models (FinBERT, etc.)
- Faster iteration and experimentation
- Lower barrier to entry for ML development

**Negative**:
- Less flexibility in model architecture design
- Dependency on external model repositories
- May need to adapt models that weren't designed for trading
- Potential licensing considerations for commercial use

#### Implementation Notes
- Prioritize financial-specific models (FinBERT, financial sentiment analyzers)
- Use Hugging Face Transformers library as primary framework
- Implement fine-tuning pipeline with PyTorch/TensorFlow
- Leverage local GPU (RTX 5090) for efficient fine-tuning
- Document all pre-trained models used and their licenses

---

### [DECISION-003] - Local Development with NVIDIA RTX 5090
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need to optimize development environment for ML model fine-tuning and training with available hardware: AMD R7-7700X CPU, NVIDIA RTX 5090 FE GPU (24GB VRAM), 32GB RAM.

#### Options Considered
1. Cloud-based GPU training (AWS, GCP, Azure)
2. Local GPU development with RTX 5090
3. Hybrid approach (local dev, cloud for large-scale training)

#### Decision
Optimize for **local development using NVIDIA RTX 5090** with full CUDA, PyTorch, and TensorFlow GPU acceleration.

#### Consequences
**Positive**:
- Zero cloud compute costs during development
- Full control over environment and dependencies
- 24GB VRAM sufficient for fine-tuning large models
- Low latency for iterative development
- No data transfer costs or privacy concerns
- Can utilize all 8 CPU cores for data preprocessing

**Negative**:
- Limited to single GPU (no multi-GPU training)
- 32GB system RAM may limit very large dataset operations
- Electricity costs for GPU usage
- Cannot scale beyond local hardware limits
- Need to maintain CUDA/driver compatibility

#### Implementation Notes
- Install CUDA 12.x with cuDNN 8.9+ for optimal RTX 5090 performance
- Configure PyTorch with CUDA backend (cu121)
- Enable mixed precision training (FP16) for faster training
- Use gradient checkpointing for memory-intensive models
- Monitor GPU temperature and utilization
- Consider cloud deployment for production inference at scale

---

### [DECISION-004] - Poetry for Dependency Management
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Need a robust, modern dependency management solution for Python 3.14.0 project with complex dependencies including CUDA-enabled ML frameworks, multiple package sources (PyPI, PyTorch repos), and development/production separation.

#### Options Considered
1. pip with requirements.txt - Traditional approach, simple but limited
2. Poetry - Modern dependency management with lock files
3. Pipenv - Alternative to Poetry, less actively maintained
4. Conda - Heavy, primarily for data science, complex with pip packages

#### Decision
Use **Poetry** as the primary dependency management tool with pyproject.toml configuration.

#### Consequences
**Positive**:
- Deterministic builds with poetry.lock file
- Clear separation of development and production dependencies
- Better dependency resolution and conflict detection
- Modern pyproject.toml standard (PEP 518)
- Built-in virtual environment management
- Support for private package repositories
- Easier version management and updates
- Optional dependency groups (jupyter, cuda extras)
- Integration with modern Python tooling (black, ruff, mypy)

**Negative**:
- Additional tool to learn for team members
- Slightly slower than pure pip installations
- Some edge cases with CUDA packages require pip fallback
- Poetry lock file adds repository size
- May need pip for some specialized packages (PyTorch CUDA wheels)

#### Implementation Notes
- Create comprehensive pyproject.toml with all dependencies
- Use poetry extras for optional dependencies (cuda, jupyter)
- Configure PyTorch CUDA installation as separate pip step
- Set up dependency groups: main, dev, jupyter
- Configure all tooling (black, ruff, mypy, pytest) in pyproject.toml
- Keep requirements.txt as fallback for pip-only environments
- Document Poetry installation and usage in README.md
- Use poetry.lock for reproducible builds (commit to repository)

---

### [DECISION-005] - Remove pickle5 Dependency
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
Poetry dependency resolution failed because `pickle5` package requires Python >=3.5, <3.8, which is incompatible with the project's Python 3.14.0 requirement. The `pickle5` package is a backport that brings pickle protocol 5 (introduced in Python 3.8) to earlier Python versions (3.5-3.7).

#### Options Considered
1. Keep pickle5 and downgrade Python to 3.7 - Not viable, loses modern language features and ML library support
2. Use Poetry markers to conditionally include pickle5 - Unnecessary complexity for a backport package
3. Remove pickle5 entirely - Native pickle protocol 5+ support in Python 3.14

#### Decision
**Remove `pickle5` package completely** from dependencies. Python 3.14.0 has native support for pickle protocol 5 and all subsequent protocols, making the backport package unnecessary.

#### Consequences
**Positive**:
- Resolves Poetry dependency conflict immediately
- Reduces dependency count and package complexity
- Uses native Python standard library (more reliable, no external dependency)
- Better performance with native implementation
- No compatibility issues with future Python versions
- One less package to maintain and update

**Negative**:
- None - pickle5 is purely a backport for old Python versions

#### Implementation Notes
- Removed `pickle5 = "^0.0.12"` from pyproject.toml
- Removed `pickle5==0.0.12` from requirements.txt
- No code changes needed - Python 3.14's `pickle` module is drop-in replacement
- Native `pickle` module supports protocols 0-5 and beyond
- Use `import pickle` directly from standard library

---

### [DECISION-006] - Split CLAUDE.md into Focused Documentation Files
**Date**: 2025-11-15
**Status**: Accepted
**Decider**: Project Team

#### Context
CLAUDE.md grew to over 1,260 lines, becoming difficult to navigate and maintain. The file combined project overview, decisions, changes, risks, roadmap, and testing strategy into a single document. This size made it challenging to find specific information quickly and violated the principle of focused, single-purpose documentation.

#### Options Considered
1. Keep CLAUDE.md as single file - Simple but unwieldy
2. Split into multiple focused files with cross-references - Better organization
3. Move to wiki-based system - Too much overhead for small team

#### Decision
**Split CLAUDE.md into focused documentation files** while keeping CLAUDE.md as the main index and project overview. Create separate files for:
- `DECISIONS.md` - Decision log
- `CHANGES.md` - Change log
- `RISKS.md` - Risk register
- `ROADMAP.md` - Project phases and milestones
- `TESTING.md` - Testing strategy

#### Consequences
**Positive**:
- Easier to find specific information (decisions, changes, risks)
- Smaller file sizes load faster and are easier to navigate
- Each document has a single, clear purpose
- Can update individual aspects without touching entire memory file
- Better separation of concerns (decisions vs implementations vs risks)
- Reduced cognitive load when reading documentation
- Easier to reference specific sections via links

**Negative**:
- Need to maintain cross-references between files
- Slightly more complex navigation (but mitigated by clear links)
- More files to keep in sync

#### Implementation Notes
- Keep CLAUDE.md as main index with project overview and quick reference
- Create clear cross-references using markdown links
- Maintain consistent header structure across all files
- Include "Documentation Home" links at top of each split file
- Update README.md to reference new documentation structure
- Keep templates in each file for future entries
- Document the new structure in CLAUDE.md "Related Documentation" section

---

## Decision Statistics

**Total Decisions**: 6
**Accepted**: 5
**Superseded**: 1
**Rejected**: 0
**Proposed**: 0

**By Category**:
- Documentation: 2
- Technology Stack: 3
- Development Process: 1

---

**Last Updated**: 2025-11-15
**Next Review**: 2025-11-22

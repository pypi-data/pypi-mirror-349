# Release Process

This document describes the release process for the `zc-podcastmaker-common` package.

## Automated Releases

The package uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) for automated versioning and publishing. The process is triggered automatically when commits are pushed to the `main` branch.

### How It Works

1. When code is pushed to `main`, the GitHub Actions workflow `.github/workflows/release.yml` is triggered
2. The workflow analyzes commit messages since the last release
3. Based on [Conventional Commits](https://www.conventionalcommits.org/) format, it determines the next version number:
   - `fix:` commits trigger a patch version bump (e.g., 1.0.0 → 1.0.1)
   - `feat:` commits trigger a minor version bump (e.g., 1.0.0 → 1.1.0)
   - `feat!:` or `fix!:` commits (or any with a breaking change footer) trigger a major version bump (e.g., 1.0.0 → 2.0.0)
4. The workflow then:
   - Updates the version in `pyproject.toml`
   - Updates the `CHANGELOG.md` file
   - Creates a new Git tag
   - Creates a GitHub release with release notes
   - Builds the package
   - Publishes the package to PyPI

### Manual Release

To manually trigger a release:

1. Go to the GitHub Actions tab in the repository
2. Select the "Release" workflow
3. Click "Run workflow"
4. Select the desired release type (patch, minor, or major)
5. Click "Run workflow"

## Writing Good Commit Messages

For the automated release process to work correctly, commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Where `<type>` is one of:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Changes that don't affect code functionality (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or correcting tests
- `chore`: Changes to the build process, tooling, etc.

Examples:
```
feat(config): add support for environment variables
fix(storage): handle file not found errors properly
docs: update installation instructions
```

For breaking changes, add an exclamation mark after the type/scope or add a `BREAKING CHANGE:` footer:

```
feat!: change API interface

BREAKING CHANGE: The API interface has been completely redesigned.
```

## Pre-commit Hook

A pre-commit hook is configured to enforce the Conventional Commits format. To install it:

```bash
pre-commit install --hook-type commit-msg
```

## Publishing to PyPI

The package is automatically published to PyPI. For this to work, the GitHub Actions workflow needs access to the repository credentials.

These credentials are stored as GitHub Secrets:
- `PYPI_API_TOKEN`: Token for authenticating with PyPI

To create a PyPI API token:
1. Create an account on [PyPI](https://pypi.org/)
2. Go to your account settings
3. Navigate to the API tokens section
4. Create a new token with the scope "Upload packages"
5. Add this token as a secret in your GitHub repository settings

## Troubleshooting

If a release fails, check:

1. GitHub Actions logs for detailed error information
2. Ensure commit messages follow the Conventional Commits format
3. Verify that the PyPI credentials are correctly configured
4. Check that the package version in `pyproject.toml` is correct

For manual intervention, you can:

1. Update the version in `pyproject.toml`
2. Create and push a tag: `git tag v1.2.3 && git push origin v1.2.3`
3. Create a GitHub release manually
4. Build and publish the package manually:
   ```bash
   python -m build
   twine upload dist/*
   ```

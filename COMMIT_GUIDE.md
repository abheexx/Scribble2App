# Commit Message Generator Guide

This guide explains how to use the `commit_messages.py` script to generate humanized, random commit messages for the Scribble2App project.

## Usage

### Generate a commit message
```bash
python3 commit_messages.py
```

This will generate and display a random commit message that you can copy and use.

### Automatically commit with generated message
```bash
python3 commit_messages.py --commit
```

This will generate a commit message and automatically execute the git commit command.

## Message Types

The generator creates different types of commit messages based on common development activities:

### Feature Messages (30% probability)
- `feat: element detection with enhanced capabilities`
- `add: OCR processing functionality`
- `implement: code generation support`
- `create: UI schema building implementation`

### Bug Fix Messages (25% probability)
- `fix: element detection accuracy`
- `resolve: OCR text recognition issue`
- `patch: code generation errors`
- `correct: image processing bugs`

### Refactor Messages (15% probability)
- `refactor: code structure for better maintainability`
- `restructure: module organization`
- `optimize: data flow to improve performance`
- `cleanup: function signatures for cleaner code`

### Documentation Messages (10% probability)
- `docs: README with examples`
- `update: API documentation for clarity`
- `improve: installation guide`
- `add: configuration options documentation`

### Test Messages (10% probability)
- `test: unit tests for reliability`
- `add: integration tests coverage`
- `improve: end-to-end tests to prevent regressions`
- `fix: accessibility tests`

### Chore Messages (10% probability)
- `chore: dependencies maintenance`
- `update: build tools configuration`
- `bump: CI/CD pipeline`
- `clean: development environment`

## Message Features

### Emotional Suffixes
Some messages include emotional suffixes to make them more human:
- `finally!`, `at last`, `phew`, `wow`, `amazing`, `incredible`
- `fantastic`, `brilliant`, `awesome`, `sweet`, `nice`, `cool`

### Technical Suffixes
Some messages include technical context:
- `with improved performance`, `for better UX`
- `with enhanced security`, `for scalability`
- `with better error handling`, `for maintainability`

### Commit Bodies
30% of messages include a commit body with:
- List of improvements
- Issue references (random issue numbers)
- Additional context

## Examples

```
feat: React component generation with enhanced capabilities - fantastic

fix: OCR text recognition bug - phew

refactor: code structure for better maintainability

docs: README with examples

This commit includes:
- Improved functionality and reliability
- Better error handling and validation
- Enhanced user experience

Closes #456
```

## Customization

You can modify the `commit_messages.py` file to:
- Add new message types
- Change probability weights
- Add new components or issues
- Modify emotional/technical suffixes
- Adjust commit body frequency

## Best Practices

1. **Review before committing**: Always review the generated message before using it
2. **Edit if needed**: Feel free to edit the message to better reflect your changes
3. **Use with --commit carefully**: The automatic commit feature should be used when you're confident about the changes
4. **Keep it professional**: While the messages are humanized, they remain professional and descriptive

## Integration

You can integrate this into your workflow by:
- Adding it to your git hooks
- Creating aliases in your shell configuration
- Using it in CI/CD pipelines for automated commits
- Incorporating it into your IDE or text editor 
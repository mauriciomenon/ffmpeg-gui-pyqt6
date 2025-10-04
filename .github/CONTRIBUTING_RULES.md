# Repository Rules and Standards

## Mandatory Writing Standards

### Forbidden Characters and Symbols
- **No emojis** in any documentation, code comments, or file names
- **No special characters** (accented_characters) in any text content
- **No spaces** in directory or file names - use underscores or hyphens
- **No cedillas or accents** in any content

### Forbidden Language and Phrases
These terms are **strictly prohibited** in all repository content:

#### Cringe Marketing Terms
- "made with love" / "feito com amor"
- "ultimate" / "final" / "professional" / "enhanced" / "improved"
- "amazing" / "awesome" / "incredible" / "fantastic"
- Any heart symbols or love references
- Star solicitation phrases

#### Banned Adjectives
- ultimate, final, professional, enhanced, improved, optimized
- perfect, amazing, awesome, incredible, fantastic, revolutionary
- cutting-edge, state-of-the-art, next-generation, world-class

### Required Writing Style
- **Objective and technical language only**
- **Direct, factual descriptions**
- **No marketing language or emotional appeals**
- **Clear, concise instructions without fluff**

## Code Standards

### File Naming
- Use only ASCII characters (a-z, A-Z, 0-9, _, -)
- No spaces in file or directory names
- Use snake_case for Python files
- Use kebab-case for documentation files

### Documentation Standards
- Focus on functionality, not promotion
- Use simple present tense
- Avoid superlatives and marketing terms
- Provide factual information only

### Commit Message Standards
- Use imperative mood ("add feature" not "added feature")
- Be specific and technical
- No emotional or promotional language
- Reference issues with numbers only

## Enforcement

### Pre-commit Checks
The repository enforces these rules through:
- Git hooks that scan for forbidden characters
- Automated checks for prohibited phrases
- File name validation

### Pull Request Requirements
All contributions must:
- Pass automated rule validation
- Use only approved language patterns
- Follow ASCII-only naming conventions
- Contain no marketing language

### Violations
Content that violates these rules will be:
- Automatically rejected by pre-commit hooks
- Flagged in pull request reviews
- Required to be corrected before merge

These rules ensure consistent, technical documentation free of promotional language and special characters.
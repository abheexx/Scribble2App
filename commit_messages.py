#!/usr/bin/env python3
"""
Commit Message Generator for Scribble2App
Generates random, humanized commit messages for various development activities.
"""

import random
import subprocess
import sys
from datetime import datetime

class CommitMessageGenerator:
    def __init__(self):
        self.feature_prefixes = [
            "feat", "add", "implement", "create", "introduce", "enable", "support"
        ]
        
        self.fix_prefixes = [
            "fix", "resolve", "patch", "correct", "repair", "address", "solve"
        ]
        
        self.refactor_prefixes = [
            "refactor", "restructure", "reorganize", "cleanup", "optimize", "improve", "enhance"
        ]
        
        self.docs_prefixes = [
            "docs", "document", "update", "clarify", "improve", "add"
        ]
        
        self.test_prefixes = [
            "test", "add", "improve", "fix", "update", "cover"
        ]
        
        self.chore_prefixes = [
            "chore", "update", "bump", "upgrade", "maintain", "clean"
        ]
        
        self.feature_components = [
            "element detection", "OCR processing", "code generation", "UI schema building",
            "image upload", "text extraction", "React component generation", "Tailwind styling",
            "pipeline optimization", "error handling", "validation", "export functionality",
            "responsive design", "accessibility features", "performance monitoring",
            "configuration management", "deployment automation", "testing framework"
        ]
        
        self.fix_issues = [
            "element detection accuracy", "OCR text recognition", "code generation errors",
            "image processing bugs", "memory leaks", "performance bottlenecks",
            "UI rendering issues", "export failures", "validation errors",
            "dependency conflicts", "build errors", "deployment issues",
            "cross-browser compatibility", "mobile responsiveness", "accessibility violations"
        ]
        
        self.refactor_targets = [
            "code structure", "module organization", "function signatures", "class hierarchy",
            "data flow", "error handling", "configuration management", "testing approach",
            "documentation structure", "build process", "deployment pipeline"
        ]
        
        self.docs_sections = [
            "README", "API documentation", "installation guide", "usage examples",
            "configuration options", "troubleshooting guide", "contributing guidelines",
            "deployment instructions", "development setup", "testing procedures"
        ]
        
        self.test_areas = [
            "unit tests", "integration tests", "end-to-end tests", "performance tests",
            "accessibility tests", "cross-browser tests", "mobile tests", "API tests"
        ]
        
        self.chore_items = [
            "dependencies", "build tools", "CI/CD pipeline", "development environment",
            "code formatting", "linting rules", "git hooks", "deployment scripts"
        ]
        
        self.emotional_suffixes = [
            "finally!", "at last", "phew", "wow", "amazing", "incredible", "fantastic",
            "brilliant", "awesome", "sweet", "nice", "cool", "great", "excellent"
        ]
        
        self.technical_suffixes = [
            "with improved performance", "for better UX", "with enhanced security",
            "for scalability", "with better error handling", "for maintainability",
            "with comprehensive testing", "for production readiness"
        ]

    def generate_feature_message(self):
        """Generate a feature commit message."""
        prefix = random.choice(self.feature_prefixes)
        component = random.choice(self.feature_components)
        
        messages = [
            f"{prefix}: {component}",
            f"{prefix}: {component} functionality",
            f"{prefix}: {component} support",
            f"{prefix}: {component} implementation",
            f"{prefix}: {component} with enhanced capabilities"
        ]
        
        if random.random() < 0.3:
            suffix = random.choice(self.emotional_suffixes + self.technical_suffixes)
            return f"{random.choice(messages)} - {suffix}"
        
        return random.choice(messages)

    def generate_fix_message(self):
        """Generate a bug fix commit message."""
        prefix = random.choice(self.fix_prefixes)
        issue = random.choice(self.fix_issues)
        
        messages = [
            f"{prefix}: {issue}",
            f"{prefix}: {issue} bug",
            f"{prefix}: {issue} issue",
            f"{prefix}: {issue} problem",
            f"{prefix}: critical {issue}",
            f"{prefix}: {issue} regression"
        ]
        
        if random.random() < 0.4:
            suffix = random.choice(self.emotional_suffixes)
            return f"{random.choice(messages)} - {suffix}"
        
        return random.choice(messages)

    def generate_refactor_message(self):
        """Generate a refactor commit message."""
        prefix = random.choice(self.refactor_prefixes)
        target = random.choice(self.refactor_targets)
        
        messages = [
            f"{prefix}: {target}",
            f"{prefix}: {target} for better maintainability",
            f"{prefix}: {target} to improve performance",
            f"{prefix}: {target} for cleaner code",
            f"{prefix}: {target} architecture"
        ]
        
        return random.choice(messages)

    def generate_docs_message(self):
        """Generate a documentation commit message."""
        prefix = random.choice(self.docs_prefixes)
        section = random.choice(self.docs_sections)
        
        messages = [
            f"{prefix}: {section}",
            f"{prefix}: {section} documentation",
            f"{prefix}: {section} with examples",
            f"{prefix}: {section} for clarity",
            f"{prefix}: {section} improvements"
        ]
        
        return random.choice(messages)

    def generate_test_message(self):
        """Generate a test commit message."""
        prefix = random.choice(self.test_prefixes)
        area = random.choice(self.test_areas)
        
        messages = [
            f"{prefix}: {area}",
            f"{prefix}: {area} coverage",
            f"{prefix}: {area} for reliability",
            f"{prefix}: {area} to prevent regressions",
            f"{prefix}: comprehensive {area}"
        ]
        
        return random.choice(messages)

    def generate_chore_message(self):
        """Generate a chore commit message."""
        prefix = random.choice(self.chore_prefixes)
        item = random.choice(self.chore_items)
        
        messages = [
            f"{prefix}: {item}",
            f"{prefix}: {item} maintenance",
            f"{prefix}: {item} updates",
            f"{prefix}: {item} cleanup",
            f"{prefix}: {item} configuration"
        ]
        
        return random.choice(messages)

    def generate_random_message(self):
        """Generate a random commit message based on type."""
        message_types = [
            self.generate_feature_message,
            self.generate_fix_message,
            self.generate_refactor_message,
            self.generate_docs_message,
            self.generate_test_message,
            self.generate_chore_message
        ]
        
        # Weight the types (features and fixes are more common)
        weights = [0.3, 0.25, 0.15, 0.1, 0.1, 0.1]
        chosen_type = random.choices(message_types, weights=weights)[0]
        
        return chosen_type()

    def generate_commit_with_body(self):
        """Generate a commit message with an optional body."""
        subject = self.generate_random_message()
        
        # 30% chance to add a body
        if random.random() < 0.3:
            body_lines = [
                "",
                "This commit includes:",
                "- Improved functionality and reliability",
                "- Better error handling and validation",
                "- Enhanced user experience",
                "",
                "Closes #" + str(random.randint(100, 999))
            ]
            return subject + "\n".join(body_lines)
        
        return subject

def main():
    """Main function to generate and optionally commit with a message."""
    generator = CommitMessageGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--commit":
        # Generate message and commit
        message = generator.generate_commit_with_body()
        print(f"Generated commit message:\n{message}")
        print("\n" + "="*50)
        
        try:
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True,
                check=True
            )
            print("Commit successful!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Commit failed:")
            print(e.stderr)
            print("\nYou can manually commit with:")
            print(f'git commit -m "{message}"')
    else:
        # Just generate and display message
        message = generator.generate_commit_with_body()
        print("Generated commit message:")
        print("="*50)
        print(message)
        print("="*50)
        print("\nTo use this message:")
        print(f'git commit -m "{message}"')
        print("\nOr run with --commit flag to automatically commit")

if __name__ == "__main__":
    main() 
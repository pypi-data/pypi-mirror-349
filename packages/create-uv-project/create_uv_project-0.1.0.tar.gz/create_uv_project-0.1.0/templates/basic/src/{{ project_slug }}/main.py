"""Main entrypoint for {{ project_slug }}."""

import sys


def main():
    """Main function to print a greeting from the project."""
    print(
        f"Hello from {{ project_name }}! (Version loaded: {{ project_slug }}.__version__)"
    )
    # Example of how to access a variable that might be in config/settings.yaml
    # config = load_config() # You would need to implement load_config()
    # print(f"A setting from config: {config.get('some_setting', 'Not found')}")
    return 0


if __name__ == "__main__":
    # This allows running the module directly using `python -m {{ project_slug }}.main`
    sys.exit(main())

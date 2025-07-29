import argparse
from datetime import datetime  # Keep this for current_year
import os
import pathlib
from jinja2 import Environment, FileSystemLoader
import logging


def generate_project_from_template(
    template_name: str, project_name: str, output_dir: str, context: dict
):
    """
    Generates a project from a specified template.
    """
    logging.info(
        f"Generating project '{project_name}' from template '{template_name}' in '{output_dir}'..."
    )

    # Derive project_slug from project_name
    project_slug = project_name.lower().replace(" ", "_").replace("-", "_")
    current_year = datetime.now().year  # Calculate current_year here
    full_context = {
        "project_name": project_name,
        "project_slug": project_slug,
        "project_version": "0.1.0",
        "current_year": current_year,  # Add current_year to the context for templates
        **context,  # Merge with user-provided context
    }

    # Correctly locate the templates directory relative to this file
    # Assuming app.py is in src/create_uv_project/app.py
    # and templates are in /templates/
    script_dir = pathlib.Path(__file__).parent.parent.parent
    template_root_dir = script_dir / "templates"
    specific_template_dir = template_root_dir / template_name

    if not specific_template_dir.is_dir():
        logging.error(
            f"Template '{template_name}' not found at '{specific_template_dir}'"
        )
        return

    env = Environment(
        loader=FileSystemLoader(str(specific_template_dir)), keep_trailing_newline=True
    )

    target_project_path = pathlib.Path(output_dir) / project_slug

    if target_project_path.exists():
        logging.error(
            f"Target directory '{target_project_path}' already exists. Please remove it or choose a different name/output directory."
        )
        # Optionally, add a --force flag to overwrite
        # For now, we'll just exit.
        # user_response = input(f"Directory {target_project_path} already exists. Overwrite? [y/N]: ")
        # if user_response.lower() != 'y':
        #     print("Aborted by user.")
        #     return
        # shutil.rmtree(target_project_path) # Be careful with this
        return

    # print(f"Creating project directory: {target_project_path}") # This is implicitly covered by dir creation logs or final success.
    # We will create the root project directory later based on rendered template root names or project_slug

    for root, dirs, files in os.walk(str(specific_template_dir)):
        # Relative path from the specific_template_dir to the current root
        relative_root = pathlib.Path(root).relative_to(specific_template_dir)
        logging.debug(f"--- Walking new root ---")
        logging.debug(f"Current root: {root}")
        logging.debug(f"Dirs in current root: {dirs}")
        logging.debug(f"Files in current root: {files}")

        # Render directory names
        rendered_relative_root_parts = []
        for part in relative_root.parts:
            try:
                rendered_part = env.from_string(part).render(full_context)
                rendered_relative_root_parts.append(rendered_part)
            except Exception as e:
                logging.warning(
                    f"Could not render directory part '{part}': {e}. Using original name."
                )
                rendered_relative_root_parts.append(part)

        current_target_dir_path = target_project_path
        if rendered_relative_root_parts:  # if not the template root itself
            current_target_dir_path = target_project_path.joinpath(
                *rendered_relative_root_parts
            )

        for dir_name in dirs:
            rendered_dir_name = env.from_string(dir_name).render(full_context)
            target_dir_path = current_target_dir_path / rendered_dir_name
            if not target_dir_path.exists():
                logging.info(f"Creating directory: {target_dir_path}")
                target_dir_path.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            # Skip .DS_Store and other unwanted files
            if file_name == ".DS_Store":
                continue

            logging.debug(f"----- Processing file_name: {file_name} -----")
            if ".gitignore" in file_name:  # More specific debug for gitignore
                logging.debug(
                    f"Found a gitignore-related file: {file_name} in root {root}"
                )

            template_file_path = pathlib.Path(root) / file_name

            # Render file name
            rendered_file_name = env.from_string(file_name.replace(".j2", "")).render(
                full_context
            )  # Remove .j2 extension before rendering name
            if ".gitignore" in file_name:
                logging.debug(
                    f"Rendered file name for {file_name} is: {rendered_file_name}"
                )

            target_file_path = current_target_dir_path / rendered_file_name
            if ".gitignore" in file_name or ".gitignore" in str(target_file_path):
                logging.debug(
                    f"Target file path for {file_name} is: {target_file_path}"
                )

            # Ensure parent directory of the target file exists
            target_file_path.parent.mkdir(parents=True, exist_ok=True)

            # print(f"Processing template file: {template_file_path} -> {target_file_path}")
            logging.debug(
                f"Processing template file: {template_file_path} -> {target_file_path}"
            )

            try:
                # Correctly form the relative path for Jinja's get_template
                relative_template_file_path_for_jinja = template_file_path.relative_to(
                    specific_template_dir
                )
                if ".gitignore" in str(target_file_path):
                    logging.debug(
                        f"Attempting to get template for: {relative_template_file_path_for_jinja}"
                    )
                template = env.get_template(str(relative_template_file_path_for_jinja))
                rendered_content = template.render(full_context)

                if ".gitignore" in str(target_file_path):
                    logging.debug(f"Attempting to write to: {target_file_path}")
                with open(target_file_path, "w", encoding="utf-8") as f:
                    f.write(rendered_content)
                # print(f"Generated file: {target_file_path}")
                logging.info(f"Generated file: {target_file_path}")
                if ".gitignore" in str(target_file_path):
                    logging.debug(f"Successfully wrote file: {target_file_path}")
            except Exception as e:
                # print(f"Error rendering or writing file {template_file_path}: {e}")
                logging.error(
                    f"Error rendering or writing file {template_file_path}: {e}"
                )
                if ".gitignore" in str(template_file_path) or ".gitignore" in str(
                    target_file_path
                ):
                    logging.debug(
                        f"ERROR SPECIFIC TO GITIGNORE: {e} while processing {template_file_path}"
                    )
                # Optionally copy if not a template, or handle error
                # For now, we'll just print an error and continue
                # if not file_name.endswith(".j2"):
                #     shutil.copy2(template_file_path, target_file_path)
                #     print(f"Copied (non-template): {target_file_path}")

    logging.info(
        f"Project '{project_name}' created successfully at '{target_project_path}'!"
    )


def main():
    # Basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(
        description="Create a new Python project using UV and pre-defined templates."
    )
    parser.add_argument("project_name", help="The name of the new project.")
    parser.add_argument(
        "-t",
        "--template",
        default="basic",
        help="The project template to use (e.g., basic, fastapi, cli). Default: basic",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="The directory where the project will be created. Default: current directory",
    )
    # Add more arguments for context if needed, e.g., author_name, author_email
    parser.add_argument(
        "--author-name", default="Your Name", help="Author's name for pyproject.toml"
    )
    parser.add_argument(
        "--author-email",
        default="you@example.com",
        help="Author's email for pyproject.toml",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (DEBUG level logging)",
    )

    args = parser.parse_args()

    # Reconfigure logging level if verbose is set
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled. DEBUG level logging active.")

    user_context = {
        "author_name": args.author_name,
        "author_email": args.author_email,
        # Add any other variables you want to pass to templates
    }

    generate_project_from_template(
        template_name=args.template,
        project_name=args.project_name,
        output_dir=args.output_dir,
        context=user_context,
    )


if __name__ == "__main__":
    main()

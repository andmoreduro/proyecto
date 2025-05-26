# Thesis project
This application is essentially an interactive form to create academic documents in the APA format. Initially developed for Windows.

## Running
Before anything you must have Typst installed in your system. See: [Typst GitHub](https://github.com/typst/typst#installation)

Clone the repo, install the pip requirements, initialize git submodules (`git submodule update --init`), cd into `templates/APA`, run `git sparse-checkout init --no-cone`, then `git sparse-checkout set /versatile-apa/lib.typ /versatile-apa/utils/ /versatile-apa/assets/`. Or you can run the initialization script for your OS inside the `scripts/` folder.

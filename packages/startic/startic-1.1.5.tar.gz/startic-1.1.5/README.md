# Startic v1.1.5

**Project**: Startic
<br>**Version**: 1.1.5
<br>**OS**: OS Independent
<br>**Author**: Irakli Gzirishvili
<br>**Mail**: gziraklirex@gmail.com

**Startic** is a Python command-line interface application. Startic is a Python CLI tool for quickly building static webpages, allowing you to start publishing lightweight templates with ease

## Installation

To use **Startic**, follow these steps:

- Open CMD and run the following command to install `pip install startic` then restart your CMD
- To check if **Startic** is installed correctly, run the following command `startic`

## Commands

These are the available commands you can use:

- `startic` - To list available commands
- `startic new` - Create new project
- `startic start` - Start project development
- `startic render` - Render project pages

## Usage

To use this framework, follow these rules:

- Do not rename or remove the `assets` folder
- Do not rename the `parts` folder
- Define your page structure in `pages.yml` as shown in the default example
- To include a part in your code, use this format: `((folderName: partName))`
- To include a configuration from the `assets` folder, use this format: `{{configName: keyName}}`
- To include a collection from a folder, use this format: `[[folderName]]`
- To include the first member of the collection, use this format: `[[folderName: first]]`
- To include the last member of the collection, use this format: `[[folderName: last]]`
- To get the count of collection members, use this format: `[[folderName: count]]`

## Default System Variables

Here is a list of default system variables that you can use in your code:

- `{{DATE}}` — UTC date string
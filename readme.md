## Index Block Script

### Description
This script takes a CSV as input. The CSV contains the assets that have sitemap metadata of "No" and sets it to "Yes".
***note**: This script is for site www.csi.edu only*
### Toolchain
| programs| links |
|--------|--------------------------|
| Python | https://www.python.org/  (install anything above 3.12)|
| VSCode | https://code.visualstudio.com/download (required for VSCode extension)|
|Rainbow CSV|https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv (for formatting csv files)|
### How to use
1. Clone this repo and open the working directory with VSCode
2. [Create a virtual environment](#creating-virtual-environment-for-python-in-vscode)

> **Generating CSV**
    > - Navigate to /_common/_cms/formats/_dev/_dev-sitemap-csv
    > - Edit the format
    > - Under `Preview Options`
        - **Select an asset type**: Block & context page
        - **Context block**: /_common/_cms/blocks/_dev/all-pages-sitewide
        - Leave the page blank <br>
    > - Click `Test Format`
    > - Copy & paste output into a new file inside the working directory with a `.csv` extension
3. Rename [.env.example](.env.example) to `.env` and fill in the required values.
    - [Where to get API Key?](#getting-api-key-in-cascade)
4. Open the `.csv` you created, Rainbow CSV should auto-detect file extension
5. Go to the bottom of the VSCode look for a button named 'align' click it once
6. It should change to 'shrink' click it again *(this removes tabs and inconsistant formatting)*
7. Run the program!
    - *common error while running the program the Cascade format may generate extra fields this program will detect these and notify the user which path to correct*
    - Results will be generated as a `.log` file

### Getting API key in Cascade
1. Click on the User Menu: The circle with your profile picture
2. Click `API Key`
3. Click `Regenerate API Key`
4. Copy & paste into the `.env`

### Creating virtual environment for Python in VSCode
1. Press `Ctrl+Shift+P` type "create environment"
2. select option starting with 'Python:Create Environment...'
3. Select your installed version of Python
4. When prompted select `requirements.txt`
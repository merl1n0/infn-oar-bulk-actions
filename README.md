# INFN OAR Bulk Actions

These command line scripts allow to execute a set of actions in bulk against the [INFN Open Access Repository](https://www.openaccessrepository)  (or any [Zenodo](https://zenodo.org) based one) from a list of records stored in a [YAML](https://yaml.org) file. Currently the supported actions are:

- `deposit` - deposit (upload) files and register related metadata
- `delete`  - delete deposited record
- `publish` - make public (publish) an already deposited record
- `curate`  - (for community curators) allow to accept/reject published records into a given community
- `search`  - returns a list of records (in YAML format) that satisfy a set of given criteria

... to be continued

---


## Requirements

Python3 (and `pip`) should be installed on your machine


## 📋 Installation

1. Clone this repository into a folder of your local machine:
   
   ```
   git clone https://github.com/acaland/infn-oar-bulk-actions.git
   ```

   Alternatively you can download the source from https://github.com/acaland/infn-oar-deposit/archive/refs/heads/master.zip

2. Using the Terminal app (macOS) or PowerShell (Windows) navigate to the folder where you cloned/unzipped the source code:

   ```
   cd <path_to_infn-oar-deposit>
   ```

   Alternatively you can use Visual Studio Code and its integrated terminal. In this case you need just to open the folder with the source code. VS Code defaults the terminal to the root of your opened workspace.

3. (Optional) Create a Python virtual environment and activate it. With `venv` for example:
   
   ```
   python -m venv .oar
   
   # Activate the virtual environment (macOS/Linux)
   $ source .oar/bin/activate

   # Activate the virtual environment (Windows PowerShell)
   PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   PS C:\> .oar\Scripts\activate.ps1

   ```

4. Install the needed dependencies with:

   ```
   pip install -r requirements.txt
   ```

  5. If you haven't already created a _Personal Access Token_ to access INFN OAR API, go to https://www.openaccessrepository.it/account/settings/applications/ and create a **New Token**. Copy the new token and save it in a safe place as you cannot retrieve it again. 
   
  6. Create a `.env` file in the same folder as `oar-deposit.py` with the line:
     ```bash
     OAR_TOKEN=<your_personal_token_from_OAR_here>
     ```
     Alternatively, you can set an environment variable into your system. For example, :

     ```
     # on macOS/*nix environment
     $ export OAR_TOKEN=<your_personal_token_from_OAR_here>

     # on Windows
     PS C:\> $env:OAR_TOKEN="<your_personal_token_from_OAR_here>"
     ```



  ## 🚀 Usage
  
  1. (Optional) Load the virtual environment where you set up infn-oar-deposit:
     ```
     # macOS/*nix
     $ source <path_to_infn-oar-deposit>/.oar/bin/activate
     
     # Windows
     PS C:\> .<path_to_infn-oar-deposit>\Scripts\activate.ps1
     ```
  
  2. (Optional) Set your OAR_TOKEN env variable (if you don't use the `.env` file)
  
  3. Start the bulk deposit script with:   
     ```
     python oar-deposit.py <path_of_the_yml_file> [record_start_index] [record_end_index]
     ```
     
     where
     - `<path_of_the_yml_file>` is the full path (absolute or relative) of the `.yml` input file that contains the list of records to deposit

     With no other parameters **all** the records in the input YAML file will be deposited.

     Additionally you can pass: 
     
     - `<record_start_index>`: is the index of the first record to deposit, according to the sequence in the input file. The sequence is numbered started by 0

     - `<record_end_index>` is the index of the last record to deposit. If you don't provide it, it will be the last record of the file
     
     Example:
     ```
     python oar-deposit.py adone-prova1.yml 1
     ```
     Will deposit records starting from the *second* to the last one listed in the `adone-prova1.yml`.




### Prerequisites
- Python 3.13.x

### Collaborating
Collaboration will be done through pull requests (PRs).

To start collaborating, clone the repo, then create and move into a branch to start working. Here are the steps in code:  
```
git clone https://github.com/aleguy02/COP3530-project3.git
cd COP3530-project3
git status
git branch <your-name>/<branch-description>
git checkout <your-name>/<branch-description>
```
<your-name> should be your name, just so we can keep track of who's doing what a little easier, and <branch-description> should be a short, hyphen-separated description of what changes you are making in the branch. For example:  
`ale/fix-visual-bug`  
`ale/refactor-tests`  
`ale/create-graph-api`  

Now that you're in your branch you can start doing work. When you're ready and want to make a PR, commit your changes and push them to a remote branch by the same name as your local branch. Again, here's the steps in code:  
```
git add .
git commit -m "Commit message"
git push origin <your-name>/<branch-description>
```
To submit a PR, go back to the GitHub page. You should see a button that says something like "BRANCH had recent pushes x ago [Compare & pull request]". Press that button, fill out a description if you want (coderabbit will auto generate one either way) and create the pull request.

### Getting Started - Server
First
```
cd server
python -m venv .myenv
<activate virtual environment>
pip install -r requirements.txt
```

**Scraping UF SoC Data**
```
python ../scripts/scrape_soc.py
python ../scripts/clean_soc.py
```
Optionally, you can verify duplicates were removed with `./../scripts/verify_cleaned.sh`

**Running the Server**
First, make a new file called `.env` at the root directory, then copy the contents in `example.env` into this new file.
To start the develepment server do:
`flask run`

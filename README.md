![socialify image](https://socialify.git.ci/aleguy02/COP3530-project3/image?custom_description=See+where+a+class+can+take+you+with+GraphUF&custom_language=Python&description=1&font=Inter&language=1&name=1&pattern=Circuit+Board&stargazers=1&theme=Light)

# GraphUF
GraphUF is a web tool that helps students see not just what a class requires, but what a class enables. When planning your schedule, it’s hard to know which future opportunities a course will unlock — the official UF site only shows prerequisites, not the courses that depend on it.

With GraphUF, you can select any course and instantly see every class it leads to, including indirect ones (prerequisite-of-a-prerequisite). You can even enter the classes you’ve already taken, and GraphUF will filter results to show only the courses you would be NEWLY eligible to take. This makes it easy to discover hidden pathways and plan strategically for your academic goals.

## Table of Contents

1. [Local Setup](#local-setup)
2. [Collaboration Workflow](#collaboration-workflow)
3. [Server Setup](#server-setup)
4. [Data Processing](#data-processing)
6. [Disclaimers](#disclaimers)

---

## Local Setup

### Prerequisites

* Python **3.13.x**
* Linux-based OS (preferred, but not required)
* [Flask](https://flask.palletsprojects.com/) and project dependencies (installed later)

---

## Collaboration Workflow

We use a feature branch and pull request (PR) workflow.

1. **Clone the repository**

   ```bash
   git clone https://github.com/aleguy02/COP3530-project3.git
   cd COP3530-project3
   ```

2. **Create a branch**

   ```bash
   git branch <your-name>/<branch-description>
   git checkout <your-name>/<branch-description>
   ```

   * `<your-name>` → your name (e.g., `ale`)
   * `<branch-description>` → short, hyphen-separated description (e.g., `fix-visual-bug`, `refactor-tests`, `create-graph-api`)

4. **Ensure you are passing the tests (update the tests only if necessary)**

   ```bash
   python -m pytest
   ```

4. **Commit and push changes**

   ```bash
   git add .
   git commit -m "Commit message"
   git push origin <your-name>/<branch-description>
   ```

5. **Open a pull request**

   * Go to the repository’s GitHub page.
   * Click **Compare & pull request** when prompted.
   * Add a description (optional; Coderabbit can auto-generate one).
   * Submit the PR for review.

---

## Server Setup

1. **Navigate to the server directory**

   ```bash
   cd server
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv .myenv
   source .myenv/bin/activate   # Linux/Mac
   .myenv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**

   * Copy `example.env` to `.env` in the root directory.
   * Update environment variables as needed.

5. **Run the development server**  
!! WAIT !!  
If this is your first time setting the app up, you need to get all the data from UF's Schedules API. Luckily, there's a few scripts that do this for you. See [Data Processing](#data-processing) for more information on how to do this.

   ```bash
   flask run
   ```

---

## Data Processing

### Scraping UF SoC Data  
Do this from the `server` directory with your virtual environment enabled and dependencies installed. `scrape_soc.py` will take roughly 40 minutes to execute, depending on your connection. It should be outputting hints live, so if you are running the script but not seeing output in your terminal, something went wrong.  
```bash
python ../scripts/scrape_soc.py
python ../scripts/clean_soc.py
```

(Optional) Verify duplicates were removed:

```bash
../scripts/verify_cleaned.sh
```

### Streamlining JSON Data (Linux)

Sometimes in development, you'll want to be able to glance only at the important data. Run the following command to create a streamlined file only keeping `{code, name, prerequisites}` for each course:

```bash
jq '{courses: [.courses[] | {code, name, prerequisites}]}' src/json/soc_cleaned.json > src/json/streamlined_soc.json
```

If you only want to keep courses **with** prerequisites:

```bash
jq '{courses: [.courses[] | select(.prerequisites != "") | {code, name, prerequisites}]}' src/json/soc_cleaned.json > src/json/streamlined_soc.json
```

---

## Disclaimers

* Some courses list special prerequisites such as *instructor permission* or *graduate student status* — these are ignored for now.
* AND/OR prerequisites are currently treated the same for simplicity.
* This tool is not officially supported by UF. We encourage you to independently verify the validity of results.

---

Made with ❤️ by Alejandro Villate, Kevin Pugliese, and Michael Pierre-Canel

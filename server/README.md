### Running Tests  
`python -m pytest`

### Data  
If you want to streamline the json to only see the important fields {code, name, prerequisites}, do the following command (Linux only, you can try to ChatGPT a way to do it on windows): `jq '{courses: [.courses[] | {code, name, prerequisites}]}' src/json/soc_cleaned.json > src/json/streamlined_soc.json`

If you only care about courses with prerequisites, do `jq '{courses: [.courses[] | select(.prerequisites != "") | {code, name, prerequisites}]}' src/json/soc_cleaned.json > src/json/streamlined_soc.json`

### Debugging
One of the ways I've been debugging is with pdb, which is a built in Python debugger similar to GDB. Here's a helpful intro article: https://www.bitecode.dev/p/intro-to-pdb-the-python-debugger

### Disclaimers
Handling corequisites seems hard, so I'm ignoring them completely for now and only handling prereqs.

Some classes have prerequisites like instructor permission or must be grad student. I'm ignoring these specific prereqs for now because it also seems annoying.

AND/OR prerequisites are treated the same for simplicity
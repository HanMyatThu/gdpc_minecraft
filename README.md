# Procedural Content Generation in Minecraft

This repository contains all the source code for the submission of the first project for the course "Modern Game AI"  in the Master Artificial Intelligence at Leiden University.

The task was to use the [GDPC] Python package to generate a structure in Minecraft that is somewhat adaptable to the environment.

## Instructions

To run the code, you will need to have the following software installed:
- Minecraft 1.19.2 (Java Edition)
- Forge for Minecraft 1.19.2 [download](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.19.2.html)
- The GDMC HTTP interface mod [download](https://github.com/Niels-NTG/gdmc_http_interface/releases/tag/v1.0.0)
- The GPDC Python package [download](https://github.com/avdstaaij/gdpc)
- Python 3
- NumPy
  
When you do, open a Minecraft world with the mods enabled.
Run the following command in the chat:

```bash
\setbuildarea ~ ~ ~ ~100 ~100 ~100 (or whatever build area you want)
```

Finally, clone this repo and do the following commands:

```bash
pip install -r requirements.txt
cd assignments/
python assignment.py
```

Depending on your hardware, this may take a couple of minutes.
When it is done, you should see a structure in the build area.

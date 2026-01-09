<div align="center">
  <br>
  <h1>Charged triangles</h1>
  <strong>Simulating the electrostatic charge distribution for (somewhat) arbitrary objects</strong>
</div>
<br>


## Table of Contents

- [Table of Contents](#table-of-contents)
- [What is this project?](#what-is-this-project)
- [Contributors](#contributors)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Acknowledgements](#acknowledgements)
- [License](#license)
- [Questions](#questions)

## What is this project
This is code for the project "Simulating the electrostatic chargedistribution" in the course "Project in applied physics" at Uppsala university. The code works standalone but for theoretical background, some example usecases and discussion of some limitations in the code we refer you to the project report in the course.

The code aims to simulate and visualize the electrostatic charge distribution that would occur on a user inputed body. The code uses either point-charge approximation or homogenously charged triangles as described by Okon and Harrington. It should also be relatively easy to add other approximations using most of the code provided.

## Contributors

The code was written by master students Hampus Berndt and Filip Eriksson at Uppsala university
under the supervision of Anders Eriksson at IRFU.

## Getting Started

This section provides a high-level quick start guide. 

The code runs on python using open3d for visualization. To run the code you will need both downloaded along with some (smaller) packages. For all packages see dependencies.

There are many files of code in the project that you will not need to touch to run the code. The idea when running the code is that you choose (or create) the correct script and run it. The script will require you to choose (or create) a settings file in which you specify the setup for this simulation. After running the script you will get the appropriate visualization and also save the result into a save file. Some scripts take a save file and can make changes to the visualization methods or some smaller setup changes and then display the result without needing to calculate everything again.

Beware! If you are running with may triangles (and especcially homogenously charge triangles) the scripts that calculate will take a long time to reach a result. Choose your settingfile wisely and test it with the testing scripts before comitting to a long calculation.

Relevant scripts to run:
-main (takes a simulation_setting and visualization_setting file and runs all calculations and visualize them. The "full" program)
-run_saved (takes a save file and a visualization_setting file and visualizes the save. Goes a lot faster and is used when the simulation is already calculated)
-test_bodies (takes a simulation_setting file and shows you the bodies you currently have in the settings. Good to use before running full program so that you dont calculate everything in error)

## Dependencies

### Languages:
Python 3.12.3

### External dependancies:
open3d 0.19.0
numpy 1.26.4
matplotlib 3.8.4
dill 0.3.8
GitPython 3.1.46

### Python internal libraries:
concurrent.futures
argparse
functools
time
copy
os
importlib

## Acknowledgements

Thank you to Anders Eriksson at IRFU for help and supervision of the project.

Thank you to Anders Eriksson at IRFU for coming up with the idea in the first place.

Thank you to Anders Eriksson at IRFU for creating a first simpler version of the project in matlab from which inspiration and 2 lines of code was taken.

Thank you in advance to the two students at Uppsala university who will take their time to review this project (I did not include your names because you might want to be anonamous, tell us otherwise and we will add you!)

## License




## Questions
If you have any questions, dont hesitate to reach out to us! We can not promise we will answer though. Especialy not if this is years later.

We wish you the best of luck!
Hampus and Filip

[⬆ Back to Top](#table-of-contents)



# Preliminary design of multirotor tool
*Written by Marc Budinger, Aitor Ochotorena (INSA Toulouse) and Scott Delbecq (ISAE Supaero)*

Click on the Binder tab to start the Voila standalone web app:

launch on Voilà tool: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aitorochotorena/multirotor-all/master?urlpath=voila)

launch on binder:[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aitorochotorena/multirotor-all/master)

Work related to the design and optimization of multirotor drone as part of the tasks for the DroneApp project and SizingLab Project.

To start run:
    
    1. cd notebooks
    
    2. jupyter notebook

Then, open the file `00_Introduction.ipynb`.

![DroneApp](DroneApp_logo.png)
<img src="logo_sizinglab.png" style="float:right; max-width: 15px; display: inline" alt="SizingLab" /></a>

**Table of contents**

1. Case Study. An overview of the different drone's architecture history and components.
2. Sizing scenarios definition. Definition of the design drivers for each of the different static and vertical flight missions.
3. Sizing scenarios equation. Overview of some of the main design equations for each missions.
4. Scaling laws for electric motors. Application of the derived scaling laws on given references from data catalogues.
5. Scaling laws for ESC. Application of the derived scaling laws on given references from data catalogues.
6. Scaling laws for batteries. Application of the derived scaling laws on given references from data catalogues.
7. Scaling laws for cables. Application of the derived scaling laws on given references from data catalogues.
8. Propeller static regressions. Application of derived surrogate models on given references from data catalogues for static missions, such as hovering or take-off.
9. Propeller regressions for vertical flight. Visualization tools of thrust and power coefficient as function of beta and advance ratio.
10. Single sizing code for propeller component (TP, consideration of just hover and take-off)
11. Single sizing code for motor component (TP, consideration of just hover and take-off)
12. Single sizing code for battery and ESC component (TP, consideration of just hover and take-off)
13. Single sizing code for frame component (TP, consideration of just hover and take-off)
14. Basic global sizing code (hover, take-off)
15. Sizing code of propeller considering vertical flight.
16. Basic sizing code considering all global constraints.
17. Monotonicity table to reduce the problem to the necessary constraintss.
18. Basic sizing code after application of MP1.
19. Basic sizing code considering coupling techniques and MP1.
20. Mathematical optimization and rendering the final geometry using 3D visualization tools.
21. Complete optimization (hovering, take-off and vertical flight) using data catalogues, pareto charts and decision trees and rendering the final geometry using 3D visualization tools.
22. Complete optimization (hovering, take-off and vertical flight) using data catalogues, pareto charts and decision trees.
23. Validation on mini quadcopter MK4.
24. Validation on oktocopter S1000+.
25. Validation on taxi-drone Ehang184.
26. Multiinput creation of Pareto charts for any data catalogue (use of upload button)

A1. Quadro description

A2. Sizing equations overview.

+ decision trees files

# [First Lego League](https://first-lego-league.org)

# [Greensubmarines](https://green-machine.webflow.io/) FirstLegoLeague programm

---

#### robot:
  > power should never drop under 8000 (mAh) (out of 8350 mAh). Otherwise driving could result in pure jank. [You should also keep an eye on a fully charged battery, because "overfilling" the battery (probabbly over 8300mAh) can cause mayhem as well.]

#### IDE / extension:
Visual Studio Code extensions:
  > Python (IntelliSense)
  > LEGO SPIKE Prime / MINDSTORMS Robot Inventor Extension
  > GitLense
  > (TODO Tree)

### multiple file system:
  > multiple file system is now implemented by standard. You just save and upload the main program. The rest happens automatically.

### COM port stuff
new binding in Linux:
  > When setting up a new linux device with the Spike Prime, first create a new port:
  > sudo rfcomm bind [number for new port, i.e.: 0] [mac address of spike]
  > then use `dev/rfcomm0` port to connect to in the VisualStudioCode extension.
  > bluetooth-app has to be closed

### Use git
> - main is only updated in consense
> - main gets tags for marking important points
> - branches for testing and development
> - two types of branches: run/xxx and feature/xxx
> - never fix backend problems in a run/xxx branch

[BezierCurveCalculator](https://acegikmo.com/bezier/)

The contents of this repository are intelectual property of Green Machine. Without written approval, you are not allowed to copy, distribute, sell, modify, loose or change any contents. © Green Machine 2023
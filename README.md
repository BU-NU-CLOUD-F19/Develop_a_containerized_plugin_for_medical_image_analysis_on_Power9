# Develop a containerized plugin for medical image analysis on Power9

# Vision and Goals
We will create a plugin for ChRIS that enables end-users to do their image processing using FreeSurfer on Power9 computers in the MOC.

High level goals include:
* A container with FreeSurfer compiled for the PowerPC architecture
* A ChRIS plugin that uses this container
* Ability for end users to select which architecture they want to run FreeSurfer on


# Users and Personas
The end user of our plugin will be hospitals that need to do computationally intensive image processing.

It targets:
* Hospitals that need image processing (in the Greater Boston Area)
# Scope and Features
* Containerize FreeSurfer as a ChRIS plugin (?)
* Compile FreeSurfer to PowerPC architecture
* Utilize Power9 machines on the MOC
* Add flag in ChRIS internals to denote which architecture to use on the MOC

# Solution Concept

High Level Outline:
* Create a container with FreeSurfer compiled to PowerPC architecture
  - Compile FreeSurfer on x86 (Ubunutu or CentOS)
  - Containerize FreeSurfer on x86
  - Cross compile x86 to PowerPC
* tbd...

# Acceptance Criteria
* The minimum acceptance critiera is to compile (at least some components of) FreeSurfer to the PowerPC architecture and containerize it and create a ChRIS 'app' that uses the PowerPC FreeSurfer container
* Stretch goal: tbd

# Release Planning
* Release #1
  - Compile FreeSurfer on x86 (Ubunutu or CentOS)
  - Containerize FreeSurfer on x86
  - Cross compile x86 to PowerPC architecture

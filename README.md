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
* Containerize FreeSurfer as a ChRIS plugin
* Compile FreeSurfer to PowerPC architecture
* Utilize Power9 machines on the MOC
* Add flag in ChRIS internals to denote which architecture to use on the MOC

# Solution Concept

High Level Outline:
* Create a container with FreeSurfer compiled to PowerPC architecture
  - Compile FreeSurfer on x86 (Ubunutu or CentOS)
  - Containerize FreeSurfer on x86
  - Cross compile x86 to PowerPC

FreeSurfer - Open source software suite for processing and analyzing brain and MRI images. This is what will be containerized to run on PowerPC.

Linux Server running CentOS - This platform is currently used for FreeSurfer computation. Switching to the Power9 computers will decrease the time taken for computation and allow for a higher volume of requests.

Client - ChRIS - MOC - Review Data - The end goal is to have a containerized FreeSurfer that is compatible with ChRIS and runs on PowerPC. This will allow users of the ChRIS client to have access to much more powerful computers for the image processing.
 
![Product Structure](https://raw.githubusercontent.com/rschneid1/hello-world/master/images/Diagram.png)



ChRIS - ChRIS is a collaborative project between Boston Children's Hospital and Red Hat. It is an open source framework that utilizes cloud technologies to bring medical analytics and allows health organizations to own their data and benefit from public computational power.

Our team will make the FreeSurfer container compatible with ChRIS over the course of the semester as we learn more about the ChRIS platform. 

![ChRIS platform overview](https://raw.githubusercontent.com/rschneid1/hello-world/master/images/Image%20from%20iOS.jpg)


# Acceptance Criteria
* The minimum acceptance critiera is to compile (at least some components of) FreeSurfer to the PowerPC architecture and containerize it, and create a ChRIS 'app' that uses the PowerPC FreeSurfer container.
* Stretch goal: TBD

# Release Planning
* Release #1 (in 2 Weeks)
  - Compile FreeSurfer on x86 (Ubuntu or CentOS)
  - Containerize FreeSurfer on x86
  
* Release #2 (in 4 weeks)
  - Cross compile x86 to PowerPC architecture
  
* Release #3 (in 6 weeks)
  - Flag that allows ChRIS to pick which architecture to use on MOC.
  

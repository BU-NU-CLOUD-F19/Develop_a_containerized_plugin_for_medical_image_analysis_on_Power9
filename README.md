# Develop a containerized plugin for medical image analysis on Power9

# Background
Our project is to create a plugin for ChRIS, an existing system, that allows the end user (i.e. Doctors and Neuro-Researchers) to upload their image files to the system, run jobs on the images, and get the results back.

To understand the goals and scope of our project, one needs to understand the architecture of the ChRIS platform.  
The ChRIS documentation can be found here: https://github.com/FNNDSC/CHRIS_docs

![ChRIS architecture](https://github.com/FNNDSC/CHRIS_docs/raw/master/chris_architecture_overview.png)

The typical dataflow of ChRIS is as follows:  
1. The user uploads their images (data) via the web interface
2. The data is sent to the server labelled as ChRIS within the image
3. The data can be saved in the database here (optional??? idk)
4. ChRIS plugin??? Research this
5. The data is then sent from the database (or directly from server memory??? idk) to the MOC
6. The MOC spins up a cluster. The user can specify what computing environment they want to use for their cluster.
7. blah blah
tbc

# Vision and Goals
We will be creating a plugin for ChRIS that enables end-users to do their image processing using FreeSurfer on Power9 computers in the Mass Open Cloud.

High level goals include:
* A container with FreeSurfer compiled for PowerPC architecture
* Ensuring the FreeSurfer container runs efficiently with PowerPC architecture
* A ChRIS plugin that uses the FreeSurfer container
* Ability for end-users to select which architecture they want to run FreeSurfer on
* Integration with the ChRIS client (allowing users to use ChRIS to run their data on the MOC and
  get their results delivered in efficient time).


# Users and Personas
The plugin will be used by Doctors and Technicians that currently use FreeSurfer to process their patients' brain MRI images. The project targets those in the Greater Boston Area; however with the addition of the Power9 computers, the long-term goal is that Doctors beyond the Greater Boston Area will have the ability to process their requests using the plugin.

It does not target:
* Those who do not use FreeSurfer. This is not a general purpose project, it is only meant for                
  FreeSurfer.
* Users of FreeSurfer who do not use the MOC and ChRIS. There may be other Doctors and Technicians      
  that use FreeSurfer on the MOC but are not users of the ChRIS platform. This project will only affect those on the ChRIS
  system.

# Scope and Features
* Containerize FreeSurfer as a ChRIS plugin
* Compile FreeSurfer and its container to PowerPC architecture
* Utilize Power9 machines on the MOC
* Add a flag in ChRIS internals to denote which architecture to use on the MOC

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



ChRIS - ChRIS is a collaborative project between Boston Children's Hospital and Red Hat. It is an open source framework that utilizes cloud technologies to bring medical analytics and allows health organizations to benefit from public computational power in addition to owning their data.

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
  - Instantiate a flag that allows ChRIS to pick which architecture to use on MOC.
  

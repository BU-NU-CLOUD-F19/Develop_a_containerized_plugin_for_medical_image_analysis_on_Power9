# Develop a containerized plugin for medical image analysis on Power9

# Background
ChRIS is a collaborative project between Boston Children's Hospital and Red Hat. It is an open source framework that utilizes cloud technologies to bring medical analytics and allows health organizations to benefit from public computational power in addition to owning their data. One of its main charicteristics is allowing the developers to make medical analytic plugins that can be embedded into the Mass Open Cloud deployment. The creating of a plug-in is what we are doing with this project.

ChRIS functions as a web service. A user will log into a ChRIS client, choose their program, and then upload their files to the ChRIS client. ChRIS will then send the data to the MOC network, where the MOC will download the files and the FreeSurfer program and run it. Currently this occurs on x86 machines. Once the container is created on PowerPC, the goal is that when ChRIS sends the user files and FreeSurfer program, it will include a flag to run the process on a Power9 machine. This will greatly decrease computational time. As a side note, a complete understanding of the inner workings of how ChRIS and the MOC stores information is beyond the scope of this project. Our advisor informed us that we should be concerned with how the flag is passed and creating the ChRIS plugin. However, he did give us a brief explanation, which is shown in the ChRIS platform overview.

Our team will make the FreeSurfer container compatible with ChRIS over the course of the semester as we learn more about the ChRIS platform.

To understand the goals and scope of our project, one needs to understand the architecture of the ChRIS platform.  
The ChRIS documentation can be found here: https://github.com/FNNDSC/CHRIS_docs

![ChRIS architecture](https://github.com/FNNDSC/CHRIS_docs/raw/master/chris_architecture_overview.png)

The typical dataflow of ChRIS is as follows:  
1. The user uploads their images (data) via the web interface.
2. The data is sent to the server labelled as ChRIS within the image and stored in the database.
3. When a user wants to run a job, the ChRIS server sends the data to the MOC. The MOC creates a container and pulls the ChRIS plugin (that corresponds to the job requested) and runs the job.
4. The MOC communicates results to the server and the server communicates the results to the client.

# Vision and Goals
We will be creating a containerized plugin for ChRIS that enables end-users to do their image processing using FreeSurfer on Power9 computers in the Mass Open Cloud.

(FreeSurfer is a software package used for processing and analyzing human brain MRI images. This is what will be containerized to run on PowerPC.)

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
* Feature: FreeSurfer is containerized as a ChRIS plugin
* Feature: FreeSurfer compiles to PowerPC architecture
* Feature: Flag in plugin --> denotes which architecture (PowerPC or x86) to use on the MOC 
* Feature: ChRIS is able to read PowerPC images on PowerPC machines and x86 images on x86 machines 

* Out of Scope: Inner workings of OpenShift, how ChRIS stores information, and how the MOC stores information.

# Solution Concept

Global Architectural Structure Of the Project: help

High Level Outline:
* Create a container with FreeSurfer compiled to PowerPC architecture
  - Compile FreeSurfer on x86 (Ubuntu or CentOS)
  - Containerize FreeSurfer on x86
  - Cross compile x86 to PowerPC
  
## Design Implications and Discussion:

Why PowerPC architecture? The goal is to successful compile the containerized FreeSurfer plugin with PowerPC architecture because this cloud-based architecture will decrease computation time and allow for a higher volume of requests than x86 architecture.

Why is it containerized? Containers contain all of the necessary executables, and are lightweight and portable. This will help us migrate FreeSurfer to the PowerPC architecture.

Why are we using Docker? Docker is popular for creating and building software inside containers, which is what we need to do.

Why are we cross-compiling onto PowerPC? We honestly have no idea what this means and may not even be doing this, but it's what our project mentor suggested we do.

It is likely that we will need to discuss more specific design implications as we execute these higher-level design processes.
 
![Product Structure](https://raw.githubusercontent.com/rschneid1/hello-world/master/images/Diagram.png)

![ChRIS platform overview](https://raw.githubusercontent.com/rschneid1/hello-world/master/images/Image%20from%20iOS.jpg)


# Acceptance Criteria
* The minimum acceptance critiera is to compile (at least some components of) FreeSurfer to the PowerPC architecture and containerize it, and create a ChRIS 'app' that uses the PowerPC FreeSurfer container.
* Stretch goal: Compile all of FreeSurfer to the PowerPC architecture. This is a stretch goal because some parts of FreeSurfer rely on third-party libraries that may not be compatible with PowerPC architecture.

# Release Planning
Sprint planning is conducted on Taiga, which we are still learning how to use: https://tree.taiga.io/project/onesphore-template-for-cloud-computing-fall-2019-bu-3/taskboard/demo-1-7
* Release #1 (in 2 Weeks)
  - Compile FreeSurfer on x86 (Ubuntu or CentOS)
  - Containerize FreeSurfer on x86
  
* Release #2 (in 4 weeks)
  - Cross compile x86 to PowerPC architecture
  
* Release #3 (in 6 weeks)
  - Instantiate a flag that allows ChRIS to pick which architecture to use on MOC.
  
# Open Questions
- What is cross-compiling and why should we potentially use it to compile FreeSurfer on PowerPC architecture?
- How do we use Docker to make a container? How do we use Docker Hub?
- What exactly is the function of the ChRIS plugin?

# Risks (or opportunities?)
- Lack of knowledge/general understanding (aka learning curve)

# Sprint Demo Presentations
- Sprint 1 Demo: https://docs.google.com/presentation/d/1gTr5xhz9U68FB50PdQvl90KYEqc4Fye6mlfKmVhlSXU/edit?usp=sharing
  
  
  

# Develop a Containerized Plugin for Medical Image Analysis on Power9
Mentor: Rudolph Pienaar of Boston Children's Hospital

# Contributors
- Nicole Elbeery
- Quinn Meurer
- Ryan Schneider
- Erin Thomas

# Background
ChRIS is a collaborative project between Boston Children's Hospital and Red Hat. It's an open source framework that utilizes cloud technologies to bring medical analytics and allows health organizations to benefit from public computational power in addition to owning their data. One of its main charicteristics is allowing the developers to make medical analytic plugins that can be embedded into the Mass Open Cloud deployment. The creating of a plug-in is what we are doing with this project. 

ChRIS functions as a web service. A user will log into a ChRIS client, choose their program, and then upload their files to the ChRIS client. The ChRIS client will send the data to the ChRIS server which will then send it to the MOC network, where a container in the MOC will download the  plugin and run it. Currently this works on x86 machines. Once the container is created on PowerPC, the goal is that when ChRIS sends the user files and the program, it will include a flag for the user to choose whether they want to run the process on PowerPC or x86. Running the process on Power9 machines in the MOC allows for a decrease in computational time. As a side note, a complete understanding of the inner workings of how ChRIS and the MOC stores information is beyond the scope of this project. Our advisor informed us that we should be concerned with how the flag is passed and creating the ChRIS plugin. However, he did give us a brief explanation, which is shown in the ChRIS platform overview.

To understand the goals and scope of our project, one needs to understand the architecture of the ChRIS platform.  
The ChRIS documentation can be found here: https://github.com/FNNDSC/CHRIS_docs

![ChRIS architecture](https://github.com/FNNDSC/CHRIS_docs/raw/master/chris_architecture_overview.png)

The typical dataflow of ChRIS is as follows:  
1. The user uploads their images (data) via the web interface.
2. The data is sent to the server labelled as ChRIS within the image and stored in the database.
3. When a user wants to run a job, the ChRIS server sends the data to the MOC. The MOC creates a container and pulls the ChRIS plugin (that corresponds to the job requested) and runs the job.
4. The MOC communicates results to the server and the server communicates the results to the client.

# Vision and Goals
We will be creating a containerized plugin for ChRIS that enables end-users to do their MRI image processing on Power9 computers in the Mass Open Cloud. We will be containerizing the mri_convert application of Freesurfer, which is an open-source brain imaging software package.

High level goals include:
* Compile mri_convert application of Freesurfer software package on PowerPC
* Create a containerized ChRIS plugin with mri_convert binary
* Build pman and pfioh on PowerPC
* Communicate to pman and pfioh on PowerPC through ChRIS instance

# Users and Personas
The plugin will be used by Doctors/Technicians and Neuro-Researchers that need to run FreeSurfer, for example to process MRI scans. The goal of the overall ChRIS project is to make these computationally intensive tasks accessible through the cloud for medical professionals. Our specific project mainly targets existing ChRIS users that already are running FreeSurfer via ChRIS. We want to give these users the option to run FreeSurfer on Power9 machines, which will speed up the processing time.

It does not target:
* Those who do not use FreeSurfer. This project is an optimization that only affects FreeSurfer.
* Users of FreeSurfer who do not use the MOC and ChRIS. There may be other Doctors and Technicians      
  that use FreeSurfer on the MOC but are not users of the ChRIS platform. This project will only affect those who use the ChRIS system.

# Scope and Features
Our minimum viable product was to containerize mri_convert application of the Freesurfer software package to run as ChRIS plugin on PowerPC machines and to implement this into the ChRIS system. To clarify, Freesurfer is an open-source brain imaging software package, and mri_convert is an application of this package that converts between different file formats.

Our original minimum viable product consisted of containerizing all of the Freesurfer software package, however compiling some of these packages was beyond our scope, so we scaled it down to just compiling mri_convert. We chose this application because it is the most widely used Freesurfer application for target users.


# Solution Concept

Global Architectural Structure Of the Project: 

High Level Outline:
* Create a container with FreeSurfer compiled to PowerPC architecture
  - Compile FreeSurfer on x86 (Ubuntu or CentOS)
  - Containerize FreeSurfer on x86
  - Cross compile x86 to PowerPC
  
## Design Implications and Discussion:

Why PowerPC architecture? The goal is to successfully compile the containerized FreeSurfer plugin with PowerPC architecture because this architecture will decrease computation time. Power9 machines are optimzed for performing matrix operations, so using Power9 machines should give FreeSurfer a speed increase.

Why is it containerized? A ChRIS plugin is a container that is run on the MOC machines. We need to containerize FreeSurfer so that we can use it in a ChRIS plugin. Containers allow us to run our ChRIS plugin on machines in the cloud without having to worry about the environment. 
  - Decouple application from environment. in our case that means we can easily spin up a container on the p9 machine in the    moc.
  - It was really difficult for us to get all this software set up and configured, and now if someone else wants to use it they don’t have to go through that pain point themselves
  - Main benefit of containers over VM is that VMs each need to virtualize an OS but containers run on top of a shared OS, which makes them much more lightweight


Why are we using Docker? We are using Docker because the existing ChRIS infrastructure uses Docker and we are using the existing ChRIS plugin template. The ChRIS infrastructure also uses OpenShift and our mentor said we should not concern ourselves with the inner workings of this. 

 
![Product Structure](https://raw.githubusercontent.com/rschneid1/hello-world/master/images/Diagram.png)

![ChRIS platform overview](https://raw.githubusercontent.com/rschneid1/hello-world/master/images/Image%20from%20iOS.jpg)


# Acceptance Criteria
* The minimum acceptance critiera is to compile (at least some components of) FreeSurfer to the PowerPC architecture and containerize it, and create a ChRIS 'app' that uses the PowerPC FreeSurfer container.
* Stretch goal: Compile all of FreeSurfer to the PowerPC architecture. This is a stretch goal because some parts of FreeSurfer rely on third-party libraries that may not be compatible with PowerPC architecture.

# Release Planning
Sprint planning is conducted on Taiga, which we are still learning how to use: https://tree.taiga.io/project/onesphore-template-for-cloud-computing-fall-2019-bu-3/taskboard/demo-1-7
* Release #1 - September 26th
  - Compile some of Freesurfer on x86
  - Create a "Hello World!" ChRIS plugin
  
* Release #2 - October 10th
  - Compile some of Freesurfer on x86
  - Figure out design options for containerization
  
* Release #3 - October 24th
  - Compile and containerize Freesurfer on x86
  - Create "Hello World!" container on PowerPC
  
* Release #4 - November 10th
  - Create a containerized ChRIS plugin with mri_convert binary on x86
  
* Release #5 - November 21st
  - Compile mri_convert on Power9
  - Built pman and pfioh on Power9
  - Containerize ChRIS plugin with mri_convert on Power9
  
* Release #6 - December 7th
  - Make ChRIS backend instance and integrate plugin
  
# Open Questions
- What is cross-compiling and why should we potentially use it to compile FreeSurfer on PowerPC architecture?
- How do we use Docker to make a container? How do we use Docker Hub?
- What exactly is the function of the ChRIS plugin?

# Risks (or opportunities?)
- Lack of knowledge/general understanding (aka learning curve)

# Sprint Demo Presentations
- Sprint 1 Demo: https://docs.google.com/presentation/d/1gTr5xhz9U68FB50PdQvl90KYEqc4Fye6mlfKmVhlSXU/edit?usp=sharing
- Sprint 2 Demo: https://docs.google.com/presentation/d/1QpS4oyl4nnCyd4yITBuRRuyBGb8_NXvphm98m-eAIZU/edit?usp=sharing
- Sprint 3 Demo: https://docs.google.com/presentation/d/1Pt14AbmzgGssEnWz1327LCw7CKAM8O3XLj8-ODPceeg/edit?usp=sharing
- Sprint 4 Demo: https://docs.google.com/presentation/d/19zGiUAN0KiV_gWRhAXAceXLDhsOxsDNBWPam9VT9hFc/edit?usp=sharing
- Sprint 5 Demo: https://docs.google.com/presentation/d/13li_IvCtlmfqs_kvQWMxBVQsnhc62L5bN8tt4nnNJCk/edit?usp=sharing

# Google Cloud Spanner Presentation
https://docs.google.com/presentation/d/1r1mF2JLrkIEE0HnX7CcssxO__eYmr4oz3VWf_d6U6EU/edit?usp=sharing

# Final Demo Presentation
- Presentation: https://docs.google.com/presentation/d/1GZrYl_EeKrZcqR-DsP34QPbXfkMqWcicQZNeKs4SeuQ/edit?usp=sharing
- Video: 
  
  
  

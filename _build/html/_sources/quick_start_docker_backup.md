# Getting started with the CESM Lab container

The following instructions describe how to download Docker, get the CESM-Lab container, and run the CESM-Lab for NEON tower sites.

If you prefer to see a slide deck with more images, see this [Docker
Tutorial](https://drive.google.com/file/d/1Zs_SrlpGVlS3KHvFDUVyCGPXOfKgG4_c/view).

In this tutorial:
1. Download and install Docker
2. Download the CESM-Lab container within Docker
3. Set up a directory where simulations will be stored on your computer
4. Run and connect to the CESM-Lab container
5. Access the NEON Tower Simulation tutorial
6. End your session

Steps 1-3 only need to be completed once. You can continue to use the container system starting at step 4. 

If you already have Docker installed on your computer, start at Step 2.


## Container Basics

CTSM and CESM typically require computing resources that can be
complicated to set up on a personal computer. Now you can easily run
CTSM using a container. 

### What is a container?
A container is preconfigured, portable
application that can reliably run on any computing infrastructure.

### Why use a container?
* **Portable** : Containers can run almost everywhere (Mac, Windows, Linux).
* **Pre-configured** : No installation or porting required on containers.
* **Standardized** : All users get the same environment.

### CESM-Lab
The capability to run NEON tower simulations is available using the CESM-Lab container.


![CESM-Lab](cesm_lab_overview.png)

:::{note}
CESM-Lab is a containerized environment with CESM and  Jupyter Lab.
:::

### How do I get started?

The software is available through a Docker
container. This tutorial will guide you through setting up the CTSM
container, where you will find a separate tutorial on running CTSM
at NEON tower sites.

Before diving in, we’ll need to install Docker, which we’ll cover
next.

Some of the instructions also in this tutorial also use basic Linux
commands, which you can run on Macs using the Terminal application
(in the Utilities folder) or a similar application for PCs, like
Windows PowerShell.


:::{seealso}
Knowledge of Linux is not required for this tutorial. If you are unfamiliar with Linux and would like to know more, there are several tutorials online.
 Software Carpentry is one organization that has accessible [online lessons]( https://software-carpentry.org/lessons/).
:::

## Download & Install Docker
**Docker is available for free from** [this website](https://www.docker.com/products/docker-desktop)

Follow the instructions to install the Docker Desktop App. The [Getting Started guide on Docker] (https://www.docker.com/get-started) has detailed instructions for setting up Docker on Mac, Windows, or Linux.

:::{tip}
To access the container, you can interface with Docker using the Desktop App or using a command line.
:::

:::{note}
If you have trouble installing the latest Docker, please try Docker 3.x. Some newer versions of Docker may be incompatible with your operating system.
:::


:::{seealso}
If you are unfamiliar with Docker or are having trouble, you may find the following links helpful:

* [Cyverse Docker tutorial](https://learning.cyverse.org/projects/foss-2020/en/latest/Containers/introtocontainers.html)

* [Learn more about containers on Docker](https://www.docker.com/resources/what-container)

* [Docker FAQs](https://docs.docker.com/engine/faq/)

* [Docker community forums](https://forums.docker.com/)

* [Docker Q&A on StackOverflow](https://forums.docker.com/)

:::


## Download the CESM-Lab Container

This only needs to be done one time -- you can keep using this
container any time you run NEON simulations. Please note that this step
can take a little time as it will download \~5GB of data (time will vary
based on internet speed).*

### Getting CESM-Lab: using a Linux command-line

- Mac: find “Terminal” in your Utilities
- Windows: Run the ‘PowerShell’ from the Start menu

### Download the CTSM Docker Container

In your Terminal or PowerShell window, type:

    docker pull escomp/ctsm-lab-2.3-preview

:::{note}
Docker needs to be running on your computer before using the ‘pull’ command above. 
You can run Docker by either opening the app or typing “docker login” in the command line.
:::

## Set up a directory for your simulations

This step is used to create a directory that will map into the container. 
The directory will store all the files required to run a simulation so that it does is saved when you exit the container. 

### Create a location for the container

These instructions create a new folder `Simulations` on your desktop. 

You may customize the name and location of the folder.
If you change the name or location you will need to update the container location in the next step.

In your terminal or PowerShell window, type:

    mkdir \$HOME/Desktop/Simulations

Confirm that this step worked properly. Do you see the `Simulations` folder on your desktop?


## Run & connect to CESM-Lab container

To access CESM-Lab, you need to first run or launch the container and then connect to it. The next steps launch the container (4a) and then ‘forwards’ a web browser to it (4b), with descriptions included below the commands to help understand what it is doing. Note that this step uses the command line to run the container (recommended). If you prefer to use the GUI interface within the Docker App, see the alternate instructions below (Alt 4a).

There are two options for running the container.

### Running CESM-Lab using a Linux command-line

In your terminal or PowerShell window, type:

```
  docker run -it --rm -p 9999:8888 -v \$HOME/Desktop/Simulations:/home/user escomp/ctsm-lab-2.3-preview

```
Description of some flags or options that are available for running the `docker run`:

*  `-it --rm` = 'Ease-of-use’ options: interactive & clean-up
*  `-p` = Port number
*  `-v` = Directory to mount into the container (first half), and the container’s mount location
*  `"escomp/ctsm-..."` = Container Image Name

Your terminal screen will show the following:  


![CESM-Lab Terminal](docker_terminal_screenshot.png)

:::{note}
Note that you can change the first part of the port number (9999) to a different number to run multiple instances of the container, but you will need to change the port number in the next step. 
:::


### Connect to CESM-Lab using a web browser

Open a new web browser window.

In the search bar type:

    localhost:9999

:::{note}
*This connects to an interface. Note the ‘9999’ at the end of this
number is the same as the beginning of the port in step 4 above. If you
launch more than one container at a time, you will need to change the
port number.
:::

## Accessing the NEON Tower Simulation Tutorial
Your browser window will open a Jupyter Notebook environment.

-   Click on the `tutorials` folder on the left, then
-   Click on the `notebooks` folder.
-   Open the `NEON_Tower_Simulation_Tutorial`


![Jupyter-Lab screenshot](notebook_screenshot.png)

Follow the tutorial instructions to run a NEON tower site simulation. 
Once you complete this tutorial, you can use the `NEON_Visualization_Tutorial` to explore and evaluate the data.


:::{tip}

-   *If you want to access the container again in the future and do not
    end your session, you can open a web browser and point to the
    container (Step 5).*
-   *If you end your session (Step 7) or restart your computer, you can
    restart the container from Step 4*
:::


## Ending your session

When you are ready to close your session, you will need to identify and kill your terminal sessions.

Identify active sessions by typing the following into terminal:

```
    docker ps 
```

:::{note}
You may need to open a new terminal window to do the following command.
:::

Once the container ID has been identified, kill the job by typing the
following into terminal:


```
    docker kill <session ID> 
```

If the `docker run` command was not run in the background, you might find
that you cannot type anything into the open terminal window. Either open
a new terminal window to identify and kill sessions, or you can use
`ctrl + c` to kill all active sessions.

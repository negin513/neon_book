The following instructions describe how to download docker, get the
CESM-Lab container, and run the CESM-Lab for NEON tower sites.

If you prefer to see a slide deck with more images, see this [Docker
Tutorial](https://drive.google.com/file/d/1Zs_SrlpGVlS3KHvFDUVyCGPXOfKgG4_c/view).

**Container Basics**

*CESM-Lab: A containerized environment with CESM + Jupyter Lab*

CTSM and CESM typically require computing resources that can be
complicated to set up on a personal computer. Now you can easily run
CTSM using a container. A container is preconfigured, portable
application that can reliably run on any computing infrastructure.

-   *How do I get started?* The software is available through a Docker
    container. This tutorial will guide you through setting up the CTSM
    container, where you will find a separate tutorial on running CTSM
    at NEON tower sites.
-   Before diving in, we’ll need to install Docker, which we’ll cover
    next.
-   Some of the instructions also in this tutorial also use basic Linux
    commands, which you can run on Macs using the Terminal application
    (in the Utilities folder) or a similar application for PCs, like
    Windows Command Prompt.
-   Knowledge of Linux is not required for this tutorial. If you are
    unfamiliar with Linux and would like to know more, there are several
    [online tutorials](https://software-carpentry.org/lessons/)

  Download & Install Docker
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Docker is available from** [this website](https://www.docker.com/products/docker-desktop)
  Follow the instructions to install the Docker Desktop App
  \* To access the container, you can interface with Docker using the Desktop App or using a command line
  \* *Note* If you have trouble installing the latest Docker, please try Docker 3.x. Some newer versions of Docker may be incompatible with your operating system.
  .. \_download-the-CESM-Lab-container:
  ============
  Download the CESM-Lab Container

*This only needs to be done one time -- you can keep using this
container any time you run NEON simulations. Please note that this step
can take a little time as it will download \~5GB of data (time will vary
based on internet speed).*

Getting CESM-Lab: using a Linux command-line ==============

-   Mac: find “Terminal” in your Utilities
-   Windows: Run the ‘PowerShell’ from the Start menu

Download the CTSM Docker Container ==============

In your Terminal or PowerShell window, type:

    docker pull escomp/ctsm-lab-2.3-preview

  Set up a directory for your simulations
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *These instructions create a new folder 'Simulations' (or whatever name you choose) on your desktop. You may customize the location of the folder.*
  In your terminal or PowerShell window, type::
  mkdir \$HOME/Desktop/Simulations
  ============
  Running CESM-Lab on the command line
  ============
  There are two options for running the container.
  The example below walks through the command line option (recommended), but this Docker Tutorial \<https://drive.google.com/file/d/1Zs\_SrlpGVlS3KHvFDUVyCGPXOfKgG4\_c/view\_\_ also walks trough using the GUI interface within the Docker App.
  **This runs the container using an interactive session.** *Descriptions are included below the command line to help understand what it’s doing.*
  In your terminal or PowerShell window, type::
  docker run -it --rm -p 9999:8888 -v \$HOME/Desktop/Simulations:/home/user escomp/ctsm-lab-2.3-preview
  \* -it --rm = 'Ease-of-use’ options: interactive & clean-up
  \* -p = Port number
  \* -v = Directory to mount into the container (first half), and the container’s mount location
  \* "escomp/ctsm-..." = Container Image Name
  *Your terminal screen will show the some text*
  .. \_connecting-to-cesm-lab-using-a-browser:
  ============
  Connecting to CESM-Lab using a browser

**Open a new web browser window.**

In the search bar type:

    localhost:9999

*This connects to an interface. Note the ‘9999’ at the end of this
number is the same as the beginning of the port in step 4 above. If you
launch more than one container at a time, you will need to change the
port number*

============ Accessing the NEON Tower Simulation Tutorial ============
*Your browser window will open a Jupyter Notebook environment*

-   Click on the “tutorials” folder on the left, then
-   Click on the “notebooks” folder.
-   Open the ‘NEON\_Tower\_Simulation\_Tutorial’

*Follow the tutorial instructions to run a NEON tower site simulation &
explore the data*

**Note:**

-   *If you want to access the container again in the future and do not
    end your session, you can open a web browser and point to the
    container (Step 5).*
-   *If you end your session (Step 7) or restart your computer, you can
    restart the container from Step 4*

============ Ending your session ============ **When you are ready to
close your session**

Identify active sessions by typing the following into terminal.
(**Note,** you may need to open a new terminal window to do this):

    docker ps 

Once the container ID has been identified, kill the job by typing the
following into terminal:

    docker kill <session ID> 

*If the docker run command was not run in the background, you might find
that you cannot type anything into the open terminal window. Either open
a new terminal window to identify and kill sessions, or you can use
ctrl + c to kill all active sessions.*

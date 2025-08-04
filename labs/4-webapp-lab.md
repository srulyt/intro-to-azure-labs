# Create a Web App

## Overview

In the previous set of labs, you focused on a scenario where you wanted to be able to host a web application, or web site, on Azure. Using the IaaS model, you implemented the necessary infrastructure such as:

- creating a virtual network
- create and deploy a virtual machine
- setup secure remote access
- remotely access the VM and install the IIS role on the server to host the web files

While we didn't deploy a working web site, the intention was to familiarize you with the requirements for hosting a web app in the IaaS model.

In this lab, you will use the same scenario of wanting to host a web application on Azure, but you will do so using the PaaS model. By completing this lab, you will be able to compare and contrast the effort that is necessary to perform the same hosting scenario, using the different models. After completing the lab, you will have reinforced your knowledge and understanding of the responsibility matrix for areas of ownership for IaaS and PaaS.

![Image showing the VM icon from the Azure portal.](../content/images/lab4/azure-web-app-icon.png)

### Learning Objectives

In this lab, you will learn the foundations of implementing a web app on Azure, using the platform as a service (PaaS) model.

You will:

- Provision a simple web app using the Azure portal

### Naming Conventions

Throughout the exercises, you will need to define names for different Azure Resources (e.g., Virtual Networks).

To guarantee the uniqueness of those resources please add the first 4 letters of your alias plus the last 2 numbers of your phone number. For example:

* The *special alias* for JohnDoe is John23
* When instructions say to enter __\<alias\>-rg__ you would enter **john23-rg**  

### Lab Execution Notes and Warnings

#### Where To Do This Lab

This lab can be performed on your laptop/desktop. There are no code dependencies.

#### Lab Dependencies

 - __Locally installed tools:__ None. 

 - __Previous lab dependencies:__ This lab depends on the _Resource Group_ and _virtual network_ you created in Lab 0 and Lab 2.

 - __Lab code:__ None. This lab does not use any lab code.

## Create a web app in the Azure portal (10 mins)

In this lab, you will provision a simple web app in the Azure portal. While the steps you take within this lab will setup a simple web app hosted on Azure, they are designed to show the differences between hosting a web app in the IaaS model vs the PaaS model, which will be demonstrated in this lab.

> __Note:__
> Take time during this lab to click and read the informational icons.

> __Note:__
> As you progress through the labs, frequently you will see instructions indicating "**+ Add, + Create, + New**". Be aware that various places in the Azure portal use **Add** *or* **Create** *or* **New** when you are creating / deploying a new resource. For convenience,  lab steps mention all three though you will most often find only one of them in the portal for any given step.

### Task 1: Create a web app using the Azure portal 

1. Sign in to the Azure portal: **https://portal.azure.com**

1. From the **Home** page in the portal, select **+ Create a resource**.

1. In the **Search services and marketplace** text field, enter **Web App**, and press Enter.

1. Find the Web App entry in the displayed services and select **Create**, then **Web App**.

> __Note:__
> You will also typically find the **Web App** resource on the list of Popular Azure services found on the **Create a resource** pane.

3. On the **Basics** tab, fill in the following information (leave the defaults for everything else):

    - **Subscription:** - **Visual Studio Enterprise Subscription** per instructions above
    - **Resource group:** - Use the resource group you created in the previous lab
    - **Name** - Use the name **`<alias>-WebApp`** (Ensure you replace <alias> with your own alias)
    - **Publish** - Ensure that the **Code** option is selected
    - **Runtime stack** - From the drop-down, select **ASP.NET V4.8**. You will note that the **Operating System** option automatically selects Windows.  If you chose **.NET 6 (LTS)** or many of the other options, you could use Linux as the base OS but we will use ASP.NET for this exercise.
    - **Region** - Use the same region from the previous labs
    - **Pricing Plans** - leave the defaults for both options under this section.
    - Select the **Deployment** tab at the top of the page. Many times an organization will use GitHub for the repository for the files that make up the web app. This is a great option for continuous deployment scenarios. We are not adding any additional files at this time so we can leave the defaults on this page.
    - Select **Next" Networking** at the bottom of the page. Recall that in the IaaS lab, you had to configure a virtual network and then add your VM and other components to that virtual network. In the PaaS model, you don't need to worry about configuring a virtual network.  Instead, as you can see from this page, you simply ensure that **Enable public access** is turned on, to allow inbound traffic to the web server.
    - Select **Review + Create** and then select **Create** to begin the process of creating your web app.
    - After a few minutes, your web app should be deployed and you can select **Go to resource** to see the status.

### Task 2: Confirm successful deployment of the web app

In this task, you will confirm that our new web app was successfully deployed.

1. On the Overview page for your web app, locate the **URL** for the web site inn the upper right section.

![Screenshot depicting where the URL is located on the Overview page](../content/images/lab4/web-app-url.png)

2. Right-click the URL and select to open in a tab.

1. Your web app should display a static web page in the browser window

3. **Congratulations!** You have successfully created and deployed a static web app in Azure.

> __Note__
> While this lab may seem less compelling than the previous one, it's important to note a few things.
> - You have a working web application that is being hosted on Windows Server using the IIS role
> - You did not have to configure any infrastructure components such as networking
> - You did not have to create, deploy, and configure a virtual machine
> - You did not have to create a network security group or firewall rules
> - You did not have to add the Azure Bastion host for remote access.  
> - As a matter of fact, you do not have remote access to the VM that is running this service for you. You are simply responsible only for the code and web pages that make up your web app

## Summary

Congratulations! You just created a web app in Azure using the Platform as a Service (PaaS) model.

In this lab, you learned the foundations of creating, deploying, and verifying a simple web app using the Azure portal.

As discussed in the lectures, this is an example of utilizing a PaaS offering.

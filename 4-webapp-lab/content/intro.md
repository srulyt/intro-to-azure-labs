# Lab Overview

In the previous set of labs, you focused on a scenario where you wanted to be able to host a web application, or web site, on Azure. Using the IaaS model, you implemented the necessary infrastructure such as:

- creating a virtual network
- create and deploy a virtual machine
- setup secure remote access
- remotely access the VM and install the IIS role on the server to host the web files

While we didn't deploy a working web site, the intention was to familiarize you with the requirements for hosting a web app in the IaaS model.

In this lab, you will use the same scenario of wanting to host a web application on Azure, but you will do so using the PaaS model. By completing this lab, you will be able to compare and contrast the effort that is necessary to perform the same hosting scenario, using the different models. After completing the lab, you will have reinforced your knowledge and understanding of the responsibility matrix for areas of ownership for IaaS and PaaS.

![Image showing the VM icon from the Azure portal.](img/azure-web-app-icon.PNG)

## Learning Objectives

In this lab, you will learn the foundations of implementing a web app on Azure, using the platform as a service (PaaS) model.

You will:

- Provision a simple web app using the Azure portal

## Naming Conventions

Throughout the exercises, you will need to define names for different Azure Resources (e.g., Virtual Networks).

To guarantee the uniqueness of those resources please add the first 4 letters of your alias plus the last 2 numbers of your phone number. For example:

* The *special alias* for JohnDoe is John23
* When instructions say to enter __\<alias\>-rg__ you would enter **john23-rg**  

## Lab Execution Notes and Warnings

### Where To Do This Lab

This lab can be performed on your laptop/desktop. There are no code dependencies.

### Lab Dependencies

 - __Locally installed tools:__ None. 

 - __Previous lab dependencies:__ This lab depends on the _Resource Group_ and _virtual network_ you created in Lab 0 and Lab 2.

 - __Lab code:__ None. This lab does not use any lab code.

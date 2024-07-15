# Lab Overview

This lab continues the IaaS scenario by working through the process of creating a virtual machine, using the Azure portal. The VM will be used at some point to host a web site for a fictional company and you will need to remotely access the VM for administrative tasks. Remote access is typically accomplished by opening the remote desktop protocol (RDP) port. Exposing ports on public facing virtual machines, or other Azure resources for that matter, should be carefully considered. The open ports can become attack surfaces for hackers to gain entry into your Azure resources. Bastion host is the preferred method to expose a virtual machine across the internet, in a more secure manner. You already configured your virtual network to support Azure Bastion and when you add this VM to that virtual network, support for Azure Bastion will be available. 

![Image showing the VM icon from the Azure portal.](img/vm.PNG)

## Learning Objectives

In this lab, you will learn the foundations of creating virtual machines in Microsoft Azure.

You will:

- Provision a simple virtual machine
- Associate the VM with a virtual network

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

# AI CloudOps | AWS, Kubernetes & GitOps

An AI-powered application deployment project demonstrating modern DevOps practices using Docker, AWS, Kubernetes, and GitOps.

## Tech Stack

- **AI Integration:** OpenAI API
- **Application:** Python, Flask
- **Containerization:** Docker
- **Cloud Platform:** AWS
- **Container Registry:** Amazon ECR
- **Orchestration:** Amazon EKS, Kubernetes
- **GitOps:** Argo CD
- **Version Control:** Git, GitHub

## Overview

AI CloudOps focuses on deploying and managing an AI-powered application using AWS and modern DevOps practices.

The application is containerized using Docker, with images stored in Amazon ECR and deployment managed through Kubernetes manifests on Amazon EKS.

Argo CD is being integrated to introduce GitOps practices, using Git as the source of truth for Kubernetes configuration.

## DevOps Workflow

- Containerize the application using Docker.
- Store container images in Amazon ECR.
- Deploy the application to Amazon EKS using Kubernetes manifests.
- Manage application configuration using Kubernetes Secrets.
- Integrate Argo CD for GitOps-based deployment management.

Automated image building and publishing through GitHub Actions, along with automated image updates for GitOps deployments, have not yet been implemented.

## Project Goal

Demonstrate the deployment of an AI-powered application on AWS using Docker, Kubernetes, Amazon EKS, Amazon ECR, and Argo CD, with an emphasis on cloud infrastructure and GitOps-based deployment practices.
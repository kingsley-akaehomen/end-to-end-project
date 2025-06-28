# My Time Display App

[![Docker Build and Push](https://github.com/kingsley-akaehomen/end-to-end-project/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/kingsley-akaehomen/end-to-end-project/actions/workflows/build-and-push.yml)


This project contains a simple Python web application that displays current date as well as time and a CI pipeline to automatically build and publish a Docker image to Docker Hub.

## Features
-   Automated builds on push to `main`.
-   Smart tagging with `latest`, branch names, and version tags.
-   Container ochestration with Kubernetes.
-   And more!

## 📦 Helm Deployment (Recommended)
Helm is a package manager for Kubernetes. Helm does the exact same thing for Kubernetes applications. This  FastAPI project consists of multiple Kubernetes resources (Deployments, Services, Secrets, PVCs). Helm bundles all of these into a single, manageable package called a Chart. 

### 🔧 Understanding `deployment.yaml`
[When you run (helm create), Helm generates a default deployment.yaml under templates/. This file defines how the FastAPI app will   be   deployed to Kubernetes. Here’s a breakdown of key templating directives and how Helm uses them:

{{ include "chart.name" . }}
-  Useful for consistent naming across templates.
{{ .Values.replicaCount }}
-  Reads the number of pod replicas from values.yaml.
-  Used in the .spec.replicas field of the Deployment.
{{ .Values.image.repository }}
-  Sets the container image repo from values.yaml, e.g., "akaehomen321/time-api-app".
-  Often used alongside .Values.image.tag to pull the full image.
{{- if .Values.serviceAccount.create }}
-  Conditional logic: this block is only rendered if serviceAccount.create is true in values.yaml
serviceAccountName: {{ include "timeapi.serviceAccountName" . }}
securityContext:
  {{- toYaml .Values.podSecurityContext | nindent 8 }}
-  Injects service account (if enabled).
-  Sets pod-level security options, e.g., user ID, read-only root, etc.
{{- toYaml .Values.resources | nindent 8 }}
-  Converts resources from values.yaml into valid YAML.
-  nindent 8 indents it correctly to match the surrounding manifest structure.
{{- if not .Values.autoscaling.enabled }}
replicas: {{ .Values.replicaCount }}
{{- end }}
-  Only sets replica count if autoscaling is disabled.
-  .Values.replicaCount comes from values.yaml.

All {{ .Values.* }} items come from the values.yaml file. They can be passed during during install/upgrade time.
-  command: helm install my-app-release ./time-api-chart/ -n time-api-app
Helm will read your values.yaml, process all the templates, render them into final Kubernetes YAML, and apply them to your cluster in the correct namespace.]

### 🔄 Flow: Templates + Values = Final YAML
-  You define placeholders and logic in deployment.yaml.
-  Helm reads values.yaml (and any overrides)
-  Helm renders the final manifest by filling in values and applying logic.
-  The final YAML is applied to your Kubernetes cluster.
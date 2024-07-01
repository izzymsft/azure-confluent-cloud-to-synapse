### Deploying the Function App to Azure

## Create supporting Azure resources for your function

We need to login to Azure and then we need to set up the following resources
- A Resource Group
- A Storage Account
- A Function App
-
Navigate to the root directory and run these com

````bash
# Log into your Azure Account in the CLI
az login

# Take a look at what regions you have access to in your account
az account list-locations -o table

# Create a resource group named premiumfunctions -rg in your chosen region
az group create --name <RESOURCE_GROUP_NAME> --location <REGION>
az group create --name premiumfunctions --location eastus


# Create a General Purpose Storage Account in the same resource group and region
az storage account create --name <STORAGE_NAME> --location <REGION> --resource-group <RESOURCE_GROUP_NAME> --sku Standard_LRS

az storage account create --name premiumfunctionsdepot --location eastus --resource-group premiumfunctions --sku Standard_LRS

### Create a Premium Function Plan
az functionapp plan create --name izzypremium --resource-group premiumfunctions --location eastus --sku EP1

### List the Function Plans you have in this group
az functionapp plan list -g premiumfunctions -o json

### List the Current Function Apps (if Any)
az functionapp list -g premiumfunctions

### Tear Down any prior Function Apps (If Any)
az functionapp delete -g premiumfunctions -n contosopremiumapis

### Create a Function App with the Premium Plan
az functionapp create --name contosopremiumapis --storage-account premiumfunctionsdepot --plan izzypremium --resource-group premiumfunctions --os-type linux --runtime python --runtime-version 3.11 --functions-version 4

### List all the functions in the group
az functionapp list -g premiumfunctions
````

## Deploy the function project to Azure

````bash

# Use the following command to prepare your TypeScript project for deployment:

func azure functionapp publish contosopremiumapis

az functionapp config appsettings set -g premiumfunctions -n contosopremiumapis --settings FUNCTIONS_WORKER_RUNTIME=python @appsettings.json

````

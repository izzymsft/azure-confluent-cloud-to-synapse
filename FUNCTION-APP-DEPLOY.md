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

az storage account create --name premiumfunctionsdepot --location eastus --resource-group ConfluentPOC --sku Standard_LRS

# Delete if necessary
az functionapp plan delete -g ConfluentPOC -n izzypremium

### Create a Premium Function Plan
az functionapp plan create --name izzypremium --resource-group ConfluentPOC --location eastus --sku EP1 --is-linux 

### List the Function Plans you have in this group
az functionapp plan list -g ConfluentPOC -o json

### List the Current Function Apps (if Any)
az functionapp list -g ConfluentPOC

### Tear Down any prior Function Apps (If Any)
az functionapp delete -g ConfluentPOC -n contosopremiumapis

### Create a Function App with the Premium Plan
az functionapp create --name contosopremiumapis --storage-account premiumfunctionsdepot --plan izzypremium --resource-group ConfluentPOC --os-type linux --runtime python --runtime-version 3.11 --functions-version 4

### List all the functions in the group
az functionapp list -g ConfluentPOC
````

## Deploy the function project to Azure

````bash

# Use the following command to prepare your TypeScript project for deployment:

func azure functionapp publish contosopremiumapis

az functionapp config appsettings set -g ConfluentPOC -n contosopremiumapis --settings FUNCTIONS_WORKER_RUNTIME=python @appsettings.json

````

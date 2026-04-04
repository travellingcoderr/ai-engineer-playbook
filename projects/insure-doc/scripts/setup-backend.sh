#!/bin/bash

# InsureDoc: Terraform Backend Bootstrap Script (FIXED)
# This script creates the Resource Group, Storage Account, and Container 
# required to store your Terraform state remotely in Azure.

# --- CONFIGURATION (Shortened to stay under 24 chars) ---
RESOURCE_GROUP_NAME="rg-insuredoc-tfstate"
LOCATION="eastus"
# Prefix (6) + Timestamp (10) = 16 chars (Safe limit is 24)
STORAGE_ACCOUNT_NAME="stinsu$(date +%s)" 
CONTAINER_NAME="tfstate"

echo "Using Resource Group: $RESOURCE_GROUP_NAME"
echo "Using Storage Account: $STORAGE_ACCOUNT_NAME"

# 1. Create Resource Group
echo "Creating Resource Group..."
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# 2. Create Storage Account (Private/Secure)
# Added --min-tls-version TLS1_2 to remove retirement warnings
echo "Creating Storage Account..."
az storage account create \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $STORAGE_ACCOUNT_NAME \
    --sku Standard_LRS \
    --encryption-services blob \
    --min-tls-version TLS1_2

# 3. Create Blob Container
# Added --auth-mode login to use your active az login session
echo "Creating Blob Container..."
az storage container create \
    --name $CONTAINER_NAME \
    --account-name $STORAGE_ACCOUNT_NAME \
    --auth-mode login

# 4. Output Configuration for backend.tf
ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query '[0].value' -o tsv)

echo ""
echo "--- BOOTSTRAP COMPLETE ---"
echo "Add the following to your projects/insure-doc/terraform/backend.tf:"
echo ""
echo "terraform {"
echo "  backend \"azurerm\" {"
echo "    resource_group_name  = \"$RESOURCE_GROUP_NAME\""
echo "    storage_account_name = \"$STORAGE_ACCOUNT_NAME\""
echo "    container_name       = \"$CONTAINER_NAME\""
echo "    key                  = \"terraform.tfstate\""
echo "  }"
echo "}"
echo ""
echo "EXPORT THE KEY BEFORE RUNNING TERRAFORM INIT:"
echo "export ARM_ACCESS_KEY=$ACCOUNT_KEY"

# AWS EBS Volume Cleanup Project

This project aims to reduce costs by automating the deletion of unused Amazon Elastic Block Store (EBS) volumes in AWS.
It consists of two Python Lambda functions, orchestrated by an AWS Step Function, to manage the cleanup process efficiently.




![delete_unused_volumes_updates](https://github.com/amithub29/delete-unused-ebs-volumes/assets/84683865/384395a3-f044-4823-a12c-ccc890b4f39a)


## Features

#### Lambda Function 1:
* Retrieves details of all unattached EBS volumes in the AWS account.
* Generates a CSV file containing the volume details.
* Uploads the CSV file to a specified S3 bucket.
* Creates snapshots of all unattached EBS volumes for data backup.


#### Lambda Function 2:
* Deletes the unattached EBS volumes identified by Lambda Function 1.
* Ensures that no unnecessary volumes are left running, thereby reducing AWS costs.

#### AWS Step Function:
* Orchestrates the cleanup process by coordinating the execution of Lambda Function 1 and Lambda Function 2.
* Includes a wait state to allow time for EBS volume snapshots to be created before initiating the deletion process.


## Workflow

#### Lambda Function 1 Execution:
Lambda Function 1 is triggered to scan the AWS account for unattached EBS volumes.
It generates a CSV file containing the volume details and uploads it to the specified S3 bucket.
Simultaneously, snapshots of all unattached EBS volumes are created for backup purposes.

#### Wait State:
After the execution of Lambda Function 1, the Step Function enters a wait state for one hour to allow sufficient time for EBS volume snapshots to be created.

#### Lambda Function 2 Execution:
Upon completion of the wait period, Lambda Function 2 is triggered to delete the unattached EBS volumes identified by Lambda Function 1.
        This ensures that unnecessary volumes are removed, optimizing resource utilization and reducing costs.

## Objective

The primary objective of this project is to optimize AWS costs by automating the cleanup of unattached EBS volumes while preserving essential data. 
By regularly identifying and removing unused resources, organizations can efficiently manage their AWS infrastructure and minimize unnecessary expenses.
Additionally, the project ensures data safety by creating snapshots of volumes before deletion, enabling potential restoration if critical data is discovered.

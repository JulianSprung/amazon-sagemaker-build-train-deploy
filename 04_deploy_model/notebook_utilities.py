import boto3

def get_latest_training_job_name(base_job_name):
    client = boto3.client('sagemaker')
    response = client.list_training_jobs(NameContains=base_job_name, SortBy='CreationTime', 
                                         SortOrder='Descending', StatusEquals='Completed')
    if len(response['TrainingJobSummaries']) > 0 :
        return response['TrainingJobSummaries'][0]['TrainingJobName']
    else:
        raise Exception('Training job not found.')

def get_training_job_s3_model_artifacts(job_name):
    client = boto3.client('sagemaker')
    response = client.describe_training_job(TrainingJobName=job_name)
    s3_model_artifacts = response['ModelArtifacts']['S3ModelArtifacts']
    return s3_model_artifacts

def check_dependencies():

    import sagemaker
    
    import sys
    import os
    import IPython

    def versiontuple(v):
        return tuple(map(int, (v.split("."))))
    
    kernel_restart_required = False
    
    required_version = '2.90.0'
    if (versiontuple(sagemaker.__version__) < versiontuple(required_version)): 
        print('This workshop was tested with sagemaker version {} but you are using {}. Installing required version...'.format(required_version, sagemaker.__version__) )
        stream = os.popen('{} -m pip install -U sagemaker=={}'.format(sys.executable, required_version))
        output = stream.read()
        print(output)
        kernel_restart_required = True
    
    if kernel_restart_required:
        print("Restarting kernel after installing new dependencies...")
        IPython.Application.instance().kernel.do_shutdown(True)     
        print('WARNING: Kernel restarting...please wait 30 seconds before moving to the next cell!')
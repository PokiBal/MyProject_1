import time
import boto3
import subprocess
import os
from jenkinsapi.jenkins import Jenkins
import sqlite3
import requests
from jenkinsapi.custom_exceptions import JenkinsAPIException
import jenkins


ec2 = boto3.resource("ec2")
instance_type = "t2.micro"
key_pair_name = "jenkins-master"
image_id = "ami-0778521d914d23bc1"
security_group_id = "sg-0a9d87cae2328bea9"


class EC2InstanceCreator:
    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.public_ip = None
        self.instance = None
    
    def create_ec2_instance(self):
        try:
            self.instance = self.create_instance()
            self.tag_instance(self.instance, self.instance_name)
            self.wait_for_instance(self.instance)
            self.public_ip = self.instance.public_ip_address
            URL = f'http://{self.public_ip}:8080/'
            print("EC2 instance created with Public IP:", self.public_ip)
            
            if self.instance_name == "MyJenkinsMaster":
                self.configure_jenkins()
            
            return self.public_ip

        except Exception as e:
            print("Error occurred while creating EC2 instance:", str(e))
            return None

    def configure_jenkins(self):
        JENKINS_URL = f'http://{self.public_ip}:8080/'
        initial_password = self.get_initial_password()
        self.unlock_jenkins(initial_password)
        self.configure_jenkins_credentials(JENKINS_URL, initial_password)

    def get_initial_password(self):
        # Get the Jenkins container ID
        command = "docker ps -aqf 'name=My-Jenkins'"
        response = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        container_id = response.stdout.strip()

        # Get the initialAdminPassword from the container
        command = f"docker exec {container_id} cat /var/jenkins_home/secrets/initialAdminPassword"
        response = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        initial_password = response.stdout.strip()
        return initial_password

    def unlock_jenkins(self, initial_password):
        # Update the initialAdminPassword file in the container
        command = f"docker exec -u 0 My-Jenkins sh -c 'echo -n {initial_password} > /var/jenkins_home/secrets/initialAdminPassword'"
        subprocess.run(command, shell=True)
        print("Jenkins unlocked successfully.")

    def configure_jenkins_credentials(self, jenkins_url, initial_password):
        username = 'admin'
        new_username = JENKINS_USERNAME
        new_password = JENKINS_PASSWORD

        # Create a Jenkins instance
        server=JenkinsConnection(self.public_ip)
        #server = Jenkins(jenkins_url, username=username, password=initial_password)
        try:
            server.create_user(new_username, new_password)
            print("New Jenkins user created successfully.")
        except Exception as e:
            print("Failed to create new Jenkins user:", str(e))

    def create_instance(self):
        instances = ec2.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            KeyName=key_pair_name,
            SecurityGroupIds=[security_group_id],
            MinCount=1,
            MaxCount=1,
            UserData=self.jenkins_user_data()
        )
        return instances[0]

    def tag_instance(self, instance, instance_name):
        instance.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': instance_name
                }
            ]
        )

    def wait_for_instance(self, instance):
        instance.wait_until_running()
        instance.load()

    def jenkins_user_data(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        user_data_file_path = os.path.join(current_directory, 'jenkins_user_data.sh')

        with open(user_data_file_path, 'r') as file:
            user_data = file.read()

        return user_data


#-------------------------------Data Base-------------------------------


def get_image_data_from_DB():
    connection = sql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT image_name, id FROM images ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        image_name = result[0]
        image_id = result[1]
    else:
        # Default values if no records found in the database
        image_name = 'flask_docker'
        image_id = 0  # Replace with an appropriate default ID
    image_tag = f"1.0.{image_id}"
    # Close the database connection
    connection.close()
    return image_name, image_tag

#TODO: the DB path should be generic since it will run on ec2 instance
# connect to exist db named: registration
def sql_connection():
    connection = sqlite3.connect("C:/Users/Inbal-Laptop/Documents/myRepository/MyProject_1/instance/registrations.db")
    return connection


# instance_creator = EC2InstanceCreator("MyJenkinsMaster")
# public_ip_Jenkins_Server = instance_creator.create_ec2_instance()


##-----------------------------Jenkins------------------------------------------##
JENKINS_USERNAME = 'python-user'
JENKINS_PASSWORD = '1234!'
jenkins_URL = 'http://54.160.109.92:8080/'
prod1_URL= 'http://54.208.185.84:5000'
    
def JenkinsConnection():
    try:
        server = jenkins.Jenkins(jenkins_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        return server
    except Exception as e:
        print("Failed to connect Jenkins:", str(e))
        return str(e)



# Creating new job(pipeline/freestyle) in jenkins, assuming I have the public ip of ec2 that just created
def CreateJob(job_xml):
    server = JenkinsConnection()
    with open(job_xml, 'r') as file:
        config = file.read()
    if job_xml == 'pipeline_config':
        server.create_job('Build-test-flaskApp-pipeline', config)
    elif job_xml == 'job_config':  
        server.create_job('Deploy-flask-production', config)

#creating new jon from infra_flask application
def CreateJobFromFlask(job_name):
    result = "test"
    server = JenkinsConnection()

    try:
        with open('C:\\Users\\Inbal-Laptop\\Documents\\myRepository\\MyProject_1\\my_infrastructure\\general_job_config.xml', 'r') as file:
            config = file.read()
        server.create_job(job_name, config)
        print(f"Job '{job_name}' created successfully.")
        result = f"New job {job_name} created"
    except JenkinsAPIException as e:
        print("Failed to connect to Jenkins:", str(e))
        return str(e)
    except Exception as e:
        result = "An error occured while creating the job"
        print(f"An error occured while creating the job",e)
        return result
    return result


#this will run any job according to the name recived, and check for specific the ppipeline jobs that needs parameter for building the image    
# def run_job(job_name):
#     server = JenkinsConnection()
#     print(server)
#     if job_name == 'build and test pipeline':
#         image_name, image_tag = get_image_data_from_DB()
#         print({image_name},{image_tag})
#         try:
#             parameters = {'imagename':image_name, 'imagetag':image_tag}
#             server.build_job(job_name,parameters)
#             time.sleep(10)
#         except Exception as e:
#             print(e)
#         # server.build_job(job_name, parameters={'imageName': image_name, 'imageTag': image_tag})
#     else:
#         server.build_job(job_name)
#     time.sleep(5)
#     result =server.get_build_info(job_name,nextBuildNumber)

#     return False
from jenkinsapi.jenkins import Jenkins

def run_job(job_name):
    server = JenkinsConnection()
    print(server)
    resultMessage = "test"
    if job_name == 'build and test pipeline':
        image_name, image_tag = get_image_data_from_DB()
        print({image_name},{image_tag})
        try:
            parameters = {'imagename':image_name, 'imagetag':image_tag}
            server.build_job(job_name,parameters)
            last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
            build_info = server.get_build_info(job_name, last_build_number)
            time.sleep(20)  # Wait for the build to complete
            if 'result' in build_info:
                result = build_info['result']
                if result == "SUCCESS":
                    resultMessage = f"Build succeeded and uploaded to DockerHub, please use production env here:{prod1_URL}"
                elif result == 'FAILURE':
                    resultMessage = "Pipeline Build failed! please check logs"
                else:
                    print("Build result: ", result)
        except Exception as e:
            print(e)
    else:
        server.build_job(job_name)
        time.sleep(5)
        last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
        print("    last_build_number:",last_build_number)
        build_info = server.get_build_info(job_name, last_build_number)
        print("    build_info:",build_info)
        if 'result' in build_info:
            result = build_info['result']
            print("    build result:", result)
            if result == "SUCCESS":
                print("Build succeeded!")
                resultMessage = "Build succeeded!!"
        elif result == 'FAILURE':
            resultMessage = "Last completed build failed!"
            print(resultMessage)
        else:
            print("Last completed build result: ", result)
    
    return resultMessage




# creating a new user in jenkins
# def create_new_jenkins_user(user_name, password):
#     result="testUser"
#     new_username = user_name
#     new_password = password
#     fullname= "Inbal Rozenfeld"
#     email="inbalamr@gmail.com"
#     try:
#         server = jenkins_connection()
#         # if server is not None:
#         server.create_user(new_username, password, fullname, email)
#         # server.create_user(new_username, new_password)
#         result = "New Jenkins user created successfully."
#         print("New Jenkins user created successfully.")
#     except Exception as e:
#         print(f"Failed to create new Jenkins user:", e)
#         result = "An error occured while creating the User"
#         return result
#     return result

def new_jenkins_user(username, password):
    
    server = JenkinsConnection()
    if not server:
        return "Failed to connect to Jenkins."

    api_url = f"{jenkins_URL}/createUser"
    result = "testUser"
    fullname = "Inbal Rozenfeld"
    email = "inbalamr@gmail.com"
    data = {
        'username': username,
        'password1': password,
        'password2': password,
        'fullname': fullname,
        'email': email
    }

    try:
        response = requests.post(api_url, data=data)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        result = "New Jenkins user created successfully."
        print("New Jenkins user created successfully.")
    except requests.exceptions.RequestException as e:
        result = f"An error occurred while creating the user: {str(e)}"
        print(result)

    return result
## ----------------------------Image--------------------------------##





# def test_credentials(jenkins_url, username, password):
#     try:
#         server = Jenkins(jenkins_url, username=username, password=password)
#         if server.is_jenkins_alive():
#             print("Credentials are valid. Jenkins server is reachable.")
#             return True
#         else:
#             print("Credentials are valid, but Jenkins server is not reachable.")
#     except Exception as e:
#         print("Failed to authenticate with the provided credentials:", str(e))
    
#     return False

def upload_to_docker_hub():
    print("upload to docker hub")
    return


# # create iam user with AdmindevOps permissions
# #TODO: add try - catch exception if the user already exist
def create_iam_user(user_name,password):
    iam = boto3.client("iam")
    # user_name = "iam-project"
    try:
        response = iam.create_user(UserName=user_name)
        response = iam.create_login_profile(
            UserName = user_name,
            Password = password,
            PasswordResetRequired = True
        )
        response = iam.create_access_key(
            UserName = user_name
        )

        response = iam.add_user_to_group(
            GroupName = "AdminDevOps",
            UserName = user_name
        )
        result = f"IAM user {user_name} was created"
        return result
    except Exception as e:
        print("An error occured while trying to create IAM user",e)
        return e


# def GetInitialPassword():
#     docker_exec_command = f"docker exec jenkins-master cat /var/jenkins_home/secrets/initialAdminPassword"
#     response = subprocess.run(['aws', 'ec2', 'invoke-shell-command', '--instance-id', instance.id, '--document-name', 'AWS-RunShellScript', '--parameters', f"commands=['{docker_exec_command}']", '--query', 'Commands[0].CommandResponses[0]'], capture_output=True, text=True)
#     initial_password = response.stdout.strip()
#     print("Initial password:",initial_password)
#     return initial_password


# def run_app():
#     flag = True
#     pipeline_flag = run_job("build and test pipeline") #the pipeline will do: pull, build image, run container, test, save results
#     # upload_results_to_S3() # boto3 or pipeline?
#     # upload_S3_to_dynamoDB() # use boto3
#     # if pipeline_flag: #if the pipeline pass - continue to next job, and upload to dockerHub
#     #     upload_to_docker_hub()
#         # Public_Ip_Prod1 = create_ec2_instance("Prod_1")
#         # Public_Ip_Prod2 = create_ec2_instance("Prode_2")
#         # if run_job(Public_Ip_Prod1,"job_config"):
#         #      result =  f'Application is on prodection, you may check it in this ip: {Public_Ip_Prod1}:8085'
#         # else:
#         #      result =  "somthing went wrong in the production job, please check..."
#     # else:
#     #     result = "The pipeline finished with failure - please check the logs for furture information..."
    
#     flag = False 
#     return flag, result



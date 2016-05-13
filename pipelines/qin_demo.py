"""
Execute the following steps before you attempt to run this pipeline

make grunt 
make demo
make ants
make machinelearn
you might need to use sudo (this is attributed to the way docker is designed)

To run the docker webapps use
sudo docker run -d -p 9917:9901 pesscara/machinelearn
sudo docker run -d -p 9916:9901 pesscara/ants

For instance the ports for the webapps offered by pesscara/ants are accessible at port 9916 of you local service 

If you have added custom docker based webapps please initialize. 

This file is depended on the request python library (http://docs.python-requests.org/en/master/user/install/#install). Please see requirements.txt

Example of a curl command 

curl -v -X POST --form clusternumber=6 --form imageA=@T1c.nii.gz --form imageB=@1.nii.gz --form output=cluster.nii.gz ril-gpu10:9913/rest/service/kmeansseg

curl -v -X POST --form fixed=@T1c.nii.gz --form registered=1.nii.gz ril-gpu10:9919/rest/service/n4


"""
from _grunt import *

g = grunt("http://192.168.99.100:9918")
# Syntax 1
j=g.n4
j.fixed="/Users/m112447/Documents/TestData/T2.nii.gz"
j.registered="T2N4.nii.gz"
job =j()
job.wait()
# Write some output
job.save_output("registered", "/Users/m112447/Downloads/")


# Syntax 2

j = g.n4(fixed="/Users/m112447/Documents/TestData/T1c.nii.gz",registered="T1cN4.nii.gz")
print dir(j)
j.wait()
j.save_output("registered", "/Users/m112447/Downloads/")
# # # Register T1 and T2
# But the code 
# Create an affine registration proxy for the grunt service
affine = g.affine
# Set parameters
affine.moving="/Users/m112447/Downloads/T2N4.nii.gz"
affine.fixed="/Users/m112447/Downloads/T1cN4.nii.gz"
affine.registered="T2reg.nii.gz"
# Don't need this
# affine = g.affine()
# Call the method
job = affine()
job.wait()
# Write some output
job.save_output("registered", "/Users/m112447/Downloads/")
# # Kmeans
g = grunt("http://192.168.99.100:9919")
print dir(g.services.get('kmeansseg'))
Info=g.services.get('kmeansseg')
print Info.inputs()
print Info.outputs()
print Info.parameters()
j = g.kmeansseg(imageA="/Users/m112447/Downloads/T1cN4.nii.gz",imageB='/Users/m112447/Downloads/T1cN4.nii.gz',clusternumber=6,output="Cluster.nii.gz")
print dir(j)
j.wait()
j.save_output("output", "/Users/m112447/Downloads/")

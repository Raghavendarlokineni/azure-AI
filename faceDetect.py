"""
Face detection/comparison with azure cognitive face services
"""

import glob

# To install this module, run:
# python -m pip install Pillow
#from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
#from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# Azure face Cognitive Service key
KEY = "abcdef"

# Azure face Cognitive Service endpoint
ENDPOINT = "end-point"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

Decorator = """
           *******************************************************\n
           """
images_list = [file for file in glob.glob('**/*.jpg', recursive=True)]
#print(images_list)

referenceImage = "/app/faceImages/ishaan.jpg"
#image2 = "/app/faceImages/ishaan2.jpg"

detectReferenceFace = face_client.face.detect_with_stream(open(referenceImage, 'rb'))
referenceFaceID     = [face.face_id for face in detectReferenceFace]

for image in images_list:
    print(Decorator)
    print("opening image", image)
    #first_image  = open(image1, 'rb')
    #second_image = open(image2, 'rb')
    read_image = open(image, "rb")

    #faces_first  = face_client.face.detect_with_stream(first_image)
    #second_photo = face_client.face.detect_with_stream(second_image)

    print("detecting faces in the image", image)
    detect_face = face_client.face.detect_with_stream(read_image)

    print("listing detected face IDs")
    for face in detect_face:
        print(face.face_id)
    
    print("\nsearching for similar faces")
    similar_faces = face_client.face.find_similar(face_id= referenceFaceID[0], face_ids = list(map(lambda x: x.face_id, detect_face))) 
    #print(list(map(lambda x: x.face_id, second_photo)))

    if not similar_faces:
        print("no similar faces found")
    else:
        print("found similar faces in {0} and {1}".format(referenceImage, image))

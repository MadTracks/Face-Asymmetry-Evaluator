from imutils import face_utils
import dlib
import cv2
import json
import math
import numpy as np
import open3d as o3d
import copy

def read_json(image_name,x1,y1):
    # Opening JSON file
    f = open('../sfm/results/reconstruction_sequential/sfm2_data.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    for c1 in data['views']:
        if c1['value']['ptr_wrapper']['data']['filename'] == image_name:
            filejpeg = c1['key']

    closest_distance = 999999

    # Iterating through the json
    # list
    for i in data['structure']:
        for j in i['value']['observations']:
            if j['key'] == filejpeg:
                dist = math.sqrt(((j['value']['x'][0]-x1)*(j['value']['x'][0]-x1))+((j['value']['x'][1]-y1)*(j['value']['x'][1]-y1)))
                if dist < closest_distance:
                    closest_distance = dist
                    closest_3dpoint = i['value']['X']
                #print(j['value']['x'])#pixel of point in image
                #print(i['value']['X'])#xyz coordinates of point
    
    #print(data['structure'][0]['value']['X'])#xyz coordinates
    #print(data['structure'][0]['value']['observations'][1]['key'])#image number of point
    #print(data['structure'][0]['value']['observations'][1]['value']['x'])#pixel of point in image
    # Closing file
    f.close()
    print(closest_distance)
    print(closest_3dpoint)
    return closest_3dpoint
 
def affine_transformation_matrix_calculator(p1,p2,p3,p4):
    fixed_nose =[0, -13.3595,3.0624]
    fixed_lefteye=[-8.27412,-10.6349,1.33849]
    fixed_righteye=[8.27412,-10.6349,1.33849]
    fixed_chin=[0, -13.7732, -16.8611]
    ins = [p1, p2, p3, p4]  # <- points
    out = [fixed_nose, fixed_lefteye, fixed_righteye, fixed_chin] # <- mapped to
    # calculations
    l = len(ins)
    B = np.vstack([np.transpose(ins), np.ones(l)])
    D = 1.0 / np.linalg.det(B)
    entry = lambda r,d: np.linalg.det(np.delete(np.vstack([r, B]), (d+1), axis=0))
    M = [[(-1)**i * D * entry(R, i) for i in range(l)] for R in np.transpose(out)]
    A, t = np.hsplit(np.array(M), [l-1])
    t = np.transpose(t)[0]
    # output
    print("Affine transformation matrix:\n", A)
    print("Affine transformation translation vector:\n", t)
    # unittests
    print("TESTING:")
    for p, P in zip(np.array(ins), np.array(out)):
        image_p = np.dot(A, p) + t
        result = "[OK]" if np.allclose(image_p, P) else "[ERROR]"
        print(p, " mapped to: ", image_p, " ; expected: ", P, result)
    T= np.empty((4, 4))
    T[:3,:3]= A
    T[3,:] = [0,0,0,1]
    return T

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    #source_temp.paint_uniform_color([1, 0.706, 0])
    #target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4459,
                                      front=[0.9288, -0.2951, -0.2242],
                                      lookat=[1.6784, 2.0612, 1.4451],
                                      up=[-0.3402, -0.9189, -0.1996])
    return source_temp

# Vamos inicializar um detector de faces (HOG) para então
# let's go code an faces detector(HOG) and after detect the 
# landmarks on this detected face

# p = our pre-treined model directory, on my case, it's on the same script's diretory.
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

#cap = cv2.VideoCapture(0)
image_location = "images/8.jpg"
 
while True:
    # Getting out image by webcam 
    #_, image = cap.read()
    image = cv2.imread(image_location)
    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Get faces into webcam's image
    rects = detector(gray, 0)
    
    # For each detected face, find the landmark.
    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
    
        # Draw on our image, all the finded cordinate points (x,y) 
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        #cv2.circle(image,(shape[27][0],shape[27][1]),2, (0, 0, 255), -1)
        #cv2.circle(image,(shape[8][0],shape[8][1]),2, (0, 0, 255), -1)
    
    # Show the image
    cv2.imshow("Output", image)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
print(shape)

point_nose = read_json('8.jpg',shape[27][0],shape[27][1])
point_lefteye = read_json('8.jpg',shape[36][0],shape[36][1])
point_righteye = read_json('8.jpg',shape[45][0],shape[45][1])
point_chin = read_json('8.jpg',shape[8][0],shape[8][1])

source = o3d.io.read_point_cloud('../sfm/results/reconstruction_sequential/colorized.ply')
target = o3d.io.read_point_cloud('male.ply')
transform_matrix = affine_transformation_matrix_calculator(point_nose,point_lefteye,point_righteye,point_chin)
threshold = 200
current_source = draw_registration_result(source, target, transform_matrix)
p = np.empty(4)
p[:3] = point_nose
p[3] = 0
new_point_nose = np.matmul(transform_matrix,p)
p[:3] = point_lefteye
new_point_lefteye = np.matmul(transform_matrix,p)
p[:3] = point_righteye
new_point_righteye = np.matmul(transform_matrix,p)
p[:3] = point_chin
new_point_chin = np.matmul(transform_matrix,p)
print(new_point_nose)
print(new_point_lefteye)
print(new_point_righteye)
print(new_point_chin)

current_source.translate((-8.27412,-10.6349,1.33849), relative = False)
o3d.visualization.draw_geometries([current_source, target])

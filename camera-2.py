import cv2  as cv
#from cv2 import cuda
import numpy as np 
import os
import time
#from tracker import *
#import sys
import math
#print(cuda.printCudaDeviceInfo(0))
class Application():
    def __init__(self):
        super().__init__()
        fun = []
        confThreshold = 0.5  
        nmsThreshold = 0.3   
        inpWidth = 608
        inpHeight = 608  
        
        cood = [[0,200],[1280,200],[0,500],[1280,500]]
        #tracker = EuclideanDistTracker()
        classesFile = "classes_cars.names";
        classes = None

        with open(classesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
        

        modelConfiguration = "yolov3_carsv2.cfg";
        modelWeights = "finalcar.weights";
        
        net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        self.counter = 0

        cap = cv.VideoCapture('car6.mp4')
        

        self.num = 0
        def getOutputsNames(net):
            layersNames = net.getLayerNames()
            return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]   

        def drawPred(classId, conf,width,height, left, top, right, bottom,box):
        
            
            roi_face = demo[top:top+height,left:left+width]
            
        
            if classes:
                assert(classId < len(classes))
                class_name = classes[classId]
            #for circle radius
            #center of circle
            
            
            
                

            
            
            #dom  = tracker.append([left,top,width,height])   
            #
            #print(dom)    
            
            
                
                
            #print(boxes_ids)
            
            cx =0 
            cy = 0
                    
            c1 = (left + 1920)/2
            c2 = (top + 1080)/2
                    #cv.circle(demo,(int(c1),int(c2)),35,(255,0,0),3)
            cv.rectangle(demo, (left, top+10), (right, bottom), (255, 120, 50,0), 5)
                    #image_new = cv.addWeighted(demo,0.4,demo,1-0.4,0)
                #cv.rectangle(demo,(left,top),(right,top),(255,0,100,0),55)
            #cv.putText(demo,str(class_name),(left,top+2),cv.FONT_HERSHEY_SIMPLEX,2,(255,150,0),5,cv.LINE_AA)
           
            if (left >=cood[0][0] and top >= cood[0][1]):
                cv.line(frame, (cood[0][0], cood[0][1]), (cood[1][0], cood[1][1]), (255,122,111), 2)                 
                print("entered")
                time1 = time.time()
            if (left >=cood[2][0] and top >= cood[2][1]):
                cv.line(frame, (cood[2][0], cood[2][1]), (cood[3][0], cood[3][1]), (255,122,111), 2)                 
                print("exit")
                time2 = time.time()
                total_time = ((time2 - time1))/10
                
                if total_time > 0.0:
                    speed = 3/total_time
                    
                    speed1 = speed/500
                    print(speed1)
                    
                    if speed1 > 60:
                        with open("overspeed.txt","a") as f:
                            f.write(str(self.counter) +"-"+str(speed1))
                            f.write("\n")
                    #print(self.counter)
                            
                            cv.imwrite("car_exceed"+str(self.num)+".jpg",roi_face)
                            self.num +=1
                            self.counter +=1
                
                
                
                    
            
                
        def postprocess(demo, outs):
            frameHeight = demo.shape[0]
            
            frameWidth = demo.shape[1]
        
            classIds = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    classId = np.argmax(scores)
                    confidence = scores[classId]
                    if confidence > confThreshold:
                        center_x = int(detection[0] * frameWidth)
                        center_y = int(detection[1] * frameHeight)
                        width = int(detection[2] * frameWidth)
                        height = int(detection[3] * frameHeight)
                        left = int(center_x - width / 2)
                        top = int(center_y - height / 2)
                        classIds.append(classId)
                        confidences.append(float(confidence))
                        boxes.append([left, top, width, height,])
            
                        #fun.append([left,height,width,height])
                        #boxes_ids = tracker.update()
                        #boxes_id = tracker.update(fun)
                        
                    # for box_id in boxes_id:
                            #x,y,w,h,id = box_id
                            #cv.putText(demo,str(id),(10,50),cv.FONT_HERSHEY_PLAIN,10,(255,0,0),2)
                            #cv.rectangle(demo,(left,top),(left+width, top+height),(255,0,100,0),55)

        
            indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
            '''k = 0
            
            dom = len(boxes)
            for l in boxes:
                if len(boxes) > k:
                    k = len(boxes)
                    fun.append(k)
            print("length:")
            print(fun)
            res = [*set(fun)]
            print(len(res))'''
            #for i in :
                #if i >k:
                    #print(i)
                    #k =i
            for i in indices:
                #print(i)
                #time.sleep(1)
                
                #if i >k:
                    #print(i)
                    #k = i
                
                box = boxes[i]
                left = box[0]
                top = box[1]
                width = box[2]
                height = box[3]
                drawPred(classIds[i], confidences[i],width,height, left, top, left + width, top + height,box)        

        
        count = 0 
        while cv.waitKey(1) < ord('q'):
            net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)   
            hasFrame, frame = cap.read()
            print(hasFrame)
            #cv.rectangle(demo,(10,10),(100,200),(0,200,0),-1)
            
            overlay = frame.copy()
            demo = cv.resize(frame,(1280,720),interpolation = cv.INTER_AREA)   
            
            #fps = cap.get(cv.CAP_PROP_FPS)
            #print(str(fps))
            
            
            

            #semi = cv.addWeighted(demo,0.4,demo=,1-0.4,0)
        
            blob = cv.dnn.blobFromImage(demo, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
        
            net.setInput(blob)
        
            outs = net.forward(getOutputsNames(net))
        
            postprocess(demo, outs)

            #cv.line(demo,(0,300),(1280,300),(255,0,0),5,cv.LINE_AA)
            #cv.line(demo,(0,700),(1280,700),(255,0,0),5,cv.LINE_AA)
            cv.line(demo,(cood[0][0],cood[0][1]),(1280,200),(255,0,0),5,cv.LINE_AA)
            cv.line(demo,(cood[2][0],cood[2][1]),(1280,500),(255,0,0),5,cv.LINE_AA)

            
            
            cv.imshow('demo',demo)

def  main():
    app = Application()
    return app

if __name__=="__main__":
    main()    
    

        
     


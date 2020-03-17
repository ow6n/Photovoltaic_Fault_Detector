#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:55:42 2020

@author: dlsaavedra
"""
import numpy as np

def disconnect(image, boxes, obj_thresh = 0.5, area_min = 400, merge = 0):
    
    new_boxes = []
    for num, box in enumerate(boxes):
       
        xmin = box.xmin + merge
        xmax = box.xmax - merge
        ymin = box.ymin + merge
        ymax = box.ymax - merge
        
        if xmin > 0 and ymin > 0 and xmax < image.shape[1] and ymax < image.shape[0] and box.classes[0] > obj_thresh:
            
            area = (ymax - ymin)*(xmax - xmin)
            z_score = np.sum(image[np.int(ymin):np.int(ymax), np.int(xmin):np.int(xmax)]) / area
            
            if area > area_min:
                
                box.score = z_score
                new_boxes.append(box)
                #boxes_area_score[str(num)] = {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax, 'score' : score, 'area' : area}
       
    mean_score = np.mean([box.score for box in new_boxes])
    sd_score  = np.std([box.score for box in new_boxes])
    
    new_boxes = [box for box in new_boxes if (box.score - mean_score)/sd_score > 2]
    
    for box in new_boxes:
        
        z_score = (box.score - mean_score)/sd_score
        box.classes[0] = min((z_score-2)*0.5+ 0.5, 1)
        
    return new_boxes
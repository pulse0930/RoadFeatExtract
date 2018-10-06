# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:28:17 2018

@author: Pallav
"""
import math
import numpy as np
roll = 0.0
pitch = 0.0

def find_pitch_angle(x,y,z):
    '''Calculate pitch angle '''
    sqrt_sum_sqr = math.sqrt(y*y + z*z)
    return (math.atan2(-x ,sqrt_sum_sqr))

def find_roll_angle(y,z):
    '''Calculate roll angle '''
    return (math.atan2(y ,z))

'''Reorientation of x y and z'''
def reorient_x(roll,pitch,x,y,z):
    cos_pitch = math.cos(pitch)
    cos_roll = math.cos(roll)
    sin_pitch = math.sin(pitch)
    sin_roll = math.sin(roll)
    return cos_pitch * x + sin_pitch * sin_roll * y + cos_roll * sin_pitch * z

def reorient_y(roll,y,z):
    cos_roll = math.cos(roll)
    sin_roll = math.sin(roll)
    return cos_roll * y - sin_roll * z

def reorient_z(roll,pitch,x,y,z):
    cos_pitch = math.cos(pitch)
    cos_roll = math.cos(roll)
    sin_pitch = math.sin(pitch)
    sin_roll = math.sin(roll)
    return  - (sin_pitch * x) + (cos_pitch * sin_roll * y) + (cos_pitch * cos_roll * z)


gravity = [0.0,0.0,0.0]
alpha = 0.8
def gravity_filter(x,y,z):
    '''Low pass and high pass filters to remove gravity from x,y and z'''
    gravity[0] = alpha * gravity[0] + (1-alpha) * x
    gravity[1] = alpha * gravity[1] + (1-alpha) * y
    gravity[2] = alpha * gravity[2] + (1-alpha) * z
    x = x - gravity[0]
    y = y - gravity[1]
    z = z - gravity[2]
    return x,y,z

def accelerometer_correction(x,y,z):
    '''
    correcting accelerometer readings
    '''
    roll = find_roll_angle(y,z)
    pitch = find_pitch_angle(x,y,z)
    x,y,z = gravity_filter(x,y,z)
    r_x = reorient_x(roll,pitch,x,y,z)
    r_y = reorient_y(roll,y,z)
    r_z = reorient_z(roll,pitch,x,y,z)
    return r_x,r_y,r_z,x,y,z

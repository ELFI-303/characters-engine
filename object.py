from math import sin,cos,tan,sqrt,pi,atan,acos,asin
import numpy as np

class Camera:
    def __init__(self):
        self.position = (0,0,0)
        self.angle = (0,0)
        self.fov = 90
        self.aspect = (16,9)
        self.distance = 100

    def GetCam(self):
        fov = DegRad(self.fov)
        aspect_ratio = self.aspect
        ratio=aspect_ratio[0]/aspect_ratio[1]
        h_fov=(aspect_ratio[0]/ratio)*fov
        v_fov=(aspect_ratio[1]/ratio)*fov
        h_fov = DegRad(h_fov)
        v_fov = DegRad(v_fov)
        a = tan(v_fov/2)
        b = tan(h_fov/2)

        phi,teta = self.angle
        phi = DegRad(phi)
        teta = DegRad(teta+90)
        position = self.position
        center = (position[0]+sin(teta)*cos(phi),position[1]+cos(teta),position[2]+sin(teta)*sin(phi))
        top_right = (center[0]-a*cos(teta)-b*sin(phi),center[1]+a*sin(teta),center[2]+b*cos(phi))
        top_left = (center[0]-a*cos(teta)+b*sin(phi),center[1]+a*sin(teta),center[2]-b*cos(phi))
        bottom_right = (center[0]+a*cos(teta)-b*sin(phi),center[1]-a*sin(teta),center[2]+b*cos(phi))
        bottom_left = (center[0]+a*cos(teta)+b*sin(phi),center[1]-a*sin(teta),center[2]-b*cos(phi))

        return [top_right,top_left,bottom_right,bottom_left]
    
    def GetPlan(self,dist=0):
        plan = self.GetCam()
        if dist == 0:
            distance = self.distance
        else:
            distance = dist
        fov = DegRad(self.fov)
        aspect_ratio = self.aspect
        ratio=aspect_ratio[0]/aspect_ratio[1]
        h_fov=(aspect_ratio[0]/ratio)*fov
        v_fov=(aspect_ratio[1]/ratio)*fov
        h_fov = DegRad(h_fov)
        v_fov = DegRad(v_fov)
        a = tan(v_fov/2)*distance
        b = tan(h_fov/2)*distance

        phi,teta = self.angle
        phi = DegRad(phi)
        teta = DegRad(teta+90)
        position = self.position
        center = (position[0]+distance*sin(teta)*cos(phi),position[1]+distance*cos(teta),position[2]+distance*sin(teta)*sin(phi))
        top_right = (center[0]-a*cos(teta)-b*sin(phi),center[1]+a*sin(teta),center[2]+b*cos(phi))
        top_left = (center[0]-a*cos(teta)+b*sin(phi),center[1]+a*sin(teta),center[2]-b*cos(phi))
        bottom_right = (center[0]+a*cos(teta)-b*sin(phi),center[1]-a*sin(teta),center[2]+b*cos(phi))
        bottom_left = (center[0]+a*cos(teta)+b*sin(phi),center[1]-a*sin(teta),center[2]-b*cos(phi))

        farPlan = [top_right,top_left,bottom_right,bottom_left]

        return plan,farPlan
    
    def TriangleInView(self,triangle):
        result = False
        arr = []
        for point in triangle:
            x,y,z = point[0]-self.position[0],point[1]-self.position[1],point[2]-self.position[2]
            hypoXZ = sqrt(x**2+z**2)
            r = NormVect((x,y,z))
            phi = asin(z/hypoXZ)
            teta = acos(y/r)
            arr.append([phi,teta])
            fov = DegRad(self.fov)
            aspect_ratio = self.aspect
            ratio=aspect_ratio[0]/aspect_ratio[1]
            h_fov=(aspect_ratio[0]/ratio)*fov
            v_fov=(aspect_ratio[1]/ratio)*fov
            h_fov = DegRad(h_fov)/2
            v_fov = DegRad(v_fov)/2
            
            cphi,cteta = self.angle
            cphi = DegRad(cphi)
            cteta = DegRad(cteta+90)
            if 1 <= r and r <= self.distance+1:
                if cphi-h_fov <= phi and phi <= cphi+h_fov:
                    if cteta-v_fov <= teta and teta <= cteta+h_fov:
                        result = True
        return result,arr
    
    def ElementInView(self,element):
        viewElement = []
        for triangle in element:
            viewedTriangle = self.TriangleInView(triangle)
            if viewedTriangle[0] == True:
                viewElement.append([min([NormVect((point[0]-self.position[0],point[1]-self.position[1],point[2]-self.position[2])) for point in triangle]),viewedTriangle[1]])
        viewElement.sort(key=lambda x: x[0])
        screen = []
        for viewTriangle in viewElement:
            screen.append([[atan(point[0]), atan(point[1]-pi/2)] for point in viewTriangle[1]])
        return screen
            
                    



        

class Sphere:
    def __init__(self):
        self.position = (0,0,0)
        self.rayon = 5
    def GetMat(self,precision=1000):
        i,j = 0,0
        sphere_precision = (precision/1000)*self.rayon
        dphi = sphere_precision
        dteta = sphere_precision/2
        sphere_mat = []
        pphi,pteta = DegRad(dphi/2),DegRad(dteta/2)
        for phi in np.arange(0,360,dphi):
            for teta in np.arange(0,180+dteta,dteta):
                r_phi,r_teta = DegRad(phi),DegRad(teta)
                if r_teta + pteta >= pi:
                    r_teta = DegRad(180)

                    a = (self.position[0]+self.rayon*sin(r_teta-pteta)*cos(r_phi+pphi),self.position[1]+self.rayon*cos(r_teta-pteta),self.position[2]+self.rayon*sin(r_teta-pteta)*sin(r_phi+pphi))
                    b = (self.position[0]+self.rayon*sin(r_teta-pteta)*cos(r_phi-pphi),self.position[1]+self.rayon*cos(r_teta-pteta),self.position[2]+self.rayon*sin(r_teta-pteta)*sin(r_phi-pphi))
                    c = (self.position[0],self.position[1]+self.rayon*cos(r_teta),self.position[2])

                    sphere_mat.append([a,b,c])

                elif r_teta - pteta <= 0:
                    r_teta = 0

                    a = (self.position[0],self.position[1]+self.rayon*cos(r_teta),self.position[2])
                    b = (self.position[0]+self.rayon*sin(r_teta+pteta)*cos(r_phi+pphi),self.position[1]+self.rayon*cos(r_teta+pteta),self.position[2]+self.rayon*sin(r_teta+pteta)*sin(r_phi+pphi))
                    c = (self.position[0]+self.rayon*sin(r_teta+pteta)*cos(r_phi-pphi),self.position[1]+self.rayon*cos(r_teta+pteta),self.position[2]+self.rayon*sin(r_teta+pteta)*sin(r_phi-pphi))

                    sphere_mat.append([a,b,c])
                else:
                    a = (self.position[0]+self.rayon*sin(r_teta-pteta)*cos(r_phi+pphi),self.position[1]+self.rayon*cos(r_teta-pteta),self.position[2]+self.rayon*sin(r_teta-pteta)*sin(r_phi+pphi))
                    b = (self.position[0]+self.rayon*sin(r_teta-pteta)*cos(r_phi-pphi),self.position[1]+self.rayon*cos(r_teta-pteta),self.position[2]+self.rayon*sin(r_teta-pteta)*sin(r_phi-pphi))
                    c = (self.position[0]+self.rayon*sin(r_teta+pteta)*cos(r_phi+pphi),self.position[1]+self.rayon*cos(r_teta+pteta),self.position[2]+self.rayon*sin(r_teta+pteta)*sin(r_phi+pphi))
                    d = (self.position[0]+self.rayon*sin(r_teta+pteta)*cos(r_phi-pphi),self.position[1]+self.rayon*cos(r_teta+pteta),self.position[2]+self.rayon*sin(r_teta+pteta)*sin(r_phi-pphi))

                    sphere_mat.append([a,b,c])
                    sphere_mat.append([c,b,d])
        return sphere_mat

def piP(nombre):
    if 0 <= nombre and nombre <= pi:
        return nombre
    elif nombre <= 0:
        return piP(nombre+pi)
    else:
        return piP(nombre-pi)

def NormVect(vect):
    return sqrt(vect[0]**2+vect[1]**2+vect[2]**2)

def DegRad(angle,rad=True):
    if rad == True:
        return (angle*pi)/180
    else:
        return (angle*180)/pi

def GetCenter(plan):
    top_right,top_left,bottom_right,bottom_left = plan
    top_center = ((top_right[0]+top_left[0])/2,(top_right[1]+top_left[1])/2,(top_right[2]+top_left[2])/2)
    bottom_center = ((bottom_right[0]+bottom_left[0])/2,(bottom_right[1]+bottom_left[1])/2,(bottom_right[2]+bottom_left[2])/2)
    return ((top_center[0]+bottom_center[0])/2,(top_center[1]+bottom_center[1])/2,(top_center[2]+bottom_center[2])/2)
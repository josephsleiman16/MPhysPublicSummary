import numpy as np
from typing import List
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Knot:
    """Base knot class
    
    """
    def __init__(self, crossings: int = None, name: str = None, coordinates: np.ndarray = None):
        """Constructor of the knot class

        :param crossings (int): An integer denoting the minimal crossing number of a knot
        :param name (str): A string denoting a given name to a knot
        :param self.coordinates (np.ndarray): a 3D array containing the Cartesian coordinates of the generated torus knot
        """
        self.crossings = crossings
        self.name = name
        self.coordinates = coordinates

    def plot(self, save_image: bool = False):
        """Visualises the knot coordinates using a 3D plot
        
        :param save_image (bool): a flag indicating (if True) to save the generated 3D visualisation 
        """
        fig = plt.figure(figsize = (6, 5))
        ax = plt.axes(projection = "3d")
        
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        z = self.coordinates[:, 2]

        ax.plot3D(x, y, z)
        ax.text2D(0.15, 0.85, str(self.name), transform = ax.transAxes)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        if save_image:
            plt.savefig(str(self.name) + "_knot.png")

        plt.show()
        return

    def visualise(self):
        """Visualises the knot coordinates using a 3D interactive plot
        
        :param save_image (bool): a flag indicating (if True) to save the generated 3D visualisation 
        """        
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        z = self.coordinates[:, 2]

        #fig = px.line_3d(self.coo)
        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers')])
        
        fig.show()
  
        return

    def save_coordinates(self, title: str = None, suffix: str = "dat"):
        """Saves 3D coordinates of the knot to a textfile
        
        :param title (str): The prefix for the file name to save the coordinates
        :param suffix (str): The filenmae extension type to save as (default: "dat")
        """
        if title is None:
            if self.name is not None:
                title = self.name
            else:
                title = "Knot"

        np.savetxt(title + "." + suffix, self.coordinates, fmt='%1.4f')

        return


class Torus(Knot):
    """Class to generate Torus knots
    """
    def __init__(self, p: int = 3, q: int = 2, N: int = 100, chirality: str = "right"):
        """Constructor of the Torus knot class

        Initialises the p and q integer values defining a Torus knot, as well as the number of coordinates to generate

        :param p (int): p-integer denoting the number of times the knot crosses the longitudinal direction (through the "hole")
        :param q (int): q-integer denoting the number of times the knot crosses the meridonial direction (revolutions)
        :param N (int): the number of coordinates to generate
        :param chirality (str): the handedness of the torus knot (either left handed or right handed)

        """
        Knot.__init__(self, name="(" + str(p) + "-" + str(q) + ")-Torus-" + chirality + "handed." + str(N))
        self.p = p
        self.q = q
        self.N = N
        self.chirality = chirality


    def generate_coordinates(self, r_inner: float = None, r_outer: float = None) -> np.ndarray:
        """Generates the coordiantes of a (p-q) torus knot

        :param r_inner (float): controls radius of inner circle of torus
        :param r_outer (float): controls radius of outer circle of torus

        :return self.coordinates (np.ndarray) a 3D array containing the Cartesian coordinates of the generated torus knot
        """
        
        self.coordinates = np.empty((self.N, 3))
        if r_inner is None:
            r_inner = 2

        if r_outer is None:
            r_outer = 1

        if self.chirality == "left" or self.chirality == "Left" or self.chirality == "L" or self.chirality == "l":
            self.p *= -1
            self.q *= -1
            
        for bead in range(self.N):
            t = 2 * np.pi * bead / self.N
            r = np.cos(self.q*t) + r_inner

            self.coordinates[bead][0] = r_outer * (r * np.cos(self.p*t))
            self.coordinates[bead][1] = r_outer * (r * np.sin(self.p*t))
            self.coordinates[bead][2] = r_outer * (- np.sin(self.q*t))      


        return self.coordinates 


class Lissajous(Knot):
    """Class to generate Lissajous knots
    """
    def __init__(self, n: List[int], phi: List[int], N: int = 100):
        """Constructor of the Lissajous knot class

        Initialises the n integer and phi phase-shift values defining a Lissajous knot

        :param n List(int): a list of integers defining the n_x, n_y, and n_z Lissajous integers
        :param phi List(int): a list of integers defining the phi_x, phi_y, and phi_z Lissajous phase-shifts
        :param N (int): the number of coordinates to generate

        """
        Knot.__init__(self, name="Lissajous." + str(N))
        self.n = n
        self.phi = phi
        self.N = N


    def generate_coordinates(self, r_outer: float = None):
        """Generates the coordiantes of a Lissajous knot

        :param r_outer (float): controls amplitude of Lissajous knot
        """
        self.coordinates = np.empty((self.N, 3))

        if r_outer is None:
            r_outer = 2

        for bead in range(self.N):
            t = 2 * np.pi * bead / self.N

            for dimension in range(3):
                self.coordinates[bead][dimension] = r_outer * np.cos(self.n[dimension]*t + self.phi[dimension])

        return 


class Special(Knot):
    """Class to generate Special knots (4_1, granny)
    """
    def __init__(self, id: int, N: int = 100):
        """Constructor of Special knots
        
        :param id (int): integer id to specify which type of knot is being generated
        :param N (int): the number of coordinates to generate

        """
        Knot.__init__(self, name="Figure-eight." + str(N) if id == 0 else "Granny." + str(N))
        self.id = id
        self.N = N

    def generate_coordinates(self, r_inner: float = None, r_outer: float = None):
        """
        
        :param r_inner (float): controls radius of inner circle of torus
        :param r_outer (float): controls radius of outer circle of torus
        """
        self.coordinates = np.empty((self.N, 3))
        
        # 4_1 knot
        if self.id == 0:

            if r_inner == None:
                r_inner = 2

            if r_outer == None:
                r_outer = 1

            for bead in range(self.N):
                t = 2 * np.pi * bead / self.N
                r = np.cos(2*t) + r_inner
                self.coordinates[bead][0] = r_outer * (r * np.cos(3*t))
                self.coordinates[bead][1] = r_outer * (r * np.sin(3*t))
                self.coordinates[bead][2] = r_outer * (- np.sin(4*t))  

        # granny knot
        elif self.id == 1:
            for bead in range(self.N):
                t = 2 * np.pi * bead / self.N
                self.coordinates[bead][0] = (-22*np.cos(t) - 128*np.sin(t) - 44*np.cos(3*t) - 78*np.sin(3*t)) / 80
                self.coordinates[bead][1] = (-10*np.cos(2*t) - 27*np.sin(2*t) + 38*np.cos(4*t) + 46*np.sin(4*t)) / 80
                self.coordinates[bead][2] = (70*np.cos(3*t) - 40*np.sin(3*t)) / 100

        return 

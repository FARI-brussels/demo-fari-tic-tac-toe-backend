import numpy as np
import yaml
import pickle
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

def load_data_from_yaml(file_path):
    """
    Loads x, y, z data from a YAML file.
    
    Parameters:
        file_path (str): Path to the YAML file.
        
    Returns:
        tuple: Arrays of x, y, z.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    points = np.array(data['points'])
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    return x, y, z

class Interpolator:
    def __init__(self, x=None, y=None, z=None):
        if x is not None and y is not None and z is not None:
            self.fit(x, y, z)
        else:
            self.points = None
            self.values = None

    def fit(self, x, y, z):
        """
        Fits a bilinear interpolation based on the given x, y, z points using scipy's griddata.
        
        Parameters:
            x (array-like): The x-coordinates of the points.
            y (array-like): The y-coordinates of the points.
            z (array-like): The z-values of the points.
        """
        self.points = np.column_stack((x, y))
        self.values = z

    def predict(self, xi, yi):
        """
        Predicts the z value based on the given x, y coordinates using the provided interpolator.
        
        Parameters:
            xi (float): The x-coordinate of the point to predict.
            yi (float): The y-coordinate of the point to predict.
        
        Returns:
            float: The predicted z value.
        """
        return griddata(self.points, self.values, (xi, yi), method='linear')

    def save(self, pickle_path):
        """
        Saves the interpolator to a pickle file.
        
        Parameters:
            pickle_path (str): Path to save the pickled interpolator.
        """
        with open(pickle_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(pickle_path):
        """
        Loads the pickled interpolator.
        
        Parameters:
            pickle_path (str): Path to the pickled interpolator.
        
        Returns:
            Interpolator: The loaded interpolator instance.
        """
        with open(pickle_path, 'rb') as f:
            return pickle.load(f)

def plot_interpolation(interpolator, x, y, z):
    """
    Plots the bilinear interpolation.
    
    Parameters:
        interpolator (Interpolator): The bilinear interpolation instance.
        x (array-like): The x-coordinates of the original points.
        y (array-like): The y-coordinates of the original points.
        z (array-like): The z-values of the original points.
    """
    # Create grid to evaluate the interpolator
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = interpolator.predict(xi, yi)

    # Contour plot
    plt.figure()
    plt.contourf(xi, yi, zi, levels=100, cmap='viridis')
    plt.colorbar()
    plt.scatter(x, y, c=z, edgecolor='k', marker='o')
    plt.title('Bilinear Interpolation - Contour Plot')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    # 3D surface plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xi, yi, zi, cmap='viridis', edgecolor='none')
    ax.scatter(x, y, z, color='r', s=50)
    ax.set_title('Bilinear Interpolation - 3D Surface Plot')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# Load data from YAML file
x, y, z = load_data_from_yaml('data.yaml')

# Fit the bilinear interpolation and pickle it
interpolator = Interpolator(x, y, z)
pickle_path = 'interpolator.pkl'
interpolator.save(pickle_path)

# Load the pickled interpolator
loaded_interpolator = Interpolator.load(pickle_path)

# Predict the z value for a given (x, y) pair
xi, yi = 1.5, 1.5
zi = loaded_interpolator.predict(xi, yi)
print(f"Predicted z value at (x={xi}, y={yi}): {zi}")

# Plot the interpolation
plot_interpolation(loaded_interpolator, x, y, z)

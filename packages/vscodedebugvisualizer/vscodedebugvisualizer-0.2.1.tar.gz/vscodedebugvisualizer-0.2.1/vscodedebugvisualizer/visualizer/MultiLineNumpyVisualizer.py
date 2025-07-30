import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from vscodedebugvisualizer.visualizer.PlotlyVisualizer import PlotlyVisualizer


class MultiLineNumpyVisualizer(PlotlyVisualizer):
    def __init__(self) -> None:
        super().__init__()

    def checkType(self, t):
        # Check if it's a numpy array with at least 2 dimensions
        if isinstance(t, np.ndarray) and len(t.shape) >= 2:
            return True
            
        # Check if it's a list of numpy arrays
        if isinstance(t, list) and len(t) > 0 and all(isinstance(item, np.ndarray) for item in t):
            return True
            
        return False

    def selectAndTailorData(self, data):
        maxLength = 1000
        maxLines = 20  # Maximum number of lines to display
        
        # Handle list of numpy arrays
        if isinstance(data, list):
            # Convert list of arrays to a single 3D array if possible
            if all(len(arr.shape) == 1 for arr in data):
                # List of 1D arrays - convert to shape [len(data), 1, max_length]
                max_len = max(arr.shape[0] for arr in data)
                padded_data = []
                for arr in data[:maxLines]:
                    # Pad shorter arrays with NaN
                    padded = np.full(max_len, np.nan)
                    padded[:arr.shape[0]] = arr
                    padded_data.append([padded])
                data = np.array(padded_data)
            elif all(len(arr.shape) == 2 for arr in data):
                # List of 2D arrays - keep as is, but limit number
                data = data[:maxLines]
            else:
                # Mixed dimensions, handle each separately
                processed_data = []
                for arr in data[:maxLines]:
                    if len(arr.shape) == 1:
                        processed_data.append([arr])
                    else:
                        processed_data.append(arr)
                data = processed_data
        else:
            # Handle single numpy array
            shape = data.shape
            numDim = len(shape)
            
            # Handle arrays with different dimensions
            if numDim == 2:
                # Add a new dimension at the beginning for 2D arrays
                data = data.reshape(1, *shape)
                shape = data.shape
            elif numDim > 3:
                # For higher dims, keep only first 3 dimensions
                new_shape = (shape[0], shape[1], np.prod(shape[2:]))
                data = data.reshape(new_shape)
                shape = data.shape
            
            # Limit number of plots (first dimension)
            if shape[0] > maxLines:
                data = data[:maxLines]
        
        # Apply downsampling - handle both list and np.array cases
        if isinstance(data, np.ndarray):
            shape = data.shape
            factor = 1
            if shape[2] > maxLength:
                factor = shape[2] // maxLength
            
            xValues = np.arange(0, shape[2], factor)
            data = data[:, :, ::factor]
            
            return data, xValues
        else:
            # For list of arrays, downsample each separately
            downsampled_data = []
            xValues_list = []
            
            for arr in data:
                if len(arr.shape) == 2:
                    factor = 1
                    if arr.shape[1] > maxLength:
                        factor = arr.shape[1] // maxLength
                    
                    xValues = np.arange(0, arr.shape[1], factor)
                    downsampled_data.append(arr[:, ::factor])
                    xValues_list.append(xValues)
            
            return downsampled_data, xValues_list

    def visualize(self, data):
        data, xValues = self.selectAndTailorData(data)
        
        # Create figure based on data type
        if isinstance(data, np.ndarray):
            # Handle numpy array case
            num_plots = data.shape[0]
            num_lines = data.shape[1]
            
            # Create subplots
            fig = make_subplots(
                rows=num_plots, 
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=[f"Slice {i}" for i in range(num_plots)]
            )
            
            # Add traces
            for i in range(num_plots):
                for j in range(num_lines):
                    fig.add_trace(
                        go.Scatter(
                            x=xValues,
                            y=data[i, j],
                            mode="lines",
                            name=f"[{i}, {j}]",
                        ),
                        row=i+1,
                        col=1,
                    )
        else:
            # Handle list of arrays case
            num_plots = len(data)
            
            # Create subplots
            fig = make_subplots(
                rows=num_plots, 
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=[f"Array {i}" for i in range(num_plots)]
            )
            
            # Add traces
            for i, (arr, x_vals) in enumerate(zip(data, xValues)):
                num_lines = arr.shape[0]
                for j in range(num_lines):
                    fig.add_trace(
                        go.Scatter(
                            x=x_vals,
                            y=arr[j],
                            mode="lines",
                            name=f"Array {i}, Line {j}",
                        ),
                        row=i+1,
                        col=1,
                    )
        
        # Update layout for better visualization
        fig.update_layout(
            height=300 * (num_plots if num_plots > 0 else 1),
            showlegend=True,
            legend_title_text="Lines"
        )
        
        return super().visualize(fig)

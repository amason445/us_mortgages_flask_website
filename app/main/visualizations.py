import matplotlib.pyplot as plt
from io import BytesIO
import base64

def dummy_plot():
    
    x = range(0, 100)
    y = range(0, 200, 2)

    plt.plot(x, y)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode()
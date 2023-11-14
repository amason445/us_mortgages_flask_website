import app.utilities as utl
import app.models as mdl

from matplotlib import pyplot as plt
import seaborn as sns
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

def state_interest_rates(state_name):
    try:

        df = mdl.StateInterestRateSeries(state_name= state_name).return_df()

        sns.lineplot(data = df, x = 'Year', y = 'value', hue= 'Loan Term')

        plt.locator_params(axis="x", integer=True, tight=True)
        
        plt.title(f"Average Interest Rates for the US State of {utl.state_abbreviation_mapping(state_name)}")
        plt.xlabel('Year')
        plt.ylabel('Interest Rate (%)')
        plt.legend(title = 'Loan Term')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        plt.clf()
        plt.close()
        
        return base64.b64encode(buffer.read()).decode()
    
    except Exception as e:
        print(e)

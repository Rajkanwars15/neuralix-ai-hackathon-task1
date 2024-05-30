from h2o_wave import ui, data
import pandas as pd

def create_summary_card() -> ui.PlotCard:
    # Load the dataset
    monthly_data = pd.read_csv('data/interim/monthly_data.csv')

    # Create a bar plot card
    return ui.plot_card(
        box='1 1 4 4',
        title='Monthly Sum of LV ActivePower',
        data=dict(month=monthly_data['Month'].astype(str).tolist(), lv_activepower=monthly_data['LV ActivePower'].tolist()),
        plot=ui.plot([
            ui.mark(type='interval', x='=month', y='=lv_activepower', y_min=0)
        ])
    )

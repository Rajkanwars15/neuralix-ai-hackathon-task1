import logging
from h2o_wave import Q, main, app, copy_expando, handle_on, on, ui, data
import cards

# Set up logging
logging.basicConfig(format='%(levelname)s:\t[%(asctime)s]\t%(message)s', level=logging.INFO)

@app('/')
async def serve(q: Q):
    """
    Main entry point. All queries pass through this function.
    """
    try:
        # Initialize the app if not already
        if not q.app.initialized:
            await initialize_app(q)

        # Initialize the client (browser tab) if not already
        if not q.client.initialized:
            await initialize_client(q)

        # Update theme if toggled
        elif q.args.toggle_theme is not None:
            await toggle_theme(q)

        # Handle navigation
        elif q.args['#']:
            await handle_navigation(q)

        # Delegate query to query handlers
        elif await handle_on(q):
            pass

        # Adding this condition to help in identifying bugs (instead of seeing a blank page in the browser)
        else:
            await handle_fallback(q)

    except Exception as error:
        await show_error(q, error=str(error))

async def initialize_app(q: Q):
    """
    Initialize the app.
    """
    logging.info('Initializing app')
    # Set initial argument values
    q.app.cards = ['main', 'sidebar', 'content', 'example', 'summary', 'total_turbines', 'active', 'out_of_commission', 'healthy', 'predicted_failure', 'down_for_repairs', 'mean_time_until_failure', 'Monthly_Sum_of_LV_ActivePower', 'footer', 'error']
    q.app.initialized = True

async def initialize_client(q: Q):
    """
    Initialize the client (browser tab).
    """
    logging.info('Initializing client')
    # Add layouts, header, sidebar, main content, and footer
    q.page['meta'] = cards.meta
    q.page['header'] = cards.header
    q.page['content'] = cards.main_content

    q.page['total_turbines'] = cards.total_turbines
    q.page['active'] = cards.active
    q.page['out_of_commission'] = cards.out_of_commission
    q.page['healthy'] = cards.healthy
    q.page['predicted_failure'] = cards.predicted_failure
    q.page['down_for_repairs'] = cards.down_for_repairs
    q.page['Monthly_Sum_of_LV_ActivePower'] = cards.Monthly_Sum_of_LV_ActivePower

    q.page['mean_time_until_failure'] = cards.mean_time_until_failure
    q.page['top_root_causes'] = cards.top_root_causes

    q.page['footer'] = cards.footer
    q.client.initialized = True
    await q.page.save()

async def handle_navigation(q: Q):
    """
    Handle sidebar navigation.
    """
    logging.info(f"Navigating to {q.args['#']}")
    # Update content based on navigation item clicked
    if q.args['#'] == '#menu/spam':
        q.page['content'].items = [ui.text('### Spam Content')]
    elif q.args['#'] == '#menu/ham':
        q.page['content'].items = [ui.text('### Ham Content')]
    elif q.args['#'] == '#menu/eggs':
        q.page['content'].items = [ui.text('### Eggs Content')]
    elif q.args['#'] == '#about':
        q.page['content'].items = [ui.text('### About Page')]
    elif q.args['#'] == '#support':
        q.page['content'].items = [ui.text('### Support Page')]

    await q.page.save()

def clear_cards(q: Q, card_names: list):
    """
    Clear cards from the page.
    """
    logging.info('Clearing cards')
    # Delete cards from the page
    for card_name in card_names:
        del q.page[card_name]

async def show_error(q: Q, error: str):
    """
    Displays errors.
    """
    logging.error(error)
    # Clear all cards
    clear_cards(q, q.app.cards)
    # Format and display the error
    q.page['error'] = cards.crash_report(q)
    await q.page.save()

@on('reload')
async def reload_client(q: Q):
    """
    Reset the client (browser tab).
    This function is called when the user clicks "Reload" on the crash report.
    """
    logging.info('Reloading client')
    # Clear all cards
    clear_cards(q, q.app.cards)
    # Reload the client
    await initialize_client(q)

@on('toggle_theme')
async def toggle_theme(q: Q):
    """
    Toggle between light and dark themes.
    """
    if q.args.toggle_theme:
        q.client.theme_dark = True
        q.page['meta'].theme = 'neuralix-dark'
        q.page['header'].image = 'https://i.imgur.com/ZS6G3f4.png'
        logging.info('Updating theme to dark mode')
    else:
        q.client.theme_dark = False
        q.page['meta'].theme = 'neuralix-light'
        q.page['header'].image = 'https://i.imgur.com/yThsZ40.png'
        logging.info('Updating theme to light mode')
    # Save the updated page state
    await q.page.save()

async def handle_fallback(q: Q):
    """
    Handle fallback cases.
    This function should never get called unless there is a bug in our code or query handling logic.
    """
    logging.info('Adding fallback page')
    q.page['fallback'] = cards.fallback
    await q.page.save()

import sys
import traceback
from h2o_wave import Q, expando_to_dict, site, ui

# App name
app_name = 'Dashboard'

# Link to repo. Report bugs/features here :)
repo_url = 'https://github.com/rajkanwars15/neuralix-ai-hackathon-task1'
issue_url = f'{repo_url}/issues/new?assignees=rajkanwars15&labels=bug&template=error-report.md&title=%5BERROR%5D'

# Meta card to hold the app's title, layouts, dialogs, theme and other meta information
meta = ui.meta_card(
    themes=[
        ui.theme(
            name='neuralix-dark',
            primary='#5ab5ad',
            text='#ffffff',
            card='#181A1B',
            page='#2d2f30',
        ),
        ui.theme(
            name='neuralix-light',
            primary='#5ab5ad',
            text='#181A1B',
            card='#ffffff',
            page='#DCE3E3',
        )
    ],
    box='',
    title='Neuralix Wind Farm Dashboard',
    icon='https://i.imgur.com/s9w0xce.png',
    layouts=[
        ui.layout(
            breakpoint='xs',
            zones=[
                ui.zone(name='header'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    # Use space for content
                    ui.zone('content'),
                ]),
                ui.zone(name='footer')
            ]
        )
    ],
    theme='neuralix-light'
)

header = ui.header_card(
    box='header',
    title='neuralix.ai',
    subtitle='',
    image='https://i.imgur.com/yThsZ40.png',
    nav=[
        ui.nav_group('Menu 1', items=[
            ui.nav_item(name='#menu/1', label='Item 1'),
            ui.nav_item(name='#menu/2', label='Item 2'),
            ui.nav_item(name='#menu/3', label='Item 3'),
        ]),
        ui.nav_group('Menu 2', items=[
            ui.nav_item(name='#a', label='Item 4'),
            ui.nav_item(name='#b', label='Item 5'),
        ])
    ],
    items=[
        # dark mode toggle switch
        ui.toggle(name='toggle_theme', label='', value=False, trigger=True),
        # profile in header
        ui.menu(image='default', items=[
            ui.command(name='profile', label='Profile', icon='Contact'),
            ui.command(name='preferences', label='Preferences', icon='Settings'),
            ui.command(name='logout', label='Logout', icon='SignOut'),
    ])
    ]
)

# Main content card
main_content = ui.form_card(
    box='content',
    items=[
        ui.text('### Welcome to the Neuralix Wind Farm Dashboard'),
        ui.text('Here you can monitor and analyze the performance of your wind farm.'),
    ]
)

# The footer shown on all the app's pages
footer = ui.footer_card(
    box='footer',
    caption=f'Learn more about <a href="{repo_url}" target="_blank"> this dashboard</a>'
)

# A fallback card for handling bugs
fallback = ui.form_card(
    box='main',
    items=[ui.text('Uh-oh, something went wrong!')]
)

def crash_report(q: Q) -> ui.FormCard:
    """
    Card for capturing the stack trace and current application state, for error reporting.
    This function is called by the main serve() loop on uncaught exceptions.
    """
    def code_block(content): return '\n'.join(['```', *content, '```'])

    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)

    dump = [
        '### Stack Trace',
        code_block(stack_trace),
    ]

    states = [
        ('q.app', q.app),
        ('q.user', q.user),
        ('q.client', q.client),
        ('q.events', q.events),
        ('q.args', q.args)
    ]
    for name, source in states:
        dump.append(f'### {name}')
        dump.append(code_block([f'{k}: {v}' for k, v in expando_to_dict(source).items()]))

    return ui.form_card(
        box='main',
        items=[
            ui.stats(
                items=[
                    ui.stat(
                        label='',
                        value='Oops!',
                        caption='Something went wrong',
                        icon='Error'
                    )
                ],
            ),
            ui.separator(),
            ui.text_l(content='Apologies for the inconvenience!'),
            ui.buttons(items=[ui.button(name='reload', label='Reload', primary=True)]),
            ui.expander(name='report', label='Error Details', items=[
                ui.text(
                    f'To report this issue, <a href="{issue_url}" target="_blank">please open an issue</a> with the details below:'),
                ui.text_l(content=f'Report Issue in App: **{app_name}**'),
                ui.text(content='\n'.join(dump)),
            ])
        ]
    )

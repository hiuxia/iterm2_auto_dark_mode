#!/usr/bin/env python3

import iterm2
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

# for iterm debugging
logging.basicConfig(
    filename='your_log_path', level=logging.DEBUG)

dark_keyword_list = ['dark', 'Dark', 'DARK']
light_keyword_list = ['light', 'Light', 'LIGHT']

# get current color scheme of iterm2
executor = ThreadPoolExecutor(max_workers=4)


def ColorsUnequal(profile_color, preset_color):
    return (round(profile_color.red) != round(preset_color.red) or
            round(profile_color.green) != round(preset_color.green) or
            round(profile_color.blue) != round(preset_color.blue) or
            round(profile_color.alpha) != round(preset_color.alpha) or
            profile_color.color_space != preset_color.color_space)


def ProfileUsesPreset(profile, preset):
    for preset_color in preset.values:
        key = preset_color.key
        profile_color = profile.get_color_with_key(key)
        if ColorsUnequal(profile_color, preset_color):
            return False
    return True


async def PresetForProfile(connection, profile):
    presets = await iterm2.ColorPreset.async_get_list(connection)
    for preset_name in presets:
        preset = await iterm2.ColorPreset.async_get(connection, preset_name)
        if ProfileUsesPreset(profile, preset):
            return preset_name
    return None


async def get_iterm_color_theme(connection):
    app = await iterm2.async_get_app(connection)
    session = app.current_terminal_window.current_tab.current_session
    profile = await session.async_get_profile()
    theme = await PresetForProfile(connection, profile)
    return theme


async def get_current_color_scheme(connection):
    logging.info('Getting current color scheme...')
    app = await iterm2.async_get_app(connection)
    if app is not None:
        theme = await app.async_get_theme()
    else:
        raise Exception("No iterm2 app found")
    logging.info(f'Got current color scheme: {theme}')
    return theme


async def update_color_scheme(connection, preset):
    try:
        logging.info(f'Updating color scheme to {preset}...')
        profiles = await iterm2.PartialProfile.async_query(connection)
        logging.info(f'Got profiles: {profiles}')
        for partial in profiles:
            profile = await partial.async_get_full_profile()
            await profile.async_set_color_preset(preset)
        logging.info('Color scheme updated.')
    except Exception as e:
        logging.error(f'Failed to update color scheme: {str(e)}')


async def main(connection):
    logging.info('Running main function...')
    current_color_scheme = await get_iterm_color_theme(connection)
    theme = await get_current_color_scheme(connection)
    logging.info(
        f"current theme: {theme}, current color scheme: {current_color_scheme}")
    # parts = theme.split(" ")
    if ("dark" in theme and "Dark" in current_color_scheme) or ("light" in theme and "Light" in current_color_scheme):
        logging.info('Color scheme matches system theme, doing nothing.')
    else:
        logging.info('Color scheme does not match system theme.')
        if "dark" in theme:
            logging.info(
                'System theme is dark, updating color scheme to Solarized Dark...')
            preset = await iterm2.ColorPreset.async_get(connection, "Solarized Dark")
            if preset is None:
                logging.info(preset)
            else:
                logging.info('preset is not none')
            await update_color_scheme(connection, preset)
        else:
            preset = await iterm2.ColorPreset.async_get(connection, "Light Background")
            await update_color_scheme(connection, preset)

    async with iterm2.VariableMonitor(connection, iterm2.VariableScopes.APP, "effectiveTheme", None) as mon:
        while True:
            theme = await mon.async_get()
            parts = theme.split(" ")
            if "dark" in parts:
                preset = await iterm2.ColorPreset.async_get(connection, "Solarized Dark")
            else:
                preset = await iterm2.ColorPreset.async_get(connection, "Light Background")
            await update_color_scheme(connection, preset)

iterm2.run_forever(main)

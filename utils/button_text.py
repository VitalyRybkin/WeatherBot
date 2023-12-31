from dataclasses import dataclass


@dataclass
class ButtonSigns:
    cancel: str = "\U0000274C Cancel"
    setting_location: str = "\U0001F3E1 Set location"
    adding_location: str = "\U0001F5C3 Add location"
    set_favorite_location: str = "\U00002705 Set"
    add_wishlist_location: str = "\U0001F5C3 Add"
    changing_location: str = "\U0001F3E1 Change"
    change_favorite_location: str = "\U00002705 Change"
    clear_wishlist: str = "\U0001F5D1 Clear"
    set_wishlist: str = "\U00002705 Set wishlist"
    current: str = "\U0001F4C5 Current"
    forecast: str = "\U0001F4C8 Forecast"

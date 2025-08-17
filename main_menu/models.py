from enum import StrEnum
from localization import Localization


class Buttons(StrEnum):
    SECTION_PERSONAL = Localization.PERSONAL_ACCOUNT_BUTTON
    SECTION_MASTERCLASSES = Localization.MASTERCLASSES_BUTTON
    SECTION_VIDEOCOURSES = Localization.VIDEOCOURSES_BUTTON
    SECTION_PATTERNS = Localization.PATTERNS_BUTTON
    SECTION_SUPPORT = Localization.SUPPORT_BUTTON

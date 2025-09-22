from enum import StrEnum
from localization import Localization


class Buttons(StrEnum):
    section_personal = Localization.section_personal_button
    section_masterclasses = Localization.section_masterclasses_button
    section_videocourses = Localization.section_videocourses_button
    section_patterns = Localization.section_patterns_button
    section_support = Localization.section_support_button


class Section(StrEnum):
    masterclasses = "masterclasses"
    videocourses = "videocourses"
    patterns = "patterns"
    support = "support"

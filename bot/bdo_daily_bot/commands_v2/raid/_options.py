"""Command options for raid related commands."""
from interactions import LocalisedDesc
from interactions import SlashCommandChoice

server_choices = [
    SlashCommandChoice(name=LocalisedDesc(english_us="Arsha", russian="Арша"), value="Arsha"),
    SlashCommandChoice(name=LocalisedDesc(english_us="K-1", russian="К-1"), value="K-1"),
    SlashCommandChoice(name=LocalisedDesc(english_us="K-2", russian="К-2"), value="K-2"),
    SlashCommandChoice(name=LocalisedDesc(english_us="K-3", russian="К-3"), value="K-3"),
    SlashCommandChoice(name=LocalisedDesc(english_us="K-4", russian="К-4"), value="K-4"),
]

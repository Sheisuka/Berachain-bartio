import questionary
import berakiller.berakiller

def run():
    bera = berakiller.berakiller.Berakiller()
    choice = questionary.select(
        "What we gonna do?",
        choices=[
            "Get Bera",
            "Delegate",
            "Check delegation queue",
        ]
    ).ask()

    match choice:
        case 1: ...
        case 2: ...


if __name__ == "__main__":
    run()
from dataextractor.cli import CliHandler
from dataextractor.core.app import main as app_main

def main():
    cli = CliHandler()
    args = cli.parse()
    if args.g:
        print("git")
    elif args.j:
        print("jira")

    app_main()

if __name__ == "__main__":
    main()

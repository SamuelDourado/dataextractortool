from dataextractor.cli import CliHandler


def main():
    cli = CliHandler()
    args = cli.parse()
    if args.g:
        print("git")
    elif args.j:
        print("jira")


if __name__ == "__main__":
    main()

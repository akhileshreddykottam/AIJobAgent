from ai_helper import create_client


def main():
    with create_client() as client:
        for model in client.models.list():
            print(model.name)


if __name__ == "__main__":
    main()
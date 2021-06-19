def main():
    pages = 0
    page = 1

    while pages < 15000:
        pages += page
        page += 1

    print(page, pages)

    pages += page
    print(page, pages)


if __name__ == '__main__':
    main()

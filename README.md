# Penn CIS People

Scraper of the Penn CIS directory to a JSON format, and corresponding Anki flashcards.

Todo:
- add continuous integration
- move binary and feed to release
- create GitHub pages for feed
- improve README.md ☺️

## Format description

- For faculty (`faculty.json`):
    ```json
    [
        ...
        {
            "name": "J\u00e9r\u00e9mie O. Lumbroso",
            "image_url": "https://directory.seas.upenn.edu/wp-content/uploads/2023/09/Lumbroso_Jeremie-2023-Directory-scaled-e1695845603810.jpg",
            "titles": [
                "Practice Assistant Professor",
                "Computer and Information Science"
            ],
            "email": "lumbroso@cis.upenn.edu"
        },
        ...
    ]
    ```

- For staff (`staff.json`):
    ```json
    [
        ...
        {
            "name": "Jackie Caliman",
            "title": "Director of Administrative Operations",
            "image_url": "https://www.cis.upenn.edu/wp-content/uploads/2019/09/Caliman.jpg",
            "contact": {
                "Office": "306 Levine",
                "Phone": "215-898-5326",
                "Fax": "215-898-0587",
                "Email": "jackie@cis.upenn.edu"
            }
        },
        ...
    ]
    ```

##
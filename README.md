# README - "Driven by Reward but Attracted to Power: Decision-making in a novel Multiplayer Economic Game."

## Introduction
Welcome to the GitHub repository for the paper titled "Driven by Reward but Attracted to Power: Decision-making in a novel Multiplayer Economic Game." by Chaigneau Amine, Borozan Miloš, Pezzullo Giovanni, De Liberato Simone, Palumbo Riccardo, and Iodice Pierpaolo. This repository contains the EDMG software (web application) used for the experiment.

## Running the Application Locally

To run the EDMG web application locally with the Django backend and websocket, follow these steps:

1. Clone or download this repository to your local machine.
2. Ensure you have Python and Django installed on your system. You can install Django using pip if you haven't already: `pip install Django`
3. Navigate to the project directory: `cd EDMG-task-multiplayer`
4. Apply migrations to set up the database: `python manage.py migrate`
5. Create a superuser (admin) account for database administration: `python manage.py createsuperuser`
6. Start the local server: `python manage.py runserver`
7. Navigate to the frontend directory `cd EDMG-task-multiplayer/frontend`
8. Access the EDMG web application by opening a web browser by running the frontend app
8. Run the app or Build the app (reactjs, `npm start`)

Please note that this is a multiplayer game designed for 3 players. Three individuals should be locally connected to the web server simultaneously to participate in the game. The web server include webSocket.

## Citing the Paper
If you use or refer to the code in this repository in your work, please cite our paper as follows:

- Chaigneau Amine, Borozan Miloš, Pezzullo Giovanni, De Liberato Simone, Palumbo Riccardo, Iodice Pierpaolo. (Year). Driven by Reward but Attracted to Power: Decision-making in a novel Multiplayer Economic Game. [Journal Name/Conference Name], [Volume(Issue)], [Page Range].

## License
Please note that the code in this repository may be subject to certain licenses. Make sure to review and comply with any licensing terms associated with specific components or dependencies used in the code.

Thank you for your interest in our research, and we hope this repository proves useful to you. If you have any questions or need further assistance, please feel free to reach out.

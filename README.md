# Team1 Trip Planner

This is the repository for the Trip Planner project by CMSC 495 Team1. The project aims to create a user-friendly tool
to plan trips, considering preferences such as destination, budget, and available activities.

- Galia Adelshin (Project Manager)
- Terence Boyce (Test Director)
- Xavier Watson (Software Developer)
- Jared Brick (Software Developer)
- Greg Chelchowski (Requirements Manager/UX/UI Designer)

## Project Overview
The Trip Planner application is a web-based tool that allows users to create, edit, and share personalized travel itineraries. The core functionalities include:
- Customizable trip itineraries (create, edit, share).
- Scheduling activities and setting reminders.
- Visualizing trips on an interactive map.
- Embedded links for booking accommodations and transportation.

The project follows Agile principles, focusing on iterative development, regular feedback, and continuous testing.

## Installation and Setup
To set up the Trip Planner application locally, follow these steps:

1. **Clone the Repository**
   ```
   git clone https://github.com/CMSC495-Team1/Team1_TripPlanner.git
   ```

2. **Set Up Local Environment**
   - Make sure Python 3.8+ is installed on your system.
   - Create a virtual environment and activate it:
     ```
     python -m venv env
     source env/bin/activate  # On Windows, use `env\Scripts\activate`
     ```
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

3. **Run the Application**
   - Start the server:
     ```
     python app.py
     ```
   - Open your browser and navigate to `http://localhost:5000` to access the application.

## Usage
- Users can create an account, log in, and start planning their trips by adding destinations, activities, and accommodations.
- The interactive map feature allows users to visualize their planned routes and activities.
- Users can share their itineraries with friends or export them for offline access.

## Contribution Guidelines
We welcome contributions from all team members. Please follow these guidelines to ensure smooth collaboration:

1. **Fork and Clone**
   - Fork the repository and clone it to your local machine.

2. **Create a Branch**
   - Create a branch for your feature or bug fix:
     ```
     git checkout -b feature/your-feature-name
     ```

3. **Commit Changes**
   - Make your changes, commit them, and push to your branch:
     ```
     git add .
     git commit -m "Description of changes"
     git push origin feature/your-feature-name
     ```

4. **Submit a Pull Request**
   - Go to the GitHub repository and create a pull request from your branch. All changes will be reviewed before being merged into the main branch.

## Testing
- Unit tests are located in the `tests` directory.
- Run all tests using the following command:
  ```
  pytest
  ```

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite (can be migrated to PostgresSQL for production)
- **Testing**: PyTest, Selenium (for UI testing)

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions, please reach out to the Project Manager, Galia Adelshin, at gadelshin@student.umgc.edu.


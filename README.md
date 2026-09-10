# IFCSP-AE2-SE-Knowledge-Quiz

## Introduction
Microsoft's sales and commercial organisation, Microsoft Customer and Partner Solutions (MCAPS), delivers consultation-like sales to customers, working with third party vendors to help showcase the value of Microsoft's technology to a range of customers and clients. Within MCAPS, solution engineers sit within the pre-sales sub-organisation called the Specialist Teams Unit, which work with clients and customers to help them understand how they can use Microsoft technlogy within their organisation and secure a sales win. Solution engineers are deeply technical, but also consultative - they need to understand how to apply the technology in various nuanced and sometimes complex client situations. In order to be prepared, they will not only need to know and understand their specific technology area, but also how to know when and where to apply it. 

There are solution engineers for each of the various types of technology. For Azure cloud computing, there are three types of solution engineers - those who specialise in data platforms and tools (Data), cloud infrastructure (Infra), and AI and application technologies (AI/Apps).

This quiz is aimed at testing the various areas of knowledge a solution engineer must know for their specific technology stack and providing various example customer scenarios that will help them think about how they can apply their knowledge to their day to day jobs.

This application will be developed as an MVP using Python (with applicable libraries) and Tkinter, with data stored in a CSV, but this can be substituted with any other permanent data storage, such as a SQL database. No personal data will be stored, however, a CSV extraction of links and resources they would like to work on will be generated and provided to the user. 

Because this is an MVP, only essential functionality is within scope e.g. input validation, quiz functionality, score keeping, curation of links and resources. This is such that development can continue upon validation of the MVP. 


## Design 

### GUI Design

![Figma Diagram](img/01.png)
![Figma Diagram](img/02.png)

### Functional and Non-Functional Requirements

Functional Requirements:
- The App must present three choices of quiz topic for the user to select: AI/Apps, Data, Infrastructure, as buttons
- When user submits their choice, App must ask if they are sure, and give them the ability to go back.
- The App must display one question at a time from the topic chosen by the user.
- The App must allow for the navigation between questions using a button that navigates to the next question and one that navigates to the previous one
- App must store each answer selected, and allow the user to return to it and change it
- The first question must only allow the user to navigate to the next question, and the last question provide a way to submit their entire set of answers.
- When user submits their answers, App must ask if they are sure, and give them the ability to go back.
- When user confirms their answer submission, the App must display their score as a percentage and as a raw numerical score, and provide a button that navigates them to look at each answer.
- App must display each answer break down one at a time, with the answer they got right or wrong, the correct answer and an explanation of the correct answer.
- With each answer break down, App must also present a series of hyperlinks to documentation and further reading.
- App must provide buttons to navigate through each answer breakdown.
- App should pull questions, answers and documentation links for each question from the provided CSV files. 

Non-functional Requirements:
- The GUI should be consistent, predictable and easily navigable. 
- The interface should only allow the user to interact with the system through clicking buttons only.
- User can only select at most one answer - not more than one.
- App should navigate spin up, tear down or navigate through each window and frame near instantaneously.
- Pop up messages should appear near instantaneously and be succinct in words.

### User Persona Map
The user persona details the type of individual that this app aims to cater for. 

![User Persona](img/user_persona.png)

### Tech Stack and Code Design

The program is entirely written in Python, with the following libraries used throughout the application:
- ```tkinter``` for GUI
- ```pandas``` for structured data access and filtering
- ```webbrowser``` for hyperlink capabilities 
- ```unittest``` and ```unittest.mock``` for unit and integration testing, and for the mock and isolate functionality within the unittests

Because this is a brief proof of concept to demonstrate that this quiz app is possible, CSV files have been used for permanent storage for questions, answers and resource links, but this can just as easily be replaced by a database e.g. PostgreSQL. 

The following is the code design diagram for application:

![Class Diagram](img/class_diagram.png)

## Development -- Thurs

_In this section, include relevant code blocks using triple backticks (```) to format your code clearly. Explain how your application works by describing the main parts of your code, such as important functions, classes, or modules. Provide enough detail to demonstrate your understanding of how each part contributes to the overall functionality. There is no word limit; focus on clarity and completeness._
There are three python files that run the application - ```main.py```, ```quiz_page.py```, ```results_page.py```

### MainQuizApp - ```main.py```

```
class MainQuizApp(tk.Tk):
    """
    Main App Window that will display options for user

    This is the main Tk application that carries the rest of the windows and other parts of the application. 

    It initialises the Main Title for Window, creates instructions for the user, and creates button options for different solution area / topic option, which are bound to a method that checks to confirm the user's choice
    Methods:
        confirm_quiz_choice
        open_quiz_window
        open_results_window
    """

    def confirm_quiz_choice(self, choice):
        '''
        Produces message box to confirm if user has made the right choice, then triggers another method that opens another quiz app window.
        
        args:
            choice (str): the selected quiz topic as a string
        returns:
            True (bool): if there are no Exceptions thrown
            OR False if there are exceptions thrown
        '''

    def open_quiz_window(self, choice):
        """
        Creates seperate window to host quiz of user's choice

        args:
            choice (str): the selected quiz topic as a string
        returns:
            "OK" (str): if there are no Exceptions thrown
            OR e (Exception) if there are exceptions thrown
        """

    def open_results_window(self, question_set, answer_set, resources_set, sol_area, *colours):
        """
        Creates seperate window to host display results of user's quiz

        args:
            question_set (QuestionFrame): list of questions in the form on tk.Frames, with the associated user answers
            answer_set (pandas.DataFrame): corresponding set of answers for the questions, loaded from csv file into a pandas df
            resource_set (pandas.DataFrame): corresponding set of documentation links for the questions and answers, loaded from csv file into a pandas df
            sol_area (str): the selected quiz topic as a string
            colours (tuple of str): colour theme for the results window as a tuple of two hex strings
        returns:
            True (bool): if there are no Exceptions thrown
            OR False if there are exceptions thrown
        
        """

```

### SolAreaQuiz - ```quiz_page.py```

### ResultsWindow - ```results_window.py```

## Testing -- Thurs

_Explain your approach to testing your digital product, demonstrating a systematic and strategic approach. Address the following topics:_ 
- _Testing strategy and methodology (summarise and justify different methods of testing you have used, for example, manual and automated unit testing)_
- _Outcomes of application testing:_ 
    - _The outcome of manual tests (should be presented in a tabular format)._ 
    - _Unit testing outcome (should include screenshots of tests running - passing or failing)._ 

### Testing Strategy and Methodology

Manual testing and an iterative approach was mainly used to test the app as it was being developed. The next section details some of the outcomes of manual testing. For specific functionality within the app itself, unit testing with integration testing was used via ```unittest```. Some functionality that the being tested methods relied on needed to be abstracted, so ```unittest.mock``` provided the abilitiy to mock that functionality, so that the method itself was tested. 

### Testing Outcomes

## Documentation -- Fri

_User documentation should explain how end users, such as staff within your organisation, can interact with the quiz application, whereas technical documentation should outline steps such as running tests locally and explain parts of the code._

### User documentation

### Technical documentation

## Evaluation -- Fri
_The evaluation section should explain what went well during the development of the project and what could have been improved. The evaluation section should be written in a genuine, reflective tone. As the README follows the conventions of software documentation, hyperlinks should be used for references instead of Harvard referencing._

If I had more time, I would streamline the code even more: QuestionFrame and AnswerFrame share a lot of the same code - so there would have been a boiler plate class that both would inherit from. If I had more time, I would have generated a set of links to be downloaded!!
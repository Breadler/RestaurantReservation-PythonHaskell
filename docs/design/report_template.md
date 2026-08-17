TITLE PAGE
[PROJECT TITLE]
Programming Language Concepts Project Report
Course: [Course Code and Course Name]
Lecturer: [Lecturer Name]
Group Members:

1. [Student Name] – [Student ID]
2. [Student Name] – [Student ID]
3. [Student Name] – [Student ID]
4. [Student Name] – [Student ID]
   Submission Date: [DD Month YYYY]

---

DECLARATION
We declare that this report and the accompanying project work are entirely our own work and that all sources used have been properly acknowledged.
ABSTRACT
This project presents [brief project title or system name], developed to compare [paradigm 1] and [paradigm 2] in solving the same problem. The system [briefly describe main functions]. The report discusses the problem, requirements, design, implementation, testing, and comparison of the two paradigms. The findings show that [brief main result].
Keywords: [keyword 1], [keyword 2], [keyword 3], [keyword 4]

---

TABLE OF CONTENTS
[Insert automatic table of contents here]

---

LIST OF FIGURES
[Insert list of figures here]

---

LIST OF TABLES
[Insert list of tables here]

---

1.0 INTRODUCTION
1.1 Background
[Write the background of the project topic here.]
Sample:
Programming language concepts are important because they influence how software is structured, maintained, and extended.
1.2 Problem Statement
[Describe the problem that this project solves.]
Sample:
Students often learn programming paradigms separately and do not clearly see how the same problem can be implemented differently in each paradigm.
1.3 Project Objectives
[State the project objectives.]
Sample:
•	To develop a small working application.
•	To compare two programming paradigms.
•	To apply concepts such as types, scope, functions, and objects.
1.4 Scope of the Project
[Describe what the system will do and what it will not do.]
Sample:
The system supports add, search, update, delete, and display functions. It does not include online access or database integration.
1.5 Report Organization
[Briefly describe the remaining chapters of the report.]
Sample:
Chapter 2 presents the requirements analysis, Chapter 3 explains the design, Chapter 4 describes the implementation, Chapter 5 presents testing, and Chapter 6 discusses the findings and conclusion.

---

2.0 REQUIREMENTS ANALYSIS
2.1 Project Description
[Describe the selected application domain.]
Sample:
This project is a student record management system that stores and manages basic student information.
2.2 Functional Requirements
[List the functions the system must provide.]
Sample:
•	Add new record.
•	Display all records.
•	Search for a record by ID.
•	Update an existing record.
•	Delete a record.
2.3 Non-Functional Requirements
[List the quality requirements.]
Sample:
•	The program must be easy to use.
•	The code must be modular and readable.
•	Input must be validated.
•	The system must run without errors.
2.4 Paradigm Comparison Requirements
[Explain what is being compared between the two paradigms.]
Sample:
The project compares how the same system is represented in procedural and object-oriented programming, focusing on structure, readability, reusability, and maintainability.

2.5 User Requirements
[Describe who will use the system.]
Sample:
The intended user is a lecturer or administrator who needs to manage small sets of student records.

---

3.0 DESIGN
3.1 System Overview
[Give a short overview of the system architecture.]
Sample:
The system uses a menu-driven interface and contains two versions of the same application logic: procedural and object-oriented.
3.2 Architecture / Module Structure
[Describe the modules or components.]
Sample:
•	Main menu module
•	Input validation module
•	Record management module
•	Search module
•	Output/display module
3.3 Data Structures Used
[State how data is stored.]
Sample:
The procedural version stores records in lists or arrays, while the object-oriented version stores records as objects in a collection.
3.4 Flowchart / Pseudocode / Class Diagram
[Insert and explain the diagram or pseudocode.]
Sample:
Figure 3.1 shows the flowchart of the main menu process. The program repeatedly asks the user to choose an operation until exit is selected.
3.5 Input and Output Design
[Describe the expected inputs and outputs.]
Sample:
Input includes student ID, name, program, and GPA. Output includes confirmation messages and record listings.
3.6 Design Notes for Paradigm 1
[Explain the first paradigm design.]
Sample:
The procedural design uses functions to separate each task into a specific module.
3.7 Design Notes for Paradigm 2
[Explain the second paradigm design.]
Sample:
The object-oriented design uses classes to group data and behavior together in a single structure.

---

4.0 IMPLEMENTATION
4.1 Tools and Language Used
[State the software tools and programming language.]
Sample:
The project was developed using Python and Visual Studio Code.
4.2 Implementation of Paradigm 1
[Describe how the first version was implemented.]
Sample:
The procedural version uses functions such as addRecord(), searchRecord(), and deleteRecord().
4.3 Implementation of Paradigm 2
[Describe how the second version was implemented.]
Sample:
The object-oriented version uses classes such as Student and StudentManager.
4.4 Key Language Concepts Applied
[Explain which programming language concepts were used.]
Sample:
This project demonstrates variables, control structures, parameter passing, scope rules, modularity, and object-oriented concepts such as encapsulation and inheritance.
4.5 Code Organization
[Explain how the source code is arranged.]
Sample:
The source code is divided into separate files to improve readability and maintainability.
4.6 Sample Screenshots or Code Extracts
[Insert selected screenshots or code snippets.]
Sample:
Figure 4.1 shows the main menu output when the system starts.

---

5.0 TESTING AND RESULTS
5.1 Testing Strategy
[Explain how the system was tested.]
Sample:
The system was tested using normal input, invalid input, empty input, and boundary cases.
5.2 Test Cases
[Insert a table of test cases.]
Test ID	Test Description	Input	Expected Result	Actual Result	Status
TC01	Add valid record	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC02	Search existing record	[Input]	[Expected]	[Actual]	[Pass/Fail]
TC03	Invalid GPA	[Input]	[Expected]	[Actual]	[Pass/Fail]
5.3 Error and Edge Cases
[Describe special or invalid cases tested.]
Sample:
The system was tested with duplicate IDs and missing names to ensure validation messages were displayed correctly.
5.4 Testing Evidence
[Insert screenshots, console outputs, or logs.]
Sample:
Figure 5.1 shows the system response after entering an invalid record.
5.5 Results Summary
[Summarize the testing outcome.]
Sample:
All core functions worked as expected, and the validation mechanism successfully rejected incorrect input.

---

6.0 DISCUSSION
6.1 Comparison of the Two Paradigms
[Discuss the differences between the two implementations.]
Sample:
The procedural version is simpler for small tasks, while the object-oriented version is more modular and easier to extend.
6.2 Analysis of Programming Language Concepts
[Connect the project to the course topics.]
Sample:
The project demonstrates how scope, types, parameter passing, and abstraction affect program design and implementation.
6.3 Strengths and Limitations
[Discuss strengths and weaknesses.]
Sample:
The object-oriented version supports better reuse, but it requires more planning. The procedural version is faster to write but less flexible.
6.4 Lessons Learned
[State what the group learned.]
Sample:
The project helped us understand that the choice of programming paradigm affects code structure, readability, and maintainability.

---

7.0 CONCLUSION
7.1 Conclusion
[Give the final conclusion of the project.]
Sample:
This project successfully developed a functional system and demonstrated the differences between two programming paradigms.
7.2 Future Work
[Suggest possible improvements.]
Sample:
Future improvements may include database integration, graphical user interface support, and data export features.

---

REFERENCES
[List all references in the required citation style.]
Sample:
•	Sebesta, R. W. Concepts of Programming Languages.
•	Python Software Foundation. Python Documentation.
•	[Any article, textbook, or website used]

---

APPENDICES
Appendix A: Full Source Code
[Paste or attach the full code here.]
Appendix B: Group Contribution
[Summarize each member’s contribution.]
Member	Contribution
[Name]	[Work done]
[Name]	[Work done]

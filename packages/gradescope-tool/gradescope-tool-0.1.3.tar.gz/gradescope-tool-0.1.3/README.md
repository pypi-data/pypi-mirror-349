<p align="center">
   <img src="./docs/icon.png" width="200" height="200">
   <h1 align="center">GRADESCOPE</h1>
</p>
<p align="center">
    <em>A Python wrapper for Gradescope to easily retrieve data from your Gradescope Courses.
</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Teaching-and-Learning-in-Computing/Gradescope?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/Teaching-and-Learning-in-Computing/Gradescope?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Teaching-and-Learning-in-Computing/Gradescope?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Teaching-and-Learning-in-Computing/Gradescope?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
</p>

## Overview

Gradescope is a Python package project designed to provide seamless interaction with the Gradescope service, offering functionalities such as login, fetching course and assignment information, and submission downloads. By encapsulating key entities like Courses, Assignments, and Members, Gradescope provides a structured approach for managing data in JSON and CSV formats. The project aims to simplify tasks for users by providing wrapper functions that handle data retrieving and API calls.

---

## [Installation](https://pypi.org/project/gradescope-tool/)

```bash
pip install gradescope-tool
```

---

## Example Usage

```python
from gradescope import *

gs = Gradescope('username', 'password')

courses = gs.get_courses(role=Role.INSTRUCTOR)
# courses:
# [Course(
#    course_id=123456,
#    url='/courses/123456',
#    role='instructor',
#    term='Spring 2024',
#    short_name='Math 2B',
#    full_name='Math 2B: Calculus'
# ), ...]

assignments = gs.get_assignments(courses[0])
# assignments:
# [Assignment(
#    assignment_id=654321,
#    assignment_type='assignment',
#    url='/courses/123456/assignments/654321',
#    title='Assignment 1',
#    container_id=None,
#    versioned=False,
#    version_index=None,
#    version_name=None,
#    total_points='100.0',
#    student_submission=True,
#    created_at='Apr 01',
#    release_date='2024-04-01T00:00',
#    due_date='2024-04-07T23:59',
#    hard_due_date='2024-04-10T23:59',
#    time_limit=None,
#    active_submissions=250,
#    grading_progress=100,
#    published=True,
#    regrade_requests_open=False,
#    regrade_requests_possible=True,
#    regrade_request_count=0,
#    due_or_created_at_date='2024-04-07T23:59'
# ), ...]

members = gs.get_members(courses[0])
# members:
# [Member(
#    member_id='112233',
#    full_name='Peter Anteater',
#    first_name='Peter',
#    last_name='Anteater',
#    role='0',
#    sid='1234567890',
#    email='uci.mascot@uci.edu'
# ), ...]

past_submissions = gs.get_past_submissions(courses[0], assignments[0], members[0])
# past_submissions:
# [Submission(
#    course_id=123456,
#    assignment_id=654321,
#    member_id='112233',
#    submission_id=987654321,
#    created_at='2024-04-07T12:34:56.655388-07:00',
#    score=55.55,
#    url='/courses/123456/assignments/654321/submissions/987654321'
# ), ...]

gradebook = gs.get_gradebook(courses[0], members[0])
save_json('./gradebook.json', gradebook, encoder=EnhancedJSONEncoder)

grades_csv = gs.get_assignment_grades(assignments[0])
save_csv('./assignment_grades.csv', grades_csv)

gs.download_file('./submission.zip', past_submission[-1].get_file_url())
```

---

## Modules

| File                                                                                                                   | Summary                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [gradescope.py](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/master/gradescope/gradescope.py) | Manage interaction with Gradescope API. Provide functionality such as login; retrieving course, assignment, member, past submissions, and gradebook data; and submission downloads.                                                                      |
| [dataclass.py](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/master/gradescope/dataclass.py)   | Defines data classes for Courses, Assignments, Members, and Submissions in Gradescope. Supports generating URLs and download links.                                                                                                                      |
| [constants.py](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/master/gradescope/constants.py)   | Defines base URLs and role mappings for Gradescope API integration.                                                                                                                                                                                      |
| [utils.py](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/master/gradescope/utils.py)           | Provide dataclasse to dictionaries encoder and functions for easy loading/saving JSON and CSV files.                                                                                                                                                     |
| [errors.py](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/master/gradescope/errors.py)         | Defines custom exception classes for handling different error scenarios in the Gradescope API interactions. Includes LoginError, NotLoggedInError, and ResponseError classes to manage login failures, unauthorized access, and general response issues. |

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/issues)**: Submit bugs found or log feature requests for the `Gradescope` project.
- **[Submit Pull Requests](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Teaching-and-Learning-in-Computing/Gradescope
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

---

## Contribution

<p align="center">
   <a href="https://github.com{/Teaching-and-Learning-in-Computing/Gradescope/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Teaching-and-Learning-in-Computing/Gradescope">
   </a>
</p>

---

## License

This project is protected under the [MIT](https://github.com/Teaching-and-Learning-in-Computing/Gradescope/blob/main/LICENSE) License.

---

## Disclaimer

By using this package, you acknowledge and agree to the following terms:

- **High Traffic Warning**: This package may generate a high volume of traffic and excessive API calls to websites or services, which could affect the performance of these sites or services.

- **Potential Consequences**: Misuse of this package or unintended operation can lead to circumstances such as account suspension or permanent ban from the affected websites or services.

By using this package, you agree that you are using it at your own risk. You should comply with all applicable laws and regulations, and respect the terms of service of any website or service you interact with.

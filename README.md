# GHUCT

Stands for GitHUb Classrooms Tracker (gh as though)

## Purpose

We are moving to use github classrooms for students to checkout and submit projects (grading is still done on gradescope). 

Github tracks a lot, and I want to know how invasive we can be on tracking student project progress. 

Things I want to know:
  [X] (Python/go) when did people checkout the project?
  [ ] (Python) on average, how many commits were made per project?
  [ ] (Python) how long did it take for people to complete project?
  [ ] some uh... other stuff


## Installation

There are two versions: python and go. I find go runs faster (sometimes too fast, I get rate limited sometimes). Regardless of which version you use, you will need to setup a [github access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) and get the url of the organization of the repository that holds the classroom repos. An example `.env` file is provided.

You will also need to write a config file for each project, placed in a folder named for the project. For example, `project-1/config` is the config file for the assignment "project-1". This config file will look like:
```text
Release: MM-DD-YYYY
Due: MM-DD-YYYY
Late: MM-DD-YYYY
```
`Release` is the day the project was released, `Due` is the date it is due, and `Late` is the late deadline, if any. If there is no late deadline, you can copy the Due date, or leave the line out completely.

### Python
You can just run the python version provided you have `python-dotenv` installed (`pip install python-dotenv`), Even then, not really needed if you wanted to hardcode in your github access token and the urls.


### Go

*** This version is on hold. Please use Python ***
I am pretty sure you can just clone and run `go run main.go` given you have [golang](https://go.dev/) installed. Again you will need to install `godotenv` (`go get github.com/joho/godotenv) if you don't want to hardcode or make your own environment variable getters. 


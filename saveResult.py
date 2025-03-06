import json
import constants

# Function to save a result (name and points) to the leaderboard
def saveResult(name, points):
    leaderBoard = readResult()  # Read the current leaderboard
    data = {"name": f"{name}", "score": points}  # Create a new entry with name and score
    leaderBoard.append(data)  # Add the new entry to the leaderboard
    # Sort the leaderboard in descending order of score
    leaderBoard.sort(key=lambda x: x['score'], reverse=True)
    # Write the updated leaderboard to the file
    with open(constants.PATH_FILE_RECORDS, 'w') as file:
        json.dump(leaderBoard, file, indent=4)  # Save the leaderboard to a JSON file

# Function to read and return the leaderboard from the file
def readResult():
    try:
        # Try opening and loading the leaderboard from the file
        with open(constants.PATH_FILE_RECORDS, 'r') as file:
            leaderboard = json.load(file)
            return leaderboard  # Return the leaderboard as a list of dictionaries
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

# Function to check a player's position in the leaderboard after a new result
def checkResult(name, points):
    leaderBoard = readResult()  # Read the current leaderboard
    key = 'check pos'
    # Add a temporary entry to check the position
    data = {"name": f"{name}", "score": points, 'key': f'{key}'}
    leaderBoard.append(data)
    # Sort the leaderboard in descending order of score
    leaderBoard.sort(key=lambda x: x['score'], reverse=True)

    # Iterate over the leaderboard and return the position of the temporary entry
    for index, score in enumerate(leaderBoard):
        if 'key' in score:  # Find the entry with the 'key' to determine the position
            return index + 1  # Return the 1-based position

# Function to return the top 3 scores from the leaderboard
def redFirstThree():
    try:
        # Try reading the leaderboard from the file
        with open(constants.PATH_FILE_RECORDS, 'r') as file:
            leaderboard = json.load(file)
            listScore = []
            # Extract the scores from the leaderboard
            for obj in leaderboard:
                listScore.append(obj['score'])
            
            # If fewer than 3 scores exist, pad with zeros
            if len(listScore) < 3:
                for i in range(0, 3 - len(listScore)):
                    listScore.append(0)

            return listScore[:3]  # Return the top 3 scores
    except FileNotFoundError:
        # If the file doesn't exist, return three zero scores
        return [0, 0, 0]

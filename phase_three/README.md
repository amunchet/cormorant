# Phase 3
This is the deployment.  

- One component will be acquisition - finding related videos to given targets
- Second component will be the ratings - telling the network what works and what doesn't
- We don't have to worry about whether or not connected to the internet: for now, must always be connected

## Structure

- Dockers will control the acuqisition, display, and judgement of the songs.

- Backend: serves the judgement and interfaces with the database
    - Will also need to handle organization of the updated training files/batches

- Frontend: shows the results to the user and allows playing of the video embedded
- Database: [Mongo for now], stores the judgements of the songs and if we've already seen these songs before
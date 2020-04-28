# Whack-A-Mole
Whack-a-mole as a distributed system with requirements, multiple "vendor's" components, and configurable security/functionality settings.

## Overview
The distributed whack-a-mole is comprised of a few components that together allow a human operator to whack digital moles (no actual animals are harmed in this system). These components are:

1. UI: A web-based user inferface that displays the current sensor output of mole presence to a human operator, and provides an input mechinsm for the operator to issue a "whack" command.
2. Mole sensor: A digital sensor that determines the presence or absence of a digital mole and reports the status to the message router.
3. "Whactuator": A digital whacking actuator that dispenses a digital whack to the digital mole hole when commanded.
4. Message router: A backend server that takes messages from all the aforementioned components and ensure the messages are valid and routes them to their intended destination.

## System requirements
1. The UI must be updated to reflect the sensor's determination of a mole being present or not within 1 second of sensor identifying a mole
2. The "whactuator" must receive and act upon the "whack" request from the human operator within 1 second of user input

## Running whack-a-mole
1. Configure each component to interact and operate on your specific host system (ensure there are no conflicting ports, etc.)
2. Run the `./run.sh` script and navigate your browser to the specified localhost port to bring up the UI

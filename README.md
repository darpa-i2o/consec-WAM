# Whack-A-Mole
Whack-a-mole as a distributed system with requirements, multiple "vendor's" components, and configurable security/functionality settings.

## Overview
The distributed whack-a-mole is comprised of a few components that together allow a human operator to whack digital moles (no actual animals are harmed in this system). These components are:

1. UI: A web-based user inferface that displays the current sensor output of mole presence to a human operator, and provides an input mechanism for the operator to issue a "whack" command.
2. Mole sensor: A digital sensor that determines the presence or absence of a digital mole and reports the status to the message router.
3. "Whactuator": A digital whacking actuator that dispenses a digital whack to the digital mole hole when commanded.
4. Message router: A backend server that takes messages from all the aforementioned components, ensures the messages are valid, and routes them to their intended destination.

## System requirements
1. The UI must be updated to reflect the sensor's determination of a mole being present or not within 1 second of sensor identifying a mole.
2. The "whactuator" must receive and act upon the "whack" request from the human operator within 1 second of user input.
3. Messages exchanged between the components must be validated by the message router using the most robust integrity checks available.
4. Where possible, links between components should be encrypted.

## Running whack-a-mole
1. Configure each component to interact and operate on your specific host system (ensure there are no conflicting ports, etc.).
2. Run the `./run.sh` script and navigate your browser to the specified localhost port to bring up the UI.
3. A message will display indicating whether there is a mole present according to the sensor. Use the "whack" button to send a message to the Whactuator as moles appear, but be careful or you might whack at nothing.

## Stopping whack-a-mole
1. Run the `./shutdown.py` script to cleanly shutdown all the server threads.

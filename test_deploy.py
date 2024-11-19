import pytest

file = open(r'discord.log', 'r')
lines = file.readlines()

def test_on_ready():
    ready_status = False
    for row in lines:
        # check if string present on a current line
        phrase = 'Comrade is ready to spread propoganda!'
        # if phrase found
        if row.find(phrase) != -1:
            # don't look for next lines
            ready_status = True
            break
    
    assert ready_status == True 

def test_no_warnings():
    warning_status = False
    for row in lines:
        phrase = 'WARNING'
        if row.find(phrase) != -1:
            warning_status = True
            break

    assert warning_status == False


def test_no_errors():
    error_status = False
    for row in lines:
        phrase = 'ERROR'
        if row.find(phrase) != -1:
            error_status = True
            break
    
    assert error_status == False


def test_no_criticals():
    critical_status = False
    for row in lines:
        phrase = 'CRITICAL'
        if row.find(phrase) != -1:
            critical_status = True
            break
    
    assert critical_status == False

file.close()
        

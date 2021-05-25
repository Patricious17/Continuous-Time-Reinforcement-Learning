#!/usr/bin/python
from sys import exit


class Controller:

    def __init__(self, controlType_):
        self.controlType = controlType_  # control is a 'callable object'
        self.controlValue = 0.0  # do not apply any control initially
        self.mode = 'RL'

    def __call__(self, *args, **kwargs):
        # print('hello')
        # print(kwargs)
        if 'errors' in kwargs:
            # print('hello')
            # print(kwargs['errors'])
            self.updateControlValue(kwargs)
        else:
            return 0.0

    def updateControlValue(self, error):
        # print('hello here')
        # print(error)
        # exit()
        self.controlValue = self.controlType(**error)


# here we implement PID as a callable object

class ProportionalController:
    def __init__(self, gainDict_):
        self.gainDict = gainDict_  # 'posError' : 0.5, 'velError' : -.4, 'angular' : -5.4
        self.proportionalGain = self.gainDict['posError']  # JUST FOR TESTING, WE WANT TO AVOID USING THE NAMES HERE
        self.derivativeGain = self.gainDict[
            'lin_xError']  # SEE FOR LOOP BELOW FOR CALCULATION WITHOUT NEEDING KEY NAMES

    def __call__(self, *args, **kwargs):
        errorVals = kwargs
        control = 0.0  # default return value to 0.0
        for errorDict in errorVals:
            # print(errorDict)
            for errorType in errorVals[errorDict]:
                # print(self.gainDict[errorType])
                # print(errorVals[errorDict][errorType])
                kx = self.gainDict[errorType]
                ex = errorVals[errorDict][errorType]
                control = control + kx * ex

        # print('hiya')
        # print(control)  # ASK PATRIK WHY THE RESULT IS -16.5XXXXXXX4 AND NOT JUST -16.5 AS SHOWN ON MY CALCULATOR

        return control

    # implement ALTERNATIVE pid controller using numpy here:
    # control = gainVector.transpose() * errors   # [0.5  1.4] * [0.5, -0.2]'
    # This uses numpy --> alternative to the for loop above

    def setGains(self, proportionalGain_=None, derivativeGain_=None):
        if proportionalGain_ is not None:
            self.proportionalGain = proportionalGain_
        if derivativeGain_ is not None:
            self.derivativeGain = derivativeGain_


# implement unit tests here

def test1():
    ProportionalGain_dict = {  # create proportional gain dict to feed into PID when instantiating the class
        'posError': .5,  # values here are the gains that CORRESPOND to the quantities named
        'lin_xError': -.4,  # using rospy syntax for consistency
        'ang_zError': -5.4
    }

    nested_errors_dict = {'errors': {'posError': 1,
                                     'lin_xError': 2,
                                     'ang_zError': 3
                                     }
                          }

    print('Running test1...')
    pid = ProportionalController(ProportionalGain_dict)
    assert pid.proportionalGain == 0.5
    assert pid.derivativeGain == -0.4
    ctrl = Controller(pid)
    ctrl(**nested_errors_dict)
    assert ctrl.controlValue == -16.500000000000004

    pid.setGains(0.5, 0.4)
    assert ctrl.controlType.proportionalGain == 0.5 and ctrl.controlType.derivativeGain == 0.4
    # add more tests to test functionality of PID
    print('Test1 completed!')


test1()


def huskyTest():
    ProportionalGain_dict = {  # create proportional gain dict to feed into PID when instantiating the class
        'posError': .5,  # values here are the gains that CORRESPOND to the quantities named
        'lin_xError': -.4,  # using rospy syntax for consistency
        'ang_zError': -5.4
    }

    nested_errors_dict = {'errors': {'posError': 1,
                                     'lin_xError': 2,
                                     'ang_zError': 3
                                     }
                          }

    pid = ProportionalController(ProportionalGain_dict)  # instantiate proportional control object with necessary gains
    husky = Controller(pid)  # instantiate controller object with the desired initial control type argument
    # pid(**nested_errors_dict) #TESTING THE PID WITH ERRORS DIRECTLY BEFORE DOING IT THROUGH THE CONTROLLER

    husky(**nested_errors_dict)



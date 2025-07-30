##! python3
# Copyright (C) 2024, Tactics2D Authors. Released under the GNU GPLv3.
# @File: physics_model_base.py
# @Description: This file defines an abstract class for a physics model of a traffic participant.
# @Author: Yueyuan Li
# @Version: 1.0.0

from abc import ABC, abstractmethod

from tactics2d.participant.trajectory import State, Trajectory


class PhysicsModelBase(ABC):
    """This abstract class defines the essential interfaces required to specify a physics kinematics/dynamics model for a traffic participant.

    Please feel free to inherent this class to implement your own physics model.

    Attributes:
        _DELTA_T (int): The default time interval between the current state and the new state, 5 milliseconds (ms).
        _MIN_DELTA_T (int): The minimum time interval between the current state and the new state, 1 millisecond (ms).
        _G (float): The gravitational acceleration, 9.81 m/s^2.
    """

    _DELTA_T: int = 5
    _MIN_DELTA_T: int = 1
    _G = 9.81  # gravitational acceleration, m/s^2

    @abstractmethod
    def step(self, state: State, action: tuple, interval: int = None) -> State:
        """This abstract function defines an interface to update the state of the traffic participant based on the physics model.

        Args:
            state (State): The current state of the traffic participant.
            action (tuple): The action to be applied to the traffic participant.
            interval (int): The time interval between the current state and the new state. The unit is millisecond.

        Returns:
            A new state of the traffic participant.
        """

    @abstractmethod
    def verify_state(self, state: State, last_state: State, interval: int = None) -> bool:
        """This abstract function defines an interface to verify the validity of the new state based on the physics model.

        Args:
            state (State): The new state of the traffic participant.
            last_state (State): The last state of the traffic participant.
            interval (int): The time interval between the last state and the new state. The unit is millisecond.

        Returns:
            True if the new state is valid, False otherwise.
        """

    def verify_states(self, trajectory: Trajectory) -> bool:
        """This function verifies a sequence of states over time based on the physics model. The default implementation calls verify_state() for each state in the sequence. However, this function is expected to be overridden to implement more efficient verification.

        Args:
            trajectory (Trajectory): The trajectory of the traffic participant.

        Returns:
            True if the trajectory is valid, False otherwise.
        """
        if trajectory.stable_freq is True:
            interval = 1000 / trajectory.fps

        last_state = trajectory.history_states[trajectory.frames[0]]
        for frame in trajectory.frames[1:]:
            state = trajectory.history_states[frame]
            interval = interval if trajectory.stable_freq else state.frame - last_state.frame
            if self.verify_state(state, last_state, interval) is False:
                return False

        return True

import random
import numpy as np
import gym
import cv2

from preprocessing.framebuffer import FrameBuffer
from preprocessing import atari_wrappers
from gym.core import Wrapper

ENV_NAME = "BerzerkDeterministic-v4"


def PrimaryAtariWrap(env, clip_rewards=True, scale=100):
    # This wrapper holds the same action for <skip> frames and outputs
    # the maximal pixel value of 2 last frames (to handle blinking
    # in some envs)
    # env = atari_wrappers.MaxAndSkipEnv(env, skip=1)

    # This wrapper sends done=True when each life is lost
    # (not all the 5 lives that are givern by the game rules).
    # It should make easier for the agent to understand that losing is bad.
    # env = atari_wrappers.EpisodicLifeEnv(env)

    # This wrapper laucnhes the ball when an episode starts.
    # Without it the agent has to learn this action, too.
    # Actually it can but learning would take longer.
    # env = atari_wrappers.FireResetEnv(env)

    # This wrapper transforms rewards to {-1, 0, 1} according to their sign
    if clip_rewards:
        env = atari_wrappers.ClipRewardEnv(env)

    return env


def make_env(clip_rewards=True, seed=None, lstm=False):
    env = gym.make(ENV_NAME)  # create raw env    
    env = atari_wrappers.AtariRescale42x42(env)
    env = atari_wrappers.NormalizedEnv(env)
    
    env=PrimaryAtariWrap(env,clip_rewards=clip_rewards)
    if not lstm:
        env = FrameBuffer(env, n_frames=4)
    
    return env
import gym
import universe
import random


def main():

	# initialise environment
	env = gym.make('flashgames.CoasterRacer-v0')
	observation_n = env.reset()

	# init variables
	# iterations
	n = 0
	j = 0

	# sum of observations
	total_sum = 0
	prev_total_sum = 0
	turn = False

	# define key events
	left = [('KeyEvent', 'ArrowUp', True), ('KeyEvent',
	         'ArrowLeft', True), ('KeyEvent', 'ArrowRight', False)],
    right = [('KeyEvent', 'ArrowUp', True) ,('KeyEvent', 'ArrowLeft', False) ,('KeyEvent', 'ArrowRight', True)]
    forward = [('KeyEvent', 'ArrowUp', True) ,('KeyEvent', 'ArrowLeft', False) ,('KeyEvent', 'ArrowRight', False)]

    


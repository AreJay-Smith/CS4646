"""Assess a betting strategy.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Pranshav Thakkar (replace with your name)
GT User ID: pthakkar7 (replace with your User ID)
GT ID: 903079725 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np
import matplotlib.pyplot as mpl
  		   	  			    		  		  		    	 		 		   		 		  
def author():  		   	  			    		  		  		    	 		 		   		 		  
        return 'pthakkar7' # replace tb34 with your Georgia Tech username.
  		   	  			    		  		  		    	 		 		   		 		  
def gtid():  		   	  			    		  		  		    	 		 		   		 		  
	return 903079725 # replace with your GT ID number
  		   	  			    		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		   	  			    		  		  		    	 		 		   		 		  
	result = False  		   	  			    		  		  		    	 		 		   		 		  
	if np.random.random() <= win_prob:  		   	  			    		  		  		    	 		 		   		 		  
		result = True  		   	  			    		  		  		    	 		 		   		 		  
	return result  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
	win_prob = 0.474 # set appropriately to the probability of a win
	np.random.seed(gtid()) # do this only once  		   	  			    		  		  		    	 		 		   		 		  
	#print get_spin_result(win_prob) # test the roulette spin
  		   	  			    		  		  		    	 		 		   		 		  
	# add your code here to implement the experiments

	#Experiment 1 Figure 1

	mpl.axis([0, 300, -256, 100])

	for x in range(10):
		winnings = [0] * 1001
		winnings = np.array(winnings)
		spins = 0
		episode_winnings = 0
		while spins < 1000:
			while episode_winnings < 80 and spins < 1000:
				won = False
				bet_amount = 1
				while not won and spins < 1000:
					won = get_spin_result(win_prob)
					spins = spins + 1
					if won == True:
						episode_winnings = episode_winnings + bet_amount
						winnings[spins] = episode_winnings
					else:
						episode_winnings = episode_winnings - bet_amount
						winnings[spins] = episode_winnings
						bet_amount = bet_amount * 2
			if spins < 1000:
				spins = spins + 1
				winnings[spins] = episode_winnings
		mpl.plot(np.arange(0, 1001), winnings)

	mpl.title("Figure 1")
	mpl.savefig("fig1.png")

	#Experiment 1 Figure 2
	mpl.clf()

	mpl.axis([0, 300, -256, 100])

	simul_winnings = []

	for x in range(1000):
		winnings = [0] * 1001
		winnings = np.array(winnings)
		spins = 0
		episode_winnings = 0
		while spins < 1000:
			while episode_winnings < 80 and spins < 1000:
				won = False
				bet_amount = 1
				while not won and spins < 1000:
					won = get_spin_result(win_prob)
					spins = spins + 1
					if won == True:
						episode_winnings = episode_winnings + bet_amount
						winnings[spins] = episode_winnings
					else:
						episode_winnings = episode_winnings - bet_amount
						winnings[spins] = episode_winnings
						bet_amount = bet_amount * 2
			if spins < 1000:
				spins = spins + 1
				winnings[spins] = episode_winnings
		simul_winnings.append(winnings)

	mean = np.mean(simul_winnings, axis=0)
	stdev = np.std(simul_winnings, axis=0)
	median = np.median(simul_winnings, axis=0)
	mpl.title("Figure 2")
	mpl.plot(mean)
	mpl.plot(mean + stdev)
	mpl.plot(mean - stdev)
	mpl.savefig("fig2.png")

	# Experiment 1 Figure 3
	mpl.clf()
	mpl.axis([0, 300, -256, 100])

	mpl.title("Figure 3")
	mpl.plot(median)
	mpl.plot(median + stdev)
	mpl.plot(median - stdev)
	mpl.savefig("fig3.png")

	# Experiment 2 Figure 4

	mpl.clf()

	mpl.axis([0, 300, -256, 100])

	simul_winnings = []

	for x in range(1000):
		winnings = [0] * 1001
		winnings = np.array(winnings)
		spins = 0
		episode_winnings = 0
		while spins < 1000:
			while episode_winnings < 80 and episode_winnings != -256 and spins < 1000:
				won = False
				bet_amount = 1
				while not won and spins < 1000:
					won = get_spin_result(win_prob)
					spins = spins + 1
					if won == True:
						episode_winnings = episode_winnings + bet_amount
						winnings[spins] = episode_winnings
					else:
						episode_winnings = episode_winnings - bet_amount
						winnings[spins] = episode_winnings
						if (episode_winnings - (bet_amount*2) > -256):
							bet_amount = bet_amount * 2
						else:
							bet_amount = episode_winnings + 256
			if spins < 1000:
				spins = spins + 1
				winnings[spins] = episode_winnings
		simul_winnings.append(winnings)

	mean = np.mean(simul_winnings, axis=0)
	stdev = np.std(simul_winnings, axis=0)
	median = np.median(simul_winnings, axis=0)
	mpl.title("Figure 4")
	mpl.plot(mean)
	mpl.plot(mean + stdev)
	mpl.plot(mean - stdev)
	mpl.savefig("fig4.png")

	# Experiment 2 Figure 5
	mpl.clf()
	mpl.axis([0, 300, -256, 100])

	mpl.title("Figure 5")
	mpl.plot(median)
	mpl.plot(median + stdev)
	mpl.plot(median - stdev)
	mpl.savefig("fig5.png")
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
